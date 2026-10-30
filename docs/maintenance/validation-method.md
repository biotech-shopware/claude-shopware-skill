# Validation Method

## Release Gates

Structural success is not behavioral success. Run the deterministic gates, then
have a human or independent semantic reviewer score blind CLI responses. No
keyword, exact-prose, reference-name or heading matcher grades model behavior.

From the repository root, using Python 3.12 or newer:

```sh
python -m pip install -r eval/requirements.txt
python -m unittest discover -s plugin-tests/shopware-knowledge -p 'test_*.py' -v
python scripts/validate_skill_pack.py
python eval/run.py check
```

The prepared validation virtual environment can run each command by substituting
its `bin/python`. Dependencies are mandatory: PyYAML 6.0.3, `skills-ref` at commit
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`, and upstream `agent-skills-export`
at commit `a276558d12d0e09696fb9d1a7b4cd1925c44baf6`. The requirements file pins
these direct dependencies; it is not a complete transitive/hash lock. CI installs
them and fails on missing imports or missing CLI executables, never silently skips.

## Structural Contract

- Native plugin: `plugins/shopware-knowledge/`, Claude and Codex manifests named
  `shopware-knowledge`, version `0.10.0`. Optional skill declarations must resolve
  to the bundled skill directory. Both repository marketplaces must resolve the
  plugin entry to that root. Marketplace names are independent of plugin names;
  this repository uses `biotech-shopware-skills`.
- Native skill: `skills/shopware-development/SKILL.md`, YAML name
  `shopware-development`, top-level version `0.10.0`, nonblank description at most
  1024 characters, and `.agent-skills` beside the entrypoint. Neither
  `agents/openai.yaml` nor MCP is required. This knowledge-only pack must not
  enable executable hooks, commands, agents or MCP servers via its manifests.
- References: local Markdown destinations and backticked `references/*.md` paths
  must resolve within the skill, with valid heading fragments. Every reference
  Markdown file must be reachable, possibly transitively, from `SKILL.md`.
  Symlinks, escapes and case-only mismatches fail. External URLs are not fetched.
- Runtime Markdown: lint host/private paths and private Slack provenance, plus
  explicit runtime-specific tool dependencies. Frontmatter preapproval declarations
  may contain only Read/Glob/Grep, not editing or shell grants. These conservative
  lints do not prove every instruction is runtime-neutral or permission-safe;
  semantic review remains necessary. Code examples are excluded from instruction
  lints but not from private-content hygiene.
- Index: `knowledge-index.json` requires integer `schema_version: 1`, skill
  `shopware-development`, and nonempty `topics`. Each topic has a unique nonblank
  `id`, a real bundled reference `path`, nonempty supported `modes`, explicit
  `shopware` applicability containing 6.6 or 6.7, a `feature_flags` string array
  (empty allowed), and nonempty `sources` string locators with no blank entries.
  Every reference file is covered once. Paths may be skill-relative
  (`references/...`) or plugin-relative (`skills/shopware-development/references/...`).
  Shopware applicability may be a string or array of nonblank version constraints.
  Supported modes: plan/planning, implement/implementation, refactor, debug, review,
  audit, research, migrate, report, operate and test. Source-locator accuracy,
  feature-flag applicability and version-constraint meaning require source review.
- Export: invoke the installed upstream `build-agent-skill`, then `skills-ref
  validate` on its portable output. Also invoke the required `skills_ref` API.
  Portable frontmatter has no top-level version and has `metadata.version: 0.10.0`.
  Instruction body and all reference/asset bytes must survive, except the export
  marker. ZIP entries must exactly match the validated directory, without duplicate
  entries. Build output is temporary; nothing writes back to the source pack.

`--structural-only` is a diagnostic option, never a substitute release gate.
The custom manifest checks validate this pack's supported shape, not every field
in the complete evolving vendor schemas. Primary format references:
[OpenAI packaging](https://developers.openai.com/plugins/build/plugins),
[Claude manifest reference](https://code.claude.com/docs/en/plugins-reference), and
[Agent Skills specification](https://agentskills.io/specification).

## Blind CLI Evaluation

`eval/cases.json` contains 14 fixed small fixtures. Each includes an exact Shopware
core Composer target (`6.7.15.1`, or `6.6.10.30` for compatibility), source files,
a neutral review prompt and a separate expected behavioral rubric. The fixtures
are review slices, not full installable applications with Composer dependencies.
Payment authority, saved-method ownership, renewal idempotency, cart I/O, cache
variation, queue concurrency, the indexer contract, translated CMS configuration,
parent save flow, plugin update execution, accessibility and 6.6 compatibility are
covered. Two additional clean controls cover a pure formatter and a guarded,
batched cart collector. The compatibility case is also a negative control against
forcing a 6.7-only migration on 6.6.

List/check/materialize never invokes a model. `run` also remains a dry-run unless
`--execute` is supplied. No environment variable, auth file or user setting is
changed or copied. Omit `--model` to use the unchanged CLI default; for controlled
A/B, pass the same explicit model to both arms. Each case gets a fresh random
temporary project. The CLI receives only source, a copied skill and the neutral
prompt, never `expected` or an answer key. Rubrics remain in this maintainer file
set outside the project. `run.json` records invocation, input hashes, CLI version
and help, return code and source-integrity check, but no semantic score.

```sh
python eval/run.py check
python eval/run.py materialize --case c01 --runtime codex --skill plugins/shopware-knowledge/skills/shopware-development --arm B
python eval/run.py run --all --runtime codex --skill plugins/shopware-knowledge/skills/shopware-development --arm B --model gpt-6.1-sol --execute
python eval/run.py run --all --runtime codex --skill /path/to/baseline/shopware-development --arm A --model gpt-6.1-sol --execute
python eval/run.py run --case c01 --runtime claude --skill plugins/shopware-knowledge/skills/shopware-development --arm B --execute
```

Replace the baseline placeholder with an independently preserved skill snapshot.
Main may run the two whole-arm commands concurrently; each runner executes cases
serially in distinct temporary directories. There is no built-in parallel job
pool. Start with a few cases to establish authentication, cost and latency before
`--all`. Codex has a timeout but no runner-enforced API spend cap. Claude has a
per-case `--max-budget-usd` cap (default 2); increase deliberately if insufficient.

Codex uses temporary project `.agents/skills`, `--sandbox read-only`, approval
`never`, `--ephemeral`, `--ignore-user-config`, `--ignore-rules` and per-invocation
`--config skills.config=[...]` disables for discovered global copies of this skill.
Auth remains in the ordinary configured location. Extra global/plugin copies can
be disabled with repeatable `--disable-skill /path/to/SKILL.md`. No HOME or
CODEX_HOME override is used. These flags were inspected in local
`codex-cli 0.163.0-alpha.10.2` help. See
[OpenAI skill discovery and disable configuration](https://learn.chatgpt.com/docs/build-skills).

Claude uses a temporary `--plugin-dir` wrapper, `--setting-sources ''`,
`--restricted`, read-only Read/Glob/Grep plus Skill tools, `dontAsk`, and an empty
strict MCP configuration. The wrapper exposes only the selected skill, not any
hooks/MCP from a baseline plugin. Local help inspected: Claude Code `2.1.296`.
The runner captures current help and fails if its required flags disappear.

Default `--invocation explicit` prefixes the native skill invocation. Use
`--invocation auto` without that prefix to study discovery separately. Omit
`--skill` for a no-skill control. Do not conflate explicit-use decision quality
with trigger recall. Existing prose trigger prompts remain useful exploratory
inputs but are not statistical evidence or executable pass/fail assertions.

## Scoring And Gaps

Give a blinded reviewer the response and trace first; provide rubric/source files
only to the reviewer, not the agent under test. Record, per case, whether the
demonstrated issue was found, evidence/causal reasoning was correct, proposed fix
closed the failure path, validation was relevant, and severity was justified.
Record missed issues, unsupported claims and invented findings separately.
For clean controls, success includes explicitly finding no demonstrated defect
and respecting the stated boundary. Expected filenames are routing hints for the
reviewer, not required literal citations. Grade equivalent correct explanations
equally; do not reward reproducing the rubric or headings.

Record real trace evidence of skill loading/reference reads, A/B model and skill
hashes, case order, timing, configuration differences and failures. Randomize arm
order and repeat contentious cases before attributing a difference to the skill.
CLI exit zero proves neither skill invocation nor answer quality. If a model reads
the rubric or repository outside its fixture, discard the contaminated run.
Codex read-only sandboxing is not a universal read-confidentiality barrier;
managed settings and bundled/global skills can still affect behavior. Use trace
review and an independently isolated host if strict blindness is necessary.

Executed comparisons, fixture corrections, transient runtime failures and
remaining authentication/integration gates are recorded in
[validation results](validation-results.md). Keep that run record separate from
this reusable method; do not infer a completed evaluation from runner output
or fixture existence alone.

Local fixture QA: all 13 PHP fixture files passed `php -l` with PHP 8.5.12.
The clean c14 collector also loaded successfully against the actual 6.7.15.1
`CartDataCollectorInterface`, including signature compatibility. Both cart
fixtures import `Cart\\LineItem\\CartDataCollection`. These narrow checks are
not a dependency installation or a Shopware container/integration test.

The PHP/JS/Twig fixtures are not a substitute for target-version integration tests,
actual provider verification, concurrent database tests or browser/assistive-
technology checks. In particular clean controls must be syntax/contract checked
before interpreting a false positive as model regression. Synthetic unit tests
exercise the validator without depending on concurrent edits to the real pack.
