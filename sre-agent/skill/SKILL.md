---
name: azure-capacity-management
description: Investigate Azure quota, capacity reservations, quota groups, region access, zonal enablement, and capacity evidence for SaaS workloads.
---

# Azure capacity management

Use this skill for Azure capacity evidence in subscriptions the SaaS provider owns or controls. Treat quota, region access, zonal enablement, capacity reservations, Azure Reservations, and savings plans as separate Azure controls.

Ground Azure behavior in Microsoft Learn or command output collected in the active task. [Azure quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests), [quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups), and [capacity reservations](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview) document the related Azure resource surfaces.

Use Azure CLI and Azure Resource Graph read operations to collect current state. For a write operation, present the exact operation and wait for explicit user approval before running it.

State which subscription, region, VM family, capacity reservation group, or quota group each result covers. State missing inputs rather than filling them from assumption.

For shared capacity reservations, include the logical-to-physical availability-zone mapping consideration documented in the [availability zones overview](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview#configuring-resources-for-availability-zone-support).
