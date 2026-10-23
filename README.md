# Writing Prose Like a Human for Agents

[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code_Plugin-555?logo=claude)](https://code.claude.com/docs/en/plugins)
[![Codex Plugin][codex_plugin_badge]](https://developers.openai.com/plugins/build/plugins)
[![CI](https://github.com/kylehughes/writing-prose-like-a-human-for-agents/actions/workflows/check.yml/badge.svg?branch=main)](https://github.com/kylehughes/writing-prose-like-a-human-for-agents/actions/workflows/check.yml)
[![Latest Release](https://img.shields.io/github/v/release/kylehughes/writing-prose-like-a-human-for-agents)](https://github.com/kylehughes/writing-prose-like-a-human-for-agents/releases)

A shared prose-editing skill for Claude Code and Codex. It reduces generic phrasing, inflated claims, and repetitive structure while preserving facts and the author's voice.

The guidance adapts [Wikipedia's “Signs of AI writing” essay](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) into five editing rules: be specific, use plain verbs, remove empty commentary, vary rhythm, and earn every adjective. Vocabulary and formatting patterns prompt judgment; they are not word bans or evidence of AI authorship.

## Installation

### Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add kylehughes/writing-prose-like-a-human-for-agents
/plugin install writing-prose-like-a-human-for-agents@writing-prose-like-a-human-for-agents
```

Start a new session after installation. The plugin includes the shared skill and a `prose-humanizer` subagent for delegated edits.

For a team repository, merge the following into `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "writing-prose-like-a-human-for-agents@writing-prose-like-a-human-for-agents": true
  },
  "extraKnownMarketplaces": {
    "writing-prose-like-a-human-for-agents": {
      "source": {
        "source": "github",
        "repo": "kylehughes/writing-prose-like-a-human-for-agents"
      }
    }
  }
}
```

Claude Code prompts team members to install the plugin when they trust the repository's marketplace configuration. See [Claude Code's marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).

### Codex

With a Codex CLI version that supports plugin marketplaces, run:

```sh
codex plugin marketplace add kylehughes/writing-prose-like-a-human-for-agents
codex plugin add writing-prose-like-a-human-for-agents@writing-prose-like-a-human-for-agents
```

Start a new session after installation. The same skill is available in Codex; the Claude Markdown subagent is not registered as a native Codex agent. Codex can apply the skill directly or pass its instructions to an available native worker when delegation suits the task.

These commands use Codex's [plugin marketplace support](https://learn.chatgpt.com/docs/cli/reference#codex-plugin-marketplace). The repository includes a portable `plugin.json`, a compatible `.codex-plugin/plugin.json`, and a Codex marketplace catalog.

### Standalone skill

Download `writing-prose-like-a-human-skill.zip` from the [releases page](https://github.com/kylehughes/writing-prose-like-a-human-for-agents/releases). Extract it into a directory named `writing-prose-like-a-human` in your host's skills directory. The archive has `SKILL.md` at its root and includes its reference, attribution, UI metadata, and license.

For Codex, a user-level skill can live at `~/.agents/skills/writing-prose-like-a-human/`. Use either the standalone skill or the plugin to avoid duplicate discovery. Other [Agent Skills](https://agentskills.io) hosts can use the same directory.

## Usage

Ask for the edit in plain language:

> Edit this README for clarity while preserving its technical meaning.

> Make this paragraph less formulaic. Keep the facts and uncertainty intact.

> Review this draft for inflated claims without editing the file.

The skill can be selected automatically when its description matches your task. To select it explicitly in Codex, type `$` and choose `writing-prose-like-a-human-for-agents:writing-prose-like-a-human` from the skill picker. A standalone installation uses `$writing-prose-like-a-human`. In Claude Code, use `/writing-prose-like-a-human-for-agents:writing-prose-like-a-human`, or ask Claude to delegate to the `prose-humanizer` agent.

Reviews stay read-only. Rewrites preserve supplied facts, citations, qualifications, and the intended voice; they do not invent details to make a passage more specific. Code, commands, identifiers, frontmatter, and structured data stay intact unless you ask to change them.

The short [skill](skills/writing-prose-like-a-human/SKILL.md) contains the workflow. Its [reference](skills/writing-prose-like-a-human/REFERENCE.md) adds contextual vocabulary checks and before/after examples. No extra tools, credentials, or runtime dependencies are needed to use the skill.

## Development

Use Python 3.10 or later for the repository checks and packaging:

```sh
python3 scripts/check.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/package.py
```

The checks verify manifest consistency, packaged paths, skill metadata, local references, and attribution. Packaging creates the standalone skill archive and `dist/writing-prose-like-a-human-plugin.zip`, which contains the shared skill, Claude subagent, runtime manifests, and license.

Validate a local checkout with Claude Code:

```sh
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
claude --plugin-dir .
```

Claude's validator warns that the checkout's `CLAUDE.md` is not installed plugin context. It imports maintainer instructions from `AGENTS.md`; both files are excluded from the plugin archive. Validate the extracted plugin archive with `--strict` to check the shipping contents without that repository-only warning.

To test the local marketplace in Codex, run `codex plugin marketplace add "$PWD"`, install the plugin with the command above, and start a new session. When switching between a local checkout and the GitHub marketplace, remove the existing source with `codex plugin marketplace remove writing-prose-like-a-human-for-agents` before adding the replacement.

### Source updates

Read the current Wikipedia essay before updating its adaptation. Record the consulted revision and changes in [ATTRIBUTION.md](skills/writing-prose-like-a-human/ATTRIBUTION.md). Check every example for invented facts, lost qualifications, and changes in meaning. Keep the entrypoint short and load detailed guidance from the reference as needed.

### Releases

From a clean `main` branch, check a proposed release without changing the repository:

```sh
./release.sh --dry-run 1.2.1
```

Run `./release.sh 1.2.1` to update all manifest versions, validate and package the content, commit, tag, and push the branch and new tag together. The release workflow checks that the tag matches the manifests and publishes both ZIP archives. The existing standalone archive name and layout remain compatible with earlier releases.

## Contributions

Not accepting source contributions. Bug reports are welcome.

## Author

[Kyle Hughes](https://kylehugh.es)

[![Bluesky][bluesky_image]][bluesky_url]  
[![LinkedIn][linkedin_image]][linkedin_url]  
[![Mastodon][mastodon_image]][mastodon_url]

[bluesky_image]: https://img.shields.io/badge/Bluesky-0285FF?logo=bluesky&logoColor=fff
[bluesky_url]: https://bsky.app/profile/kylehugh.es
[linkedin_image]: https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=fff
[linkedin_url]: https://www.linkedin.com/in/kyle-hughes
[mastodon_image]: https://img.shields.io/mastodon/follow/109356914477272810?domain=https%3A%2F%2Fmister.computer&style=social
[mastodon_url]: https://mister.computer/@kyle

## License

Derived from Wikipedia's “Signs of AI writing” by Wikipedia contributors and distributed under [CC BY-SA 4.0](LICENSE). See [ATTRIBUTION.md](skills/writing-prose-like-a-human/ATTRIBUTION.md) for the source revision and adaptation history.

<!-- Official OpenAI artwork: https://cdn.openai.com/brand/OpenAI-Logos-2025.zip -->
[codex_plugin_badge]: https://img.shields.io/badge/Codex_Plugin-555?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjExOC41NTcgMTIwLjc1OCA0ODQuMTM5IDQ3OS44MTgiPjxwYXRoIGZpbGw9IndoaXRlIiBkPSJNMzA0LjI0NiAyOTUuNDExVjI0OS44MjhDMzA0LjI0NiAyNDUuOTg5IDMwNS42ODcgMjQzLjEwOSAzMDkuMDQ0IDI0MS4xOTFMNDAwLjY5MiAxODguNDEyQzQxMy4xNjcgMTgxLjIxNSA0MjguMDQyIDE3Ny44NTggNDQzLjM5NCAxNzcuODU4QzUwMC45NzEgMTc3Ljg1OCA1MzcuNDQgMjIyLjQ4MiA1MzcuNDQgMjY5Ljk4MkM1MzcuNDQgMjczLjM0IDUzNy40NCAyNzcuMTc5IDUzNi45NTkgMjgxLjAxOEw0NDEuOTU0IDIyNS4zNThDNDM2LjE5NyAyMjIgNDMwLjQzNyAyMjIgNDI0LjY4IDIyNS4zNThMMzA0LjI0NiAyOTUuNDExWk01MTguMjQ1IDQ3Mi45NDVWMzY0LjAyNEM1MTguMjQ1IDM1Ny4zMDQgNTE1LjM2NCAzNTIuNTA3IDUwOS42MDggMzQ5LjE0OUwzODkuMTc0IDI3OS4wOTZMNDI4LjUxOSAyNTYuNTQzQzQzMS44NzcgMjU0LjYyNiA0MzQuNzU3IDI1NC42MjYgNDM4LjExNSAyNTYuNTQzTDUyOS43NjIgMzA5LjMyM0M1NTYuMTU0IDMyNC42NzkgNTczLjkwNSAzNTcuMzA0IDU3My45MDUgMzg4Ljk3MUM1NzMuOTA1IDQyNS40MzYgNTUyLjMxNSA0NTkuMDI0IDUxOC4yNDUgNDcyLjk0MVY0NzIuOTQ1Wk0yNzUuOTM3IDM3Ni45ODJMMjM2LjU5MiAzNTMuOTUyQzIzMy4yMzUgMzUyLjAzNCAyMzEuNzk0IDM0OS4xNTQgMjMxLjc5NCAzNDUuMzE1VjIzOS43NTZDMjMxLjc5NCAxODguNDE2IDI3MS4xMzkgMTQ5LjU0OCAzMjQuNCAxNDkuNTQ4QzM0NC41NTUgMTQ5LjU0OCAzNjMuMjY0IDE1Ni4yNjggMzc5LjEwMiAxNjguMjYyTDI4NC41NzggMjIyLjk2NEMyNzguODIyIDIyNi4zMjEgMjc1Ljk0MiAyMzEuMTE5IDI3NS45NDIgMjM3LjgzOFYzNzYuOTg2TDI3NS45MzcgMzc2Ljk4MlpNMzYwLjYyNiA0MjUuOTIyTDMwNC4yNDYgMzk0LjI1NVYzMjcuMDgzTDM2MC42MjYgMjk1LjQxNkw0MTcuMDAyIDMyNy4wODNWMzk0LjI1NUwzNjAuNjI2IDQyNS45MjJaTTM5Ni44NTIgNTcxLjc4OUMzNzYuNjk4IDU3MS43ODkgMzU3Ljk4OSA1NjUuMDcgMzQyLjE1MSA1NTMuMDc1TDQzNi42NzQgNDk4LjM3NEM0NDIuNDMxIDQ5NS4wMTcgNDQ1LjMxMSA0OTAuMjE5IDQ0NS4zMTEgNDgzLjQ5OVYzNDQuMzUyTDQ4NS4xMzggMzY3LjM4MkM0ODguNDk1IDM2OS4yOTkgNDg5LjkzNiAzNzIuMTc5IDQ4OS45MzYgMzc2LjAxOFY0ODEuNTc3QzQ4OS45MzYgNTMyLjkxNyA0NTAuMTA5IDU3MS43ODUgMzk2Ljg1MiA1NzEuNzg1VjU3MS43ODlaTTI4My4xMzQgNDY0Ljc5TDE5MS40ODYgNDEyLjAxQzE2NS4wOTQgMzk2LjY1NCAxNDcuMzQzIDM2NC4wMjkgMTQ3LjM0MyAzMzIuMzYyQzE0Ny4zNDMgMjk1LjQxNiAxNjkuNDE1IDI2Mi4zMDkgMjAzLjQ4IDI0OC4zOTNWMzU3Ljc5MUMyMDMuNDggMzY0LjUxIDIwNi4zNjEgMzY5LjMwOCAyMTIuMTE3IDM3Mi42NjVMMzMyLjA3NCA0NDIuMjM3TDI5Mi43MjkgNDY0Ljc5QzI4OS4zNzIgNDY2LjcwNyAyODYuNDkxIDQ2Ni43MDcgMjgzLjEzNCA0NjQuNzlaTTI3Ny44NTkgNTQzLjQ4QzIyMy42MzkgNTQzLjQ4IDE4My44MTMgNTAyLjY5NSAxODMuODEzIDQ1Mi4zMTRDMTgzLjgxMyA0NDguNDc1IDE4NC4yOTQgNDQ0LjYzNiAxODQuNzcxIDQ0MC43OTdMMjc5LjI5NSA0OTUuNDk4QzI4NS4wNTEgNDk4Ljg1NiAyOTAuODEyIDQ5OC44NTYgMjk2LjU2OCA0OTUuNDk4TDQxNy4wMDIgNDI1LjkyN1Y0NzEuNTA5QzQxNy4wMDIgNDc1LjM0OSA0MTUuNTYyIDQ3OC4yMjkgNDEyLjIwNCA0ODAuMTQ2TDMyMC41NTcgNTMyLjkyNkMzMDguMDgxIDU0MC4xMjIgMjkzLjIwNiA1NDMuNDggMjc3Ljg1NCA1NDMuNDhIMjc3Ljg1OVpNMzk2Ljg1MiA2MDAuNTc2QzQ1NC45MTEgNjAwLjU3NiA1MDMuMzcgNTU5LjMxMyA1MTQuNDEgNTA0LjYxMkM1NjguMTQ5IDQ5MC42OTYgNjAyLjY5NiA0NDAuMzE1IDYwMi42OTYgMzg4Ljk3NkM2MDIuNjk2IDM1NS4zODcgNTg4LjMwMyAzMjIuNzYyIDU2Mi4zOTIgMjk5LjI1QzU2NC43OTEgMjg5LjE3MyA1NjYuMjMxIDI3OS4wOTYgNTY2LjIzMSAyNjkuMDI0QzU2Ni4yMzEgMjAwLjQxMSA1MTAuNTcxIDE0OS4wNjcgNDQ2LjI3NCAxNDkuMDY3QzQzMy4zMjIgMTQ5LjA2NyA0MjAuODQ2IDE1MC45ODQgNDA4LjM3IDE1NS4zMDVDMzg2Ljc3NSAxMzQuMTkyIDM1Ny4wMjYgMTIwLjc1OCAzMjQuNCAxMjAuNzU4QzI2Ni4zNDIgMTIwLjc1OCAyMTcuODgzIDE2Mi4wMiAyMDYuODQzIDIxNi43MjFDMTUzLjEwNCAyMzAuNjM3IDExOC41NTcgMjgxLjAxOCAxMTguNTU3IDMzMi4zNTdDMTE4LjU1NyAzNjUuOTQ2IDEzMi45NSAzOTguNTcxIDE1OC44NjEgNDIyLjA4M0MxNTYuNDYyIDQzMi4xNiAxNTUuMDIyIDQ0Mi4yMzcgMTU1LjAyMiA0NTIuMzA5QzE1NS4wMjIgNTIwLjkyMiAyMTAuNjgyIDU3Mi4yNjYgMjc0Ljk3OCA1NzIuMjY2QzI4Ny45MzEgNTcyLjI2NiAzMDAuNDA3IDU3MC4zNDkgMzEyLjg4MyA1NjYuMDI4QzMzNC40NzMgNTg3LjE0MSAzNjQuMjIyIDYwMC41NzYgMzk2Ljg1MiA2MDAuNTc2WiIvPjwvc3ZnPg%3D%3D
