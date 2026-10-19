# Chapter Title Collision Finder

[![CI](https://github.com/loganpendragonmultiverse/chapter-title-collision-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/chapter-title-collision-finder/actions/workflows/ci.yml)

Find duplicate and confusingly similar chapter titles within or across manuscripts. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
chapter-title-collisions examples/sample.json
chapter-title-collisions examples/sample.json --format json --output report.json
```

The example documents the complete input shape. Version 1.1 supports `similarity_threshold`, `ignore_words`, and `comparison_scope` (`all`, `within`, or `cross`) and reports shared-token evidence for each candidate. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All title lists stay local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

Similarity is lexical and deliberately conservative. Shared thematic words may be intentional, and meaning is not inferred.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.2.0: manuscript identity

Give every manuscript a unique, nonempty string `id` to compare books independently of their display `name`. For example, `{"id":"draft-a","name":"Untitled","titles":["Arrival"]}` and `{"id":"draft-b","name":"Untitled","titles":["Arrival"]}` produce a cross-manuscript duplicate. When any ID is supplied, all manuscripts must have IDs, and duplicates are rejected even for empty title lists. Findings retain the display name and add `manuscript_id`. Without IDs, the legacy name-based comparison and output remain unchanged. Thresholds still use the unrounded Jaccard score; exact title duplicates always match.

Try the synthetic example:

```bash
chapter-title-collisions examples/feature.json --format json
```

## Validation and report files — 1.2.1

Input must be a JSON object. `manuscripts` is a nonempty array of objects; each optional `titles` value is an array of strings, and each supplied `name` is a string. Empty title arrays are allowed. `ignore_words` is an array of strings. `similarity_threshold` is a finite JSON number between 0 and 1; booleans and numeric strings are rejected.

Reports must use new destinations: existing files, directories and symlinks are refused. Invalid inputs and output errors return status 2; success returns 0. Closed stdout pipes are handled inside the command. A failed new report write may leave a partial file; power-loss transactions are not promised. Inputs remain read-only.

Install a downloaded release wheel with `python -m pip install ./PACKAGE.whl`, using the actual filename. The source distribution can also be installed with pip. The installed package includes README, changelog, development/testing instructions, license and examples under `share/doc/chapter-title-collision-finder/` in the installation prefix. The repository checkout is convenient for running the example paths as written.
