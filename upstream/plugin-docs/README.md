# Shopware Knowledge

Version-aware Shopware 6.6/6.7 development and review guidance for Claude Code and Codex. Includes backend/DAL, classic storefront, administration, CMS, cart/checkout, payments, recurring commerce, caching, queues, indexing, translations, accessibility, and tests.

## Installation

Use the marketplace or portable-skill instructions in the [repository README](../../README.md). The plugin name is `shopware-knowledge`; the skill name remains `shopware-development`.

```bash
/plugin install shopware-knowledge@shopware-ai-coding-tools
# Codex
codex plugin add shopware-knowledge@shopware-ai-coding-tools
```

The skill opts into the host portable exporter through its `.agent-skills` marker. A portable export strips the native top-level version into metadata; it contains the same self-contained references. This preparation does not publish a new release artifact.

Claude Code: `/shopware-knowledge:shopware-development <task>` (or the unqualified skill name when unique). Codex: `$shopware-development <task>`. Natural-language Shopware requests can also discover the skill.

No MCP server, hook, executable service, extra credentials, or other plugin is required. Runtime permissions and repository instructions still apply. Existing `test-writing`, `contributor-writing`, `shopware-documentation`, and `shopware-env` plugins retain their specialized workflow ownership.

## Scope

The entrypoint selects a mode and topic; examples live beside their owning rules. References do not cap reasoning or investigation. Version-sensitive behavior must be checked against installed source or a matching stable core tag.

- [Skill entrypoint](../../plugins/shopware-knowledge/skills/shopware-development/SKILL.md)
- [Topic/applicability index](../../plugins/shopware-knowledge/knowledge-index.json)
- [Changelog](CHANGELOG.md)
- [Maintenance and validation](AGENTS.md)

The index is maintainer metadata, not an additional runtime classification step. Future filtered retrieval can use the same corpus; the portable skill remains self-contained.
