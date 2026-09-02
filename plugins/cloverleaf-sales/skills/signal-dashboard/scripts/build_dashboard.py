#!/usr/bin/env python3
"""
build_dashboard.py: Turn Cloverleaf signals into a branded, sortable HTML dashboard.

Accepts ANY of:
  • search-meetings output    -> {"meeting_hits": [...], "meetings": [...]}   (discussion)
  • search-insights output    -> {"insights": [...], "total": N}              (discussion)
  • search-documents output   -> {"documents": [...]}                        (procurement)
  • run-document-keyword-search output -> {"object_api_response": {...}}      (procurement)
  • legacy transcript search  -> {"results": [...]}                          (discussion)
  • a normalized signals list -> {"signals": [...]}  (or a bare [...] )

Response shapes for search-meetings, search-insights, and search-documents were verified
against live connector output on 2026-09-02. The run-document-keyword-search reader follows
the shape recorded in cloverleaf-mcp-operations (verified 2026-08-18); it was not re-verified
on 2026-09-02 because that tool needs an array `terms` parameter the probe harness could not
send.

A dashboard can mix both signal types: discussion signals (what officials say) and
procurement signals (what they're buying). Each card carries `signal_type` and the view
lets you filter to one or the other.

Normalized signal schema (all fields optional except quote + jurisdiction):
  {
    "signal_type": "discussion",        # "discussion" (default) | "procurement"
    "jurisdiction": "City of Spokane Valley, WA",
    "meeting_id": "18214101",
    "meeting_title": "City Council Budget Workshop - Jun 09, 2026",
    "date": "2026-06-09",                # or epoch ms in "time"
    "time": 1781049599000,
    "quote": "one ransomware attack and the city is shut down...",
    "start_time": 18451.04,             # seconds into the meeting
    "speaker_name": "Erik Lamb",
    "speaker_title": "Deputy City Manager",
    "email": "elamb@SpokaneValleyWA.gov",
    "phone": "509-720-5100",
    "terms": ["ransomware", "cybersecurity audit"],
    "video_url": "https://.../media.mp4",   # OPTIONAL fallback only
    "cloverleaf_url": "https://app.cloverleaf.ai/meetings/18451",  # the citation link, copied
                                             # verbatim from the connector response. The script
                                             # never builds a Cloverleaf link from an id.
    "fit": "Active cyber audit cycle; named gap = no pen testing.",  # model-written
    "next_action": "Email Erik referencing the pen-testing gap.",     # model-written
    "score": 88                          # optional; computed if omitted

    # --- procurement-only fields (signal_type="procurement") ---
    "vendor": "Bitdefender",            # named incumbent/vendor from the doc, if any
    "amount": "$10,803.80",             # dollar figure from the line item, if any
    "procurement_stage": "Renewal",     # Renewal | Award | RFP | Budget item | ...
    "doc_type": "agenda",               # agenda | packet | notice
    "org_id": 500                        # Cloverleaf organization_id (doc hits lack a name)
  }

Procurement signals usually have NO speaker, so they're scored on dollar figure, stage,
document type, and recency instead of speaker/contact, so a contract about to be awarded
ranks Hot even with no named person.

Usage:
  python build_dashboard.py INPUT.json -o dashboard.html [--title "..."] [--subtitle "..."]
  python build_dashboard.py search_results.json -o dashboard.html      # raw transcript search
  python build_dashboard.py document_results.json -o dashboard.html    # raw document search
"""
import argparse, html, json, re, sys, time
from datetime import datetime, timezone

NAVY = "#1B232E"   # Ink Navy (official brand)
SKY  = "#A9E3F4"   # Sky-deep, the official signature accent. Cloverleaf brand has NO green.
LOGO_URI = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDI4LjMuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCA2MDAgMTE2IiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCA2MDAgMTE2OyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+Cgkuc3Qwe2ZpbGw6bm9uZTtzdHJva2U6I0ZGRkZGRjtzdHJva2Utd2lkdGg6MS41O3N0cm9rZS1taXRlcmxpbWl0OjEwO30KCS5zdDF7ZmlsbDojRkZGRkZGO30KPC9zdHlsZT4KPHBhdGggY2xhc3M9InN0MCIgZD0iTTQ3LjUsMzYuOGM4LjksMCwxNi4yLDcuMywxNi4yLDE2LjJ2MGMwLDguOS03LjMsMTYuMi0xNi4yLDE2LjJIMzEuNmMtOC45LDAtMTYuMi03LjMtMTYuMi0xNi4ydjAKCWMwLTguOSw3LjMtMTYuMiwxNi4yLTE2LjIiLz4KPHBhdGggY2xhc3M9InN0MCIgZD0iTTMxLjYsODQuOWMtOC45LDAtMTYuMi03LjMtMTYuMi0xNi4ydjBjMC04LjksNy4zLTE2LjIsMTYuMi0xNi4yaDE1LjljOC45LDAsMTYuMiw3LjMsMTYuMiwxNi4ydjAKCWMwLDguOS03LjMsMTYuMi0xNi4yLDE2LjIiLz4KPHBhdGggY2xhc3M9InN0MCIgZD0iTTYzLjYsNjguOGMwLDguOS03LjMsMTYuMi0xNi4yLDE2LjJoMGMtOC45LDAtMTYuMi03LjMtMTYuMi0xNi4yVjUyLjljMC04LjksNy4zLTE2LjIsMTYuMi0xNi4yaDAKCWM4LjksMCwxNi4yLDcuMywxNi4yLDE2LjIiLz4KPHBhdGggY2xhc3M9InN0MCIgZD0iTTE1LjUsNTIuOWMwLTguOSw3LjMtMTYuMiwxNi4yLTE2LjJoMGM4LjksMCwxNi4yLDcuMywxNi4yLDE2LjJ2MTUuOWMwLDguOS03LjMsMTYuMi0xNi4yLDE2LjJoMAoJYy04LjksMC0xNi4yLTcuMy0xNi4yLTE2LjIiLz4KPGc+Cgk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNNzcuMyw2MC4ydi0wLjFjMC0xMi4yLDkuMi0yMi4zLDIxLjgtMjIuM2M3LDAsMTEuNCwyLjIsMTUuNCw1LjZjMC41LDAuNCwxLDEsMSwyYzAsMS4zLTEuMiwyLjQtMi41LDIuNAoJCWMtMC43LDAtMS4yLTAuMy0xLjYtMC42Yy0zLjQtMy03LTQuOS0xMi40LTQuOWMtOS42LDAtMTYuNyw3LjgtMTYuNywxNy43djAuMWMwLDEwLDcuMSwxNy44LDE2LjcsMTcuOGM1LjQsMCw5LjEtMS44LDEyLjgtNS4yCgkJYzAuNC0wLjQsMS0wLjcsMS41LTAuN2MxLjIsMCwyLjMsMS4xLDIuMywyLjNjMCwwLjctMC40LDEuMy0wLjgsMS43Yy00LjMsMy45LTguOSw2LjMtMTYsNi4zQzg2LjUsODIuNCw3Ny4zLDcyLjYsNzcuMyw2MC4yeiIvPgoJPHBhdGggY2xhc3M9InN0MSIgZD0iTTEyNC43LDQwLjdjMC0xLjQsMS4xLTIuNSwyLjQtMi41YzEuNCwwLDIuNSwxLDIuNSwyLjV2MzYuNWgyMi40YzEuMiwwLDIuMiwxLDIuMiwyLjNzLTEsMi4yLTIuMiwyLjJoLTI0LjgKCQljLTEuMywwLTIuNC0xLTIuNC0yLjVWNDAuN3oiLz4KCTxwYXRoIGNsYXNzPSJzdDEiIGQ9Ik0zMzQuMiw0MC43YzAtMS40LDEuMS0yLjUsMi40LTIuNWMxLjQsMCwyLjUsMSwyLjUsMi41djM2LjVoMjIuNGMxLjIsMCwyLjIsMSwyLjIsMi4zcy0xLDIuMi0yLjIsMi4yaC0yNC44CgkJYy0xLjMsMC0yLjQtMS0yLjQtMi41VjQwLjd6Ii8+Cgk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNMTU1LjgsNjAuMnYtMC4xYzAtMTEuOSw4LjktMjIuMywyMi4xLTIyLjNjMTMuMSwwLDIxLjksMTAuMywyMS45LDIyLjJ2MC4xYzAsMTEuOS04LjksMjIuMy0yMi4xLDIyLjMKCQlDMTY0LjYsODIuNCwxNTUuOCw3Mi4xLDE1NS44LDYwLjJ6IE0xOTQuNyw2MC4ydi0wLjFjMC05LjgtNy4xLTE3LjgtMTctMTcuOHMtMTYuOSw3LjktMTYuOSwxNy43djAuMWMwLDkuOCw3LjEsMTcuOCwxNywxNy44CgkJUzE5NC43LDcwLDE5NC43LDYwLjJ6Ii8+Cgk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNMjIyLjcsODIuMWMtMS40LDAtMi4zLTAuOC0yLjgtMmwtMTYuNi0zOC40Yy0wLjItMC4zLTAuMi0wLjctMC4yLTEuMWMwLTEuMiwxLTIuNCwyLjUtMi40CgkJYzEuMiwwLDIuMSwwLjgsMi41LDEuOGwxNC45LDM1LjdsMTUtMzUuOWMwLjQtMC45LDEuMi0xLjcsMi40LTEuN2MxLjQsMCwyLjQsMS4xLDIuNCwyLjNjMCwwLjQtMC4xLDAuNy0wLjIsMWwtMTYuNywzOC42CgkJYy0wLjYsMS4yLTEuNCwyLTIuOCwySDIyMi43eiIvPgoJPHBhdGggY2xhc3M9InN0MSIgZD0iTTI1Mi4zLDgxLjZjLTEuMywwLTIuNC0xLTIuNC0yLjVWNDFjMC0xLjQsMS4xLTIuNSwyLjQtMi41aDIyLjhjMS4yLDAsMi4yLDEsMi4yLDIuMmMwLDEuMi0xLDIuMi0yLjIsMi4yCgkJaC0yMC4zdjE0LjdoMTcuNmMxLjIsMCwyLjIsMSwyLjIsMi4yYzAsMS4yLTEsMi4yLTIuMiwyLjJoLTE3LjZ2MTUuMWgyMC42YzEuMiwwLDIuMiwxLDIuMiwyLjJzLTEsMi4yLTIuMiwyLjJIMjUyLjN6Ii8+Cgk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNMzc1LjgsODEuNmMtMS4zLDAtMi40LTEtMi40LTIuNVY0MWMwLTEuNCwxLjEtMi41LDIuNC0yLjVoMjIuOGMxLjIsMCwyLjIsMSwyLjIsMi4yYzAsMS4yLTEsMi4yLTIuMiwyLjIKCQloLTIwLjN2MTQuN2gxNy42YzEuMiwwLDIuMiwxLDIuMiwyLjJjMCwxLjItMSwyLjItMi4yLDIuMmgtMTcuNnYxNS4xaDIwLjZjMS4yLDAsMi4yLDEsMi4yLDIuMnMtMSwyLjItMi4yLDIuMkgzNzUuOHoiLz4KCTxwYXRoIGNsYXNzPSJzdDEiIGQ9Ik0zMTEuNCw2Mi43bDQuMiwwLjZsMi42LDMuNmMwLDAtMS40LDIuOS0xLjgsMS4yYy0xLTMuNy02LjItMy4yLTYuMi0zLjJoLTE2LjR2MTQuNmMwLDEuNC0xLDIuNS0yLjUsMi41CgkJYy0xLjMsMC0yLjQtMS0yLjQtMi41VjQxYzAtMS40LDEuMS0yLjUsMi40LTIuNWgxNi4xYzUuNCwwLDkuNiwxLjYsMTIuMyw0LjNjMi4yLDIuMiwzLjMsNS4xLDMuMyw4LjV2MC4xYzAsNS41LTIuOSw5LjMtNy40LDExLjIKCQkgTTMwNy4xLDYwLjVjNi40LDAsMTEuMS0zLjMsMTEuMS04Ljl2LTAuMWMwLTUuNC00LjEtOC41LTExLTguNWgtMTMuM3YxNy41SDMwNy4xeiIvPgoJPHBhdGggY2xhc3M9InN0MSIgZD0iTTQxMC4xLDc4LjRsMTcuNS0zOC4zYzAuNy0xLjQsMS41LTIuMiwzLjEtMi4yaDAuMmMxLjQsMCwyLjUsMC43LDMsMi4ybDE3LjUsMzguMmMwLjIsMC41LDAuMywwLjksMC4zLDEuMgoJCWMwLDEuMy0xLDIuMy0yLjMsMi4zYy0xLjIsMC0yLTAuOC0yLjQtMS44bC00LjUtOS45aC0yMy43bC00LjUsMTBjLTAuNCwxLjEtMS4yLDEuNy0yLjMsMS43Yy0xLjIsMC0yLjItMS0yLjItMi4yCgkJQzQwOS44LDc5LjMsNDA5LjksNzguOSw0MTAuMSw3OC40eiBNNDQwLjYsNjUuOGwtOS45LTIyLjFsLTkuOSwyMi4xSDQ0MC42eiIvPgoJPHBhdGggY2xhc3M9InN0MSIgZD0iTTQ2MS44LDQxYzAtMS40LDEuMS0yLjUsMi40LTIuNWgyMS43YzEuMiwwLDIuMiwxLDIuMiwyLjJjMCwxLjItMSwyLjMtMi4yLDIuM2gtMTkuMnYxNS40aDE2LjQKCQljMS4yLDAsMi4yLDEsMi4yLDIuMnMtMSwyLjItMi4yLDIuMmgtMTYuNHYxNi42YzAsMS40LTEsMi41LTIuNSwyLjVjLTEuMywwLTIuNC0xLTIuNC0yLjVWNDF6Ii8+Cgk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNNTE2LjEsNzguNGwxNy41LTM4LjNjMC43LTEuNCwxLjUtMi4yLDMuMS0yLjJoMC4yYzEuNCwwLDIuNSwwLjcsMywyLjJsMTcuNSwzOC4yYzAuMiwwLjUsMC4zLDAuOSwwLjMsMS4yCgkJYzAsMS4zLTEsMi4zLTIuMywyLjNjLTEuMiwwLTItMC44LTIuNC0xLjhsLTQuNS05LjloLTIzLjdsLTQuNSwxMGMtMC40LDEuMS0xLjIsMS43LTIuMywxLjdjLTEuMiwwLTIuMi0xLTIuMi0yLjIKCQlDNTE1LjgsNzkuMyw1MTYsNzguOSw1MTYuMSw3OC40eiBNNTQ2LjYsNjUuOGwtOS45LTIyLjFsLTkuOSwyMi4xSDU0Ni42eiIvPgoJPHBhdGggY2xhc3M9InN0MSIgZD0iTTU2Ni40LDQwLjdjMC0xLjQsMS4xLTIuNSwyLjQtMi41YzEuNCwwLDIuNSwxLDIuNSwyLjV2MzguOGMwLDEuNC0xLDIuNS0yLjUsMi41Yy0xLjMsMC0yLjQtMS0yLjQtMi41VjQwLjd6IgoJCS8+Cgk8Zz4KCQk8cmVjdCB4PSIzMTYuNCIgeT0iNjguMSIgY2xhc3M9InN0MSIgd2lkdGg9IjQuOSIgaGVpZ2h0PSI4LjEiLz4KCQk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNMzIxLjIsNjguMWMwLDAsMC4xLTIuNy0yLjMtNS4xYy0yLjQtMi40LTQuMi0yLjgtNC4yLTIuOGwtNC4yLDIuNmMwLDAsMy44LDEsNSwzLjNjMC44LDEuNSwwLjcsMS45LDAuNywxLjkKCQkJIi8+CgkJPHBhdGggY2xhc3M9InN0MSIgZD0iTTMyMi42LDc4LjNjLTEuMy0wLjgtMS40LTIuMi0xLjQtMi4yaC00LjljMCwwLTAuMiwyLjgsMi42LDUuNyIvPgoJCTxjaXJjbGUgY2xhc3M9InN0MSIgY3g9IjMyMC45IiBjeT0iODAuMSIgcj0iMi41Ii8+Cgk8L2c+CjwvZz4KPC9zdmc+Cg=="   # official white Cloverleaf AI logo lockup

# ---------- ingest + normalize ----------

def _meeting_num(mid):
    if mid is None:
        return ""
    m = re.search(r"(\d+)", str(mid))
    return m.group(1) if m else str(mid)

def _date_from(sig):
    if sig.get("date"):
        return str(sig["date"])[:10]
    t = sig.get("time")
    if t:
        try:
            return datetime.fromtimestamp(int(t) / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        except Exception:
            pass
    return ""

def _days_since(sig):
    t = sig.get("time")
    if not t and sig.get("date"):
        try:
            t = datetime.strptime(str(sig["date"])[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000
        except Exception:
            t = None
    if not t:
        return None
    return (time.time() - int(t) / 1000) / 86400.0

STATE_ABBR = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI",
    "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
    "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND",
    "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "puerto rico": "PR", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
    "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI",
    "wyoming": "WY", "federal": "US",
    "alberta": "AB", "british columbia": "BC", "manitoba": "MB", "new brunswick": "NB",
    "newfoundland and labrador": "NL", "nova scotia": "NS", "ontario": "ON",
    "prince edward island": "PE", "quebec": "QC", "saskatchewan": "SK",
}

def _state_code(name):
    if not name:
        return ""
    n = str(name).strip()
    if len(n) == 2 and n.isalpha():
        return n.upper()
    return STATE_ABBR.get(n.lower(), "")

def _jurisdiction(org_name, state_name):
    """'County of Adams' + 'Colorado' -> 'County of Adams, CO'. The ', ST' suffix is what
    turns on the dashboard state filter, so always append it when the state is known."""
    org = (org_name or "").strip()
    code = _state_code(state_name)
    if org and code:
        return f"{org}, {code}"
    return org or "Unknown jurisdiction"

def normalize_search_meetings(payload):
    """Read live `search-meetings` output: `meeting_hits[]` joined to `meetings[]` on id.

    Verified against connector output 2026-09-02. Transcript chunks carry only
    {id, text, start_time, score}. There is NO speaker or contact block on this tool, so
    every card from it is speaker-blank by design. Pull names from list-contacts and set
    them on a normalized signal instead of inventing them here.
    """
    meta = {m.get("id"): m for m in payload.get("meetings", []) if m.get("id") is not None}
    out = []
    for hit in payload.get("meeting_hits", []):
        m = meta.get(hit.get("id"), {})
        if m.get("is_spam") or m.get("user_marked_spam"):
            continue
        chunks = sorted(hit.get("transcripts", []) or [],
                        key=lambda c: c.get("score") or 0, reverse=True)
        best = chunks[0] if chunks else {}
        out.append({
            "signal_type": "discussion",
            "jurisdiction": _jurisdiction(m.get("organization_name"), m.get("state")),
            "meeting_id": _meeting_num(hit.get("id")),
            "meeting_title": m.get("title") or "",
            "cloverleaf_url": m.get("cloverleaf_url") or "",
            "video_url": m.get("source_video_url") or "",
            "time": hit.get("time"),
            "date": (m.get("published_at") or "")[:10],
            "quote": (best.get("text") or "").strip(),
            "start_time": best.get("start_time"),
            "hits": hit.get("hits", 0),
            "best_score": hit.get("best_score"),
            "already_viewed": hit.get("already_viewed", False),
            "org_id": m.get("organization_id"),
        })
    return out

_SCORE_RE = re.compile(r"Signal\s*Match:\s*(\d+)\s*/\s*10", re.I)

def normalize_insights(payload):
    """Read live `search-insights` output: {"insights": [...], "total": N}.

    Verified 2026-09-02. Each insight carries summary, result (markdown, sometimes
    truncated), organization_name, state_name/county_name/city_name, meeting_id,
    creator_email, created_at, and cloverleaf_url. The Signal Match score in `summary`
    becomes the card score, rescaled 0-100. Rows scored 0/10 are relevance-gate rejects
    from the insight's own prompt and are dropped.
    """
    out = []
    for ins in payload.get("insights", []):
        summary = (ins.get("summary") or "").strip()
        m = _SCORE_RE.search(summary) or _SCORE_RE.search(ins.get("result") or "")
        raw = int(m.group(1)) if m else None
        if raw == 0:
            continue
        quote = _SCORE_RE.sub("", summary).replace("**", "").strip()
        out.append({
            "signal_type": "discussion",
            "jurisdiction": _jurisdiction(ins.get("organization_name"), ins.get("state_name")),
            "meeting_id": _meeting_num(ins.get("meeting_id")),
            "meeting_title": ins.get("prompt_name") or "",
            "cloverleaf_url": ins.get("cloverleaf_url") or "",
            "date": (ins.get("created_at") or "")[:10],
            "quote": quote,
            "score": int(raw * 10) if raw is not None else None,
            "hits": 0,
        })
    return [s for s in out if s.get("score") is not None or s.get("quote")]

def normalize_search_documents(payload):
    """Read live `search-documents` output: {"documents": [...]}.

    Verified 2026-09-02. Each document carries document_id, cloverleaf_url, hits,
    best_score, chunks[] ({id, text, score}), organization_id, document_type, and
    meeting_date. It does NOT carry an organization name, so cards read 'Org #<id>' until
    you resolve the name and set `jurisdiction` on a normalized signal.
    """
    out = []
    for doc in payload.get("documents", []):
        chunks = sorted(doc.get("chunks", []) or [],
                        key=lambda c: c.get("score") or 0, reverse=True)
        text = " ".join((c.get("text") or "").replace("\n", " ") for c in chunks[:2]).strip()
        if not text:
            continue
        org_id = doc.get("organization_id")
        out.append(_tag_type({
            "signal_type": "procurement",
            "jurisdiction": f"Org #{org_id}" if org_id else "Unknown jurisdiction",
            "org_id": org_id,
            "doc_type": doc.get("document_type") or "",
            "meeting_id": str(doc.get("document_id") or ""),
            "cloverleaf_url": doc.get("cloverleaf_url") or "",
            "date": (doc.get("meeting_date") or "")[:10],
            "quote": chunks[0].get("text", "").replace("\n", " ").strip(),
            "hits": doc.get("hits", 0),
            "best_score": doc.get("best_score"),
            "amount": _amount_near_topic(text, ["firewall", "network", "security", "contract",
                                                "license", "renewal", "cyber"]),
            "procurement_stage": _detect_stage(text),
            "vendor": _detect_vendor(text),
        }))
    return out

def normalize_raw_search(payload):
    """Legacy reader for the older {"results": [...]} transcript payload, which carried a
    per-line `person.contact` block. The current search-meetings tool no longer returns one.
    Kept so saved older result files still render."""
    out = []
    for r in payload.get("results", []):
        lines = r.get("transcripts", []) or []
        # rank lines: contact > person > none, then longer text
        def rank(ln):
            p = ln.get("person") or {}
            has_contact = 1 if (p.get("contact") or {}).get("email") or (p.get("contact") or {}).get("phone") else 0
            has_person = 1 if p else 0
            return (has_contact, has_person, len(ln.get("text", "")))
        best = max(lines, key=rank) if lines else {}
        p = best.get("person") or {}
        c = p.get("contact") or {}
        org = (c.get("organization") or {}).get("name") or p.get("organization") or ""
        if not org:  # fall back to any identified org elsewhere in the meeting
            for ln in lines:
                lp = ln.get("person") or {}
                org = (lp.get("contact") or {}).get("organization", {}).get("name") or lp.get("organization") or ""
                if org:
                    break
        out.append({
            "jurisdiction": org or "Unknown jurisdiction",
            "meeting_id": _meeting_num(r.get("id")),
            "time": r.get("time"),
            "quote": best.get("text", ""),
            "start_time": best.get("start_time"),
            "speaker_name": c.get("name") or p.get("name") or "",
            "speaker_title": c.get("title") or p.get("title") or "",
            "email": c.get("email") or "",
            "phone": c.get("phone") or "",
            "terms": [t.get("term") for t in r.get("terms", []) if t.get("term")],
            "hits": r.get("hits", 0),
            "signal_type": "discussion",
        })
    return out

def ingest(payload):
    if isinstance(payload, list):
        return [_tag_type(s) for s in payload]
    if "signals" in payload:
        return [_tag_type(s) for s in payload["signals"]]
    if "meeting_hits" in payload:
        return normalize_search_meetings(payload)
    if "insights" in payload:
        return normalize_insights(payload)
    if "documents" in payload:
        return normalize_search_documents(payload)
    if "results" in payload:
        return normalize_raw_search(payload)
    if "object_api_response" in payload or "hits" in payload:
        return normalize_raw_documents(payload)
    raise SystemExit(
        "Unrecognized JSON. Expected search-meetings {meeting_hits:[...]}, "
        "search-insights {insights:[...]}, search-documents {documents:[...]}, "
        "run-document-keyword-search {object_api_response:...}, {signals:[...]}, "
        "or a bare list.")

def _tag_type(sig):
    """Default signal_type to 'discussion' unless explicitly procurement."""
    if not sig.get("signal_type"):
        sig["signal_type"] = "procurement" if (sig.get("amount") or sig.get("vendor")
                                               or sig.get("doc_type")) else "discussion"
    return sig

# ---------- document (procurement) ingest ----------

# dollar figures like $10,803.80, $337,500, $1.2M
_MONEY_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?\s?(?:million|M|K)?", re.I)
# stage cues, ordered so the strongest/earliest-to-close wins
_STAGE_CUES = [
    ("Award", re.compile(r"\baward(ed|ing)?\b|notice of award|recommend(ed)? award", re.I)),
    ("Renewal", re.compile(r"\brenew(al|ing|ed)?\b|extend(ed|ing)? the (agreement|contract)", re.I)),
    ("Agreement", re.compile(r"\b(consideration of|approv\w+|enter into)\b.{0,40}\bagreement\b|professional services agreement|not[- ]to[- ]exceed|not to exceed", re.I)),
    ("RFP", re.compile(r"\bRFP\b|request for proposals?|request for qualifications|invitation to bid|solicitation", re.I)),
    ("Budget item", re.compile(r"\bbudget\b|line item|appropriat", re.I)),
]
# crude vendor catch: "<Proper Name> renewal", "with <Proper Name>", "<Name> LLC/Inc/Corp"
_VENDOR_RE = re.compile(r"\b([A-Z][A-Za-z0-9&.\-]+(?:\s+[A-Z][A-Za-z0-9&.\-]+){0,3})\s+(?:LLC|L\.L\.C\.|Inc\.?|Corp\.?|Solutions|Technologies|Systems|Networks|Security)\b")

# procurement boilerplate that is NOT a topic on its own; a doc matching only these is noise
_BOILERPLATE_TERMS = {
    "renewal", "agreement", "award", "resolution", "consent agenda", "rfp",
    "request for proposals", "request for qualifications", "invitation to bid",
    "not to exceed", "professional services agreement", "sole source",
    "cooperative purchase", "interlocal", "solicitation",
}

def _passages(hit):
    """Matched passages, accepting either envelope reported for the keyword document tool:
    an Elasticsearch-style `highlight.plain_text[]` or a flat `highlights[]`."""
    hl = (hit.get("highlight") or {}).get("plain_text") or hit.get("highlights") or []
    if isinstance(hl, str):
        hl = [hl]
    # strip the <mark> tags for clean display; keep order
    return [re.sub(r"</?mark>", "", p).strip() for p in hl if p and str(p).strip()]

def _best_passage(passages, topic_terms):
    """Prefer a passage that contains BOTH a topic term and a dollar figure, then one
    with a topic term, then any passage with money, then the first."""
    if not passages:
        return ""
    low = [t.lower() for t in topic_terms]
    def has_topic(p):
        pl = p.lower()
        return any(t in pl for t in low)
    for p in passages:
        if has_topic(p) and _MONEY_RE.search(p):
            return p
    for p in passages:
        if has_topic(p):
            return p
    for p in passages:
        if _MONEY_RE.search(p):
            return p
    return passages[0]

_VENDOR_STOPWORDS = {
    "response", "service", "services", "subscription", "agreement", "contract",
    "renewal", "cybersecurity", "city", "county", "council", "board", "department",
    "managed", "detection", "security", "technology", "support", "the", "annual",
    "master", "cooperative", "purchase", "approval", "consideration", "item", "total",
}

def _amount_near_topic(text, topic_terms):
    """Pick the dollar figure closest to a topic term. If the nearest figure is far from
    any topic mention (likely an unrelated invoice in the same block), return blank rather
    than guess. A wrong dollar amount on a card is worse than none."""
    monies = list(_MONEY_RE.finditer(text))
    if not monies:
        return ""
    low = [t.lower() for t in topic_terms]
    tl = text.lower()
    topic_pos = [tl.find(t) for t in low if tl.find(t) >= 0]
    if not topic_pos:
        return ""  # no topic anchor → don't attribute a dollar figure
    monies = [m for m in monies if re.search(r"[1-9]", m.group(0))]  # drop $0 placeholders
    if not monies:
        return ""
    best = min(monies, key=lambda m: min(abs(m.start() - tp) for tp in topic_pos))
    nearest_gap = min(abs(best.start() - tp) for tp in topic_pos)
    return best.group(0).strip() if nearest_gap <= 120 else ""

def _detect_stage(text):
    for label, rx in _STAGE_CUES:
        if rx.search(text):
            return label
    return ""

def _clean_vendor(name):
    if not name:
        return ""
    toks = [t for t in re.split(r"\s+", name.strip()) if t]
    # reject if every token is a stopword, or it's a single generic word
    if not toks:
        return ""
    if all(t.lower().strip(".,") in _VENDOR_STOPWORDS for t in toks):
        return ""
    if len(toks) == 1 and toks[0].lower().strip(".,") in _VENDOR_STOPWORDS:
        return ""
    return name.strip()

def _detect_vendor(text):
    # 1) corporate-suffix names (PKI Solutions LLC, Acme Technologies), most reliable
    m = _VENDOR_RE.search(text)
    if m:
        return _clean_vendor(m.group(0))
    # 2) "with <Proper Name>" (consideration of an agreement WITH X)
    m = re.search(r"\bwith\s+([A-Z][A-Za-z0-9&.\-]+(?:\s+[A-Z][A-Za-z0-9&.\-]+){0,2})\b", text)
    if m:
        v = _clean_vendor(m.group(1))
        if v:
            return v
    # 3) "<Proper Name> Renewal|Subscription|Contract", but only a clean, non-stopword name
    m = re.search(r"\b([A-Z][A-Za-z0-9&.\-]{3,})\s+(?:Renewal|Subscription|Contract)\b", text)
    if m:
        return _clean_vendor(m.group(1))
    return ""

def normalize_raw_documents(payload):
    """Collapse raw run-document-keyword-search output into procurement signals.

    Keeps only documents where at least one NON-boilerplate (topic) term hit, so generic
    procurement-language matches are dropped, mirroring the document-signal-search skill's
    filtering rule. Vendor/amount/stage are extracted best-effort from the highlight text;
    for the cleanest cards, have the model read the passages and pass normalized
    {signals:[...]} with vendor/amount/procurement_stage set explicitly.
    """
    resp = payload.get("object_api_response", payload)
    raw = resp.get("hits")
    if isinstance(raw, dict):
        hits = raw.get("hits") or []            # Elasticsearch-style envelope
    elif isinstance(raw, list):
        hits = raw                              # flat list of hit records
    else:
        hits = resp.get("documents") or []
    out = []
    for h in hits:
        src = h.get("_source") or h             # flat records carry the fields inline
        tf = h.get("term_frequencies") or src.get("term_frequencies") or {}
        topic_terms = [t for t, n in tf.items() if n and t.lower() not in _BOILERPLATE_TERMS]
        if not topic_terms:
            continue  # only procurement boilerplate matched (or nothing); skip
        passages = _passages(h)
        text = _best_passage(passages, topic_terms)
        out.append(_tag_type({
            "signal_type": "procurement",
            "jurisdiction": f"Org #{src.get('organization_id')}" if src.get("organization_id") else "Unknown jurisdiction",
            "org_id": src.get("organization_id"),
            "doc_type": src.get("document_type") or "",
            "meeting_id": str(h.get("_id") or src.get("document_id") or ""),
            "cloverleaf_url": h.get("cloverleaf_url") or src.get("cloverleaf_url") or "",
            "time": src.get("meeting_date"),
            "quote": text,
            "terms": topic_terms,
            "hits": sum(int(n) for n in tf.values() if isinstance(n, (int, float))),
            "amount": _amount_near_topic(text, topic_terms),
            "procurement_stage": _detect_stage(" ".join(passages)),
            "vendor": _detect_vendor(text),
        }))
    return out

# ---------- scoring ----------

def score(sig):
    if isinstance(sig.get("score"), (int, float)):
        return int(sig["score"])
    if sig.get("signal_type") == "procurement":
        return _score_procurement(sig)
    return _score_discussion(sig)

def _recency_points(sig, near=20, mid=12, far=6):
    d = _days_since(sig)
    if d is None:
        return far // 2
    if d <= 30:
        return near
    if d <= 90:
        return mid
    if d <= 180:
        return far
    return 0

def _score_discussion(sig):
    """Speaker and contact points only apply once a person has been attached to the signal
    (from list-contacts or enrichment). search-meetings returns no speaker, so relevance
    carries those cards: semantic `best_score` stands in for the missing person factors."""
    s = 0
    if sig.get("speaker_name"):
        s += 30
    if sig.get("email") or sig.get("phone"):
        s += 25
    s += _recency_points(sig)
    hits = sig.get("hits") or 0
    s += min(hits, 10) / 10 * 15
    if len(sig.get("quote", "")) > 140:
        s += 10
    bs = sig.get("best_score")
    if isinstance(bs, (int, float)) and not sig.get("speaker_name"):
        if bs >= 0.80:
            s += 30                  # strong intent match (ops-reference calibration)
        elif bs >= 0.75:
            s += 20                  # read it before trusting it
        elif bs >= 0.70:
            s += 10
    return int(min(round(s), 100))

def _score_procurement(sig):
    """Procurement signals have no speaker; reward deal mechanics instead.
    A named vendor + dollar figure + imminent stage is the Hot case."""
    s = 0
    if sig.get("amount"):
        s += 30                      # a dollar figure = a real line item
    if sig.get("vendor"):
        s += 18                      # named incumbent = displacement clock
    stage = (sig.get("procurement_stage") or "").lower()
    if stage in ("award", "renewal", "agreement"):
        s += 25                      # decision imminent / about to close
    elif stage in ("rfp",):
        s += 18                      # open competition, still influenceable
    elif stage in ("budget item",):
        s += 10                      # next fiscal year
    s += _recency_points(sig, near=22, mid=14, far=7)
    if (sig.get("doc_type") or "").lower() == "notice":
        s -= 8                       # notices are usually publication boilerplate
    return int(min(max(round(s), 0), 100))

def tier(sc):
    return "Hot" if sc >= 70 else ("Warm" if sc >= 45 else "Cool")

# ---------- render ----------

def esc(x):
    return html.escape(str(x if x is not None else ""))

def card(sig):
    sc = score(sig)
    tr = tier(sc)
    terms = sig.get("terms") or []
    pills = "".join(f'<span class="pill">{esc(t)}</span>' for t in terms if t)
    spk = esc(sig.get("speaker_name") or "Speaker not identified")
    title = esc(sig.get("speaker_title") or "")
    contact_bits = []
    if sig.get("email"):
        contact_bits.append(f'<a href="mailto:{esc(sig["email"])}">{esc(sig["email"])}</a>')
    if sig.get("phone"):
        contact_bits.append(f'<a href="tel:{esc(sig["phone"])}">{esc(sig["phone"])}</a>')
    contact = " · ".join(contact_bits)
    has_contact = "1" if (sig.get("email") or sig.get("phone")) else "0"
    st = sig.get("start_time")
    # Readable mm:ss hint so the rep knows where in the meeting the quote lands.
    ts_hint = ""
    if st:
        try:
            _s = int(float(st))
            ts_hint = f" · quote ~{_s // 60}:{_s % 60:02d} in"
        except (TypeError, ValueError):
            ts_hint = ""
    watch = ""
    # Cite `cloverleaf_url` exactly as the connector returned it. Never construct a
    # Cloverleaf link from an id: a built link can point at a page that does not exist.
    # With no url, show the meeting id so the rep can find it in the platform.
    cl_url = sig.get("cloverleaf_url")
    if cl_url:
        hint = f'<span class="watch muted">{esc(ts_hint)}</span>' if ts_hint else ""
        watch = f'<a class="watch" href="{esc(cl_url)}" target="_blank" rel="noopener">▶ Watch on Cloverleaf</a>{hint}'
    elif sig.get("video_url"):
        href = sig["video_url"]
        if st:
            href = f'{href}#t={int(float(st))}'
        watch = f'<a class="watch" href="{esc(href)}" target="_blank" rel="noopener">▶ Watch the moment</a>'
    elif sig.get("meeting_id"):
        watch = f'<span class="watch muted">Meeting #{esc(sig["meeting_id"])}{esc(ts_hint)}</span>'
    fit = f'<div class="fit"><b>Why it matters:</b> {esc(sig["fit"])}</div>' if sig.get("fit") else ""
    nxt = f'<div class="next"><b>Next:</b> {esc(sig["next_action"])}</div>' if sig.get("next_action") else ""
    stage = esc(sig.get("procurement_stage") or "")
    stage_html = f'<span class="stage">{stage}</span>' if stage else ""
    timing = sig.get("timing") or (sig.get("money_timing") or {}).get("budget_notes") or ""
    timing_html = f'<div class="timing">\U0001f5d3 {esc(timing)}</div>' if timing else ""
    crows = []
    for ct in (sig.get("contacts") or []):
        nm = esc(ct.get("name") or "")
        if not nm:
            continue
        ti = esc(ct.get("title") or "")
        bits = []
        if ct.get("email"):
            bits.append(f'<a href="mailto:{esc(ct["email"])}">{esc(ct["email"])}</a>')
        if ct.get("phone"):
            bits.append(f'<a href="tel:{esc(ct["phone"])}">{esc(ct["phone"])}</a>')
        meta_c = (", " + ti) if ti else ""
        cc = (" \u00b7 " + " \u00b7 ".join(bits)) if bits else ""
        crows.append(f"<li>{nm}{meta_c}{cc}</li>")
    contacts_html = f'<div class="who-to-call"><b>Who to call:</b><ul>{"".join(crows)}</ul></div>' if crows else ""
    meeting = esc(sig.get("meeting_title") or "")
    date = esc(_date_from(sig))
    juris = esc(sig.get("jurisdiction") or "Unknown jurisdiction")
    sigtype = sig.get("signal_type") or "discussion"
    is_proc = sigtype == "procurement"

    # procurement signals: foreground vendor + dollar amount; suppress the empty speaker line
    deal_bits = []
    if sig.get("vendor"):
        deal_bits.append(f'<span class="vendor">{esc(sig["vendor"])}</span>')
    if sig.get("amount"):
        deal_bits.append(f'<span class="amount">{esc(sig["amount"])}</span>')
    deal_html = f'<div class="deal">{"".join(deal_bits)}</div>' if deal_bits else ""

    if is_proc:
        speaker_html = ""  # no speaker on a document signal
        # sub-line shows doc type instead of meeting title
        dt = (sig.get("doc_type") or "").title()
        sub = " · ".join(x for x in [dt + " document" if dt else "", date] if x)
    else:
        contact_span = f'<span class="contact">{contact}</span>' if contact else ""
        who_meta = (", " + title) if title else ""
        speaker_html = (f'<div class="speaker"><span class="who">{spk}{who_meta}</span>'
                        f'{contact_span}</div>')
        sub = (meeting + (" · " + date if date else "")) if (meeting or date) else ""

    blob = " ".join(str(x) for x in [juris, meeting, sig.get("quote"), spk, title,
                                     sig.get("vendor"), sig.get("amount"), sigtype,
                                     " ".join(terms)]).lower()
    return f'''
  <article class="card" data-score="{sc}" data-tier="{tr}" data-contact="{has_contact}"
           data-type="{esc(sigtype)}" data-juris="{esc(juris)}" data-date="{date}" data-search="{esc(blob)}">
    <div class="card-top">
      <div class="badge {tr.lower()}">{tr} · {sc}</div>
      <div class="meta"><span class="juris">{juris}</span>
        <span class="sub">{esc(sub)}</span></div>
      {stage_html}
    </div>
    {deal_html}
    <blockquote>“{esc(sig.get("quote"))}”</blockquote>
    {speaker_html}
    <div class="pills">{pills}</div>
    {timing_html}{contacts_html}{fit}{nxt}
    <div class="card-foot">{watch}</div>
  </article>'''

def build(signals, title, subtitle):
    for s in signals:
        _tag_type(s)
        s["_score"] = score(s)
    signals.sort(key=lambda s: s["_score"], reverse=True)
    total = len(signals)
    hot = sum(1 for s in signals if tier(s["_score"]) == "Hot")
    with_contact = sum(1 for s in signals if s.get("email") or s.get("phone"))
    n_proc = sum(1 for s in signals if s.get("signal_type") == "procurement")
    n_disc = total - n_proc
    jurisdictions = len({(s.get("jurisdiction") or "").strip() for s in signals if s.get("jurisdiction")})
    states = sorted({m.group(1) for s in signals
                     for m in [re.search(r",\s*([A-Z]{2})\b", s.get("jurisdiction") or "")] if m})
    if states:
        opts = "".join(f'<option value="{st}">{st}</option>' for st in states)
        state_select = f'<select id="state" onchange="apply()"><option value="">All states</option>{opts}</select>'
    else:
        state_select = ""
    # only show the discussion/procurement filter when the board actually mixes both
    if n_proc and n_disc:
        type_select = ('<select id="type" onchange="apply()"><option value="">All signals</option>'
                       '<option value="discussion">Discussion</option>'
                       '<option value="procurement">Procurement</option></select>')
    else:
        type_select = ""
    # fourth stat adapts: show Procurement when present, else With contact info
    if n_proc:
        stat4_val, stat4_lbl = n_proc, "Procurement"
    else:
        stat4_val, stat4_lbl = with_contact, "With contact info"
    cards = "\n".join(card(s) for s in signals)
    gen = datetime.now().strftime("%b %d, %Y %I:%M %p")
    return TEMPLATE.format(
        navy=NAVY, sky=SKY, logo=LOGO_URI, title=esc(title), subtitle=esc(subtitle),
        total=total, hot=hot, stat4_val=stat4_val, stat4_lbl=stat4_lbl,
        jurisdictions=jurisdictions, state_select=state_select, type_select=type_select,
        cards=cards, gen=gen)

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --navy:{navy}; --sky:{sky}; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
         background:#f4f6f9; color:#1d2330; }}
  header {{ background:var(--navy); color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0; font-size:21px; letter-spacing:.2px; }}
  header .sub {{ opacity:.8; font-size:13px; margin-top:4px; }}
  header .logo {{ height:26px; width:auto; display:block; margin-bottom:10px; }}
  .stats {{ display:flex; gap:14px; flex-wrap:wrap; padding:18px 28px 4px; }}
  .stat {{ background:#fff; border:1px solid #e5e9f0; border-radius:12px; padding:12px 18px; min-width:120px; }}
  .stat b {{ display:block; font-size:24px; color:var(--navy); }}
  .stat span {{ font-size:12px; color:#6b7280; text-transform:uppercase; letter-spacing:.5px; }}
  .toolbar {{ position:sticky; top:0; z-index:5; background:#f4f6f9; padding:14px 28px;
             display:flex; gap:10px; flex-wrap:wrap; align-items:center; border-bottom:1px solid #e5e9f0; }}
  .toolbar input, .toolbar select {{ padding:8px 10px; border:1px solid #cdd5e0; border-radius:8px; font-size:13px; }}
  .toolbar input[type=search] {{ min-width:230px; }}
  .toolbar label {{ font-size:12px; color:#4b5563; display:flex; align-items:center; gap:6px; }}
  .grid {{ padding:18px 28px 60px; display:grid; gap:16px;
          grid-template-columns:repeat(auto-fill,minmax(380px,1fr)); }}
  .card {{ background:#fff; border:1px solid #e5e9f0; border-radius:14px; padding:18px 18px 14px;
          box-shadow:0 1px 2px rgba(20,30,60,.04); display:flex; flex-direction:column; gap:10px; }}
  .card-top {{ display:flex; gap:12px; align-items:flex-start; }}
  .badge {{ font-size:12px; font-weight:700; color:#fff; padding:5px 10px; border-radius:20px; white-space:nowrap; }}
  .badge.hot {{ background:#c0392b; }} .badge.warm {{ background:var(--sky); color:var(--navy); }} .badge.cool {{ background:#7f8c9b; }}
  .meta .juris {{ font-weight:700; color:var(--navy); display:block; font-size:15px; }}
  .meta .sub {{ font-size:12px; color:#6b7280; }}
  blockquote {{ margin:0; padding:10px 14px; background:#f7faf8; border-left:3px solid var(--sky);
               border-radius:6px; font-size:14px; line-height:1.45; color:#23303f; }}
  .speaker {{ font-size:13px; }} .speaker .who {{ font-weight:600; color:var(--navy); }}
  .speaker .contact {{ display:block; color:#4b5563; margin-top:2px; }}
  .speaker a {{ color:var(--navy); text-decoration:none; }}
  .pills {{ display:flex; gap:6px; flex-wrap:wrap; }}
  .pill {{ background:#eef2f7; color:#3b475a; font-size:11px; padding:3px 9px; border-radius:12px; }}
  .deal {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }}
  .deal .vendor {{ font-size:13px; font-weight:700; color:var(--navy); background:#eaf0fb;
                  border-radius:10px; padding:3px 10px; }}
  .deal .amount {{ font-size:14px; font-weight:800; color:var(--navy); background:#eaf6fb;
                  border-radius:10px; padding:3px 10px; }}
  .fit, .next {{ font-size:13px; color:#33404f; }} .next {{ color:var(--navy); }}
  .stage {{ margin-left:auto; align-self:flex-start; background:var(--navy); color:#fff; font-size:11px;
           font-weight:600; padding:4px 9px; border-radius:12px; white-space:nowrap; }}
  .timing {{ font-size:12px; color:#6b5d00; background:#fff8e1; border-radius:6px; padding:5px 9px; }}
  .who-to-call {{ font-size:12.5px; color:#33404f; }}
  .who-to-call ul {{ margin:4px 0 0; padding-left:18px; }} .who-to-call li {{ margin:1px 0; }}
  .who-to-call a {{ color:var(--navy); text-decoration:none; }}
  .card-foot {{ margin-top:2px; }}
  .watch {{ font-size:12px; font-weight:600; color:var(--navy); text-decoration:none; }}
  .watch.muted {{ color:#9aa4b2; font-weight:500; }}
  .empty {{ padding:40px; text-align:center; color:#9aa4b2; grid-column:1/-1; }}
</style></head>
<body>
<header>
  <img class="logo" src="{logo}" alt="Cloverleaf AI">
  <h1>{title}</h1>
  <div class="sub">{subtitle} · Generated {gen} · signal intelligence</div>
</header>
<div class="stats">
  <div class="stat"><b>{total}</b><span>Signals</span></div>
  <div class="stat"><b>{hot}</b><span>Hot leads</span></div>
  <div class="stat"><b>{stat4_val}</b><span>{stat4_lbl}</span></div>
  <div class="stat"><b>{jurisdictions}</b><span>Jurisdictions</span></div>
</div>
<div class="toolbar">
  <input type="search" id="q" placeholder="Search quotes, people, vendors, jurisdictions…" oninput="apply()">
  {state_select}
  {type_select}
  <select id="sort" onchange="apply()">
    <option value="score">Sort: Score</option>
    <option value="date">Sort: Newest</option>
    <option value="juris">Sort: Jurisdiction</option>
  </select>
  <label><input type="checkbox" id="contactOnly" onchange="apply()"> Has contact info</label>
  <label>Min score <input type="range" id="min" min="0" max="100" value="0" oninput="apply()"><span id="minv">0</span></label>
</div>
<div class="grid" id="grid">{cards}</div>
<script>
  const grid = document.getElementById('grid');
  const cards = Array.from(grid.children);
  function apply() {{
    const q = document.getElementById('q').value.toLowerCase().trim();
    const stEl = document.getElementById('state');
    const st = stEl ? stEl.value : '';
    const tyEl = document.getElementById('type');
    const ty = tyEl ? tyEl.value : '';
    const sort = document.getElementById('sort').value;
    const contactOnly = document.getElementById('contactOnly').checked;
    const min = +document.getElementById('min').value;
    document.getElementById('minv').textContent = min;
    let shown = 0;
    cards.forEach(c => {{
      let ok = (+c.dataset.score >= min)
        && (!contactOnly || c.dataset.contact === '1')
        && (!st || (c.dataset.juris||'').includes(', ' + st))
        && (!ty || c.dataset.type === ty)
        && (!q || (c.dataset.search||'').includes(q));
      c.style.display = ok ? '' : 'none';
      if (ok) shown++;
    }});
    const sorted = cards.slice().sort((a,b) => {{
      if (sort === 'date') return (b.dataset.date||'').localeCompare(a.dataset.date||'');
      if (sort === 'juris') return (a.dataset.juris||'').localeCompare(b.dataset.juris||'');
      return (+b.dataset.score) - (+a.dataset.score);
    }});
    sorted.forEach(c => grid.appendChild(c));
    let e = document.getElementById('empty');
    if (!shown && !e) {{ e = document.createElement('div'); e.id='empty'; e.className='empty';
      e.textContent='No signals match these filters.'; grid.appendChild(e); }}
    else if (shown && e) {{ e.remove(); }}
  }}
  apply();
</script>
</body></html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="JSON file: raw search output, {signals:[...]}, or a bare list")
    ap.add_argument("-o", "--output", default="signal_dashboard.html")
    ap.add_argument("--title", default="Cybersecurity Signal Dashboard")
    ap.add_argument("--subtitle", default="Pre-RFP buying signals from live government meetings")
    a = ap.parse_args()
    with open(a.input, encoding="utf-8") as f:
        payload = json.load(f)
    signals = ingest(payload)
    if not signals:
        print("No signals found in input.", file=sys.stderr)
    html_out = build(signals, a.title, a.subtitle)
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Wrote {a.output} ({len(signals)} signals)")

if __name__ == "__main__":
    main()
