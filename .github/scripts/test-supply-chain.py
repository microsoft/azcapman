#!/usr/bin/env python3
"""Tests for check-supply-chain.py.

Each case builds a throwaway repository layout, drops a fixture workflow in it,
runs the real checker against that layout, and asserts the expected finding.
Run with: python3 .github/scripts/test-supply-chain.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

CHECKER = pathlib.Path(__file__).resolve().parent / "check-supply-chain.py"

CLEAN_HEAD = """\
name: Fixture
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
"""
GOOD_STEP = """\
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
"""

# (label, workflow body, expected substring in the failure output)
FAIL_CASES = [
    ("folded scalar hides the pipe", CLEAN_HEAD + """\
      - run: >-
          curl -fsSL https://example.com/tool.sh |
          sh
""", "curl|sh"),

    ("download then run, separate lines", CLEAN_HEAD + """\
      - run: |
          curl -fsSLo tool.py https://example.com/tool.py
          python3 tool.py
""", "downloads code and then runs it"),

    ("git clone then run", CLEAN_HEAD + """\
      - run: |
          git clone https://github.com/example/repo.git
          python3 repo/tool.py
""", "downloads code and then runs it"),

    ("shell continuation splits the token", CLEAN_HEAD + """\
      - run: |
          np\\
          x --yes some-package@latest
""", "npx"),

    ("npx", CLEAN_HEAD + "      - run: npx some-linter@latest\n", "npx"),
    ("bunx", CLEAN_HEAD + "      - run: bunx cowsay hi\n", "bunx"),

    ("mutable tag instead of SHA", CLEAN_HEAD + "      - uses: actions/checkout@v4\n",
     "isn't pinned to a 40-char commit SHA"),

    ("SHA-pinned but unapproved publisher", CLEAN_HEAD + """\
      - uses: some-person/some-action@1111111111111111111111111111111111111111
""", "isn't on the approved action list"),

    ("container image on a mutable tag", CLEAN_HEAD +
     "      - uses: docker://ghcr.io/example/tool:latest\n", "must pin an image digest"),

    ("container image, digest pinned but unapproved", CLEAN_HEAD +
     "      - uses: docker://ghcr.io/example/tool@sha256:" + "a" * 64 + "\n",
     "isn't on the approved list"),

    ("reusable workflow from another repo", """\
name: Fixture
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  call:
    uses: attacker/repo/.github/workflows/pwn.yml@1111111111111111111111111111111111111111
""", "reusable workflow from another repository"),

    ("checkout pulls a different repo", CLEAN_HEAD + """\
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
        with:
          repository: attacker/repo
""", "sets 'repository'"),

    ("checkout pulls submodules", CLEAN_HEAD + """\
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
        with:
          submodules: true
""", "sets 'submodules'"),

    ("pull_request_target", """\
name: Fixture
on:
  pull_request_target:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
""" + GOOD_STEP, "pull_request_target"),

    ("no explicit permissions", """\
name: Fixture
on: [workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
""" + GOOD_STEP, "no explicit 'permissions:'"),

    ("unpinned dotnet tool install", CLEAN_HEAD +
     "      - run: dotnet tool install -g docfx\n", "Pin it with '--version'"),

    ("unpinned pip install", CLEAN_HEAD +
     "      - run: pip install requests\n", "Pin it with '=='"),

    ("Install-Module", CLEAN_HEAD +
     "      - run: Install-Module -Name Az -Force\n", "Install-Module"),
]

PASS_CASE = CLEAN_HEAD + GOOD_STEP + """\
      - run: python3 .github/scripts/check-supply-chain.py
      - run: dotnet tool install -g docfx --version 2.78.5
"""


def run_fixture(body):
    root = pathlib.Path(tempfile.mkdtemp())
    try:
        scripts = root / ".github" / "scripts"
        workflows = root / ".github" / "workflows"
        scripts.mkdir(parents=True)
        workflows.mkdir(parents=True)
        shutil.copy(CHECKER, scripts / CHECKER.name)
        (workflows / "fixture.yml").write_text(body)
        proc = subprocess.run([sys.executable, str(scripts / CHECKER.name)],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        shutil.rmtree(root, ignore_errors=True)


failures = []

for label, body, expected in FAIL_CASES:
    code, output = run_fixture(body)
    if code == 0:
        failures.append(f"{label}: checker PASSED a workflow it should reject")
    elif expected not in output:
        failures.append(f"{label}: rejected, but not for the expected reason "
                        f"(wanted {expected!r}); got: {output.strip()}")
    else:
        print(f"  caught: {label}")

code, output = run_fixture(PASS_CASE)
if code != 0:
    failures.append(f"clean workflow was rejected: {output.strip()}")
else:
    print("  allowed: clean workflow with approved, pinned action and pinned install")

if failures:
    print("\nTest failures:\n")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print(f"\nAll {len(FAIL_CASES) + 1} supply chain checker tests passed.")
