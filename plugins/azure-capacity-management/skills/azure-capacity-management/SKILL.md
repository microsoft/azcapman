---
name: azure-capacity-management
description: |
  This skill should be used when the user asks about Azure capacity management, quota
  operations, or capacity planning for SaaS ISVs running workloads in their own Azure
  subscriptions under EA or MCA. Also covers AI/GPU model quota and capacity (Azure
  OpenAI/Foundry TPM, PTU, cross-region capacity discovery), VM capacity reservations,
  region/SKU availability lookups, capacity-forecasting-scoped cost data (cost
  forecast/query APIs, not general cost optimization), Azure AI Gateway/APIM
  rate-limiting and throughput-control policies for AI workloads, and per-service
  resource/limit/quota reference lookups.
license: MIT
---

# Azure capacity management

Estate-level capacity and quota management for SaaS ISVs operating workloads in subscriptions they own or control under an [Enterprise Agreement (EA)](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-enterprise-agreement) or [Microsoft Customer Agreement (MCA)](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-microsoft-customer-agreement). This skill aligns with the [ISV landing zone guidance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/isv-landing-zone) and covers pure SaaS and [stamp-based isolation](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/overview#deployment-stamps-pattern) patterns where customers are isolated through dedicated or shared deployment stamps inside the ISV's Azure estate.

Read the full Azure implementation reference at `references/docs/operations/capacity-and-quotas/README.md`.

## FinOps capability mapping

Treat Azure capacity management as implementation detail under the canonical FinOps Framework. Capacity evidence commonly supports Planning & Estimating, Forecasting, Architecting & Workload Placement, Usage Optimization, Rate Optimization, Budgeting, Governance, Policy & Risk, and Automation, Tools & Services. Use [Well-Architected capacity planning](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning), [reliable scaling](https://learn.microsoft.com/en-us/azure/well-architected/reliability/scaling), and [workload supply chain guidance](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/workload-supply-chain) as Azure implementation guidance, not as a replacement framework. [Source](https://www.finops.org/framework/) [Source](https://www.finops.org/framework/domains/)

| FinOps capability | Capacity question | Azure surfaces |
|------|-------------|----------------|
| Planning & Estimating | What capacity does the planned workload, scenario, or stamp need? | Workload requirements, scale-unit assumptions, Azure Monitor, estimates, FinOps budgets |
| Forecasting | When will demand exceed quota, region, SKU, zone, or reserved-capacity headroom? | Historical usage, growth trends, forecast breach dates, capacity planning models |
| Architecting & Workload Placement | Which regions, zones, SKUs, quota pools, or deployment patterns should change? | SKU availability, region access, quota groups, capacity reservation groups, CRG sharing, overallocation |
| Usage Optimization | Which allocated capacity, quota, or deployment pattern is underused or inefficient? | Utilization, headroom, rightsizing evidence, unused reserved capacity, demand signals |
| Rate Optimization | Where should capacity guarantees be coordinated with reservations or savings plans? | Benefit recommendations, commitment utilization, CRG utilization, pricing evidence from FinOps Hub |
| Governance, Policy & Risk | Which capacity risks need ownership, exception review, or escalation? | Approved regions and SKUs, owner metadata, risk thresholds, exception status |
| Automation, Tools & Services | Which controls expose capacity risk before deployment or scale events? | Quota alerts, budget alerts, anomaly alerts, CI/CD gates, workflow status |

Read `references/docs/operations/capacity-planning/README.md` for forecasting details and `references/docs/operations/capacity-governance/README.md` for the governance program design.

## Quota operations

Azure assigns [default quota limits](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests) per subscription. EA subscriptions typically start with 350 cores; pay-as-you-go subscriptions start with 20 cores. Some VM series have offer restrictions that block deployment until you request access.

Key workflows:
- **Region access:** Submit a [region access support request](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process) when a subscription can't deploy to a restricted region.
- **Zonal enablement:** Submit a [zonal enablement request](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series) for restricted VM series in specific availability zones.
- **Quota increases:** Use [per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests) for individual subscriptions or [quota group limit increases](https://learn.microsoft.com/en-us/azure/quotas/quota-group-limit-increase) for grouped subscriptions.

CLI reference:
```bash
# List quota usage for a subscription
az quota usage list --scope /subscriptions/{sub-id}/providers/Microsoft.Compute/locations/{location}

# Request a quota increase
az quota create --resource-name "StandardDSv3Family" --scope /subscriptions/{sub-id}/providers/Microsoft.Compute/locations/{location} --limit-object value=500
```

Read `references/docs/operations/quota/README.md` for the complete quota operations reference.

## Quota groups

[Quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups) are ARM objects that aggregate compute quota across eligible subscriptions at the management group scope. They reduce stranded VM-family headroom and let you request group-level increases.

**Prerequisites:** Register the `Microsoft.Quota` resource provider on each member subscription. The management group must exist before creating the quota group.

**Limitations:**
- IaaS compute only — doesn't cover storage, networking, or PaaS services
- A subscription can belong to a single quota group at a time ([source](https://learn.microsoft.com/en-us/azure/quotas/quota-groups))
- Doesn't grant region or zone access — those require separate support requests
- [Quota transfers](https://learn.microsoft.com/en-us/azure/quotas/transfer-quota-groups) move allocation between member subscriptions but don't change the group total

**Lifecycle:** Create the quota group under a management group, [add subscriptions](https://learn.microsoft.com/en-us/azure/quotas/add-remove-subscriptions-quota-group), then request group-level limit increases. Monitor allocation snapshots and transfer as demand shifts between subscriptions.

Read `references/docs/operations/quota-groups/README.md` for the complete reference including ARM lifecycle, transfer mechanics, and monitoring integration.

## Capacity reservations

[Capacity reservation groups (CRGs)](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview) guarantee compute capacity for specific VM sizes in a region or availability zone. CRGs are capacity guarantees, not pricing commitments — unused reserved capacity is billed at the pay-as-you-go rate for the VM size.

**Cost implications:** Reserved capacity is billed whether or not VMs run against it. Pair CRGs with Azure Reservations or savings plans to get both capacity guarantee and pricing discount.

**Sharing (preview):** CRGs can be [shared across subscriptions](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-group-share) within the same tenant. The ODCR owner in the consumer subscription needs `Microsoft.Compute/capacityReservationGroups/share/action`. The VM owner in the consumer subscription needs `Microsoft.Compute/capacityReservationGroups/read`, `Microsoft.Compute/capacityReservationGroups/deploy`, `Microsoft.Compute/capacityReservationGroups/capacityReservations/read`, and `Microsoft.Compute/capacityReservationGroups/capacityReservations/deploy`. Portal support isn't available in preview; use CLI, PowerShell, or REST API.

**Overallocation:** [Overallocation](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overallocate) lets you deploy more VMs than the reserved quantity. Excess VMs don't have capacity guarantees but benefit from the reservation when capacity is available.

**Zone alignment:** CRGs are zone-specific. Before sharing across subscriptions, verify logical-to-physical zone mapping with the `Get-AzAvailabilityZoneMapping.ps1` script — [logical zones](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview#configuring-resources-for-availability-zone-support) can map to different physical zones across subscriptions.

Read `references/docs/operations/capacity-reservations/README.md` for the complete reference including automation patterns (REST API, Bicep, Terraform).

## AKS capacity governance

AKS node pools consume VM quota and can associate with capacity reservation groups, but with constraints specific to the AKS lifecycle:

- **Node pool CRG association** happens at creation time — you can't associate an existing node pool with a CRG after the fact
- **Identity requirement:** The AKS cluster must use a [user-assigned managed identity](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity) with `Microsoft.Compute/capacityReservationGroups/read` permission on the CRG
- **Disassociation** removes the CRG association but doesn't delete the node pool
- **Zone alignment** matters for cross-subscription CRG sharing — verify physical zone mapping before configuring AKS node pools against shared CRGs

Read `references/docs/operations/aks-capacity/README.md` for the complete reference including Bicep and Terraform examples.

## Non-compute quotas

Storage accounts, App Service plans, Cosmos DB throughput, Service Bus namespaces, Key Vault transactions, and other services have their own quota limits outside the compute quota system. Quota groups don't cover these — manage them through standard [quota requests](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests) and service-specific scaling controls.

Read `references/docs/operations/non-compute-quotas/README.md` for service-specific quota references.

## Monitoring and governance

Three alert types cover the capacity governance space:

1. **Quota alerts:** [Azure Monitor alerts](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting) triggered when quota usage crosses a configured threshold. Requires Reader or higher on the subscription.
2. **Budget alerts:** [Cost Management alerts](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending) triggered when actual or forecasted spend exceeds budget thresholds. Uses Cost Management RBAC.
3. **Anomaly alerts:** Cost Management anomaly detection that flags unexpected spending patterns. Deploy with `references/scripts/anomaly-alerts/Deploy-AnomalyAlert.ps1` or bulk deploy with `references/scripts/anomaly-alerts/Deploy-BulkALZ.ps1`.

**Governance cadence:** Monthly quota reviews, quarterly capacity planning cycles, and post-incident reviews when scaling events fail. Read `references/docs/operations/monitoring-alerting/README.md` for alert configuration details and `references/docs/operations/capacity-governance/README.md` for the governance program design.

## Scripts quick reference

| Script | Path | Purpose |
|--------|------|---------|
| Get-AzVMQuotaUsage.ps1 | `references/scripts/quota/` | Multi-threaded quota analysis across subscriptions |
| Show-AzVMQuotaReport.ps1 | `references/scripts/quota/` | Single-threaded quota reporting |
| Get-AzAvailabilityZoneMapping.ps1 | `references/scripts/quota/` | Logical-to-physical zone mapping |
| Get-BenefitRecommendations.ps1 | `references/scripts/rate/` | Reservation and savings plan recommendations |
| Deploy-AnomalyAlert.ps1 | `references/scripts/anomaly-alerts/` | Deploy cost anomaly alerts |
| Deploy-BulkALZ.ps1 | `references/scripts/anomaly-alerts/` | Bulk deploy anomaly alerts |
| Deploy-Budget.ps1 | `references/scripts/budgets/` | Deploy individual budgets |
| Deploy-BulkBudgets.ps1 | `references/scripts/budgets/` | Bulk deploy budgets |
| Suppress-AdvisorRecommendations.ps1 | `references/scripts/advisor/` | Suppress Advisor recommendations |
| Serverless SQL workbook | `references/scripts/serverless-sql-storage/` | Azure Monitor workbook for serverless SQL allocated vs. used storage; identifies databases worth shrinking to reclaim billing waste |

Read the README in each script directory for parameter requirements and prerequisites.

## Key distinctions

These are commonly confused — keep them separated:

- **Capacity reservation vs Azure Reservation vs savings plan:** [Capacity reservations](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview) guarantee compute supply. [Azure Reservations](https://www.finops.org/framework/capabilities/rate-optimization/) and [savings plans](https://learn.microsoft.com/en-us/azure/cost-management-billing/savings-plan/) provide pricing discounts. Capacity guarantees supply; pricing commitments reduce cost.
- **Quota group vs management group:** [Quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups) aggregate compute quota. Management groups organize subscriptions for RBAC and policy. Quota groups are created under management groups but don't inherit their policy or access controls.
- **Logical vs physical zone:** [Logical zones](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview#configuring-resources-for-availability-zone-support) are subscription-specific labels. Physical zones are datacenter locations. Zone 1 in subscription A may map to a different physical zone than zone 1 in subscription B.
- **Region access vs quota increase:** Quota increases raise limits within an already-enabled region. [Region access requests](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process) unblock a restricted region for the subscription.

## Documentation map

| Domain | Reference path |
|--------|---------------|
| Azure capacity reference | `references/docs/operations/capacity-and-quotas/README.md` |
| Glossary | `references/docs/operations/glossary.md` |
| Quota operations | `references/docs/operations/quota/README.md` |
| Quota groups | `references/docs/operations/quota-groups/README.md` |
| Capacity reservations | `references/docs/operations/capacity-reservations/README.md` |
| AKS capacity | `references/docs/operations/aks-capacity/README.md` |
| Non-compute quotas | `references/docs/operations/non-compute-quotas/README.md` |
| Monitoring and alerting | `references/docs/operations/monitoring-alerting/README.md` |
| Capacity governance | `references/docs/operations/capacity-governance/README.md` |
| Capacity planning | `references/docs/operations/capacity-planning/README.md` |
| Billing (EA) | `references/docs/billing/legacy/README.md` |
| Billing (MCA) | `references/docs/billing/modern/README.md` |
| Deployment patterns | `references/docs/deployment/README.md` |
| Tools and scripts | `references/docs/operations/tools-scripts/README.md` |
| Quota scripts | `references/scripts/quota/README.md` |
| Anomaly alerts | `references/scripts/anomaly-alerts/README.md` |
| Budgets | `references/scripts/budgets/README.md` |
| Rate optimization | `references/scripts/rate/README.md` |
| Serverless SQL storage | `references/scripts/serverless-sql-storage/README.md` |

## Vendored upstream skills (microsoft/azure-skills)

Content under `references/vendor/` is unmodified, byte-identical material copied from
[`microsoft/azure-skills`](https://github.com/microsoft/azure-skills) — it is not
azcapman-authored, is not edited to fit this skill's voice, and is exempt from AGENTS.md's
authored-content rules per the exemption clause in AGENTS.md §1.

| When to use | Vendored path |
|---|---|
| VM/family core quota checks and increase requests (CLI-driven) | `references/vendor/azure-quotas/SKILL.md` |
| Cost forecast and cost query APIs scoped to capacity forecasting (not general cost optimization) | `references/vendor/azure-cost/SKILL.md` |
| Azure AI Gateway / APIM policies for AI workload throughput and rate-limit patterns | `references/vendor/azure-aigateway/SKILL.md` |
| VM/compute capacity reservations (creation, association/disassociation) | `references/vendor/azure-compute/workflows/capacity-reservation/capacity-reservation.md` |
| Azure OpenAI/Foundry model quota (TPM, PTU, cross-region capacity discovery) | `references/vendor/microsoft-foundry/quota/quota.md` |
| Foundry model deployment capacity checks during model deploy | `references/vendor/microsoft-foundry/models/deploy-model/capacity/SKILL.md` |
| General per-service resource/limit/quota reference table | `references/vendor/azure-prepare/references/resources-limits-quotas.md` |
| Region and SKU availability lookups | `references/vendor/azure-validate/references/region-availability.md` |

The three whole-skill copies (`azure-quotas`, `azure-cost`, `azure-aigateway`) keep their
own internal `SKILL.md` structure for their own references and scripts — they are not
separately registered as standalone skills in this repo; this skill is the only
discovery path into them.

### Vendored knowledge index

Agent Skills load referenced resources on demand through
[progressive disclosure](https://agentskills.io/specification#progressive-disclosure).
Use this index to select the file that matches the task.

#### Azure AI Gateway

- [Skill overview](references/vendor/azure-aigateway/SKILL.md)
- [Authentication](references/vendor/azure-aigateway/references/auth-best-practices.md)
- [Patterns](references/vendor/azure-aigateway/references/patterns.md)
- [Policies](references/vendor/azure-aigateway/references/policies.md)
- [Python Content Safety SDK](references/vendor/azure-aigateway/references/sdk/azure-ai-contentsafety-py.md)
- [TypeScript Content Safety SDK](references/vendor/azure-aigateway/references/sdk/azure-ai-contentsafety-ts.md)
- [.NET API Management SDK](references/vendor/azure-aigateway/references/sdk/azure-mgmt-apimanagement-dotnet.md)
- [Python API Management SDK](references/vendor/azure-aigateway/references/sdk/azure-mgmt-apimanagement-py.md)
- [Troubleshooting](references/vendor/azure-aigateway/references/troubleshooting.md)

#### Azure compute capacity reservations

- [Capacity reservation workflow](references/vendor/azure-compute/workflows/capacity-reservation/capacity-reservation.md)
- [Association and disassociation](references/vendor/azure-compute/workflows/capacity-reservation/references/association-disassociation.md)
- [Capacity reservation overview](references/vendor/azure-compute/workflows/capacity-reservation/references/capacity-reservation-overview.md)

#### Azure cost

- [Skill overview](references/vendor/azure-cost/SKILL.md)
- Cost forecast:
  [error handling](references/vendor/azure-cost/cost-forecast/error-handling.md),
  [examples](references/vendor/azure-cost/cost-forecast/examples.md),
  [guardrails](references/vendor/azure-cost/cost-forecast/guardrails.md),
  [request body schema](references/vendor/azure-cost/cost-forecast/request-body-schema.md),
  and [workflow](references/vendor/azure-cost/cost-forecast/workflow.md).
- Cost optimization:
  [authentication](references/vendor/azure-cost/cost-optimization/auth-best-practices.md),
  [AKS anomalies](references/vendor/azure-cost/cost-optimization/azure-aks-anomalies.md),
  [AKS cost add-on](references/vendor/azure-cost/cost-optimization/azure-aks-cost-addon.md),
  [Azure Quick Review](references/vendor/azure-cost/cost-optimization/azure-quick-review.md),
  [Azure Resource Graph](references/vendor/azure-cost/cost-optimization/azure-resource-graph.md),
  [report template](references/vendor/azure-cost/cost-optimization/report-template.md),
  [.NET Redis SDK](references/vendor/azure-cost/cost-optimization/sdk/azure-resource-manager-redis-dotnet.md),
  [Azure Cache for Redis](references/vendor/azure-cost/cost-optimization/services/redis/azure-cache-for-redis.md),
  [Azure Storage](references/vendor/azure-cost/cost-optimization/services/storage/azure-storage.md),
  and [workflow](references/vendor/azure-cost/cost-optimization/workflow.md).
- Cost query:
  [dimensions by scope](references/vendor/azure-cost/cost-query/dimensions-by-scope.md),
  [error handling](references/vendor/azure-cost/cost-query/error-handling.md),
  [examples](references/vendor/azure-cost/cost-query/examples.md),
  [guardrails](references/vendor/azure-cost/cost-query/guardrails.md),
  [request body schema](references/vendor/azure-cost/cost-query/request-body-schema.md),
  and [workflow](references/vendor/azure-cost/cost-query/workflow.md).
- [Tools and practices](references/vendor/azure-cost/references/tools-and-best-practices.md)

#### Azure resource limits and quotas

- [Service resource limits and quotas](references/vendor/azure-prepare/references/resources-limits-quotas.md)
- [Quota skill overview](references/vendor/azure-quotas/SKILL.md)
- [Advanced quota commands](references/vendor/azure-quotas/references/advanced-commands.md)
- [Quota commands](references/vendor/azure-quotas/references/commands.md)
- [PowerShell quota checker](references/vendor/azure-quotas/scripts/check-quota.ps1)
- [Shell quota checker](references/vendor/azure-quotas/scripts/check-quota.sh)
- [Region availability](references/vendor/azure-validate/references/region-availability.md)

#### Microsoft Foundry model capacity

- [Deployment capacity workflow](references/vendor/microsoft-foundry/models/deploy-model/capacity/SKILL.md)
- Capacity discovery and ranking:
  [PowerShell](references/vendor/microsoft-foundry/models/deploy-model/capacity/scripts/discover_and_rank.ps1)
  and [shell](references/vendor/microsoft-foundry/models/deploy-model/capacity/scripts/discover_and_rank.sh).
- Capacity query:
  [PowerShell](references/vendor/microsoft-foundry/models/deploy-model/capacity/scripts/query_capacity.ps1)
  and [shell](references/vendor/microsoft-foundry/models/deploy-model/capacity/scripts/query_capacity.sh).
- [Quota overview](references/vendor/microsoft-foundry/quota/quota.md)
- [Capacity planning](references/vendor/microsoft-foundry/quota/references/capacity-planning.md)
- [Error resolution](references/vendor/microsoft-foundry/quota/references/error-resolution.md)
- [Optimization](references/vendor/microsoft-foundry/quota/references/optimization.md)
- [Provisioned throughput guide](references/vendor/microsoft-foundry/quota/references/ptu-guide.md)
- [Troubleshooting](references/vendor/microsoft-foundry/quota/references/troubleshooting.md)
- [Workflows](references/vendor/microsoft-foundry/quota/references/workflows.md)

### Vendored source

- Repository: [`microsoft/azure-skills`](https://github.com/microsoft/azure-skills)
- Last synced commit: [`6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae`](https://github.com/microsoft/azure-skills/commit/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae)
- Last synced date: 2026-07-19 (UTC)

The commit is a snapshot marker. Update it when the vendored content is refreshed.

| Vendored path | Upstream path |
|---|---|
| `references/vendor/azure-quotas/` | [`skills/azure-quotas/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-quotas) |
| `references/vendor/azure-cost/` | [`skills/azure-cost/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-cost) |
| `references/vendor/azure-aigateway/` | [`skills/azure-aigateway/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-aigateway) |
| `references/vendor/azure-compute/workflows/capacity-reservation/` | [`skills/azure-compute/workflows/capacity-reservation/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-compute/workflows/capacity-reservation) |
| `references/vendor/microsoft-foundry/quota/` | [`skills/microsoft-foundry/quota/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/microsoft-foundry/quota) |
| `references/vendor/microsoft-foundry/models/deploy-model/capacity/` | [`skills/microsoft-foundry/models/deploy-model/capacity/`](https://github.com/microsoft/azure-skills/tree/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/microsoft-foundry/models/deploy-model/capacity) |
| `references/vendor/azure-prepare/references/resources-limits-quotas.md` | [`skills/azure-prepare/references/resources-limits-quotas.md`](https://github.com/microsoft/azure-skills/blob/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-prepare/references/resources-limits-quotas.md) |
| `references/vendor/azure-validate/references/region-availability.md` | [`skills/azure-validate/references/region-availability.md`](https://github.com/microsoft/azure-skills/blob/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/skills/azure-validate/references/region-availability.md) |

### Known dangling cross-references

The partial copies retain upstream relative links that point outside the vendored
paths:

- `references/vendor/microsoft-foundry/models/deploy-model/capacity/SKILL.md`
  links to `../preset/SKILL.md`, `../customize/SKILL.md`, and
  `../SKILL.md#project-selection-all-modes`.
- `references/vendor/azure-prepare/references/resources-limits-quotas.md`
  refers to an `azure-provisioning-limit` skill that isn't present at the synced
  commit.

### License and attribution

The vendored content is distributed under the
[`microsoft/azure-skills` MIT License](https://github.com/microsoft/azure-skills/blob/6f4ff3f2f4f547bb3d42e2a00e72a1c47ffad5ae/LICENSE):

```text
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

## Updating vendored content

`references/vendor/` is refreshed manually, not by a script or scheduled job. To update
it:

1. For each of the eight paths in the vendored source table, re-fetch the file
   from `microsoft/azure-skills`'s `main` branch (e.g. via `gh api` or `curl` against
   `raw.githubusercontent.com/microsoft/azure-skills/main/<path>`) and overwrite the
   vendored copy byte-for-byte.
2. Verify each file with `git hash-object <file>` against the new upstream blob SHA
   (from the GitHub API for that path) to confirm an exact copy — no manual retyping or
   edits.
3. Update the last-synced commit SHA, date, and source links in this section.
4. Note files added or removed upstream within those same eight paths here. The
   target list only changes through a deliberate, separate decision, not as a side
   effect of a routine sync.
