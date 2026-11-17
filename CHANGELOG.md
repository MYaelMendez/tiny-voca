# Changelog

All notable changes to `tiny-voca-voice` are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-17

### Added

- First-class Hermes packaging for the tiny-voca voice layer.
- `scripts/tiny_voca_voice.py` provider contract: `--text-file` in, WAV out,
  one JSON object on the last stdout line, with canonical `voice`, supplied
  `alias`, `sha256`, `duration_s`, and `receipt` fields.
- Native TTS provider `tiny-voca` with `type: command`, `output_format: wav`,
  and `voice_compatible: true`; enable with
  `hermes config set tts.provider tiny-voca`.
- Four registered tools — `tts_speak`, `tts_voices`, `tts_receipts`, and
  `tts_verify` — plus the `speak` / `voices` shortcuts in the parent `ae` tool.
- Voice aliases: `nous-girl` and variants resolve to `F2`; `hermes-agent` and
  variants resolve to `M2`. Alias normalization is case-insensitive.
- `HUMAN://ROOT` hash-chained `TTS://SPEAK` receipts on a JSONL ledger, with a
  64-zero genesis `prev` and `sha256(prev || canonical_json(body))` linkage.
- Runtime root override `TINY_VOCA_HOME`, falling back to
  `$HERMES_HOME/tiny-voca`; SHA-256 verification for `onnx/model.onnx`.
- `skills/tiny-voca-voice/SKILL.md` and `docs/NATIVE_TTS.md`.
- `install.sh`, Apache-2.0 `LICENSE`, `NOTICE.md`, `.gitignore`, and a CI
  workflow limited to `py_compile` and `unittest`.

### Notes

- Weights are not vendored; download and verify them before first use.
- Upstream: `n4ze3m/tiny-voca` and `n4ze3m/dizione` (both Apache-2.0).

[1.0.0]: https://github.com/n4ze3m/tiny-voca/releases/tag/v1.0.0
