# Code Review Protocol

Index: setup, scope, 3-pass process, findings shape, prior-review handling, rules.

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

## Findings Shape

- **P0** carries a code diff with the smallest safe fix. No business logic changes. No frontend changes. No flow changes. Pragmatic and surgical.
- **P1 and below** explain the issue in depth and explain the solution in depth. No code. No diff.
- Every finding: what is wrong, why, where (file:line), how to verify, what breaks if done wrong.

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
