from copy import deepcopy

import pytest

from chapter_title_collision_finder.core import analyze


def test_ids_distinguish_equal_names_and_preserve_legacy():
    manuscripts = [
        {"name": "Same", "titles": ["Arrival", "Arrival"]},
        {"name": "Same", "titles": ["Arrival"]},
    ]
    old = analyze({"manuscripts": manuscripts, "comparison_scope": "cross"})
    assert old["collisions"] == []
    data = {"manuscripts": [{**m, "id": str(i)} for i, m in enumerate(manuscripts)]}
    original = deepcopy(data)
    cross = analyze({**data, "comparison_scope": "cross"})["collisions"]
    within = analyze({**data, "comparison_scope": "within"})["collisions"]
    assert len(cross) == 2 and len(within) == 1
    assert all(item["left"]["manuscript_id"] != item["right"]["manuscript_id"] for item in cross)
    assert cross[0]["left"]["manuscript"] == "Same"
    assert len(analyze(data)["collisions"]) == 3
    assert data == original


@pytest.mark.parametrize("ids", [["a", "a"], ["a", None], ["a", ""], ["a", 2], ["a", " "]])
def test_invalid_ids_rejected_including_empty_title_lists(ids):
    with pytest.raises(ValueError):
        analyze({"manuscripts": [{"id": identity, "titles": []} for identity in ids]})


@pytest.mark.parametrize("threshold,count", [(0, 1), (1 / 3, 1), (0.334, 0), (1, 0)])
def test_unrounded_threshold_boundaries(threshold, count):
    result = analyze(
        {
            "manuscripts": [
                {"id": "one", "titles": ["red road"]},
                {"id": "two", "titles": ["blue road"]},
            ],
            "similarity_threshold": threshold,
        }
    )
    assert len(result["collisions"]) == count
    assert (
        analyze(
            {
                "manuscripts": [{"id": "one", "titles": ["Road", " road "]}],
                "similarity_threshold": 1,
            }
        )["collisions"][0]["kind"]
        == "duplicate"
    )
    with pytest.raises(ValueError, match="between"):
        analyze({"manuscripts": [{"titles": []}], "similarity_threshold": 1.01})
