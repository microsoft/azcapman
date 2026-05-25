---
title: Support escalation
parent: Support & reference
nav_order: 1
---

# Support escalation guide

Self-service quota tooling handles adjustable quota requests, and some capacity problems still require Microsoft intervention through a support request ([Increase quota in Azure portal](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal), [Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)). Use this guide to recognize when escalation is necessary and how to submit a support ticket with the required context so you don't lose time gathering details after the ticket opens.

## When to escalate

- **Restricted regions or zones:** Subscriptions cannot deploy to a region or zone because of [access restrictions](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process) that only Microsoft can lift.
- **Non-adjustable quotas:** The **My quotas** blade flags the target quota as [non-adjustable](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal) or the automated request is denied.
- **Service-specific limits:** Services such as Azure Cosmos DB require engineering review to raise [account/container limits or throughput ceilings](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).
- **Capacity reservation incidents:** [Capacity reservations](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview) don't behave as expected for reserved quantity, VM association, or deployment outcomes, and need Microsoft investigation through the support request path.

## Pre-submission checklist

- Confirm you have Owner, Contributor, or Support Request Contributor rights on the subscription; without appropriate RBAC the portal blocks [ticket creation](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request).

## Creating the request

1. Open the Azure portal, select the **?** icon, and choose [**Create a support request**](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request).
2. On the **Problem description** tab, select [**Service and subscription limits (quotas)**](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request), choose the subscription, and pick the relevant quota type (for example, `Compute-VM (cores-vCPUs)`, [`Azure Cosmos DB`](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase), or `Microsoft Fabric`).
3. Provide detailed [problem statements](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process), including region, VM series, desired quota value, and [deployment blockers](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).
4. Attach [supporting files](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request) (screenshots, export logs) and specify severity and preferred contact method.
5. Submit and capture the support request ID for tracking ([Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)).

## Required technical evidence package

Include this data in the support request and in any follow-on escalation package:

- Support request ID, subscription ID, tenant ID, region, availability zone (if relevant), and workload stamp identifier ([Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)).
- Quota target details: provider namespace, quota name (for example VM family), current limit, current usage, requested limit, and requested effective date ([Per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests), [Quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups)).
- Reproduction details: exact deployment operation, expected result, actual result, correlation IDs, UTC timestamps, and error payloads ([Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)).
- Capacity reservation details when applicable: capacity reservation group, reservation SKU, zone scope, reserved quantity, associated VM or VMSS resource IDs, and failure symptoms ([Capacity reservation overview](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview)).
- Impact statement: affected subscriptions, regions, SKUs, blocked release or scale event, and quantified demand window (vCPU, VM instances, or service throughput) ([Manage your workload supply chain](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/workload-supply-chain)).
- Attachments: screenshots, activity log exports, deployment logs, and CLI output that matches the reported timeframe ([Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)).

## Escalation path on Azure surfaces

- Start with an Azure support request under the relevant quota or service surface ([Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)).
- Validate support outcomes when access or quota changes are applied, including region access, zonal enablement, quota limits, and reservation behavior ([Region access request process](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process), [Zonal enablement request for restricted VM series](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series), [Per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests), [Capacity reservation overview](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview)).
- Escalate internally only with the same SR-linked technical evidence package so Microsoft support and internal incident systems reference the same facts ([Manage your workload supply chain](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/workload-supply-chain)).

## Region and zone access workflow

- When requesting region or zone enablement ([Region access request process](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process), [Zonal enablement request for restricted VM series](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series)), list all regions, VM series, and logical zones required for upcoming deployments within the ticket.
- Reference [prior approvals](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process) if recycling subscriptions so Microsoft can reconnect previously granted access.
