#!/usr/bin/env python3
"""Prepare the pinned upstream checkout from canonical source, without staging.

Usage: python scripts/prepare_upstream.py --host /path/to/ai-coding-tools [--apply]

The default is a read-only preflight/plan. --apply owns only the registration
patch, plugin, namespaced support and dedicated workflow. It may replace files
in those destinations; unrecognized files, symlinks and conflicting tracked
registrations are refused. No branch, commit, auth, settings, dependency install,
network request, model call or report is created. Unexpected I/O failures can
leave partial copies; rerun after resolving the error, without resetting Git.
"""

from __future__ import annotations

import argparse
import json
import stat
import subprocess
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
BASELINE = "a276558d12d0e09696fb9d1a7b4cd1925c44baf6"
PLUGIN = Path("plugins/shopware-knowledge")
UPSTREAM_REPOSITORY = "https://github.com/shopwareLabs/ai-coding-tools"
UPSTREAM_HOMEPAGE = UPSTREAM_REPOSITORY + "/tree/main/plugins/shopware-knowledge"
REGISTRATIONS = frozenset({
    ".gitignore",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    ".github/ISSUE_TEMPLATE/plugin_component_other.yml",
    ".github/ISSUE_TEMPLATE/skill_issue.yml",
    "README.md",
    "plugin-tests/dev-tooling/codex_manifest.bats",
})
SCRIPTS = ("validate_skill_pack.py", "build_knowledge_index.py", "verify_core_anchors.py")
EVAL_FILES = ("cases.json", "run.py", "requirements.txt", "should-trigger.md", "should-not-trigger.md")
NAMESPACES = (PLUGIN, Path("scripts/shopware-knowledge"), Path("eval/shopware-knowledge"),
              Path("plugin-tests/shopware-knowledge"))
IGNORED = {"__pycache__", ".DS_Store"}
WORKFLOW_PATH = Path(".github/workflows/shopware-knowledge.yml")
WORKFLOW = """name: Shopware Knowledge

on:
  pull_request:
    branches: [main]
    paths:
      - 'plugins/shopware-knowledge/**'
      - 'plugin-tests/shopware-knowledge/**'
      - 'scripts/shopware-knowledge/**'
      - 'eval/shopware-knowledge/**'
      - '.claude-plugin/marketplace.json'
      - '.agents/plugins/marketplace.json'
      - '.github/workflows/shopware-knowledge.yml'
  push:
    branches: [main]
    paths:
      - 'plugins/shopware-knowledge/**'
      - 'plugin-tests/shopware-knowledge/**'
      - 'scripts/shopware-knowledge/**'
      - 'eval/shopware-knowledge/**'
      - '.claude-plugin/marketplace.json'
      - '.agents/plugins/marketplace.json'
      - '.github/workflows/shopware-knowledge.yml'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  package:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
      - uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0
        with:
          python-version: '3.12'
          cache: pip
          cache-dependency-path: eval/shopware-knowledge/requirements.txt
      - name: Install required pinned validation dependencies
        run: python -m pip install -r eval/shopware-knowledge/requirements.txt
      - name: Test isolated package contracts
        run: python -m unittest discover -s plugin-tests/shopware-knowledge -p 'test_*.py' -v
      - name: Check topic index and portable package
        run: |
          python scripts/shopware-knowledge/build_knowledge_index.py --check
          python scripts/shopware-knowledge/validate_skill_pack.py
      - name: Validate fixtures without model calls
        run: python eval/shopware-knowledge/run.py check
"""


class PreparationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PreparationError(message)


def git(host, *args, check=True):
    result = subprocess.run(["git", "-C", str(host), *args], capture_output=True, text=True)
    if check and result.returncode:
        raise PreparationError(f"git {' '.join(args[:2])}: {result.stderr.strip() or result.stdout.strip()}")
    return result


def replace_once(text, old, new):
    require(text.count(old) == 1, f"Source packaging contract changed: expected one {old!r}; update this adapter")
    return text.replace(old, new, 1)


def read_file(path):
    require(path.is_file() and not path.is_symlink(), f"Required regular source file missing: {path.relative_to(SOURCE)}")
    return path.read_bytes(), stat.S_IMODE(path.stat().st_mode)


def payload():
    """Assemble bytes in memory. Runtime files are copied, never transformed."""
    files = {}
    for path in sorted((SOURCE / PLUGIN).rglob("*")):
        rel = path.relative_to(SOURCE)
        if any(part in IGNORED for part in rel.parts):
            continue
        require(not path.is_symlink(), f"Source symlink not supported: {rel}")
        if path.is_file():
            files[rel] = read_file(path)
    require(PLUGIN / "skills/shopware-development/SKILL.md" in files, "Canonical skill is missing")
    for runtime in ("claude", "codex"):
        rel = PLUGIN / f".{runtime}-plugin/plugin.json"
        require(rel in files, f"Canonical native manifest missing: {rel}")
        content, mode = files[rel]
        manifest = json.loads(content)
        require(isinstance(manifest, dict), f"Native manifest must be an object: {rel}")
        manifest["repository"] = UPSTREAM_REPOSITORY
        manifest["homepage"] = UPSTREAM_HOMEPAGE
        files[rel] = (json.dumps(manifest, indent=2) + "\n").encode(), mode
    for name in ("README.md", "AGENTS.md", "CHANGELOG.md"):
        content, mode = read_file(SOURCE / "upstream/plugin-docs" / name)
        if name == "README.md":
            text = replace_once(content.decode(), "(../../plugins/shopware-knowledge/skills/", "(skills/")
            text = replace_once(text, "(../../plugins/shopware-knowledge/knowledge-index.json)", "(knowledge-index.json)")
            content = text.encode()
        files[PLUGIN / name] = content, mode
    for name in SCRIPTS:
        content, mode = read_file(SOURCE / "scripts" / name)
        text = replace_once(content.decode(), "Path(__file__).resolve().parents[1]", "Path(__file__).resolve().parents[2]")
        if name == "validate_skill_pack.py":
            text = replace_once(text, "Install eval/requirements.txt", "Install eval/shopware-knowledge/requirements.txt")
        files[Path("scripts/shopware-knowledge") / name] = text.encode(), mode
    for name in EVAL_FILES:
        files[Path("eval/shopware-knowledge") / name] = read_file(SOURCE / "eval" / name)
    test, mode = read_file(SOURCE / "plugin-tests/shopware-knowledge/test_package.py")
    text = test.decode()
    for old, new in (
        ('"pack_validator"', '"shopware_knowledge_pack_validator"'),
        ('"eval_runner"', '"shopware_knowledge_eval_runner"'),
        ('"scripts/validate_skill_pack.py"', '"scripts/shopware-knowledge/validate_skill_pack.py"'),
        ('"eval/run.py"', '"eval/shopware-knowledge/run.py"'),
    ):
        text = replace_once(text, old, new)
    files[Path("plugin-tests/shopware-knowledge/test_package.py")] = text.encode(), mode
    files[WORKFLOW_PATH] = WORKFLOW.encode(), 0o644
    return files


def check_target(host, rel):
    require(not rel.is_absolute() and ".." not in rel.parts, f"Unsafe destination: {rel}")
    current = host
    for part in rel.parts:
        current /= part
        require(not current.is_symlink(), f"Destination symlink refused: {rel}")
    target = host / rel
    require(not target.exists() or target.is_file(), f"Destination is not a regular file: {rel}")
    require(target.resolve().is_relative_to(host), f"Destination escapes host: {rel}")


def preflight(host, files):
    require(host.is_dir(), "--host must be an existing checkout directory")
    require(not (host == SOURCE or host.is_relative_to(SOURCE) or SOURCE.is_relative_to(host)), "Host and source checkouts must not overlap")
    root = Path(git(host, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    require(root == host, "--host must be the checkout root")
    require(git(host, "rev-parse", "HEAD").stdout.strip() == BASELINE, f"Host HEAD must be exactly {BASELINE}; no checkout or reset is performed")
    require(git(host, "diff", "--cached", "--quiet", check=False).returncode == 0, "Host has staged changes; leave its index untouched and use a clean checkout")
    patch = SOURCE / "upstream/registration.patch"
    patch_paths = [line.split("\t", 2)[2] for line in git(host, "apply", "--numstat", str(patch)).stdout.splitlines()]
    require(len(patch_paths) == len(REGISTRATIONS) and set(patch_paths) == REGISTRATIONS, "registration.patch must change exactly the six approved tracked paths")
    for rel in (*files, *(Path(p) for p in REGISTRATIONS)):
        check_target(host, rel)
    for namespace in NAMESPACES:
        for path in (host / namespace).rglob("*"):
            if any(part in IGNORED for part in path.relative_to(host).parts):
                continue
            rel = path.relative_to(host)
            require(not path.is_symlink(), f"Destination symlink refused: {rel}")
            if path.is_file():
                require(rel in files, f"Unmanaged destination file refused: {rel}; no files were removed")
    forward = git(host, "apply", "--check", "--whitespace=error", str(patch), check=False)
    if forward.returncode == 0:
        return patch, "pending"
    reverse = git(host, "apply", "--reverse", "--check", str(patch), check=False)
    require(reverse.returncode == 0, "Registration patch conflicts or is partially applied; no files changed:\n" + forward.stderr.strip())
    return patch, "already applied"


def prepare(host, apply=False):
    host = Path(host).expanduser().resolve()
    files = payload()
    patch, registration = preflight(host, files)
    changes = []
    for rel, (content, mode) in sorted(files.items()):
        path = host / rel
        if not path.is_file() or path.read_bytes() != content or stat.S_IMODE(path.stat().st_mode) != mode:
            changes.append(rel)
    print(f"Host baseline: {BASELINE}")
    print(f"Registration patch: {registration}; {len(changes)} of {len(files)} copy outputs need updating")
    for rel in changes:
        print(f"  copy {rel.as_posix()}")
    if not apply:
        print("DRY RUN: no files changed. Add --apply to prepare this checkout.")
        return
    # Git's own check is repeated during apply; no index is used or updated.
    if registration == "pending":
        git(host, "apply", "--whitespace=error", str(patch))
    for rel in changes:
        content, mode = files[rel]
        target = host / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        target.chmod(mode)
    require(git(host, "diff", "--cached", "--quiet", check=False).returncode == 0, "Host index changed concurrently; inspect before continuing")
    print("Prepared. Nothing staged, committed or pushed; no tests or model calls were run.")
    print("Validate with the namespaced scripts and plugin-tests/shopware-knowledge suite.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="apply registrations and update the owned copy outputs")
    args = parser.parse_args()
    try:
        prepare(args.host, apply=args.apply)
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
