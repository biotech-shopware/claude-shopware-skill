# Verify Install

Checklist after installing the skill to `~/.claude/skills/shopware-development/` (personal) or `.claude/skills/shopware-development/` (project).

## Step 0 — Maintainer regression guards

Run these from the repo root before releasing. Each one corresponds to a defect class that shipped in v0.8.0-dev; they fail loudly rather than relying on care.

```bash
cd shopware-development

# Frontmatter budget — description + when_to_use must stay under 1,536 chars.
# v0.8.0-dev shipped at 1,631, silently truncating its own trigger phrases.
awk '/^description: >-/{f=1;next} /^when_to_use: >-/{f=2;next} /^[a-z-]+:/{f=0}
     f==1{d=d" "$0} f==2{w=w" "$0}
     END{gsub(/  +/," ",d); gsub(/  +/," ",w); c=length(d)+length(w);
         print (c<1536 ? "PASS ("c")" : "FAIL ("c", over by "c-1536")")}' SKILL.md

# No `paths` key — it restricts auto-invocation to file-matching contexts.
grep -c '^paths:' SKILL.md   # expect 0

# Reference count matches the Reference Map.
ls references/ | wc -l
grep -c '^- \[references/' SKILL.md

# Known-bad strings must not reappear.
grep -rn "Separate destructive operations into\|dal:list\|framework:describe\|GHSA-6w82-v552-wjw2" references/ SKILL.md
```

Two checks that need a human: every `bin/console` and `composer` command named anywhere in the skill must exist on the target version, and every release-note / advisory citation must actually support the claim attached to it. Both classes shipped wrong in v0.8.0-dev.

## Step 1 — File presence

```bash
ls ~/.claude/skills/shopware-development/SKILL.md
ls ~/.claude/skills/shopware-development/references/ | wc -l
# Expected: 26 files (01 through 26)

ls ~/.claude/skills/shopware-development/agents/openai.yaml
# Expected: exists (Codex compatibility)
```

## Step 2 — Skill listing

In Claude Code:

```
/skills
```

Expected: `shopware-development` appears in the list with the description "Review, plan, implement, refactor, or debug Shopware 6 changes…".

If the skill is missing:

- restart Claude Code so the top-level skills directory is discovered
- run `claude --debug` and check skill-loading errors

## Step 3 — Auto-invocation

In a fresh Claude Code session, type:

```
review my Shopware plugin for P0/P1 issues
```

Expected: Claude activates `shopware-development` implicitly. In the response, Claude reads `references/08-analysis-and-reviews.md` and `references/22-code-review-protocol.md` before generating output.

If auto-invocation fails, run more prompts from [`eval/should-trigger.md`](../eval/should-trigger.md). Target hit rate ≥ 4/5.

## Step 4 — Reference open behavior

In a Shopware 6.7 project directory, type:

```
/shopware-development review the payment handler in this repo
```

Expected: Claude uses the Read tool on:

- `references/07-payments.md`
- `references/08-analysis-and-reviews.md`
- `references/22-code-review-protocol.md`

In the final answer, Claude references `AbstractPaymentHandler`, `pay/finalize/validate/recurring/refund`, the `shopware.payment.method` DI tag, and follows the 3-pass review protocol.

## Step 5 — Reference-specific dry runs

Test these prompts individually and confirm Claude reads the expected reference file:

| Prompt | Expected file opened |
| --- | --- |
| "Why is Shopware delaying cache invalidation for 5 minutes?" | `references/23-cache-and-http-cache.md` |
| "How should I cache TaxJar responses in cart calculation?" | `references/24-external-api-caching-in-cart.md` |
| "Patch a Shopware core class with composer-patches" | `references/25-patching-and-dependency-tooling.md` |
| "Convert admin plugin from sw-button to mt-button" | `references/06-administration-and-apps.md` |
| "Migrate 6.6 snippets to country-agnostic base files" | `references/21-internationalization-and-snippets.md` |

If Claude answers without opening the expected file, the routing matrix or Reference Map may need clearer signals.
