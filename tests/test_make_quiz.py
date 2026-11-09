import json
import pytest
from app import tools

@pytest.mark.parametrize("lecture", [1,2,3])
def test_quiz_matches_requested_lecture(lecture):
    quiz=json.loads(tools.make_quiz(lecture))
    assert any(quiz["question"] == f"「{e['term']}」の意味は？" and quiz["answer"] == e["definition"] for e in tools.load_glossary() if e["lecture"] == lecture)

@pytest.mark.parametrize("lecture", [0,-1,99])
def test_missing_lecture(lecture):
    assert "ありません" in json.loads(tools.make_quiz(lecture))["error"]
