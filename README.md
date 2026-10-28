# Shopware Knowledge for Claude Code and Codex

Shopware 6.7 development and review guidance with explicit 6.6 compatibility. One self-contained skill covers backend/DAL, classic storefront, administration, CMS, payments, recurring commerce, cart/checkout, cache/Varnish, queues, indexing, translations, accessibility, and testing.

This branch prepares **shopware-knowledge 0.10.0** for review and integration into Shopware AI Coding Tools. It is not a published release. The plugin name changes; the skill remains `shopware-development`. References do not limit reasoning, investigation, or solution breadth.

## Install the Review Branch

### Claude Code CLI and Code Sessions in the Desktop App

Register the branch marketplace once, then install its plugin:

```text
/plugin marketplace add biotech-shopware/claude-shopware-skill#ai-tooling-refactoring
/plugin install shopware-knowledge@biotech-shopware-skills
```

Invoke `/shopware-knowledge:shopware-development <task>`; when unique, the unqualified skill name also works. Marketplace registration and plugin installation are separate operations. This installs into Claude Code, not ordinary Claude app chat.

For an isolated local preview:

```bash
git clone --branch ai-tooling-refactoring https://github.com/biotech-shopware/claude-shopware-skill.git
cd claude-shopware-skill
claude --plugin-dir ./plugins/shopware-knowledge
```

### Codex CLI, IDE Extension, and Desktop App

With a Codex version supporting plugins:

```bash
codex plugin marketplace add biotech-shopware/claude-shopware-skill --ref ai-tooling-refactoring
codex plugin add shopware-knowledge@biotech-shopware-skills
```

If the client does not support branch marketplace URLs, use the direct skill installer below. A local plugin registry is not automatically available on another machine or remote IDE host.

Direct skill installation from inside Codex:

```text
$skill-installer install https://github.com/biotech-shopware/claude-shopware-skill/tree/ai-tooling-refactoring/plugins/shopware-knowledge/skills/shopware-development
```

Invoke `$shopware-development <task>`. Restart the client after a direct skill installation. IDE, CLI, and app discovery depend on the host and configuration where each runs; there is no cross-device automatic sync.

### Portable Skill / Claude App Chat

The self-contained folder is `plugins/shopware-knowledge/skills/shopware-development/`. Copy it to the personal or project skill location supported by your runtime, or export it with the host's validated `build-agent-skill` tool. Claude Code uses `~/.claude/skills/` or `.claude/skills/`; current Codex also discovers project `.agents/skills/`.

For Claude app/web custom Skills, upload the portable ZIP through the Skills UI if enabled for your account. That flow is separate from the Claude Code marketplace and does not prove repository tool access or Code-session behavior.

Official discovery/packaging references: [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [OpenAI skills](https://developers.openai.com/codex/skills), [OpenAI plugins](https://developers.openai.com/plugins).

## Use

```text
Review this Shopware 6.7 payment plugin. Trace ownership, server-side amounts,
webhooks, retries, and reconciliation. Separate proven defects from runtime gaps.

Implement the category association through its existing parent save flow.
Reuse the existing service seam; verify the relevant ACL and persistence path.

Audit this classic storefront theme for cache-safe Twig overrides,
keyboard/focus behavior, repeated-component IDs, and consent lifecycle.
```

Use the runtime's explicit invocation prefix above or a natural-language Shopware request. User and repository instructions govern scope and permissions. Keep local build restrictions, team branching policy, and intentionally dormant features in `AGENTS.md` or `CLAUDE.md`.

No MCP runtime, hook, external service, or additional plugin is required. When installed, `test-writing`, `contributor-writing`, `shopware-documentation`, and `shopware-env` own their specialized workflows; the skill retains standalone domain guidance.

## Contents

- [Skill and topic routing](plugins/shopware-knowledge/skills/shopware-development/SKILL.md)
- [Plugin documentation](plugins/shopware-knowledge/README.md) and [detailed 0.10.0 changes](plugins/shopware-knowledge/CHANGELOG.md)
- [Preservation ledger](docs/maintenance/preservation-ledger.md), [correction evidence](docs/maintenance/corrections.md), and [validation results](docs/maintenance/validation-results.md)
- [Installation checks](docs/verify-install.md) and [upstream handoff](docs/maintenance/upstream-handoff.md)
- [CodeRabbit review profile](integrations/coderabbit/shopware-review.md); copy to `.rules/shopware-review.md` in the reviewed repository
- [Future optional retrieval design](docs/maintenance/retrieval-design.md)
- [Historical changelog](CHANGELOG.md) and [MIT license](LICENSE)

## Troubleshooting and Maintenance

If the skill appears twice, remove or disable the older standalone copy or plugin; do not run two revisions under the same trigger. Use `claude --debug` or the client's plugin/skill listing to inspect discovery. A recognized package is not proof of correct behavior: see the executed checks and remaining gaps in the validation report.

Verify behavior-sensitive claims against installed source or a matching stable Shopware tag. Review supported patch releases, relevant PHPStan/framework changes, and reported failures monthly and before releases. Update the changelog and regression cases with each rule change. Tags and releases wait for review of this branch.
