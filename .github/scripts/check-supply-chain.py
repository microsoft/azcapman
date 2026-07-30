#!/usr/bin/env python3
"""Enforce AGENTS.md rule 1.4 against this repository's own CI definitions.

Scope: workflow files under .github/workflows and composite action definitions
under .github/actions. Parses YAML and walks jobs -> steps, so a folded or
literal block scalar can't hide a piped installer across a line break.

This is a tripwire that catches mistakes in review. It is not the root of trust:
a pull request can edit this file, so the controls that actually bind are branch
protection, CODEOWNERS on .github/**, and org-level action policy. See
README-plugin.md.

Standard library plus PyYAML, which is preinstalled on GitHub-hosted runners.
"""
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required. On a GitHub-hosted runner it's preinstalled.")

GITHUB = pathlib.Path(__file__).resolve().parents[1]
REPO = GITHUB.parent

# Deny by default. Every third-party action is remote code that runs with the
# job's token, so pinning alone isn't enough - the publisher has to be approved.
ALLOWED_ACTIONS = {
    "actions/checkout",
    "actions/setup-dotnet",
    "actions/upload-pages-artifact",
    "actions/deploy-pages",
}

SHA_PINNED = re.compile(r"^(?P<repo>[^@]+)@(?P<sha>[0-9a-f]{40})$")
DOCKER_DIGEST = re.compile(r"^docker://[^@]+@sha256:[0-9a-f]{64}$")
REUSABLE = re.compile(r"\.github/workflows/[^@]+\.ya?ml@")

# Fetch-and-execute in one step.
BANNED_RUN = [
    (re.compile(r"\bnpx\b"), "npx"),
    (re.compile(r"\bbunx\b"), "bunx"),
    (re.compile(r"\buvx\b"), "uvx"),
    (re.compile(r"\bpipx\s+run\b"), "pipx run"),
    (re.compile(r"\bgo\s+run\s+\S+\.\S+/"), "go run <remote>"),
    (re.compile(r"(curl|wget)[^|]*\|\s*(sudo\s+)?(ba|z|k)?sh\b"), "curl|sh"),
    (re.compile(r"\biwr\b[^|]*\|\s*iex\b"), "iwr|iex"),
    (re.compile(r"\bInstall-Module\b"), "Install-Module"),
]
# Two-step variant: pull code down, then run it from a later line in the same
# block. Catching the pair matters more than catching either half.
FETCH = re.compile(r"\b(curl|wget|git\s+clone)\b")
EXECUTE = re.compile(r"(\bchmod\s+\+x\b|\b(ba|z|k)?sh\s+\S|\bpython3?\s+\S+\.py"
                     r"|\bnode\s+\S|\bpwsh\s+\S|\./\S+\.(sh|py|ps1)\b)")

# Installs that would otherwise resolve whatever the registry serves that day.
NEEDS_PIN = [
    (re.compile(r"\bdotnet\s+tool\s+install\b"), "--version", "--version"),
    (re.compile(r"\bpip3?\s+install\b(?![^\n]*\s-r\s)"), "==", "=="),
    (re.compile(r"\bnpm\s+(i|install)\s+-g\b"), "@", "@"),
]

errors = []


def flag(where, message):
    errors.append(f"{where}: {message}")


def normalize(script):
    """Join shell line continuations so a split token can't slip through."""
    return re.sub(r"\\\s*\n\s*", "", str(script))


def check_uses(where, ref, step):
    ref = str(ref)

    if ref.startswith("./") or ref.startswith(".\\"):
        target = REPO / ref.lstrip("./")
        if not (target / "action.yml").exists() and not (target / "action.yaml").exists():
            flag(where, f"local action '{ref}' has no action.yml to review")
        return  # Contents are scanned separately by scan_action.

    if ref.startswith("docker://"):
        if not DOCKER_DIGEST.match(ref):
            flag(where, f"'{ref}' must pin an image digest (@sha256:...); "
                        f"a container tag is mutable")
        else:
            flag(where, f"'{ref}' runs a third-party container image, which isn't "
                        f"on the approved list")
        return

    if REUSABLE.search(ref):
        flag(where, f"'{ref}' calls a reusable workflow from another repository, "
                    f"which runs remote code in this repo's context")
        return

    match = SHA_PINNED.match(ref)
    if not match:
        flag(where, f"'{ref}' isn't pinned to a 40-char commit SHA. "
                    f"A tag can be repointed at any commit.")
        return

    repo = match.group("repo")
    # owner/action/subdir@sha -> compare on owner/action.
    root = "/".join(repo.split("/")[:2])
    if root not in ALLOWED_ACTIONS:
        flag(where, f"'{root}' isn't on the approved action list "
                    f"({', '.join(sorted(ALLOWED_ACTIONS))})")

    with_inputs = step.get("with") or {}
    if root == "actions/checkout":
        for risky in ("repository", "submodules", "ssh-key"):
            if with_inputs.get(risky):
                flag(where, f"checkout sets '{risky}', which pulls in code from "
                            f"outside this repository")


def check_run(where, script):
    text = normalize(script)

    for pattern, label in BANNED_RUN:
        if pattern.search(text):
            flag(where, f"'{label}' fetches and executes third-party code. Use a "
                        f"checked-in script, a preinstalled tool, or an approved action.")

    if FETCH.search(text) and EXECUTE.search(text):
        flag(where, "downloads code and then runs it in the same step")

    for pattern, token, shown in NEEDS_PIN:
        if pattern.search(text) and token not in text:
            flag(where, f"install is unpinned; it resolves whatever the registry "
                        f"serves at build time. Pin it with '{shown}'.")


def walk_steps(where, steps):
    for index, step in enumerate(steps or []):
        if not isinstance(step, dict):
            continue
        name = step.get("name") or step.get("uses") or f"step {index + 1}"
        at = f"{where} :: {name}"
        if step.get("uses"):
            check_uses(at, step["uses"], step)
        if step.get("run"):
            check_run(at, step["run"])


def scan_workflow(path):
    rel = path.relative_to(REPO)
    doc = yaml.safe_load(path.read_text()) or {}

    # `on:` parses as the boolean True in YAML 1.1, and takes string, list, or
    # mapping form.
    triggers = doc.get("on", doc.get(True)) or {}
    if isinstance(triggers, dict):
        trigger_names = set(triggers)
    elif isinstance(triggers, list):
        trigger_names = {str(t) for t in triggers}
    else:
        trigger_names = {str(triggers)}
    if "pull_request_target" in trigger_names:
        flag(str(rel), "uses 'pull_request_target', which runs with a writable "
                       "token in the context of untrusted pull request code")

    jobs = doc.get("jobs") or {}
    has_top_level_permissions = "permissions" in doc

    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        where = f"{rel} :: {job_name}"
        if not has_top_level_permissions and "permissions" not in job:
            flag(where, "no explicit 'permissions:', so it inherits the "
                        "repository default token scope")
        if job.get("uses"):
            check_uses(where, job["uses"], job)
        walk_steps(where, job.get("steps"))


def scan_action(path):
    rel = path.relative_to(REPO)
    doc = yaml.safe_load(path.read_text()) or {}
    runs = doc.get("runs") or {}
    walk_steps(str(rel), runs.get("steps"))
    if runs.get("image", "").startswith("docker://"):
        check_uses(str(rel), runs["image"], {})


workflows = sorted(GITHUB.glob("workflows/*.yml")) + sorted(GITHUB.glob("workflows/*.yaml"))
actions = sorted(GITHUB.glob("actions/**/action.yml")) + sorted(GITHUB.glob("actions/**/action.yaml"))

for path in workflows:
    scan_workflow(path)
for path in actions:
    scan_action(path)

if errors:
    print("Supply chain check failed (AGENTS.md rule 1.4):\n")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print(f"Supply chain check passed ({len(workflows)} workflow(s), "
      f"{len(actions)} composite action(s)): actions approved and SHA-pinned, "
      f"no fetch-and-execute, no unpinned installs, token scopes explicit.")
