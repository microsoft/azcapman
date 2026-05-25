<!-- T-29: RTM FR-12.1, NFR-11.2 -->
# Capacity management prompts for SRE Agent

Use these prompts to steer the SRE Agent through quota, reservation, and estate planning work. Start broad, then narrow the ask to a subscription, region, VM family, or deployment stamp, as described in [capacity planning](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning).

## Quota analysis prompts

Use these prompts when you need to inspect per-subscription and per-VM-family limits, because Azure enforces both regional and family-level vCPU quotas in each subscription and region, as described in [per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests).

| Stage | Prompt |
|---|---|
| Open-ended | "Check the quota health across our production subscriptions" |
| Direct | "Which VM families are above 80% quota utilization in East US 2?" |
| Comparison | "Compare Dv5 and Ev5 quota headroom across prod-001, prod-002, and prod-003" |
| Investigation | "Why did the latest VM deployment fail in West Europe—quota, region access, or SKU restriction?" |
| Trend | "Show the subscriptions where GPU-family quota usage grew the most this week" |
| Action | "Request a quota increase for Standard_D_v5 to 500 vCPUs in subscription prod-001" |

## Capacity reservation prompts

Use these prompts when you need to inspect or change capacity reservation coverage, because capacity reservation groups guarantee compute capacity for specific VM sizes in a region or availability zone, as described in the [capacity reservation overview](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview).

| Stage | Prompt |
|---|---|
| Open-ended | "Review our capacity reservation coverage and identify waste" |
| Direct | "What's the utilization of our CRGs in West Europe?" |
| Comparison | "Compare our quota headroom to our capacity reservation coverage for Standard_D16s_v5 across production regions" |
| Investigation | "Why did CRG sharing fail between sub-A and sub-B?" |
| What-if | "What happens to our East US 2 rollout if we size the capacity reservation group for 60 instances instead of 80?" |
| Action | "Create a capacity reservation group for Standard_D16s_v5 in East US 2, zone 1" |

## Quota group prompts

Use these prompts when you need to pool compute quota across eligible subscriptions, because quota groups are ARM resources at management group scope and each subscription can belong to only one quota group, as described in [quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups).

| Stage | Prompt |
|---|---|
| Open-ended | "Show how quota is distributed across our shared compute quota group" |
| Direct | "Which subscriptions in quota-group-prod have the least remaining Dv5 quota in East US 2?" |
| Investigation | "Why did the quota transfer from quota-group-prod to prod-004 fail?" |
| Planning | "What quota group increase should we request for East US 2 before the holiday release?" |
| Transfer | "Transfer 200 Dv5 vCPUs from prod-002 into quota-group-prod, then allocate 150 to prod-003" |
| Action | "Create a quota group under mg-platform-shared and add prod-001, prod-002, and prod-003" |

## FinOps capability prompts

Use these prompts when you want the agent to map Azure capacity evidence to FinOps capabilities. Capacity planning should connect demand forecasts to quota, reservation, and alerting decisions, as described in [capacity planning](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning), while the FinOps Foundation defines Domains and Capabilities as the outcomes and activities of the practice. [Source](https://www.finops.org/framework/domains/) [Source](https://www.finops.org/framework/capabilities/)

| Capability | Stage | Prompt |
|---|---|---|
| Planning & Estimating | Open-ended | "Estimate compute capacity for the next 90 days for our checkout stamp in East US 2" |
| Forecasting | Comparison | "Compare forecasted Dv5 demand to current quota headroom for the next release window" |
| Forecasting | What-if | "What if tenant growth lands 20% above plan in West Europe?" |
| Architecting & Workload Placement | Open-ended | "Which regions and VM families should we unblock before the Q4 rollout?" |
| Architecting & Workload Placement | Action | "List the quota increases, region-access requests, and zonal access requests we should file this month" |
| Rate Optimization | Cost | "Estimate the cost and lead-time tradeoffs between raising quota, using capacity reservations, and buying reservations for GPU burst capacity" |
| Usage Optimization | Open-ended | "Map forecasted demand to capacity reservation groups for our tier-0 services and identify unused reserved capacity" |
| Architecting & Workload Placement | What-if | "What if we shift 30% of East US 2 demand to Central US—how does that change quota and reservation coverage?" |
| Governance, Policy & Risk | Action | "Create an evidence package that pairs quota groups, capacity reservations, owners, and exceptions for our next stamp" |
| Automation, Tools & Services | Open-ended | "Create a weekly capacity evidence check that flags quota usage above 80% and reservation utilization below 60%" |
| Automation, Tools & Services | Notification | "Draft the Teams and email notifications we should send when quota pressure crosses our threshold" |
| Governance, Policy & Risk | Investigation | "Which Azure constraint blocked the failed rollout—forecast gap, quota, region access, zonal enablement, SKU availability, capacity reservation, or alert coverage?" |

## Region access and zonal enablement prompts

Use these prompts when deployment fails because a subscription can't use a region or availability zone you need, as described in the [region access request process](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process) and [zonal access request guidance](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series).

| Stage | Prompt |
|---|---|
| Open-ended | "Check which subscriptions still need region access or zonal access for our rollout regions" |
| Direct | "Can prod-001 deploy Standard_NCads_H100_v5 in East US 2 zone 1?" |
| Comparison | "Compare zone readiness for Dv5 between East US 2, Central US, and West Europe" |
| Investigation | "Why does sub-B see the zone as unavailable while sub-A can deploy?" |
| Action | "Draft the support request details we need for region access to Qatar Central and zonal access for our target VM families" |

## Notification prompts

Use these prompts when you want the agent to send a summary instead of a raw alert, because Azure SRE Agent can post HTML messages to Teams and Outlook after it investigates, as described in [Send notifications in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications).

| Stage | Prompt |
|---|---|
| Teams alert | "Post to our Teams capacity channel with the subscriptions above 80% Dv5 quota utilization" |
| Email digest | "Email the weekly capacity digest with quota pressure, reservation utilization, and next actions" |
| Thread update | "Reply to the existing Teams thread with the latest CRG sharing findings" |
| Draft | "Draft the HTML message for a quota increase recommendation before I send it" |
| Post-incident | "Send a post-incident summary to capacity-ops@contoso.com that explains the failed rollout and the follow-up actions" |

## Tips for effective capacity prompts

These prompt patterns work best when you tie the question to workload demand, supply constraints, and notification paths, as described in [capacity planning](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning) and [Send notifications in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications).

- Start with posture assessment, then drill into specific VM families or regions.
- Ask for cost implications before buying reservations or increasing quota.
- Use "what-if" framing for capacity reservation sizing decisions.
- Combine quota and reservation analysis: "Compare my quota headroom to my reservation coverage."
- Ask the agent to separate quota limits, region access, and capacity reservation issues, because those controls solve different problems.
