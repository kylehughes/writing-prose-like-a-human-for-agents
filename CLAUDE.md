# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Contains

A Claude Code plugin (`writing-prose-like-a-human`) with one skill and one subagent for writing and editing prose that avoids statistical patterns common to LLM output. Derived from Wikipedia's "Signs of AI writing" page.

## Repository Structure

- `skills/writing-prose-like-a-human/SKILL.md` — Entry point with YAML frontmatter, core rules, vocabulary watchlist
- `skills/writing-prose-like-a-human/REFERENCE.md` — Full guide with exhaustive examples and vocabulary tables
- `skills/writing-prose-like-a-human/ATTRIBUTION.md` — CC BY-SA 4.0 attribution to Wikipedia source
- `agents/prose-humanizer.md` — Autonomous prose editor subagent
- `.claude-plugin/marketplace.json` — Plugin metadata; paths in `skills` and `agents` arrays must match the filesystem

## Releasing

`./release.sh <version>` bumps the version in `marketplace.json`, commits, tags, and pushes. The GitHub Actions workflow (`.github/workflows/release.yml`) creates a GitHub release and attaches `writing-prose-like-a-human-skill.zip` (the skill directory zipped at root level).

## Key Design Principles

1. **Subtraction over addition**: The skill and agent only cut and simplify — they never add content
2. **Rules applied in order**: The five rules have a specific sequence (significance → verbs → participial phrases → rhythm → adjectives)
3. **Vocabulary-driven**: The watchlist is the core artifact — words and phrases that appear at statistically elevated rates in LLM output
4. **Before/after pairs**: Every rule is illustrated with concrete examples showing the transformation
5. **Author preservation**: The goal is to make text sound like a better version of the author, not like a different person

## Licensing

This repository is **CC BY-SA 4.0**, not MIT. The skill content is derived from a Wikipedia page licensed under CC BY-SA 4.0, which requires ShareAlike. Any modifications to the skill content must remain under CC BY-SA 4.0 with proper attribution in `ATTRIBUTION.md`.
