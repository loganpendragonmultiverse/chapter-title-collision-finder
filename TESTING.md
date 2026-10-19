# Testing

Install development tools with `python -m pip install -e ".[dev]"`.

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. Preserve the coverage gate and supported CI matrix.

## Version 1.2.0 acceptance

`tests/test_feature.py` covers the new option, boundary cases, and unchanged default reports using synthetic text only. Run `chapter-title-collisions examples/feature.json --format json` and the README sample commands against an installed wheel and an extracted source archive. Inspect packaged README, CHANGELOG, DEVELOPMENT and TESTING documents and confirm package version 1.2.0.

## 1.2.1 acceptance

Exercise malformed root and field shapes, the README examples, existing report files, dangling report symlinks, racing output creation and a real consumer-closed stdout pipe. Check unchanged source bytes and lexical evidence. Install the actual tag-built wheel and source distribution in isolation; run their CLI entrypoints away from the checkout and verify bundled handoff documents and examples. Retain all protected platform checks, CodeQL and the existing coverage floor.
