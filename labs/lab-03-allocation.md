# Lab 3: Allocation

Quota groups pool compute quota across EA/MCA subscriptions at management group scope. This lab walks you through auditing current quota posture, detecting offer restrictions, mapping availability zones, creating quota groups, transferring quota between subscriptions, and requesting increases.

## Prerequisites

- PowerShell 7+ with [Az.Compute](https://learn.microsoft.com/en-us/powershell/module/az.compute/), [Az.Quota](https://learn.microsoft.com/en-us/powershell/module/az.quota/), and Az.Accounts modules installed
- [Azure CLI 2.60.0+](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest) with the `quota` extension
- Access to the `/azcapman/scripts/quota/` directory
- Enterprise Agreement or Microsoft Customer Agreement with two or more subscriptions
- Contributor or Owner role on subscriptions and management group

## Exercise 1: Audit current quota posture

Quota includes both allocated and deallocated VMs. Before creating or modifying quota groups, understand what you're working with. See [per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests) for how Azure tracks VM-family quota usage.

### Run multi-threaded quota analysis

Open PowerShell and go to your scripts directory.

```powershell
.\Get-AzVMQuotaUsage.ps1 `
  -SubscriptionIds @("<subscription-id-1>", "<subscription-id-2>", "<subscription-id-3>") `
  -Locations @("eastus", "westus2", "northeurope") `
  -SKUs @("Standard_D2s_v3", "Standard_D4s_v3", "Standard_E2s_v3") `
  -Threads 4
```

Output is a CSV with columns: TenantId, SubscriptionId, Location, Family, Size, RegionRestricted, ZonesPresent, ZonesRestricted, CoresUsed, CoresTotal.

### Interpret the results

- **CoresUsed**: vCPU count allocated (running VMs) plus deallocated VMs that still hold quota
- **CoresTotal**: quota limit in the region
- **RegionRestricted**: true if the SKU is region-locked and requires a support request to unlock
- **ZonesPresent**: true if the region has availability zones
- **ZonesRestricted**: true if the SKU is restricted to certain zones

If `CoresUsed` approaches `CoresTotal`, you need a quota increase or must deallocate VMs.

For single-threaded execution in smaller environments:

```powershell
.\Show-AzVMQuotaReport.ps1 -SubscriptionIds @("<subscription-id-1>")
```

## Exercise 2: Detect offer restrictions and zone access

Quota limits are separate from offer restrictions. A SKU may be available but restricted to a region or zone.

### List available SKUs and their restrictions

```powershell
Get-AzComputeResourceSku | Where-Object { $_.ResourceType -eq 'virtualMachines' } | `
  Select-Object Name, Locations, Restrictions | `
  Export-Csv -Path skus.csv -NoTypeInformation
```

### Filter for regional restrictions

```powershell
Get-AzComputeResourceSku | Where-Object { $_.ResourceType -eq 'virtualMachines' } | `
  Where-Object { $_.Restrictions.Count -gt 0 } | `
  ForEach-Object {
    $sku = $_
    $sku.Restrictions | Where-Object { $_.ReasonCode -eq 'RegionRestricted' } | `
      ForEach-Object {
        [PSCustomObject]@{
          SKU = $sku.Name
          Location = $_.RestrictedLocations[0]
          ReasonCode = $_.ReasonCode
        }
      }
  } | `
  Export-Csv -Path region-restricted-skus.csv -NoTypeInformation
```

The `RegionRestricted` output from Exercise 1 aligns with this. If a SKU is region-restricted, you must request region access via a support ticket. See [region access request process](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process).

### Filter for zonal restrictions

```powershell
Get-AzComputeResourceSku | Where-Object { $_.ResourceType -eq 'virtualMachines' } | `
  Where-Object { $_.Restrictions.Count -gt 0 } | `
  ForEach-Object {
    $sku = $_
    $sku.Restrictions | Where-Object { $_.ReasonCode -eq 'NotAvailableForSubscription' } | `
      ForEach-Object {
        [PSCustomObject]@{
          SKU = $sku.Name
          ReasonCode = $_.ReasonCode
        }
      }
  } | `
  Export-Csv -Path zonal-restricted-skus.csv -NoTypeInformation
```

Zonal restrictions require a separate support request. See [zonal enablement request for restricted VM series](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series).

## Exercise 3: Map logical-to-physical availability zones

Logical zone numbering is subscription-specific. Zone 1 in one subscription may map to a different physical data center than Zone 1 in another subscription. For multi-subscription deployments, this matters.

### Run the mapping script

```powershell
.\Get-AzAvailabilityZoneMapping.ps1 `
  -SubscriptionIds @("<subscription-id-1>", "<subscription-id-2>") `
  -OutputFile zone-mapping.csv
```

Output is a CSV with columns: TenantId, SubscriptionId, Location, LogicalZone, PhysicalZone, PhysicalZoneName.

### Interpret zone alignment

```powershell
Import-Csv zone-mapping.csv | Group-Object -Property Location | `
  ForEach-Object {
    Write-Host "Location: $($_.Name)"
    $_.Group | Select-Object LogicalZone, PhysicalZone, SubscriptionId
  }
```

If your subscriptions have the same physical zone names for the same logical zones, zone-aligned deployments across subscriptions work correctly. If they differ, you must account for the misalignment in your infrastructure-as-code.

See [availability zone overview](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview) for details on zone mapping.

## Exercise 3b: Understand policy limitations for capacity

Azure Policy restricts where teams deploy, but it doesn't grant access or manage quotas.

### What Azure Policy can do

- Restrict deployments to allowed regions only
- Restrict deployments to allowed SKUs only
- Prevent deployments in certain availability zones
- Audit non-compliant resources and require remediation

### What Azure Policy cannot do

- Grant region access if the subscription is region-restricted
- Manage quotas or allocate cores
- Guarantee capacity is available for a deployment
- Substitute for quota management

### Use policy with quota groups together

Policy is a governance layer; quotas are an allocation layer. They work best together:

- **Policy** restricts which regions and SKUs teams can use
- **Quota groups** allocate cores across subscriptions and regulate total capacity

Don't use policy as a substitute for quota management. If you restrict deployments to eastus via policy, but the subscription has zero eastus quota, policy will prevent the deployment anyway—but for the wrong reason. The subscription hits the quota limit, not the policy rule.

For a quota-aware governance strategy: configure policy to align with your allocation boundaries, then use quota transfers and alerts to manage headroom.

See [Azure Policy overview](https://learn.microsoft.com/en-us/azure/governance/policy/overview) for policy architecture and built-in definitions.

## Exercise 4: Create and configure a quota group

A quota group is an ARM object at management group scope. It pools compute quota across subscriptions. Each subscription can belong to only one quota group at a time.

### Prerequisites for quota groups

- Register the `Microsoft.Quota` and `Microsoft.Compute` [resource providers](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types) on each member subscription before adding it to the group
- All subscriptions must be under the same management group
- All subscriptions must be EA or MCA offers
- No subscription can belong to more than one quota group

To register the required resource providers:

```bash
az provider register --namespace Microsoft.Quota --subscription <subscription-id>
az provider register --namespace Microsoft.Compute --subscription <subscription-id>
```

See [quota groups overview](https://learn.microsoft.com/en-us/azure/quotas/quota-groups) for the full set of prerequisites.

### Create a quota group in the portal

1. Open the [Azure portal](https://portal.azure.com)
2. Go to **Management groups**
3. Select your management group
4. On the left, select **Quotas**
5. Select **Quota groups**
6. Select **Create quota group**
7. Enter a name, for example `prod-compute-pool`
8. Select **Create**

### Create a quota group via REST

```bash
az rest --method put \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/{quotaGroupName}?api-version=2025-03-01" \
  --body '{
    "properties": {
      "displayName": "Production compute quota pool"
    }
  }'
```

Replace `{managementGroupId}` and `{quotaGroupName}` with your values. Quota groups are ARM objects at management group scope—they don't belong to individual subscriptions. See [create quota groups](https://learn.microsoft.com/en-us/azure/quotas/create-quota-groups).

### Add subscriptions to the quota group

In the portal:

1. Open the quota group
2. Select **Subscriptions**
3. Select **Add subscription**
4. Choose your subscriptions
5. Select **Add**

Via REST API:

```bash
az rest --method put \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/{quotaGroupName}/subscriptions/{subscriptionId}?api-version=2025-03-01"
```

Repeat for each subscription. A subscription can belong to only one quota group at a time.

See [add or remove subscriptions from a quota group](https://learn.microsoft.com/en-us/azure/quotas/add-remove-subscriptions-quota-group) and [create quota groups](https://learn.microsoft.com/en-us/azure/quotas/create-quota-groups).

## Exercise 4b: Validate quota group scope boundaries

Quota groups are ARM resources created at management group scope, but they operate independently of the hierarchy.

### Subscription membership is explicit, not inherited

When you add a subscription to a quota group, you're registering it explicitly. Membership isn't inherited from the management group:

- If you have a management group hierarchy like `/root/prod/eastus`, and you create a quota group at `/root`, you must add subscriptions one by one.
- Adding a management group as a member to a quota group doesn't automatically add child subscriptions.
- You must enumerate and add each subscription individually.

### Cross-hierarchy quota groups

Subscriptions from different management groups can belong to the same quota group—there's no requirement that they share a common parent. The quota group treats them as a flat collection of subscription IDs:

```bash
# All three subscriptions in one quota group, regardless of hierarchy
# Repeat for each subscription:
az rest --method put \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/prod-compute-pool/subscriptions/sub-in-prod-hierarchy?api-version=2025-03-01"

az rest --method put \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/prod-compute-pool/subscriptions/sub-in-dev-hierarchy?api-version=2025-03-01"

az rest --method put \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/prod-compute-pool/subscriptions/sub-in-isolated-tree?api-version=2025-03-01"
```

### Key caveat: management group members don't cascade

If you have:

```
/root
  /prod
    /us-east (contains sub1, sub2)
    /us-west (contains sub3)
```

And you add `/root/prod` as a member to the quota group, only `/root/prod` is registered as a member—not its children. To include `sub1`, `sub2`, and `sub3`, you must add each one explicitly.

For quota group automation, enumerate subscriptions by ARM API before adding them:

```bash
# Enumerate subscriptions and add each to the quota group
for SUB_ID in $(az account management-group entities list \
  --groupname prod \
  --query "[?type=='Microsoft.Management/managementGroups/subscriptions'].name" \
  -o tsv); do
  az rest --method put \
    --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/prod/providers/Microsoft.Quota/groupQuotas/prod-compute-pool/subscriptions/$SUB_ID?api-version=2025-03-01"
done
```

See [add or remove subscriptions from a quota group](https://learn.microsoft.com/en-us/azure/quotas/add-remove-subscriptions-quota-group) for details on membership validation and bulk operations.

## Exercise 5: Transfer quota between subscriptions

Once subscriptions are in a quota group, you can reallocate quota between them using the [quota group transfer REST API](https://learn.microsoft.com/en-us/azure/quotas/transfer-quota-groups) without requesting a limit increase. The group's total quota stays the same—you're shifting allocation from one member subscription to another through the group pool.

### Step 1: Deallocate quota from the source subscription to the group pool

Return quota from the source subscription back to the group pool. This doesn't affect running VMs—it reduces the subscription's allocation ceiling.

```bash
az rest --method patch \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/{quotaGroupName}/subscriptionQuotaAllocations/{resourceName}?api-version=2025-03-01" \
  --body '{
    "properties": {
      "subscriptionId": "<source-subscription-id>",
      "limit": <new-lower-limit>
    }
  }'
```

For example, if the source subscription has 200 D-series cores allocated and you want to release 50, set `limit` to 150. The 50 cores return to the group pool.

### Step 2: Allocate quota from the group pool to the target subscription

Assign the freed quota from the group pool to the target subscription:

```bash
az rest --method patch \
  --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/{quotaGroupName}/subscriptionQuotaAllocations/{resourceName}?api-version=2025-03-01" \
  --body '{
    "properties": {
      "subscriptionId": "<target-subscription-id>",
      "limit": <new-higher-limit>
    }
  }'
```

If the target subscription had 100 D-series cores and you're adding 50, set `limit` to 150.

### Step 3: Verify the allocation snapshot

Confirm the transfer by checking quota usage on both subscriptions:

```bash
az quota usage list \
  --scope /subscriptions/<source-subscription-id>/providers/Microsoft.Compute/locations/eastus \
  --output table

az quota usage list \
  --scope /subscriptions/<target-subscription-id>/providers/Microsoft.Compute/locations/eastus \
  --output table
```

The source subscription's limit should reflect the reduced allocation and the target subscription's limit should reflect the increased allocation. The group's total remains constant. See [transfer quota within a quota group](https://learn.microsoft.com/en-us/azure/quotas/transfer-quota-groups).

## Exercise 6: Request quota increases

### Request a per-VM quota increase

If you need more cores for a specific SKU in a specific region:

```bash
az quota create \
  --resource-name "Standard_D2s_v3/cores" \
  --scope "/subscriptions/<subscription-id-1>" \
  --display-name "D2s_v3 cores in eastus" \
  --definition '{"value": 100}'
```

This creates a request (not an automatic increase). Support will review and approve or deny it. See [per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests).

### Request a quota group limit increase

To increase the total quota across all subscriptions in a quota group:

```bash
az quota create \
  --resource-name "total_regional_cores" \
  --scope "/providers/Microsoft.Management/managementGroups/{managementGroupId}" \
  --display-name "Total cores for prod-compute-pool" \
  --definition '{"value": 1000}'
```

Support reviews quota group increase requests separately. See [quota group limit increase](https://learn.microsoft.com/en-us/azure/quotas/quota-group-limit-increase).

### Regional quota requests

If you need quota in a region you don't currently have access to, you may need a regional quota request:

```bash
az quota create \
  --resource-name "cores" \
  --scope "/subscriptions/<subscription-id-1>/providers/Microsoft.Compute/locations/japaneast" \
  --display-name "Cores in japaneast" \
  --definition '{"value": 100}'
```

See [regional quota requests](https://learn.microsoft.com/en-us/azure/quotas/regional-quota-requests).

## Exercise 7: Check non-compute quotas

Quota groups only handle compute (VM cores). Storage and App Service have separate quotas.

### Storage account quotas

Default: 250 storage accounts per region per subscription.

```bash
az quota usage list \
  --scope /subscriptions/<subscription-id-1> \
  --filter "properties/resourceType eq 'storageAccounts'" \
  --output table
```

Request a storage account quota increase:

```bash
az quota create \
  --resource-name "storageAccounts" \
  --scope "/subscriptions/<subscription-id-1>/providers/Microsoft.Storage/locations/eastus" \
  --display-name "Storage accounts in eastus" \
  --definition '{"value": 500}'
```

See [storage account quota requests](https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests).

### App Service quotas

Default: 10 App Service plans per subscription per region.

```bash
az quota usage list \
  --scope /subscriptions/<subscription-id-1> \
  --filter "properties/resourceType eq 'appServicePlans'" \
  --output table
```

Request an App Service quota increase via the portal or support ticket—CLI support varies by quota type. See [VM quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas) for the full list of quota types.

### Azure Database for PostgreSQL quotas

Default: 20 flexible servers per subscription per region. vCore limits vary by compute tier.

```bash
az quota usage list \
  --scope /subscriptions/<subscription-id>/providers/Microsoft.DBforPostgreSQL/locations/eastus \
  --output table
```

Request increases through the portal or a support ticket. See [Azure Database for PostgreSQL limits](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-limits).

### Azure Database for MySQL quotas

Default: 20 flexible servers per subscription per region. vCore limits depend on the selected service tier.

```bash
az quota usage list \
  --scope /subscriptions/<subscription-id>/providers/Microsoft.DBforMySQL/locations/eastus \
  --output table
```

Request increases through the portal or a support ticket. See [Azure Database for MySQL limits](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-limitations).

### Azure SQL Managed Instance quotas

SQL Managed Instance uses vCore-based quotas per subscription per region and requires a [dedicated subnet](https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/connectivity-architecture-overview). Default regional vCore limits vary by subscription type.

```bash
az sql mi list --subscription <subscription-id> --output table
```

To check or increase vCore limits, open a support request in the portal under **SQL Managed Instance** > **Quota**. See [Azure SQL Managed Instance resource limits](https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/resource-limits).

### Azure Service Bus quotas

Default: 100 namespaces per subscription. Messaging unit limits depend on the tier (Basic, Standard, or Premium).

```bash
az servicebus namespace list --subscription <subscription-id> --output table
```

Request namespace quota increases through the portal or a support ticket. See [Service Bus quotas](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).

### Azure Key Vault quotas

Key Vault enforces [transaction limits](https://learn.microsoft.com/en-us/azure/key-vault/general/service-limits) per vault and per subscription. Default: 5,000 transactions per 10 seconds per vault for standard tier.

```bash
az keyvault list --subscription <subscription-id> --output table
```

Transaction throttling is automatic—you can't request a limit increase. To scale, distribute keys and secrets across multiple vaults. See [Key Vault service limits](https://learn.microsoft.com/en-us/azure/key-vault/general/service-limits).

### Azure Event Hubs quotas

Default: 100 namespaces per subscription. Throughput unit limits depend on the tier (Basic, Standard, or Premium/Dedicated).

```bash
az eventhubs namespace list --subscription <subscription-id> --output table
```

Request namespace or throughput unit quota increases through the portal or a support ticket. See [Event Hubs quotas and limits](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas).

## Exercise 7b: Pre-deployment stamp readiness checklist

A "stamp" is a deployment unit—a set of resources (VMs, storage, and networking) in a specific subscription and region. Before deploying a new stamp, validate that your quota, region access, zone access, and alerting are configured. Use this checklist as a deployment gate.

### The five-check readiness gate

Before deploying a new stamp to a target subscription and region, validate all five checks. If any check fails, block the deployment and resolve the issue first.

1. **Region access approved for target subscription?**
   - Is the target subscription authorized to deploy in this region?
   - Check: run `Get-AzVMQuotaUsage.ps1` for the region. If `RegionRestricted` is true, file a region access request.
   - See [region access request process](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process).

2. **Zone access approved for target VM series?**
   - Is the target VM series available in the required zones?
   - Check: run `Get-AzComputeResourceSku` and filter for zonal restrictions. If the target SKU has `ReasonCode = NotAvailableForSubscription`, file a zonal enablement request.
   - See [zonal enablement request for restricted VM series](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series).

3. **Quota headroom sufficient for scale unit requirement?**
   - Does the subscription have enough quota to deploy the stamp?
   - Check: calculate vCPU requirement for the stamp (e.g., 10 D2s_v3 VMs = 20 cores). Verify both regional quota and per-family quota have headroom.
   - Buffer rule: keep at least 20% headroom above the scale unit requirement. If the stamp needs 20 cores and current usage is 70 cores with a 100-core limit, you have 30 cores available—only 10 cores beyond the requirement. Request a quota increase before deployment.

4. **Alert coverage configured for target subscription and region?**
   - Are quota alerts enabled for the target subscription and region?
   - Check: verify that the subscription is registered for quota alerts in the Azure portal under **Management groups** > **Quotas** > **Alerts**.
   - If alerts aren't configured, configure them before deployment. Quota monitoring is a readiness criterion—no alerts means no visibility into capacity.

5. **Subscription assigned to appropriate quota group?**
   - Is the subscription already in a quota group? If yes, is it the correct one?
   - Check: use `az rest --method get --url "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupId}/providers/Microsoft.Quota/groupQuotas/{quotaGroupName}/subscriptions?api-version=2025-03-01"` to list subscriptions in a quota group. Verify the target subscription appears and that the group's total allocation supports the stamp deployment.
   - If the subscription isn't in a quota group yet, decide whether it should be pooled with others, then add it before deployment.

### Deployment gate workflow

```
Pre-deployment check
  ├─ Check 1: region access
  │   └─ If fail: file support request, retry after approval
  ├─ Check 2: zone access
  │   └─ If fail: file support request, retry after approval
  ├─ Check 3: quota headroom
  │   └─ If fail: request quota increase, retry after approval
  ├─ Check 4: alert coverage
  │   └─ If fail: configure alerts, retry after setup
  └─ Check 5: quota group membership
      └─ If fail: add subscription to quota group or verify correct group, retry after change

  All checks pass: deploy stamp
  Any check fails: block deployment, return remediation action
```

Implement this gate in your infrastructure-as-code validation layer. For example, a Terraform module could fail plan with a clear error message if any check fails.

See [quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups) for quota group membership queries.

## Wrap-up: quota and procurement

Quota data feeds directly into procurement decisions:

1. Audit current usage (Exercise 1) to know your baseline
2. Detect restrictions (Exercise 2) to understand what requires support requests
3. Map zones (Exercise 3) to validate multi-subscription zone alignment
4. Understand policy limitations (Exercise 3b) and use them with quota groups
5. Create quota groups (Exercise 4) to pool compute quota across subscriptions
6. Validate quota group scope boundaries (Exercise 4b) for cross-hierarchy memberships
7. Transfer quota (Exercise 5) to reallocate without requesting increases
8. Request increases (Exercise 6) when you hit limits
9. Check non-compute quotas (Exercise 7) for storage, App Service, database, messaging, and key management planning
10. Validate stamp readiness (Exercise 7b) before deploying new capacity

These outputs directly inform:

- **Capacity planning**: how many cores you need and in which regions
- **Cost modeling**: quota limits affect how many VMs you can run, which drives reserved instance sizing
- **Risk mitigation**: knowing what's restricted (region, zone, SKU) prevents deployment surprises
- **Multi-subscription strategy**: quota groups centralize allocation decisions across subscriptions
- **Deployment gates**: the readiness checklist prevents under-provisioned or over-quota deployments

### Two critical distinctions

**Quota transfers don't change enforcement.** When you move cores from one subscription to another within a quota group, you're changing the allocation—how many cores that subscription can use. ARM still validates quota at the subscription scope. If the target subscription receives 50 cores for D-series VMs, but a deployment requests 60 cores, ARM rejects it. The quota group shifted allocation, not enforcement.

**Alert coverage is a readiness criterion.** Many teams configure quotas but skip alerts. If you don't have quota monitoring enabled for a subscription and region, you won't see capacity constraints until a deployment fails. Treat alert setup as a gate: no alerts means the stamp isn't ready for traffic.

See the [quota groups overview](https://learn.microsoft.com/en-us/azure/quotas/quota-groups) and [az quota CLI reference](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest) for more detail.
