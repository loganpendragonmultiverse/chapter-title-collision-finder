import json
import re
from copy import deepcopy

import pytest

from chapter_title_collision_finder.cli import main
from chapter_title_collision_finder.core import analyze, render_markdown


@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        42,
        "text",
        {"manuscripts": 17},
        {"manuscripts": {}},
        {"manuscripts": "book"},
        {"manuscripts": [None]},
        {"manuscripts": ["book"]},
        {"manuscripts": [{"name": 7}]},
        {"manuscripts": [{"titles": None}]},
        {"manuscripts": [{"titles": "AB"}]},
        {"manuscripts": [{"titles": [4]}]},
        {"manuscripts": [{}], "ignore_words": "the"},
        {"manuscripts": [{}], "ignore_words": [7]},
        {"manuscripts": [{}], "similarity_threshold": True},
        {"manuscripts": [{}], "similarity_threshold": None},
        {"manuscripts": [{}], "similarity_threshold": "0.6"},
        {"manuscripts": [{}], "similarity_threshold": float("nan")},
        {"manuscripts": [{}], "similarity_threshold": float("inf")},
        {"manuscripts": [{}], "similarity_threshold": 10**1000},
    ],
)
def test_malformed_shapes_fail_with_actionable_input_error(data):
    with pytest.raises((TypeError, ValueError)):
        analyze(data)


def test_invalid_cli_input_has_no_report_or_traceback(tmp_path, capsys):
    source = tmp_path / "source.json"
    source.write_text("[]", encoding="utf-8")
    report = tmp_path / "report.json"
    assert main([str(source), "--output", str(report)]) == 2
    assert not report.exists()
    assert source.read_text() == "[]"
    assert "input must be a JSON object" in capsys.readouterr().err


def test_empty_title_lists_and_same_display_name_ids_remain_distinct():
    data = {
        "manuscripts": [
            {"id": "a", "name": "Same", "titles": []},
            {
                "id": "b",
                "name": "Same",
                "titles": ["Road ```\n# Author heading", " road ```\n# author heading "],
            },
        ],
        "similarity_threshold": 1,
        "ignore_words": [],
    }
    original = deepcopy(data)
    report = analyze(data)
    assert data == original
    assert report["titles_checked"] == 2
    assert report["collisions"][0]["kind"] == "duplicate"
    assert report["collisions"][0]["left"]["manuscript_id"] == "b"
    payload = re.search(r"## Collisions\n\n```json\n(.*?)\n```", render_markdown(report), re.DOTALL)
    assert json.loads(payload.group(1)) == report["collisions"]
