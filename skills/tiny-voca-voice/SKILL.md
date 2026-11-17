---
name: tiny-voca-voice
description: Generate local English speech with hash-chained receipts.
version: "1.0.0"
author: Yæl Méndez (@yaelmendez), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tts, voice, onnx, local, receipts, english]
    related_skills: []
---

# tiny-voca-voice Skill

`tiny-voca-voice` turns the tiny-voca ONNX model into a local Hermes TTS
provider. It speaks English only, writes a 24 kHz mono WAV, and appends a
`HUMAN://ROOT` receipt for each utterance. It does not train voices, clone
voices, or stream audio.

## When to Use

- The user asks for speech or an audio file from text and no cloud TTS is set.
- A native Hermes TTS provider is needed (`tts.provider: tiny-voca`).
- You need to list voices, inspect receipts, or verify the receipt chain.
- Don't use for: non-English text, singing, voice cloning, or real-time
  streaming; those are outside this model's scope.

## Prerequisites

- Python 3.11+ with `numpy`, `onnxruntime`, and `dizione` importable. They are
  loaded lazily, so packaging checks need only the standard library.
- Weights under `$TINY_VOCA_HOME`, falling back to `$HERMES_HOME/tiny-voca`.
  The file `onnx/model.onnx` must match SHA-256
  `fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46`.
- The plugin installed at `$HERMES_HOME/plugins/tiny-voca-voice` (run
  `terminal(command="sh install.sh")` from the repo root).
- Hermes tools: `terminal` to run scripts, `write_file` and `read_file` for
  text files, `search_files` to locate plugin assets.

## How to Run

Prefer the registered tools: `tts_speak`, `tts_voices`, `tts_receipts`, and
`tts_verify`. When exercising the CLI directly, always go through `terminal`.
The provider contract takes a UTF-8 text file and writes a WAV; the CLI prints
one JSON object on its last stdout line. Paths below are repo-relative or
environment-based — never hardcode a machine-local directory.

- `terminal(command="python3 scripts/tiny_voca_voice.py --text-file {input_path} --output {output_path} --voice M2")`
- For ad-hoc text, create the input file with `write_file` first, then call the
  CLI. `--text` is accepted, but `--text-file` is the native provider path.
- Use a timeout of at least 180 seconds: the ONNX session loads lazily.

## Quick Reference

- `terminal(command="python3 scripts/tiny_voca_voice.py --text-file in.txt --output out.wav --voice M2")`
- `terminal(command="python3 scripts/tiny_voca_verify.py")` — validate receipts.
- `terminal(command="python3 -m py_compile scripts/*.py tests/*.py __init__.py")`
- `terminal(command="python3 -m unittest discover -s tests -v")`
- `terminal(command="hermes config set tts.provider tiny-voca")` — enable native TTS.
- `read_file(path="skills/tiny-voca-voice/SKILL.md")` — this skill.
- `read_file(path="docs/NATIVE_TTS.md")` — provider config and troubleshooting.
- Voices: `F2` (`nous-girl`) and `M2` (`hermes-agent`); aliases are normalized.
- Receipts: `TTS://SPEAK`, authority `HUMAN://ROOT`, JSONL ledger.

## Procedure

1. Provision weights. With `terminal`, download `onnx/model.onnx` from the
   upstream URL and check its SHA-256.
   Completion: the checksum equals the value in Prerequisites.
2. Install the plugin: `terminal(command="sh install.sh")`.
   Completion: `scripts/tiny_voca_voice.py` exists under
   `$HERMES_HOME/plugins/tiny-voca-voice`.
3. Write the text with `write_file` to a UTF-8 input file.
   Completion: `read_file` shows exactly the text to speak.
4. Synthesize: call `tts_speak` with `text_file`, or the CLI through `terminal`
   with `--text-file` and `--output`.
   Completion: the last stdout line is JSON with `success:true`, canonical
   `voice`, `duration_s`, and a 64-hex `sha256`.
5. Check the artifact. With `terminal`, confirm the WAV exists and that its
   sha256 equals the JSON `sha256`. Completion: both values agree.
6. Check receipts with `read_file` on `$HERMES_HOME/tiny-voca-receipts.jsonl`:
   the last `TTS://SPEAK` entry's `prev` must equal the prior entry's `hash`.
   Completion: the chain links from the previous head.
7. Validate the chain with `tts_verify({})`.
   Completion: `success:true`, `ok:true`, and `broken_at:null`.
8. Enable native TTS: `terminal(command="hermes config set tts.provider tiny-voca")`.
   Completion: the built-in `text_to_speech` tool speaks a test line and the
   ledger gains a new receipt.

## Pitfalls

- English only: `dizione` cannot phonemize other languages, so the CLI returns
  `{"success": false, "error": "..."}` instead of a WAV.
- Long text is split into sentences of at most 300 characters and joined with
  180 ms of silence; a single utterance is capped at 512 tokens.
- The native provider is fixed to `M2`. Select `F2` with `--voice F2`, an alias,
  or the `tts_speak` tool's `voice` argument.
- The first call is slow while the lazy ONNX session loads; keep a generous
  `terminal` timeout.
- Weight and phonemizer paths follow `$TINY_VOCA_HOME` / `$HERMES_HOME/tiny-voca`.
  A missing `onnx/model.onnx` fails at session creation, not at argument parse.
- A receipt-write failure never breaks synthesis: `receipt` becomes `null` and
  `receipt_error` explains why. Check the ledger path
  (`HERMES_TINY_VOCA_LEDGER` overrides the default).
- `install.sh` is POSIX `sh`; on Windows, copy the plugin directory manually.
- Receipt verification checks hash linkage and content hashes, not authenticity.

## Verification

- `terminal(command="python3 -m unittest discover -s tests -v")` — all tests
  pass with no network access and no weights required.
- `terminal(command="python3 scripts/tiny_voca_voice.py --text-file in.txt --output out.wav")`
  — the last stdout line is JSON with `success:true`, `sample_rate:24000`, and
  a 64-hex `sha256`.
- Native path: after enabling the provider, the `text_to_speech` tool produces
  a WAV and `tts_verify({})` reports `ok:true`.
