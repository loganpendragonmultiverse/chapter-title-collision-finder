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
    threshold = float(data.get("similarity_threshold", 0.6))
    if not 0 <= threshold <= 1:
        raise ValueError("similarity_threshold must be between 0 and 1")
    scope = str(data.get("comparison_scope", "all"))
    if scope not in {"all", "within", "cross"}:
        raise ValueError("comparison_scope must be all, within, or cross")
    ignored = {str(word).casefold() for word in data.get("ignore_words", [])}
    entries = [
        {"manuscript": manuscript.get("name", "Untitled"), "chapter": number, "title": str(title)}
        for manuscript in _require(data, "manuscripts")
        for number, title in enumerate(manuscript.get("titles", []), 1)
    ]
    collisions = []
    for left, right in combinations(entries, 2):
        same_manuscript = left["manuscript"] == right["manuscript"]
        if (scope == "within" and not same_manuscript) or (scope == "cross" and same_manuscript):
            continue
        left_tokens = set(re.findall("[a-z0-9]+", left["title"].casefold())) - ignored
        right_tokens = set(re.findall("[a-z0-9]+", right["title"].casefold())) - ignored
        similarity = len(left_tokens & right_tokens) / max(len(left_tokens | right_tokens), 1)
        exact = left["title"].strip().casefold() == right["title"].strip().casefold()
        if exact or similarity >= threshold:
            collisions.append(
                {
                    "left": left,
                    "right": right,
                    "kind": "duplicate" if exact else "similar",
                    "similarity": round(similarity, 3),
                    "shared_tokens": sorted(left_tokens & right_tokens),
                    "scope": "within" if same_manuscript else "cross",
                }
            )
    return {
        "titles_checked": len(entries),
        "similarity_threshold": threshold,
        "comparison_scope": scope,
        "collisions": collisions,
    }


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
