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
    raw_threshold = data.get("similarity_threshold", 0.6)
    if isinstance(raw_threshold, bool) or not isinstance(raw_threshold, (int, float)):
        raise TypeError("similarity_threshold must be a number between 0 and 1")
    if not 0 <= raw_threshold <= 1:
        raise ValueError("similarity_threshold must be between 0 and 1")
    threshold = float(raw_threshold)
    scope = str(data.get("comparison_scope", "all"))
    if scope not in {"all", "within", "cross"}:
        raise ValueError("comparison_scope must be all, within, or cross")
    ignore_words = data.get("ignore_words", [])
    if not isinstance(ignore_words, list) or any(
        not isinstance(word, str) for word in ignore_words
    ):
        raise ValueError("ignore_words must be an array of strings")
    ignored = {word.casefold() for word in ignore_words}
    manuscripts = _require(data, "manuscripts")
    if not isinstance(manuscripts, list) or any(not isinstance(m, dict) for m in manuscripts):
        raise ValueError("manuscripts must be an array of objects")
    for manuscript in manuscripts:
        if "name" in manuscript and not isinstance(manuscript["name"], str):
            raise ValueError("manuscript name must be a string")
        titles = manuscript.get("titles", [])
        if not isinstance(titles, list) or any(not isinstance(title, str) for title in titles):
            raise ValueError("manuscript titles must be an array of strings")
    use_ids = any("id" in manuscript for manuscript in manuscripts)
    if use_ids:
        ids = [manuscript.get("id") for manuscript in manuscripts]
        if any(not isinstance(identity, str) or not identity.strip() for identity in ids):
            raise ValueError(
                "every manuscript must have a nonempty string id when IDs are supplied"
            )
        if len(set(ids)) != len(ids):
            raise ValueError("manuscript IDs must be unique")
    entries = []
    for manuscript in manuscripts:
        for number, title in enumerate(manuscript.get("titles", []), 1):
            entry = {
                "manuscript": manuscript.get("name", "Untitled"),
                "chapter": number,
                "title": str(title),
            }
            if use_ids:
                entry["manuscript_id"] = manuscript["id"]
            entries.append(entry)
    collisions = []
    for left, right in combinations(entries, 2):
        identity_key = "manuscript_id" if use_ids else "manuscript"
        same_manuscript = left[identity_key] == right[identity_key]
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
    if not isinstance(data, dict):
        raise TypeError("input must be a JSON object")
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
