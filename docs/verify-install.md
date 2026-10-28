# Installation and Validation

## Package Gates

Install the pinned validation requirements into a virtual environment, then run from the repository root:

```bash
python3 scripts/build_knowledge_index.py --check
python3 scripts/validate_skill_pack.py
python3 -m unittest discover -s plugin-tests/shopware-knowledge -p 'test_*.py'
python3 scripts/preservation.py
python3 eval/run.py check
git diff --check
claude plugin validate .
claude plugin validate plugins/shopware-knowledge
```

The package validator requires the host exporter and `skills-ref`; missing dependencies fail. It checks native metadata, relative-reference reachability, marketplace roots, applicability metadata, portable frontmatter, reference-byte preservation and ZIP parity. It does not prove model behavior or all external documentation links.

## Session-Only Discovery

For Claude Code, use `claude --plugin-dir ./plugins/shopware-knowledge`, invoke `/shopware-knowledge:shopware-development`, and inspect the trace for the entrypoint and domain reference reads. Authentication is required for a live response, not for `plugin validate`.

For Codex, copy the selected skill into a temporary project's `.agents/skills/shopware-development/`, disable duplicate global copies for that invocation, then invoke `$shopware-development`. The evaluation runner implements that path without changing `HOME`, credentials, or user configuration. Current CLI support must be checked before using isolation flags.

Run explicit invocation separately from natural-language discovery. A listed skill or zero CLI exit status alone is not a behavior pass. IDE and desktop clients on the same host share the package shape but still need their own discovery/session restart; remote IDE hosts require their own installation.

## Regression Cases

Use `eval/run.py list` and the [method](maintenance/validation-method.md). Each case materializes source files in its own directory; expected rubrics stay outside the project. Compare the same model/version and unchanged fixtures against the preserved baseline and candidate. Inspect actual source reads, findings, minimal fixes, clean controls and unexecuted verification claims. Repeat high-risk cases; do not infer stability from one run.

## Portable Upload

Use the host `build-agent-skill` exporter. Its ZIP contains the skill directory with `SKILL.md` and bundled references; inspect the archive and run `skills-ref validate` on the exported folder. Upload through the custom Skills UI only where supported. Native-app chat upload is distinct from Claude Code installation and is not a repository execution test.

Executed results and outstanding gates are recorded in [validation results](maintenance/validation-results.md). Do not mark blocked Claude authentication, missing integration dependencies, or unrun browser/provider checks as passed.
