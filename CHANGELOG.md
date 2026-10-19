# Changelog

## 1.2.1 - 2026-10-19

- Validate manuscript/title arrays, ignored-word lists and numeric thresholds while preserving manuscript identity and lexical matching.
- Create report files exclusively, refuse symlink destinations and return a clean error for closed stdout pipes.
- Include release handoff documents and their license with the installed package.

## 1.2.0 - 2026-10-16

- Added manuscript identity.
- Preserved legacy defaults and added synthetic boundary and compatibility tests.

## 1.1.0 - 2026-07-27

- Added configurable similarity thresholds, ignored words, and within/cross-manuscript scopes.
- Added shared-token evidence and scope labels to findings.

## 1.0.0 - 2026-07-26

- Released the first complete Chapter Title Collision Finder command-line workflow.
- Added deterministic JSON and Markdown reporting, representative examples, and cross-platform tests.
