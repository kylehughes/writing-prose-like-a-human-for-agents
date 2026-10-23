# Writing Prose Like a Human for Agents

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-555)](https://agentskills.io)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code_Plugin-555?logo=claude)](https://code.claude.com/docs/en/plugins)
[![Codex Plugin](https://img.shields.io/badge/Codex_Plugin-555)](https://developers.openai.com/plugins/build/plugins)
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
