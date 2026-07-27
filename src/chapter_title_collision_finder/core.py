from __future__ import annotations

import json
import re
from itertools import combinations
from typing import Any

PROJECT = "chapter-title-collision-finder"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _title_collisions(data: dict[str, Any]) -> dict[str, Any]:
    entries = [
        {"manuscript": manuscript.get("name", "Untitled"), "chapter": number, "title": str(title)}
        for manuscript in _require(data, "manuscripts")
        for number, title in enumerate(manuscript.get("titles", []), 1)
    ]
    collisions = []
    for left, right in combinations(entries, 2):
        left_tokens = set(re.findall("[a-z0-9]+", left["title"].casefold()))
        right_tokens = set(re.findall("[a-z0-9]+", right["title"].casefold()))
        similarity = len(left_tokens & right_tokens) / max(len(left_tokens | right_tokens), 1)
        exact = left["title"].strip().casefold() == right["title"].strip().casefold()
        if exact or similarity >= 0.6:
            collisions.append(
                {
                    "left": left,
                    "right": right,
                    "kind": "duplicate" if exact else "similar",
                    "similarity": round(similarity, 3),
                }
            )
    return {"titles_checked": len(entries), "collisions": collisions}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_title_collisions(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
