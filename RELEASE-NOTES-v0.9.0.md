# Release Notes — v0.9.0-dev

## Summary

A correctness release, not a feature release. The skill's rules were reviewed the way code is reviewed — against Shopware core source and official docs rather than against memory. **33 defects were found and fixed**, most of them in v0.8.0-dev, the release that added the most content.

One new reference file. Everything else is a correction.

## Why this release exists

A feedback document comparing three reviewers on the same Shopware codebase closed with a meta-lesson: *the most expensive defect was in a rule, not in code.* A config instruction had said "put destructive work in `updateDestructive()`" — which reads as sound Shopware advice and is precisely backwards.

The obvious next question was whether this skill carried the same rule. It did, at `references/04-plugin-backend.md:142`. That prompted a full audit.

## What was wrong

Nine rules placed code or configuration where it would never execute:

| Rule | Consequence |
|---|---|
| `updateDestructive()` for destructive work | Plugin install/update never call it; required schema work never ran |
| `CategoryLevelLoaderCacheKeyEvent` in `Category\SalesChannel\` | Wrong namespace; subscriber registered cleanly, never fired |
| ES decorator defining `mapping()` | Contract is `getMapping()`; field never reached the index |
| `routing_overwrite` key with doubled backslashes | YAML does not unescape single-quoted scalars; never matched, override ignored |
| Rector package `friendsofshopware/shopware-rector` | Does not exist; and the named rules are not in the 6.7 set |
| `snippet:validate` | Not a command |
| `dal:list`, `framework:describe:*` in `allowed-tools` | Pre-approved commands that do not exist |

Three more would fail loudly at runtime rather than silently — arguably better, still wrong:

- The **cart collector example** combined `Criteria::addFields()` with `$product->getName()`. Partial reads return `PartialEntity`, which has no getters, so the model batching pattern for the cart hot path threw `Call to undefined method` on every recalculation.
- The **payment `pay()` examples** used `AsyncPaymentTransactionStruct`, deleted in 6.7.0.0, with a signature incompatible with `AbstractPaymentHandler`. The block was labelled "Preferred".
- The **`custom-fields.xml` example** was XSD-invalid — `name` is a required attribute, not a child element — and the file is validated at plugin install.

One was worse than a no-op. The documented way to run a *targeted* reindex —

```bash
curl -X POST /api/_action/indexing -d '{"only": ["category.indexer"]}'
```

— reads no request body at all. It calls `sendIndexingMessage([], …)`, and an empty list means **every registered indexer**. On a large catalog, following our own documentation was a production incident. The correct route is `POST /api/_action/index`, singular.

Two defects broke the skill itself rather than the advice:

- **`paths` suppressed auto-invocation.** It *limits* activation to file-matching contexts, so conceptual questions stopped triggering the skill — contradicting the trigger phrases `when_to_use` advertised. Removed.
- **Frontmatter exceeded the 1,536-character cap** at 1,631. The silently truncated tail was the trigger phrases for file 25, added in the same release that added file 25. Now 1,154 with headroom.

The rest were wrong facts: `CACHE_REWORK` is opt-in and experimental, not the 6.7 default; `shopware.cache.invalidation.delay` does not exist in 6.7; the legacy payment interfaces were *removed* in 6.7.0.0, not deprecated; PHPStan was pinned a full major behind what Shopware tests against; a security advisory was cited for a claim it does not support.

## What was added

**`references/26-plugin-lifecycle-and-activation.md`** — the gap the feedback identified. A change that runs only from a lifecycle hook needs a version bump to execute on already-installed shops, and fresh installs never surface the gap.

The mechanics are more subtle than the feedback described, so the file states them precisely: `updatePlugin()` has no version guard, the gate is in the callers, and the callers disagree — `plugin:update:all` skips ungated and inactive plugins, while `bin/console plugin:update <Name>` runs unconditionally.

Review-method additions, all folded into existing files rather than new ones:

- **Enumeration** — one correct instance of a pattern is not evidence about the others.
- **Sibling comparison** — when a file holds two constructs of the same shape, compare them before judging either.
- **Checked and Dismissed** — name what was swept clean and why, so a review that looked can be distinguished from one that did not.
- **Follow-the-code pass** — risk order decides what to read first, not what to look for.
- **Source of record** — establish which system owns an entity before reviewing code that writes it.

## What was deliberately not done

The feedback proposed two new reference files. This release adds one.

The second — a contract-review file — split cleanly: its Shopware-specific half (source-of-record per entity) went into `08`, and its generic half (read the ticket, compare requirement to code) was dropped. It fails Anthropic's stated criterion of *"only add context Claude doesn't already have"*, and a third review file alongside `08` and `22` would add routing ambiguity for no benefit, since unread reference files cost nothing.

## Root cause

`references/01-source-hierarchy.md` already defines a Core Source Verification Gate: verify a symbol exists before naming it, and state the gap when you cannot. v0.8.0-dev did not apply that gate to itself.

Three of the defects came from Slack-sourced project anecdotes encoded without checking against core — now the lowest-confidence input class in this repo.

The countermeasure is mechanical, in `docs/verify-install.md`: measure the frontmatter budget, assert no `paths` key, check that every named command exists, and spot-check citations against what they claim. Checks that fail loudly, rather than a resolution to be more careful.

## Upgrading

No action needed for content. If you installed v0.8.0-dev, reinstall to pick up the corrections — particularly if you followed the indexing or Rector guidance.

```bash
rm -rf ~/.claude/skills/shopware-development
cp -R shopware-development ~/.claude/skills/
```

Restart Claude Code afterwards; skills do not hot-reload.
