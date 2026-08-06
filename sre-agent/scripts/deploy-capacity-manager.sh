#!/usr/bin/env bash
# Deploys this package through the Azure SRE Agent v2 data-plane helper.
# Source: https://learn.microsoft.com/en-us/azure/sre-agent/api-reference
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
package_dir=$(cd -- "${script_dir}/.." && pwd)
rest_helper="${script_dir}/sre-agent-rest.sh"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  printf 'Usage: deploy-capacity-manager.sh [sre-agent-rest.sh connection arguments]\n'
  exit 0
fi

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

python3 - "$package_dir" "$tmp_dir" <<'PY'
import json
import pathlib
import sys

package_dir = pathlib.Path(sys.argv[1])
tmp_dir = pathlib.Path(sys.argv[2])

skill_content = (package_dir / "skill" / "SKILL.md").read_text()
instructions = (package_dir / "subagent" / "capacity-manager.instructions.md").read_text()

skill = {
    "name": "azure-capacity-management",
    "type": "Skill",
    "tags": [],
    "properties": {
        "name": "azure-capacity-management",
        "description": (
            "Investigate Azure quota, capacity reservations, quota groups, region access, "
            "and zonal enablement for SaaS workloads."
        ),
        "tools": [
            "RunAzCliReadCommands",
            "RunAzCliWriteCommands",
            "GetAzCliHelp",
        ],
        "skillContent": skill_content,
        "additionalFiles": [],
    },
}
subagent = {
    "name": "capacity-manager",
    "type": "ExtendedAgent",
    "tags": [],
    "properties": {
        "instructions": instructions,
        "handoffDescription": (
            "Handles Azure quota, quota groups, capacity reservations, region access, "
            "zonal enablement, capacity planning, and deployment-stamp readiness for SaaS "
            "estates. It separates access, quota, zone, reservation, and pricing constraints, "
            "gathers Azure evidence, and returns cited findings and explicit assumptions."
        ),
        "handoffs": [],
        "tools": [
            "RunAzCliReadCommands",
            "RunAzCliWriteCommands",
            "GetAzCliHelp",
        ],
        "temperature": 0.2,
        "enableSkills": True,
        "allowedSkills": ["azure-capacity-management"],
    },
}

(tmp_dir / "skill.json").write_text(json.dumps(skill))
(tmp_dir / "subagent.json").write_text(json.dumps(subagent))
PY

"$rest_helper" put --kind skills --name azure-capacity-management --body "$tmp_dir/skill.json" "$@"
"$rest_helper" put --kind agents --name capacity-manager --body "$tmp_dir/subagent.json" "$@"
