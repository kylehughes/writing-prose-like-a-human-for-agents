# Writing Prose Like a Human for Agents

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-555?logo=claude)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code_Plugin-555?logo=claude)](https://code.claude.com/docs/en/plugins)
[![Latest Release](https://img.shields.io/github/v/release/kylehughes/writing-prose-like-a-human-for-agents)](https://github.com/kylehughes/writing-prose-like-a-human-for-agents/releases)

*A skill and subagent that help AI agents write and edit prose that doesn't read like AI.*

## About

A Claude Code plugin with an Agent Skill and a Subagent for writing prose that avoids statistical patterns common to LLM output.

- **Agent Skill**: Vocabulary watchlists, structural checks, and before/after examples for identifying AI writing patterns.
- **Subagent**: Edits files in place to remove AI writing patterns. Uses the Agent Skill.

## Usage

The Subagent edits prose in place, applying five rules: cut significance inflation, use plain verbs, end sentences at the fact, vary rhythm, earn every adjective. Delegate to it from your main agent to keep prose edits out of your context window.

The Agent Skill has the vocabulary watchlist and rules. Use it directly when you want more control than the Subagent gives you.

### Automatic

Claude Code sees both the Agent Skill and Subagent and can use them on its own when it thinks they're relevant. In practice this is nondeterministic.

### Manual

Tell Claude Code what you want in plain language.

> use the prose humanizer to clean up the README

> run the prose humanizer agent on this file

> rewrite this so it doesn't sound like AI

## What's Included

### Agent Skill: `writing-prose-like-a-human`

Five rules for human-sounding prose, a vocabulary watchlist of words that appear at elevated rates in LLM output, structural patterns to avoid, and a self-edit checklist. Includes a full reference with before/after examples.

### Subagent: `prose-humanizer`

Applies the five rules in order, edits files in place, and returns a summary of changes. Cuts rather than rephrases. Uses the `writing-prose-like-a-human` skill.

## Installation

### Claude Code

#### Personal Usage

To install this plugin for your personal use in Claude Code:

1. Add the marketplace:
   ```bash
   /plugin marketplace add kylehughes/writing-prose-like-a-human-for-agents
   ```

2. Install the plugin:
   ```bash
   /plugin install writing-prose-like-a-human@writing-prose-like-a-human-for-agents
   ```

#### Project Configuration

To automatically provide this plugin to everyone working in a repository, configure the repository's `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "writing-prose-like-a-human@writing-prose-like-a-human-for-agents": true
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

When team members open the project, Claude Code will prompt them to install the plugin.

### Manual Installation

The Agent Skill conforms to the [Agent Skills](https://agentskills.io) open standard and works with any compatible tool, not just Claude Code. Download `writing-prose-like-a-human-skill.zip` from the [releases page](https://github.com/kylehughes/writing-prose-like-a-human-for-agents/releases) and add it to your agent's skills directory. The raw content is also available in this repository's `skills/` and `agents/` directories.

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

Writing Prose Like a Human Claude Code Plugin is derived from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) by Wikipedia contributors and is available under the **[Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)**. See `LICENSE` for details.
