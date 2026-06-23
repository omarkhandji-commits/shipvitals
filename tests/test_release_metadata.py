import json
import re
import tomllib
from pathlib import Path

from shipvitals_cli import __version__


ROOT = Path(__file__).parents[1]


def test_release_versions_are_aligned():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    cli_package = json.loads((ROOT / "cli/package.json").read_text(encoding="utf-8"))
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    npm_version = package["version"]
    assert cli_package["version"] == npm_version
    assert pyproject["project"]["version"].replace("b", "-beta.") == npm_version
    assert __version__.replace("b", "-beta.") == npm_version


def test_skill_metadata_matches_folder():
    skill = (ROOT / "skills/shipvitals/SKILL.md").read_text(encoding="utf-8")
    assert re.search(r"^name: shipvitals$", skill, re.MULTILINE)

    interface = ROOT / "skills/shipvitals/agents/openai.yaml"
    assert interface.exists()
    assert "$shipvitals" in interface.read_text(encoding="utf-8")


def test_public_files_have_no_owner_placeholders():
    public_roots = [
        ROOT / "README.md",
        ROOT / "README_ACTION.md",
        ROOT / "docs",
        ROOT / "registry",
        ROOT / "marketing",
        ROOT / "case-studies",
        ROOT / ".github",
    ]
    unresolved = []

    for public_root in public_roots:
        files = [public_root] if public_root.is_file() else public_root.rglob("*")
        for path in files:
            if not path.is_file() or path.suffix.lower() not in {".md", ".yml", ".yaml", ".json"}:
                continue
            text = path.read_text(encoding="utf-8")
            if "github.com/OWNER" in text or "owner/shipvitals" in text:
                unresolved.append(str(path.relative_to(ROOT)))

    assert unresolved == []


def test_action_is_a_gate_and_exposes_verdict():
    action = (ROOT / "action.yml").read_text(encoding="utf-8")
    assert "value: ${{ steps.audit.outputs.verdict }}" in action
    assert "id: audit" in action
    assert 'default: "true"' in action
    assert "INPUT_FAIL_ON_UNREADY:" in action
    assert 'if [ "$INPUT_FAIL_ON_UNREADY" = "true" ]' in action
    run_block = action.split("      run: |", 1)[1]
    assert "inputs." not in run_block
    assert '[ "$verdict" != "READY" ]' in action
