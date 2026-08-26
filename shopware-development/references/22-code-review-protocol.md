# Code Review Protocol

Index: setup, scope, 3-pass process, enumeration, sibling comparison, findings shape, checked-and-dismissed, prior-review handling, rules.

## Setup

- Single markdown report per review.
- Filename: `pluginname-YYYY-MM-DD-vX.Y.Z.md`.
- Header: plugin name, version from `composer.json`, repo URL, branch, last commit SHA, review date, model, skill used.
- SemVer the review file. Bump on each iteration.

## Scope

- Security, performance, best practices.
- Shopware, Symfony, PHP, Twig. Use the loaded skill as the entry point, then apply full model power beyond it.
- Static analysis only. No runtime execution.
- Research external API docs before any finding or fix. Never invent capabilities.
- Every finding must have proof: file path, line number, concrete scenario.

## 3 Passes

- Each pass is a complete end-to-end review of the entire codebase.
- Pass 2 receives Pass 1 as context. Confirm or reject each finding explicitly. Find new gaps.
- Pass 3 receives Pass 1 + 2. Final challenge. Remove anything without proof.
- Combine into one FINAL report. Clearly mark what was validated across passes and what is new.

## Enumeration

Finding a correct implementation of a pattern in a file is **not** evidence that other instances in that file are correct. Before concluding on any security-relevant pattern, enumerate every instance of it in the changed file and judge each separately.

The failure this prevents: checking one of two call sites, finding it parameterised, and reporting the class clean while the second one interpolates customer-controlled input.

## Sibling Comparison

When a file or module contains two or more constructs of the same shape, compare them against each other before judging any one. Divergence in version scoping, language resolution, visibility filtering, parameter binding, transaction boundaries, or error handling is a defect in one of them.

Two near-identical methods that differ in one clause are a stronger signal than either method read alone.

## Findings Shape

Severity is assigned by `08-analysis-and-reviews.md` on impact. This file governs the **output format** for each severity.

- **P0** carries a code diff with the smallest safe fix. No business logic changes. No frontend changes. No flow changes. Pragmatic and surgical.
- **P1 and below** explain the issue in depth and explain the solution in depth. No code. No diff.
- Every finding: what is wrong, why, where (file:line), how to verify, what breaks if done wrong.

## Checked and Dismissed

Close every report with a short section naming the categories swept and found clean, plus the evidence that justified dismissal.

```md
## Checked and Dismissed

- SQL injection — clean. 321 call sites, all parameterised (enumerated).
- Ownership checks on customer-facing mutations — clean. All 12 routes filter by context customer.
- Cart-time external API calls — none present.
```

A review listing only hits cannot be distinguished from a review that did not look. Writing the dismissal forces the enumeration that catches the outlier.

## When A Prior Review Exists

- Validate each prior finding. Confirmed or rejected with reason.
- Find gaps the prior review missed.
- Clearly show what is new vs what is validated from the prior review.
- Combine into a single final report with updated SemVer.

## Rules

- Do not invent things. If an external API does not support something, say so and suggest the best available alternative.
- Read IMPORTANT comments in code. Respect documented limitations.
- Small changes only. Do not change business logic. Do not change frontend. Do not break existing flow.
- Double-check each finding before including it.
- No finding without proof.
