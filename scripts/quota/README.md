---
title: Quota Management
---

# Quota management scripts

These scripts are intended to analyze quota usage across subscriptions and regions in scenarios where Quota Groups **have not** been implemented.

> [!TIP]
> Use these scripts alongside Azure quota and availability zone guidance so your analysis matches the way Azure enforces vCPU and zone limits.[^vm-quotas][^az-zones][^az-quota]

---

## What you'll need

Choose the authentication path that matches your toolchain.

**Option A: Azure PowerShell module**

1. **Azure PowerShell module**: Install the latest version ([Az module reference](https://learn.microsoft.com/en-us/powershell/azure/))
   ```powershell
   Install-Module -Name Az -Repository PSGallery -Force
   ```

2. **Authentication**: Sign in to your Azure account
   ```powershell
   Connect-AzAccount
   ```

3. **Permissions**: Reader access to target subscriptions

4. **PowerShell version**: PowerShell 7+ for multi-threading; PowerShell 5.1+ for single-threaded scripts

**Option B: Azure CLI**

1. **Azure CLI**: Install the Azure CLI if you haven't already ([Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli))
   ```bash
   # See https://learn.microsoft.com/en-us/cli/azure/install-azure-cli for platform-specific instructions
   ```

2. **Authentication**: Sign in to your Azure account
   ```bash
   az login
   ```

3. **Permissions**: Reader access to target subscriptions

4. **PowerShell version**: PowerShell 7+ for multi-threading

---

## Available scripts

### Get-AzVMQuotaUsage.ps1 (Recommended)

**Multi-threaded quota analysis** - Fast parallel processing across multiple subscriptions.

**Requirements**: Azure PowerShell module, PowerShell 7+ for multi-threading
**Best for**: Large-scale analysis

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/microsoft/azcapman/main/scripts/quota/Get-AzVMQuotaUsage.ps1" -OutFile "Get-AzVMQuotaUsage.ps1"
.\Get-AzVMQuotaUsage.ps1 -SKUs @('Standard_D2s_v5', 'Standard_E2s_v5') -Locations @('eastus', 'westus2') -Threads 4
```

What you'll get:
- Current quota usage vs. limits for VM families
- Available and restricted availability zones per SKU
- Region-level restrictions for specific VM SKUs
- Physical vs. logical availability zone mappings
- Multi-threading for faster processing

**Script Output:**

|TenantId|SubscriptionId|SubscriptionName|Location|Family|Size|RegionRestricted|ZonesPresent|ZonesRestricted|CoresUsed|CoresTotal|
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
|...|...|...|eastus|standardDSv5Family|Standard_D2s_v5|False|1,2,3||0|100|
|...|...|...|westus2|standardESv5Family|Standard_E2s_v5|False|1,2,3||0|100|
|...|...|...|westus3|standardFSv2Family|Standard_F2s_v2|True|1,2,3|1,2,3|0|100|

**What each column means:**
- **TenantId**: Your Microsoft Entra tenant ID
- **SubscriptionId**: Your subscription ID
- **SubscriptionName**: Friendly name you've given your subscription
- **Location**: Azure region name
- **Family**: VM family (used for quota calculations)
- **Size**: Specific VM SKU name
- **RegionRestricted**: Whether the SKU has regional restrictions
- **ZonesPresent**: Available availability zones for the SKU
- **ZonesRestricted**: Restricted availability zones for the SKU
- **CoresUsed**: vCPU cores you're currently using
- **CoresTotal**: Total vCPU cores available to you

---

### Get-AzVMQuotaUsageCli.ps1 (Azure CLI variant)

**Multi-threaded quota analysis using Azure CLI**—covers the same subscriptions, regions, and output columns as `Get-AzVMQuotaUsage.ps1` but calls `az` commands instead of Azure PowerShell cmdlets.

**Requirements**: [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli), PowerShell 7+ for multi-threading
**Best for**: Teams that prefer Azure CLI or don't have the Az PowerShell module installed

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/microsoft/azcapman/main/scripts/quota/Get-AzVMQuotaUsageCli.ps1" -OutFile "Get-AzVMQuotaUsageCli.ps1"
.\Get-AzVMQuotaUsageCli.ps1 -SKUs @('Standard_D2s_v5', 'Standard_E2s_v5') -Locations @('eastus', 'westus2') -Threads 4
```

What you'll get:
- Current quota usage vs. limits for VM families
- Available and restricted availability zones per SKU
- Region-level restrictions for specific VM SKUs
- Physical vs. logical availability zone mappings
- Multi-threading for faster processing

**Script output:**

|TenantId|SubscriptionId|SubscriptionName|Location|Family|Size|RegionRestricted|ZonesPresent|ZonesRestricted|CoresUsed|CoresTotal|
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
|...|...|...|eastus|standardDSv5Family|Standard_D2s_v5|False|1,2,3||0|100|
|...|...|...|westus2|standardESv5Family|Standard_E2s_v5|False|1,2,3||0|100|
|...|...|...|westus3|standardFSv2Family|Standard_F2s_v2|True|1,2,3|1,2,3|0|100|

**What each column means:**
- **TenantId**: Your Microsoft Entra tenant ID
- **SubscriptionId**: Your subscription ID
- **SubscriptionName**: Friendly name you've given your subscription
- **Location**: Azure region name
- **Family**: VM family (used for quota calculations)
- **Size**: Specific VM SKU name
- **RegionRestricted**: Whether the SKU has regional restrictions
- **ZonesPresent**: Available availability zones for the SKU
- **ZonesRestricted**: Restricted availability zones for the SKU
- **CoresUsed**: vCPU cores you're currently using
- **CoresTotal**: Total vCPU cores available to you

---

### Show-AzVMQuotaReport.ps1 (Single-threaded)
**Simple quota analysis** - Single-threaded version for smaller projects.

**Requirements**: Azure PowerShell module, PowerShell 5.1+
**Best for**: Smaller analysis or learning

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/microsoft/azcapman/main/scripts/quota/Show-AzVMQuotaReport.ps1" -OutFile "Show-AzVMQuotaReport.ps1"
.\Show-AzVMQuotaReport.ps1 -SKUs @('Standard_D2s_v5', 'Standard_E2s_v5') -Locations @('eastus', 'westus2')
```

This script provides:
- Sequential processing across subscriptions
- Formatted table display of results
- Same core functionality as the multi-threaded version
- Streamlined for educational purposes

**Script Output:**

|TenantId|SubscriptionId|SubscriptionName|Location|Family|Size|RegionRestricted|ZonesPresent|ZonesRestricted|CoresUsed|CoresTotal|
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
|...|...|...|eastus|standardDSv5Family|Standard_D2s_v5|False|1,2,3||0|100|
|...|...|...|westus2|standardESv5Family|Standard_E2s_v5|False|1,2,3||0|100|
|...|...|...|westus3|standardFSv2Family|Standard_F2s_v2|True|1,2,3|1,2,3|0|100|

---

### Get-AzAvailabilityZoneMapping.ps1 (Zone Analysis)
**Zone mapping analysis** - Shows how logical zones map to physical zones across subscriptions.

**Requirements**: Azure PowerShell module, Reader access to target subscriptions
**Best for**: Cross-subscription deployment planning

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/microsoft/azcapman/main/scripts/quota/Get-AzAvailabilityZoneMapping.ps1" -OutFile "Get-AzAvailabilityZoneMapping.ps1"
.\Get-AzAvailabilityZoneMapping.ps1 -SubscriptionIds @('sub1-id','sub2-id') -OutputFile "ZoneMappings.csv"
```

This script provides:
- Logical to physical zone mappings per subscription
- Physical zone identifiers and names
- Essential data for multi-subscription architectures
- Compliance with data residency requirements

**Script Output:**

|TenantId|SubscriptionId|SubscriptionName|Location|LogicalZone|PhysicalZone|PhysicalZoneName|
|--------|--------|--------|--------|--------|--------|--------|
|...|...|...|eastus|1|A|eastus-az1|
|...|...|...|eastus|2|B|eastus-az2|
|...|...|...|eastus|3|C|eastus-az3|

---

## Manual quota analysis examples

### Check your current quota

```powershell
$Location = 'West US 2'
$VMSize = 'Standard_D4d_v4'
$SKU = Get-AzComputeResourceSku -Location $Location | Where-Object ResourceType -eq "virtualMachines" | Select-Object Name,Family
$VMFamily = ($SKU | Where-Object Name -eq $VMSize | Select-Object -Property Family).Family
$Usage = Get-AzVMUsage -Location $Location | Where-Object { $_.Name.Value -eq $VMFamily }
```

---

## Script parameters

### Common parameters (all scripts)

- **SKUs**: Array of VM SKU names to analyze (e.g., `@('Standard_D2s_v5', 'Standard_E4s_v5')`)
- **Locations**: Array of Azure regions (e.g., `@('eastus', 'westus2')`)
- **SubscriptionIds**: Array of subscription IDs to analyze
- **OutputFile**: Name of the output CSV file

---

### Get-AzVMQuotaUsage.ps1 specific parameters

- **Threads**: Number of concurrent threads (default: 2, set to 0 for auto-detect)
- **UsePhysicalZones**: Switch to normalize output to physical zones
- **MeterDataUri**: URL for downloading VM SKU list

### Get-AzVMQuotaUsageCli.ps1 specific parameters

`Get-AzVMQuotaUsageCli.ps1` shares the same parameters as `Get-AzVMQuotaUsage.ps1`—including `SKUs`, `Locations`, `SubscriptionIds`, `Threads`, `UsePhysicalZones`, `MeterDataUri`, and `OutputFile`. The only difference is the backend: this script calls [`az rest`](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-rest) and [`az account`](https://learn.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest) instead of Azure PowerShell cmdlets.

---

### Get-AzAvailabilityZoneMapping.ps1 Specific Parameters

- **OutputFile**: Default filename is "ZonePeers.csv"

You'll need Azure PowerShell installed and signed in to use these scripts.

---

## Troubleshooting

### Common issues

**Authentication Errors**:
```powershell
# Ensure you're signed in
Connect-AzAccount
# Verify current context
Get-AzContext
```

**Permission Denied**:
- Verify you have Reader access to target subscriptions
- Check if the subscription is in a different tenant

**Empty Results**:
- Confirm the specified regions support the requested VM SKUs
- Verify subscription IDs are correct
- Check if regions have restricted access

**Multi-threading Issues** (Get-AzVMQuotaUsage.ps1):
- Reduce the number of threads if hitting API limits
- Use PowerShell 7+ for optimal multi-threading support

**Rate Limiting**:
- Reduce concurrent operations
- Add delays between API calls if necessary

### Azure CLI variant

**Authentication errors**:
```bash
# Sign in
az login
# Verify the active account
az account show
```

**Azure CLI not found**:
- Install the Azure CLI for your platform: [Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Confirm the installation: `az --version`

**JSON parsing errors**:
- Ensure you're running PowerShell 7+ for reliable `ConvertFrom-Json` behavior; PowerShell 5.1 has known limitations with deeply nested JSON responses

---

### Getting help

For issues with these scripts:
1. Check the [Azure PowerShell documentation](https://learn.microsoft.com/en-us/powershell/azure/)
2. Review Azure subscription and quota limits
3. Contact Azure support for quota increase requests

## Script versions

These scripts are maintained in the [azcapman repository](https://github.com/microsoft/azcapman). Check for updates regularly to get the latest features and bug fixes.

---

[^vm-quotas]: [Check vCPU quotas - Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas)
[^az-quota]: [az quota CLI reference](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest)
[^az-zones]: [Availability zones – physical and logical mapping](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview#configuring-resources-for-availability-zone-support)
[^az-cli-install]: [Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
