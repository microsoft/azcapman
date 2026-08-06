# Vendored skills manifest

This file is hand-maintained provenance metadata for the content under
`skills/vendor/`. It is **not** itself vendored content and is **not** covered by the
`AGENTS.md` §1 vendored-content exemption — it follows all of AGENTS.md's normal
authoring rules.

## Source

- Repository: [`microsoft/azure-skills`](https://github.com/microsoft/azure-skills)
- Last synced commit: [`6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae`](https://github.com/microsoft/azure-skills/commit/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae)
  (short: `6f4ff3f`)
- Last synced date: 2026-07-19 (UTC)

This SHA is a **last-synced snapshot marker, not a permanent pin.** When the vendored
content is refreshed in the future (see "Updating vendored content" in
`skills/azure-capacity-management/SKILL.md`), this section is updated in place with the
new commit SHA and date — the files under `skills/vendor/` are not expected to stay
frozen at this commit forever.

## What is vendored, and why

Every file below is copied **byte-for-byte, unmodified**, from the source commit above.
None of it is azcapman-authored, none of it is edited, and none of it should ever be
edited to "fix" a broken link or bring it into compliance with AGENTS.md's own rules —
see the exemption clause in `AGENTS.md` §1. If a vendored file needs to change, it is
re-copied from its source link below during a future sync, not hand-edited in place.

### Whole skills (copied in full)

| Vendored path | Upstream path |
|---|---|
| `skills/vendor/azure-quotas/` | [`skills/azure-quotas/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-quotas) |
| `skills/vendor/azure-cost/` | [`skills/azure-cost/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-cost) |
| `skills/vendor/azure-aigateway/` | [`skills/azure-aigateway/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-aigateway) |

### Partial (specific subfolders/files only)

| Vendored path | Upstream path | Why only this part |
|---|---|---|
| `skills/vendor/azure-compute/workflows/capacity-reservation/` | [`skills/azure-compute/workflows/capacity-reservation/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-compute/workflows/capacity-reservation) | Rest of `azure-compute` (vm-creator, vm-recommender, vm-troubleshooter, `essential-machine-management`) is general VM provisioning/sizing/troubleshooting/ops-onboarding — out of azcapman's capacity/quota scope. |
| `skills/vendor/microsoft-foundry/quota/` | [`skills/microsoft-foundry/quota/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/microsoft-foundry/quota) | AI/GPU model quota (TPM/PTU, region quota, cross-region capacity discovery). |
| `skills/vendor/microsoft-foundry/models/deploy-model/capacity/` | [`skills/microsoft-foundry/models/deploy-model/capacity/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/microsoft-foundry/models/deploy-model/capacity) | Same quota/capacity relevance as above; lives under a different parent (`models/deploy-model/`) in the upstream tree. Rest of `microsoft-foundry` (agent lifecycle, eval, fine-tuning, RBAC/CI-CD, preset/customize model config) is general Foundry app lifecycle, out of scope. |
| `skills/vendor/azure-prepare/references/resources-limits-quotas.md` | [`skills/azure-prepare/references/resources-limits-quotas.md`](https://github.com/microsoft/azure-skills/blob/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-prepare/references/resources-limits-quotas.md) | Rest of `azure-prepare` (azd scaffolding, Bicep/Terraform/Dockerfile generation) is general IaC, out of scope. |
| `skills/vendor/azure-validate/references/region-availability.md` | [`skills/azure-validate/references/region-availability.md`](https://github.com/microsoft/azure-skills/blob/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-validate/references/region-availability.md) | Self-contained region-availability data (real inline Static Web Apps and Azure OpenAI model-by-region tables). Rest of `azure-validate` (RBAC/Bicep/Terraform preflight checks) is out of scope. Note: `azure-prepare` has a same-named file at a different path — that copy is a thin index with dead links and was deliberately **not** vendored in favor of this self-contained one. |

## Known dangling cross-references (expected — not defects)

Because only specific subfolders were vendored, some vendored files contain relative
links to upstream content that was **not** vendored. These are left as-is (not rewritten
or removed) because editing vendored content would break the byte-identical fidelity
rule. They are documented here instead:

- `skills/vendor/microsoft-foundry/models/deploy-model/capacity/SKILL.md` links to
  `../preset/SKILL.md`, `../customize/SKILL.md`, and
  `../SKILL.md#project-selection-all-modes` — none of these (the model-preset picker,
  model-customization workflow, or the parent `deploy-model` router skill) are vendored.
- `skills/vendor/azure-prepare/references/resources-limits-quotas.md` references an
  "azure-provisioning-limit skill" that does not exist as a separate vendored or
  upstream skill under this name at the synced commit.

## License and attribution

All vendored content originates from `microsoft/azure-skills`, licensed under the MIT
License. Full text reproduced below per the license's own "include this notice in all
copies" condition:

```
MIT License

Copyright 2025 (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- author: Microsoft
