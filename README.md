# Shopware AI Skill for Claude Code and Codex

Universal Shopware 6 skill for AI-assisted planning, implementation, refactoring, review, and release work.

The installable skill folder is platform-neutral. Claude Code and Codex use the same `shopware-development/` content; only installation and invocation differ by runtime.

## Scope

- Shopware 6.7-first plugin development with explicit 6.6 compatibility handling
- backend, DAL, migrations, Store API, Admin API, HTTP cache, Varnish, queues, and indexers
- storefront Twig, JS, SCSS, themes, accessibility, snippets, and i18n
- administration modules, apps, app scripts, ACL, Vue 3, Pinia, Vite, and cloud constraints
- payments, webhooks, refunds, saved methods, recurring payments, and headless contracts
- cart, checkout, delivery, promotion, testing, search, operations, and multi-plugin reviews
- pragmatic coding defaults: smallest coherent safe change, DRY/KISS, and no defensive ceremony without a concrete failure mode

## Repository Layout

```text
claude-shopware-skill/
├── CHANGELOG.md
├── integrations/
│   └── coderabbit/
│       ├── coverage.md
│       └── shopware-review.md
├── LICENSE
├── README.md
├── .claude-plugin/           # dev branch only: Claude Code plugin manifest
│   └── plugin.json
├── docs/                     # dev branch only
│   └── verify-install.md
├── eval/                     # dev branch only
│   ├── should-trigger.md
│   └── should-not-trigger.md
└── shopware-development/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── 01-source-hierarchy.md
        ├── 02-version-targeting.md
        ├── 03-implementation-workflow.md
        ├── 04-plugin-backend.md
        ├── 05-storefront-and-themes.md
        ├── 06-administration-and-apps.md
        ├── 07-payments.md
        ├── 08-analysis-and-reviews.md
        ├── 09-symfony-and-php.md
        ├── 10-official-docs-map.md
        ├── 11-quality-and-operations.md
        ├── 12-extension-patterns.md
        ├── 13-context-and-commerce.md
        ├── 14-cli-and-dev-tooling.md
        ├── 15-subscriptions-and-recurring-payments.md
        ├── 16-headless-and-composable-frontends.md
        ├── 17-accessibility-and-template-best-practices.md
        ├── 18-cart-and-checkout-pipeline.md
        ├── 19-testing-patterns.md
        ├── 20-search-and-indexing.md
        ├── 21-internationalization-and-snippets.md
        ├── 22-code-review-protocol.md          # v0.8.0-dev
        ├── 23-cache-and-http-cache.md          # v0.8.0-dev
        ├── 24-external-api-caching-in-cart.md  # v0.8.0-dev
        ├── 25-patching-and-dependency-tooling.md # v0.8.0-dev
        ├── 26-plugin-lifecycle-and-activation.md # v0.9.0-dev
        ├── 27-cms-elements-and-blocks.md       # unreleased (cms branch)
        └── 28-local-dev-environment.md         # unreleased (local-dev-environment branch)
```

## Branches

- **`main`** — stable, currently `v0.7.3`. Use this for production installs.
- **`dev`** — preview of the next release (currently `v0.9.0-dev`). Adds five reference files (22-26), expanded frontmatter (`when_to_use`, `argument-hint`, expanded `allowed-tools`), and a Claude Code plugin manifest.

  **v0.9.0-dev is primarily a correctness release**: 33 defects in the skill's own rules were found and fixed by auditing them against Shopware core source — including nine that placed code or config where it would never execute, and one that inverted into a full production reindex. If you installed `v0.8.0-dev`, reinstall from this branch. See [CHANGELOG.md](CHANGELOG.md) and [RELEASE-NOTES-v0.9.0.md](RELEASE-NOTES-v0.9.0.md).

## Install And Use

### Claude Code CLI Or Desktop App

Clone the repo, then install the skill folder.

```bash
git clone https://github.com/biotech-shopware/claude-shopware-skill.git
cd claude-shopware-skill
```

Use `main` for the latest stable release, or pin a release:

```bash
git checkout v0.7.3
```

To preview the next version:

```bash
git checkout dev
```

Personal install:

```bash
mkdir -p ~/.claude/skills
cp -R shopware-development ~/.claude/skills/
```

Project install:

```bash
mkdir -p .claude/skills
cp -R shopware-development .claude/skills/
```

Invoke explicitly:

```text
/shopware-development review this Shopware plugin for P0/P1 security, performance, DAL, and compatibility issues
```

Claude Code discovers personal skills from `~/.claude/skills/` and project skills from `.claude/skills/`. Restart Claude Code if the top-level skills directory was created after the session started. If the skill does not appear, run `claude --debug` and check skill-loading errors.

Official reference: [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills)

### Claude Native Mac App Or Claude Web

Claude app skills are managed in the Claude UI, not by reading `~/.claude/skills`.

Package the installable skill folder as a ZIP whose root contains `SKILL.md`, `references/`, and optional support files, then upload it in Claude's Skills UI if your plan and workspace settings enable custom skills.

```bash
cd shopware-development
zip -r ../shopware-development-skill.zip SKILL.md references agents
```

Official reference: [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)

### Codex IDE, Codex CLI, Or Native Codex Mac App

Install from GitHub repo `biotech-shopware/claude-shopware-skill` with skill path `shopware-development`.

Preferred install through the Codex skill installer from inside Codex:

```text
$skill-installer install https://github.com/biotech-shopware/claude-shopware-skill/tree/main/shopware-development
```

Pinned install:

```text
$skill-installer install https://github.com/biotech-shopware/claude-shopware-skill/tree/v0.7.3/shopware-development
```

Script fallback:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo biotech-shopware/claude-shopware-skill \
  --path shopware-development
```

Pinned script fallback:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo biotech-shopware/claude-shopware-skill \
  --path shopware-development \
  --ref v0.7.3
```

Direct filesystem install:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R shopware-development "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex after installation. The Codex CLI, IDE extension, and native Mac app use the same local skill shape when they run with the same `CODEX_HOME`.

Invoke explicitly when needed:

```text
$shopware-development implement this Shopware 6.7 change with the smallest coherent safe change and call out version-specific behavior
```

The `shopware-development/agents/openai.yaml` file provides Codex UI metadata. The runtime skill content remains the same.

OpenAI reference: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) notes that OpenAI skills follow the Agent Skills standard and are supported in Codex, but skills do not sync automatically across products.

### Dry-Run Install Check

Use a temp directory to verify the package shape without changing your active install:

```bash
tmp="$(mktemp -d)"
mkdir -p "$tmp/codex/skills" "$tmp/claude/skills"
cp -R shopware-development "$tmp/codex/skills/"
cp -R shopware-development "$tmp/claude/skills/"
test -f "$tmp/codex/skills/shopware-development/SKILL.md"
test -f "$tmp/codex/skills/shopware-development/agents/openai.yaml"
test -f "$tmp/claude/skills/shopware-development/SKILL.md"
test -f "$tmp/claude/skills/shopware-development/references/01-source-hierarchy.md"
```

## CodeRabbit Review Guidelines

`integrations/coderabbit/shopware-review.md` is a compressed, review-only profile derived from the skill. It excludes agent routing, implementation workflow, and PR-writing instructions so CodeRabbit receives only criteria that help it evaluate changed Shopware code.

Install it in a Shopware repository as a root code-guideline file:

```bash
mkdir -p .rules
cp integrations/coderabbit/shopware-review.md .rules/shopware-review.md
```

CodeRabbit detects `.rules/*` automatically. A `.coderabbit.yaml` entry is needed only when the project stores guidelines under another path. The source-to-profile maintenance matrix is in `integrations/coderabbit/coverage.md`.

Official references: [CodeRabbit code guidelines](https://docs.coderabbit.ai/knowledge-base/code-guidelines) and [path instructions](https://docs.coderabbit.ai/configuration/path-instructions).

## Prompt Patterns

```text
/shopware-development review this payment flow with focus on validate/finalize, webhook authenticity, idempotency, and ownership.
```

```text
$shopware-development analyze this cart or checkout change with focus on collectors, processors, pricing, delivery, cache safety, and hot-path boundaries.
```

```text
/shopware-development review this storefront for WCAG, keyboard, focus, modal, repeated-component, and template override issues.
```

```text
$shopware-development harden this Shopware 6.7 plugin so it stays Varnish-safe, uses Messenger/RabbitMQ correctly, and keeps indexers bounded.
```

```text
/shopware-development compare 2-3 valid admin implementation directions, explain persistence and UX tradeoffs, and wait before choosing.
```

```text
$shopware-development do a full end-to-end review. Use the skill as Shopware guardrails only, not as a cap on investigation depth.
```

## Source Policy

- Detect project version from `composer.json` first.
- Use targeted package checks, vendor metadata, or focused `composer.lock` search only when exact installed versions matter.
- Treat Shopware docs as starting evidence; verify behavior-sensitive guidance and named core/admin/storefront symbols against the relevant stable core release source or installed vendor code.
- If no project version is pinned, resolve the latest stable release from the Shopware changelog or GitHub releases and use that tag instead of `trunk`, beta notes, ADR memory, or old docs.
- For Symfony behavior, check component docs, framework or bundle integration docs, and reference or config docs.
- Keep local workflow preferences in repo overlays such as `AGENTS.md` or `CLAUDE.md`.

## Release Model

- Release history lives in [CHANGELOG.md](CHANGELOG.md).
- The installable skill root is `shopware-development/`.
- The skill trigger is `shopware-development`.
- Existing Claude and Codex-specific repos should not diverge from this universal skill content after `v0.7.0`.
