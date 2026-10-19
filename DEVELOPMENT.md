# Development contract

Find duplicate and confusingly similar chapter titles within or across manuscripts.

Version 1.1 makes thresholds, ignored words, and comparison scope explicit and retains shared-token evidence.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## Version 1.2.0

Give every manuscript a unique, nonempty string `id` to compare books independently of their display `name`. For example, `{"id":"draft-a","name":"Untitled","titles":["Arrival"]}` and `{"id":"draft-b","name":"Untitled","titles":["Arrival"]}` produce a cross-manuscript duplicate. When any ID is supplied, all manuscripts must have IDs, and duplicates are rejected even for empty title lists. Findings retain the display name and add `manuscript_id`. Without IDs, the legacy name-based comparison and output remain unchanged. Thresholds still use the unrounded Jaccard score; exact title duplicates always match.

## 1.2.1 maintenance

- Validate manuscript/title arrays, ignored-word lists and numeric thresholds while preserving manuscript identity and lexical matching.
- Create report files exclusively, refuse symlink destinations and return a clean error for closed stdout pipes.
- Include release handoff documents and their license with the installed package.

Preserve manuscript identity, unrounded similarity thresholds and the documented lexical interpretation limits. Release through independent review, protected CI and exact tag-built installed-distribution acceptance.
