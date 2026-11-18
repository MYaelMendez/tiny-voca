"""Stdlib-only packaging checks; no network, weights, or heavy imports."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PackagingTest(unittest.TestCase):
    def test_cli_contract_strings(self):
        src = (ROOT / "scripts" / "tiny_voca_voice.py").read_text(encoding="utf-8")
        for token in ("--text-file", "--output", "print(json.dumps(", "sha256"):
            self.assertIn(token, src, f"CLI source missing {token!r}")

    def test_skill_frontmatter(self):
        content = (ROOT / "skills" / "tiny-voca-voice" / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "SKILL.md must start with ---")
        parts = content.split("---\n", 2)
        self.assertGreaterEqual(len(parts), 3, "frontmatter must close with ---")
        fm = parts[1]
        for key in ("name:", "description:", "version:", "author:",
                    "license:", "platforms:", "metadata:"):
            self.assertIn(key, fm, f"frontmatter missing {key}")
        m = re.search(r"^description:\s*(.+)$", fm, re.M)
        self.assertIsNotNone(m)
        desc = m.group(1).strip().strip('"')
        self.assertLessEqual(len(desc), 60, "description exceeds 60 chars")
        self.assertTrue(desc.endswith("."), "description must end with a period")
        for section in ("When to Use", "Prerequisites", "How to Run",
                        "Quick Reference", "Procedure", "Pitfalls", "Verification"):
            self.assertIn(f"## {section}", content, f"missing section {section}")

    def test_stick_lesson_assets_and_skill(self):
        assets = ROOT / "assets" / "stick-scene"
        for rel in ("stick.js", "LICENSE", "scenes/asimov-authority.js",
                    "scenes/asimov-verbs.js", "scenes/asimov-twin.js"):
            self.assertTrue((assets / rel).exists(), f"missing asset {rel}")
        skill = (ROOT / "skills" / "tiny-voca-voice" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("tts_stick_lesson", skill)
        self.assertIn("Asimov stick lessons", skill)

    def test_install_prints_provider_command(self):
        install = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("hermes config set tts.provider tiny-voca", install)
        self.assertIn("plugins/tiny-voca-voice", install)

    def test_ci_is_compile_and_unittest_only(self):
        ci = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")
        self.assertIn("py_compile", ci)
        self.assertIn("unittest", ci)
        self.assertNotIn("acceptance.py", ci)


if __name__ == "__main__":
    unittest.main()
