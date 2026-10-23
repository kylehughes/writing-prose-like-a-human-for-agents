# Repository guidance

This repository distributes Writing Prose Like a Human for Claude Code, Codex, and other Agent Skills hosts. Keep one shared skill under `skills/writing-prose-like-a-human/`.

## Content

- `SKILL.md` contains the editing workflow; `REFERENCE.md` supplies optional examples and vocabulary guidance. Keep detailed guidance in the reference rather than duplicating it in the entrypoint or agent.
- `agents/prose-humanizer.md` is a Claude Code subagent wrapper. It is not a native Codex agent registration.
- Preserve supplied facts, uncertainty, citations, technical meaning, and author voice. Every before/after example must preserve its factual basis. Editing should not invent specifics or erase meaningful caveats.
- Treat the source's patterns as editing prompts, not proof of AI authorship. Do not introduce word bans, punctuation quotas, or promises to defeat detectors.
- When refreshing from Wikipedia, inspect the current source and update `ATTRIBUTION.md` with the revision consulted and the changes made. Keep the five-rule organization where it remains useful.

## Packaging and checks

`plugin.json` is the portable manifest. `.codex-plugin/plugin.json` supplies the compatible Codex manifest and interface metadata; `.claude-plugin/plugin.json` declares the Claude plugin. Both marketplace files point to this repository root. Keep identities and release versions synchronized; do not rename the published plugin or skill without an explicit migration.

Run `python3 scripts/check.py`, `python3 -m unittest discover -s scripts -p 'test_*.py'`, and `python3 scripts/package.py` after changes. Validate the Claude manifests with `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .claude-plugin/marketplace.json`. For runtime checks, use the local marketplace in Codex and verify skill discovery separately from Claude subagent discovery.

The standalone skill ZIP keeps `SKILL.md` at its root for compatibility. Both release archives must include the license and attribution. Package only runtime content; exclude repository instructions, build tooling, local settings, and caches.

## Releases

`./release.sh --dry-run <version>` checks release preconditions without changing files. `./release.sh <version>` updates the manifests, validates, commits `Release <version>`, creates the matching tag, and pushes the main branch and that tag. Run the publishing command only when a release is requested. GitHub Actions validates the tag and builds both archives before publishing the release.

## License

The content is derived from Wikipedia's “Signs of AI writing” essay and distributed under CC BY-SA 4.0. Preserve `LICENSE`, the source attribution, and the notice describing modifications in every distribution.
