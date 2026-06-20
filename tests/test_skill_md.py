from pathlib import Path

def test_skill_md_has_frontmatter_and_honesty_rule():
    text=(Path(__file__).parents[1]/'skills/shipvitals/SKILL.md').read_text()
    assert text.startswith('---')
    assert 'NOT VERIFIED' in text
    assert len(text) < 9000
