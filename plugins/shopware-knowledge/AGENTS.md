# Shopware Knowledge Maintenance

## Ownership

- `skills/shopware-development/`: runtime-neutral, self-contained instructions and examples. Keep platform invocation and installation outside it.
- `knowledge-index.json`: stable topic IDs, applicability, feature flags, and evidence. Regenerate with `python3 scripts/build_knowledge_index.py` from the repository root.
- `docs/maintenance/`: preservation decisions, correction rationale, validation results, and future retrieval design; not installed with the skill.
- `eval/`: fixed defect cases and valid controls. A static assertion is not a model behavior test.

Preserve business invariants. Before changing a rule, record the failure it addresses, matching source evidence, and regression case. Do not add private project details, feedback provenance, personal paths, or unsupported universal thresholds.

## Checks

From the repository root:

```bash
python3 scripts/build_knowledge_index.py --check
python3 scripts/validate_skill_pack.py
python3 scripts/preservation.py
python3 -m unittest discover -s plugin-tests/shopware-knowledge -p 'test_*.py'
git diff --check
```

Use the host `agent-skills-export` with validation dependencies installed; missing validators are failures. Export and runtime discovery are separate gates. Run host version, marketplace, issue-template, and link checks when preparing the upstream patch.

## Review Cadence

Once per month and before a release, review supported Shopware patch notes and stable source changes, relevant PHPStan rules, installed Symfony/PHP compatibility, and reported skill failures. Record inspected versions, decisions, and executed tests in the changelog/validation report. The cadence is a maintenance commitment, not a background automation.

Ship `0.10.0` only after review. Keep Claude/Codex manifests, skill version, and plugin changelog synchronized using the host version-bump script. Do not publish a tag as part of the preparation branch.
