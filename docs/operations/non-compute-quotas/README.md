---
title: Non-compute quotas
parent: Capacity & quotas
nav_order: 3
---

# Non-compute quota guide

## When to use this guide

Azure capacity planning extends beyond vCPU cores. Storage accounts, App Service plans, Azure Cosmos DB accounts, and other platform services have service-specific limits and quota workflows that can block new deployments if you don't track usage and request increases ahead of demand. [Source](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests) [Source](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-app-service-limits) [Source](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase)

This guide consolidates baseline limits, monitoring patterns, and escalation paths for common non-compute services so operations teams can use one reference for quota checks, alerts, and support workflows. [Source](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting) [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)

## Service quick reference

| Service | Default scope & notable limits | How to check usage | How to request more |
| --- | --- | --- | --- |
| **Azure Storage** | [250 standard storage accounts per subscription and region (increaseable to 500)](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests); [per-account throughput and egress limits vary by SKU](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview#scalability-targets-for-standard-storage-accounts). | [`az storage account show-usage`, `Get-AzStorageUsage`](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests), or [`az quota usage list --resource-provider Microsoft.Storage`](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest). | Use [**My quotas > Storage** to submit a numeric limit](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests); [fallback to support ticket if auto-approval fails](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal). |
| **Azure App Service** | [App Service plans capped per region (10 Free/Shared, 100 per resource group for higher tiers); storage quota enforced per plan and per region/resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-app-service-limits). | [`az quota usage list --resource-provider Microsoft.Web`](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest) to export plan counts; portal usage charts per plan. | [Submit App Service quota adjustments through **My quotas > Web**; escalate via support when non-adjustable](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal). |
| **Azure SQL Database** | Regional usage is exposed on the ARM `Microsoft.Sql/locations/usages` surface, and access is controlled by `Microsoft.Sql/locations/usages/read` RBAC permission. [Source](https://learn.microsoft.com/en-us/azure/templates/microsoft.sql/locations/usages) [Source](https://learn.microsoft.com/en-us/azure/role-based-access-control/permissions/databases) | Query the location usages surface through ARM with `az rest` for estate-level checks and automation. [Source](https://learn.microsoft.com/en-us/azure/templates/microsoft.sql/locations/usages) | Use Azure support workflow when you need subscription-level assistance for limits or capacity-related blockers. [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request) |
| **Azure Cosmos DB** | [500 databases/containers per account, request throughput change limits per 5-minute window; higher limits require support review](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase). | Monitor provisioned throughput and request units in portal/metrics; track account limits manually. | [Create a support request (Quota type: Azure Cosmos DB) with workload details and desired limits](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase). |
| **Azure Database for PostgreSQL** | Regional checks can use provider location-based capability metadata exposed through documented PostgreSQL management APIs. [Source](https://learn.microsoft.com/en-us/javascript/api/@azure/arm-postgresql-flexible/locationbasedcapabilities) [Source](https://learn.microsoft.com/en-us/rest/api/postgresql/) | Use public ARM and documented API surfaces only, and validate the exact provider path in your tenant before automating checks broadly. [Source](https://learn.microsoft.com/en-us/rest/api/postgresql/) | Use the Azure support request workflow for service and subscription limit asks that need manual review. [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request) |
| **Azure SQL Managed Instance** | API details for non-compute quota and location usage checks are pending validation in this training context. Avoid speculative command guidance until validation is complete. [Source](https://learn.microsoft.com/en-us/azure/role-based-access-control/permissions/databases) | Record only validated commands in this guide. [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request) | Use support request workflow when you need limit or access review while API validation is in progress. [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request) |

If your workloads depend on other services (for example, Azure OpenAI, Dev Box, or Azure Deployment Environments), extend this guide with limits, monitoring commands, and support workflows that are documented on Microsoft Learn so teams can use one reproducible reference. [Source](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits) [Source](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal) [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)

## Azure Storage quota operations

### Key limits and dependencies

- [Each subscription can hold up to 250 standard storage accounts per region by default; increases up to 500 require approval](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).
- [Per-account scalability targets (aggregate ingress/egress, request rate, replication constraints) depend on the account kind](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview#scalability-targets-for-standard-storage-accounts). Include these constraints when forecasting storage demand.

### Usage and tooling

- Run [`az storage account show-usage --location <region>` to list the current count versus limit for storage accounts in a region](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).
- [PowerShell administrators can retrieve the same data with `Get-AzStorageUsage` for automation pipelines](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).
- Use [`az quota usage list --scope /subscriptions/<subId> --resource-provider Microsoft.Storage` to generate machine-readable quota snapshots](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest) that align with other quota reporting scripts.

### Request workflow

1. [Open **Azure portal > Quotas > Storage** and select the subscription](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).
2. [Choose the region and select the pencil icon under **Request adjustment** to enter a new limit (up to 500)](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).
3. [Submit the request; most approvals complete within minutes](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).
4. [If the request is denied or the limit is non-adjustable, use the **Create support request** link presented in **My quotas** to route the request to Microsoft support](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal).


## Azure App Service quota operations

### Key limits and dependencies

- [Free and Shared plans are limited to 10 instances per region, while Basic, Standard, Premium, and Isolated tiers allow up to 100 plans per resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-app-service-limits).
- [Storage quotas are enforced per App Service plan (10 GB Basic, 50 GB Standard, 250 GB Premium, 1 TB Isolated) and aggregated across plans within the same region/resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-app-service-limits).
- [Scale-out ceilings range from 3 instances (Basic) to 30 instances (Premium v2/v3/v4) and 100 instances (Isolated)](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-app-service-limits).

### Usage and tooling

- Use [`az quota usage list --resource-provider Microsoft.Web --scope /subscriptions/<subId>` to pull plan counts and limits for automation or dashboards](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest).
- [Review per-plan metrics (connections, storage consumption) in the App Service blade to anticipate when plan-level storage limits approach exhaustion](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-app-service-limits).

### Request workflow

1. [Navigate to **Azure portal > Quotas > Web** and locate the target region](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal).
2. [Select the relevant quota row (for example, `AppServicePlanCount`) and choose **New quota request**](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal).
3. [Enter the desired limit and submit. Azure applies the increase automatically when capacity is available](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal).
4. [If the quota is non-adjustable or the request fails, generate a support ticket from the same blade with justification and deployment timelines](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal).


## Azure Cosmos DB quota operations

### Key limits and dependencies

- [Each account supports up to 500 databases and containers combined, and provisioned throughput changes are limited to 25 updates per five-minute interval](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).
- [Azure Cosmos DB enforces additional request limits (for example, list/get keys operations) that can throttle automation if not accounted for](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).

### Request workflow

1. [From **Help + Support**, create a new support request with Issue type **Service and subscription limits (quotas)** and Quota type **Azure Cosmos DB**](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).
2. [Provide workload context, current limits, desired values, and any diagnostic artifacts requested on the Additional details tab](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).
3. [Specify severity and preferred contact, then submit. The Cosmos DB engineering team typically responds within 24 hours to confirm or gather more information](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).

[Because increases require manual approval, plan requests well ahead of large onboarding waves and track throughput usage via Azure Monitor to justify the ask](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase).

## Public API checks for SQL, Cosmos DB, and PostgreSQL

### Azure SQL Database location usages surface

- Use the ARM `Microsoft.Sql/locations/usages` resource surface as the documented location usage entry point for subscription-level checks. [Source](https://learn.microsoft.com/en-us/azure/templates/microsoft.sql/locations/usages)
- Confirm that the caller has `Microsoft.Sql/locations/usages/read` before treating a failed request as a service issue. [Source](https://learn.microsoft.com/en-us/azure/role-based-access-control/permissions/databases)

### Azure Cosmos DB regional readiness and support path

- Use `az cosmosdb locations list` and `az cosmosdb locations show` for regional capability and readiness signals before stamp placement decisions. [Source](https://learn.microsoft.com/en-us/cli/azure/cosmosdb/locations?view=azure-cli-latest)
- Use the Azure Cosmos DB quota support workflow when you need quota increases or region access enablement beyond defaults. [Source](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/create-support-request-quota-increase)

### Azure Database for PostgreSQL location usage checks

- Use provider-exposed location metadata surfaces to verify what the subscription can use in a region before provisioning or expansion. [Source](https://learn.microsoft.com/en-us/javascript/api/@azure/arm-postgresql-flexible/locationbasedcapabilities)
- Use the documented PostgreSQL management API and location capability surfaces as the reproducible entry points for regional readiness validation before provisioning or expansion. [Source](https://learn.microsoft.com/en-us/rest/api/postgresql/) [Source](https://learn.microsoft.com/en-us/javascript/api/@azure/arm-postgresql-flexible/locationbasedcapabilities)

### Azure SQL Managed Instance validation note

- API details for Azure SQL Managed Instance non-compute quota and location usage checks are pending validation in this training context, so this guide doesn't publish speculative commands. [Source](https://learn.microsoft.com/en-us/azure/role-based-access-control/permissions/databases)

## Monitoring and alerting

- [Turn on quota monitoring in the Azure portal; adjustable quotas become clickable, allowing you to open the alert rule wizard directly from **My quotas**](https://learn.microsoft.com/en-us/azure/quotas/monitoring-alerting).
- [Create usage alert rules with thresholds (for example, 70/85/95 percent) and severity levels aligned to escalation procedures](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting).
- [Integrate alerts with cost monitoring by configuring budget alerts for the same subscriptions, ensuring cost anomalies and quota exhaustion trigger complementary notifications](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending).

## Extend this guide

When you add another service to this guide, document these technical elements so checks remain reproducible and support-ready ([Azure subscription and service limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits), [How to monitor quotas and generate alerts](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting), [Create an Azure support request](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)):

- Default limits and any preview restrictions. [Source](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits)
- CLI, PowerShell, or REST commands to retrieve usage. [Source](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest) [Source](https://learn.microsoft.com/en-us/rest/api/postgresql/)
- The portal or support path required for increases. [Source](https://learn.microsoft.com/en-us/azure/quotas/quickstart-increase-quota-portal) [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)
- Monitoring hooks and escalation thresholds. [Source](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting) [Source](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending)

## Reproducibility policy for this guide

- Use only publicly documented APIs, documented CLI command groups, and documented support procedures in this guide. [Source](https://learn.microsoft.com/en-us/cli/azure/cosmosdb/locations?view=azure-cli-latest) [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request)
- If a command or endpoint isn't validated by public documentation in this context, document it as pending validation rather than publishing a speculative procedure. [Source](https://learn.microsoft.com/en-us/azure/azure-portal/supportability/how-to-create-azure-support-request) [Source](https://learn.microsoft.com/en-us/rest/api/postgresql/)
