"""Fresh-clone acceptance for tiny-voca-voice.

Checks packaging, registration, tool contracts, portability, and syntax.
Does not download weights or require ONNX Runtime.
"""
import importlib.util, json, os, py_compile, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FakeCtx:
    def __init__(self):
        self.tools = {}
        self.skills = {}
        self.hooks = {}

    def register_tool(self, name, toolset, handler, schema):
        self.tools[name] = (handler, schema)

    def register_skill(self, name, path):
        self.skills[name] = Path(path)

    def register_hook(self, name, handler):
        self.hooks[name] = handler


def main():
    with tempfile.TemporaryDirectory(prefix="tiny-voca-acceptance-") as tmp:
        os.environ["HERMES_HOME"] = tmp
        spec = importlib.util.spec_from_file_location("tiny_voca_acceptance", ROOT / "__init__.py")
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ctx = FakeCtx()
        mod.register(ctx)
        assert sorted(ctx.tools) == ["tts_receipts", "tts_speak", "tts_stick_lesson", "tts_verify", "tts_voices"], sorted(ctx.tools)

        voices = json.loads(ctx.tools["tts_voices"][0]({}))
        assert voices["success"] and [v["name"] for v in voices["voices"]] == ["nous-girl", "hermes-agent"]
        receipts = json.loads(ctx.tools["tts_receipts"][0]({"limit": 3}))
        assert receipts["success"] and receipts["count"] == 0

        lessons = json.loads(ctx.tools["tts_stick_lesson"][0]({"op": "list"}))
        assert lessons["success"] and [x["id"] for x in lessons["lessons"]] == [
            "asimov-authority", "asimov-verbs", "asimov-twin"], lessons

        for p in ROOT.rglob("*.py"):
            if any(part in {".git", "__pycache__"} for part in p.parts):
                continue
            py_compile.compile(str(p), doraise=True)

        bad_root = "/opt" + "/data"
        offenders = []
        for p in ROOT.rglob("*"):
            if not p.is_file() or any(part in {".git", "__pycache__"} for part in p.parts):
                continue
            if p.suffix in {".py", ".yaml", ".toml", ".md", ".sh"}:
                if bad_root in p.read_text(encoding="utf-8", errors="replace"):
                    offenders.append(str(p.relative_to(ROOT)))
        assert not offenders, offenders

    print(json.dumps({"success": True, "tools": sorted(ctx.tools), "version": "1.1.0",
                      "authority": "HUMAN://ROOT", "portable": True,
                      "stick_lessons": 3}))


if __name__ == "__main__":
    main()
