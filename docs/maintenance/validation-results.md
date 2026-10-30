# Validation Results

## Decision

Prepared `shopware-knowledge` **0.10.0** for review, not publication. Native/portable packaging, preservation accounting, source-anchor checks and observed Codex CLI behavior pass. Claude installation is verified; live Claude behavioral comparison remains unverified because the CLI is not authenticated. That boundary was accepted for this handoff. No tag, release, global skill replacement, or upstream merge is performed.

| Gate | Executed Result |
| --- | --- |
| Preservation | All 2,457 baseline units accounted for: 2,004 retained, 28 moved, 417 corrected, 8 self-check/provenance or unsupported-assertion units retired; no unexplained unit loss |
| Entrypoint size | 669 words versus 1,872 after contribution integration, approximately 64% smaller; this measures words, not model tokens |
| Knowledge index | 29 deterministic topic records; all 28 numbered owners plus the bounded Messenger implementation reference |
| Package tests | 34 focused tests pass, including invalid/escaping references, metadata, manifests, applicability, export failure cases and bundled-license presence |
| Portable export | Pinned host exporter, required `skills-ref`, frontmatter normalization, reference-byte preservation and ZIP parity pass |
| Source anchors | 89 pinned core URL paths resolve in actual v6.7.15.1 / v6.6.10.30 Git objects; path existence alone is not proof of every associated claim |
| Claude manifests | Native plugin and repository marketplace pass the installed Claude validator |
| Claude installation | One-step local-marketplace installation into a separate documented configuration directory succeeds; listed/enabled at 0.10.0; installed runtime files match the candidate byte-for-byte |
| Codex discovery | Native marketplace catalog lists the available plugin at 0.10.0; temporary project-skill installation loads actual relative references in live CLI traces |
| GitHub branch installation | Official Codex installer and Claude one-command marketplace install both fetch `ai-tooling-refactoring` successfully; downloaded runtime files match the source byte-for-byte |
| Downloaded-skill smoke | Codex CLI loads the GitHub-installed skill and its relative references, keeps the formatter control clean, and leaves the fixture unchanged |
| Codex semantic cases | 14 paired cases reviewed by meaning against fixed source/rubrics; expected defects preserved, three clean/compatibility controls stay clean, no new unsupported P0/P1 observed |
| Codex repetition | Payment authority, saved-method ownership, renewal idempotency and cache isolation repeated on unchanged fixtures in both arms; one model-capacity failure is excluded and retried with the same model |
| Natural-language discovery | Two unprefixed CLI prompts load the project skill and appropriate references; pricing defect detected and pure-formatter control remains clean |
| Host integration | Versions, generated issue registrations, manifests, package/export checks and all 28 focused Codex registry BATS tests pass in the pinned host checkout |
| Full host BATS suite | 1,559 passed, 0 failed, 0 skipped in disposable Ubuntu 26.04 ARM64, Git 2.53.0, non-root user; eight file workers with within-file order preserved |
| Formatting/privacy | Diff whitespace checks pass; runtime Markdown has no personal paths, private-conversation provenance or platform-specific invocation instructions |

The [GitHub validation workflow](https://github.com/biotech-shopware/claude-shopware-skill/actions/runs/40743615151) passed for implementation commit `5d2c8318d277cb54359c02d37bf054e75acd3f38`. Follow-up documentation commits do not change the tested runtime corpus; their CI status must still be checked separately.

## Behavioral Evidence

The model was `gpt-6.1-sol`, using Codex CLI `0.163.0-alpha.10.2`. Each arm ran the same source fixture and neutral prompt, with the selected skill materialized inside a temporary project. The evaluator rubric remained outside the project. Traces show actual skill/domain reads, unchanged fixture hashes and no observed evaluator/rubric access, external service use, or application execution. Per-case reviews are in [backend grading](eval-backend-review.json) and [UI/compatibility grading](eval-ui-review.json).

Cases cover payment authority, ownership, renewal retries, cart I/O, shared-cache isolation, concurrent queues, the full indexer contract, translated CMS configuration, parent save flow, version-gated deployment, accessibility, explicit 6.6 compatibility, a pure formatter, and a guarded batched collector. The candidate preserved expected findings. In the cart-I/O case, the baseline additionally mandated manual cache invalidation and overstated an unspecified consumer requirement; the candidate correctly made cross-request caching provider-dependent.

Two initial fixtures required correction: the indexer case lacked its version-pinned parent contract, and the deployment case confused targeted update with bulk version selection. The final deployment fixture also corrects Composer namespace escaping. Only corrected paired reruns are graded for those cases. The first preliminary smoke run inherited unrelated client configuration; the controlled runs use the inspected isolation flags. One repeated ownership run failed with model capacity, not a completed answer; its replacement is reviewed separately.

This is independent semantic review, not an exact-string grader. Arm order was not randomized or counterbalanced. These small review slices, one primary pair and selected repeats do not establish statistical superiority, universal finding stability, real Shopware integration correctness, or complete confidentiality from all unobservable runtime context. Later nonsemantic source-order/formatting polish is covered by structural/preservation checks; grades apply to their recorded materialized snapshots.

## Source and Example Checks

Targeted investigation used Shopware v6.7.15.1 and v6.6.10.30, installed CLI help and public primary sources. Corrected mechanics and retained invariants are documented in [correction evidence](corrections.md). Changed backend PHP/JSON examples and frontend consent/DOM lifecycle harnesses received syntax/contract checks. PHP lint ran on 8.5, not a separate 8.2 runtime. Fixture PHP syntax and the clean collector signature were checked; fixtures are not full Composer-installed applications.

The [upstream handoff](upstream-handoff.md) records host checks and reproducible preparation. The host citation checker resolves the plugin's citations but still reports inherited bare-path style warnings in the runtime corpus; legitimate instruction operands are not rewritten into fictitious links. This is a documented style limitation, not an unresolved-reference or behavior pass.

## Final Submission Recheck

The October 30 submission pass confirmed that upstream `main` still matches the pinned host baseline. Source preservation accounting, the 34 focused package tests, portable export, 29 topic records, 14 fixture schemas, 89 pinned core locators, version/issue checks, Claude marketplace validation, all 28 Codex registry BATS tests, and full repository ShellCheck were rerun. The instruction corpus is unchanged from the tested candidate. A final packaging review added the original MIT notice to the native/portable skill, two missing-notice tests, Python-bytecode ignore patterns, and upstream-facing documentation including the [detailed PR draft](upstream-pull-request.md).

A full local host BATS run was attempted but not completed. Its unrelated ChunkHound tests require `ugrep`, which is absent in the local environment; the run was stopped after that prerequisite failure. The focused changed registry suite passes. The upstream Linux CI installs `ugrep` and remains the authority for the full host suite. Do not present the interrupted local run as a full-suite pass.

The published upstream fork was then installed again through the official Codex installer and Claude marketplace CLI in separate temporary destinations. All 32 installed files, including the MIT notice, match the contributed skill byte-for-byte in both clients. A read-only Codex clean-control run from that actual GitHub installation read the entrypoint and relevant review/source references, reported no invented formatter defect, exited successfully and preserved all fixture hashes. Claude live behavior remains unverified. Upstream PR #203 is open; its workflow runs require maintainer approval.

## Whole-Host Linux Validation

All 1,559 host BATS cases passed with zero failures and zero skips against contribution commit `bc8d14150f27b010459dd07d35d32ec86b11f7b0`. The environment was the official Ubuntu 26.04 ARM64 container image at digest `sha256:6a06111c3b0a8600feadb270aec771dc239bf407b25625f93f44ab00e11f4d3c`, Git 2.53.0, the host-pinned BATS dependencies, and a non-root test user. The source checkout was mounted read-only and copied into the disposable container; no project containers or active client configurations were changed.

The completed command was:

```bash
.bats/bats-core/bin/bats --jobs 8 --no-parallelize-within-files --timing -r plugin-tests/
```

GNU Parallel scheduled independent files; execution order within each file was preserved. This is a completed local integration run, not the upstream GitHub Actions result. The longer serial probe was stopped after the full file-parallel run succeeded and is not counted as another complete run.

An earlier Ubuntu 24.04 probe with Git 2.43 failed relative-worktree membership tests. The same failure was reproduced on untouched upstream `a276558` in that environment. Git 2.48 added the relative back-pointer support those fixtures exercise; the formerly failing case passes with Git 2.53. No unrelated worktree runtime or tests were changed to force a pass. The older probe was stopped and excluded from successful-run totals. Upstream workflows remain gated on maintainer approval for the external contribution.

## Remaining Gates

- Run the paired behavioral cases in authenticated Claude Code before claiming dual-runtime behavioral equivalence. Claude Code 2.1.296 package validation/installation is not an API/model execution result.
- Test actual browser/assistive-technology behavior, real Shopware container integration, provider enforcement, concurrent database recovery, reverse-proxy rollout, and representative search consistency where applicable.
- Exercise interactive IDE/native-app UI sessions and remote IDE hosts separately; shared package shape does not prove every client/session has discovered it.
- Complete maintainer review, decide any inherited link-style cleanup, and publish only after the preparation branch is accepted. Optional MCP retrieval remains a separate design, not a shipped dependency.
