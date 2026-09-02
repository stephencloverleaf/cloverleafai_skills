#!/usr/bin/env python3
"""Check the plugin's skills against the connector tool manifests.

Fails when a skill names a retired tool, names a tool that looks like a connector's
tool but is not in that connector's manifest, or hard-codes an account-specific MCP
server prefix. Warns when a manifest tool is unused or a snapshot is stale.

Usage:
    python3 scripts/check_tool_drift.py [--json]
"""

import argparse
import datetime
import json
import pathlib
import re
import sys
import textwrap

REPO = pathlib.Path(__file__).resolve().parent.parent
CONNECTORS = REPO / "connectors"
SKILLS_GLOB = "plugins/*/skills/*/**/*.md"
STALE_DAYS = 45

IDENT = re.compile(r"`([a-z][a-z0-9_-]{2,})`")
UUID_PREFIX = re.compile(
    r"mcp__[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}__"
)
FAMILIES = {
    "apollo": re.compile(r"^apollo_"),
    "cloverleaf": re.compile(
        r"^(search-[a-z]+|run-[a-z]+-keyword-search|get-bill(-[a-z-]+)?"
        r"|get-meeting(-transcripts)?|get-document|list-[a-z-]+|lookup-organization)$"
    ),
}


def load_connectors():
    """Return {connector_name: {"tools": {...}, "snapshot": "YYYY-MM-DD"}}."""
    connectors = {}
    for path in sorted(CONNECTORS.glob("*.tools.json")):
        data = json.loads(path.read_text())
        name = data.get("connector", path.name.split(".")[0])
        connectors[name] = {
            "tools": {t["name"] for t in data.get("tools", [])},
            "snapshot": data.get("snapshot", ""),
            "file": path.name,
        }
    return connectors


def load_retired():
    path = CONNECTORS / "retired.json"
    if not path.exists():
        return {}
    entries = json.loads(path.read_text()).get("retired", [])
    return {e["name"]: e for e in entries}


def skill_files():
    for path in sorted(REPO.glob(SKILLS_GLOB)):
        yield path


def skill_name(path):
    parts = path.relative_to(REPO).parts
    return parts[parts.index("skills") + 1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    args = parser.parse_args()

    connectors = load_connectors()
    retired = load_retired()
    today = datetime.date.today()

    failures = []
    warnings = []
    usage = {}          # skill -> connector -> sorted tool names
    referenced = set()  # every known connector tool named anywhere

    for path in skill_files():
        skill = skill_name(path)
        text = path.read_text()
        rel = path.relative_to(REPO)

        for match in UUID_PREFIX.finditer(text):
            failures.append({
                "skill": skill, "file": str(rel), "kind": "account-specific server prefix",
                "name": match.group(0),
                "detail": "Server IDs differ per account. Use the bare tool name.",
            })

        for ident in sorted(set(IDENT.findall(text))):
            if ident in retired:
                entry = retired[ident]
                failures.append({
                    "skill": skill, "file": str(rel), "kind": "retired tool", "name": ident,
                    "detail": "Replaced by " + ", ".join(entry.get("replaced_by", [])) + ".",
                })
                continue
            for connector, pattern in FAMILIES.items():
                if not pattern.match(ident):
                    continue
                known = connectors.get(connector, {}).get("tools", set())
                if ident in known:
                    usage.setdefault(skill, {}).setdefault(connector, set()).add(ident)
                    referenced.add(ident)
                else:
                    failures.append({
                        "skill": skill, "file": str(rel), "kind": "unknown tool", "name": ident,
                        "detail": f"Matches the {connector} family but is not in "
                                  f"{connectors.get(connector, {}).get('file', connector)}.",
                    })

    unused = {}
    for connector, info in connectors.items():
        unused[connector] = sorted(info["tools"] - referenced)
        for tool in unused[connector]:
            warnings.append({
                "kind": "unused tool", "connector": connector, "name": tool,
                "detail": "New capability not yet used by any skill.",
            })
        snapshot = info["snapshot"]
        try:
            age = (today - datetime.date.fromisoformat(snapshot)).days
        except ValueError:
            warnings.append({
                "kind": "bad snapshot date", "connector": connector, "name": snapshot,
                "detail": "Snapshot date is missing or not ISO 8601.",
            })
            continue
        if age > STALE_DAYS:
            warnings.append({
                "kind": "stale snapshot", "connector": connector, "name": snapshot,
                "detail": f"{age} days old (limit {STALE_DAYS}). Run the refresh-connectors skill.",
            })

    table = {
        skill: {c: sorted(t) for c, t in sorted(cs.items())}
        for skill, cs in sorted(usage.items())
    }

    if args.json:
        print(json.dumps(
            {"failures": failures, "warnings": warnings, "usage": table,
             "checked_files": sum(1 for _ in skill_files())},
            indent=2))
        return 1 if failures else 0

    print("Connector tools used, by skill")
    print("-" * 72)
    for skill, connector_map in table.items():
        for connector, tools in connector_map.items():
            print(f"  {skill:<28} {connector:<11} {', '.join(tools)}")
    if not table:
        print("  (no connector tools referenced)")
    print()

    for connector, tools in sorted(unused.items()):
        if not tools:
            continue
        print(f"WARN  {connector}: {len(tools)} manifest tools no skill references "
              f"(new capability not yet used).")
        print(textwrap.fill(", ".join(tools), width=96,
                            initial_indent="      ", subsequent_indent="      "))
    for warning in warnings:
        if warning["kind"] == "unused tool":
            continue
        print(f"WARN  {warning['kind']}: {warning.get('connector', '')} "
              f"{warning['name']}: {warning['detail']}")
    if warnings:
        print()

    for failure in failures:
        print(f"FAIL  {failure['kind']}: `{failure['name']}` in {failure['file']} "
              f": {failure['detail']}")

    print(f"\n{len(failures)} FAIL, {len(warnings)} WARN "
          f"across {sum(1 for _ in skill_files())} skill files.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
