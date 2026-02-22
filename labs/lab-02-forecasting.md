# Lab 2: Forecasting

## Overview

Forecasting capacity needs is about collecting utilization signals, analyzing patterns, and translating them into infrastructure commitments. This lab walks you through using Azure Cost Management APIs, quota telemetry, and utilization metrics to build a forecast of compute and storage demand across your SaaS platform, aligned with [Well-Architected capacity planning](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning) guidance.

You'll gather baseline quota usage, analyze utilization patterns in Azure Monitor, pull savings plan recommendations, assess storage costs, and map your forecast to deployment scale units. These outputs feed directly into procurement and allocation decisions.

**Prerequisites:**
- Access to an Azure EA or MCA billing account
- At least one Azure subscription with running workloads
- PowerShell 7.0+ with `Az.CostManagement`, `Az.Quota`, and `Az.Monitor` modules
- Reader or Billing Reader role on the billing account or subscription
- Familiarity with Azure CLI (`az` command)

---

## Exercise 1: Gather baseline quota and usage data

**Objective:** Collect current quota limits and actual usage across compute SKUs and regions to understand headroom for growth.

Quota tells you what you're allowed to run; usage tells you what you're actually running. The gap is your growth buffer.

### Step 1.1: Export VM SKU quota usage across subscriptions

Run the multithreaded quota analysis script to scan all subscriptions for compute quota:

```powershell
.\scripts/quota/Get-AzVMQuotaUsage.ps1 `
  -SKUs "Standard_D2s_v3", "Standard_D4s_v3", "Standard_E2s_v3", "Standard_E4s_v3" `
  -Locations "eastus", "westus2", "northeurope" `
  -Threads 4 `
  -UsePhysicalZones
```

This script:
- Queries each subscription in parallel (4 concurrent threads)
- Returns quota limits, current usage, and utilization % per SKU per location
- Identifies subscriptions approaching quota limits (the constraint on scaling)
- Includes physical zone information if -UsePhysicalZones is set

**Output interpretation:**
- Utilization % > 80% = limited headroom; quota increase or scale-out needed
- Utilization % < 20% = oversized quota; review allocation or consolidate workloads
- Compare across regions to identify uneven capacity distribution

### Step 1.2: Query quota usage via Azure CLI

For a specific subscription and region, use the CLI to drill down:

```bash
az vm list-usage \
  --location eastus \
  --subscription YOUR_SUBSCRIPTION_ID \
  --query "[?contains(name.value, 'DSv3')].{Family: name.localizedValue, Limit: limit, CurrentUsage: currentValue}" \
  --output table
```

This returns per-family vCPU limits and current usage. Filter by family name substring (e.g., `DSv3`, `ESv3`) — the `name.value` field contains family identifiers like `standardDSv3Family`, not individual SKU names.

Reference the [az vm list-usage documentation](https://learn.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest#az-vm-list-usage) for output schema details.

**What to look for:**
- Subscriptions or regions where CurrentUsage is within 10% of Limit
- SKUs with zero usage (over-allocated)
- Patterns in which locations carry workload concentration

### Step 1.3: Document baseline

Save the output CSVs. You'll use these as a baseline to track growth rate quarter-over-quarter.

---

## Exercise 2: Analyze compute utilization with Azure Monitor

**Objective:** Measure actual CPU and memory consumption to forecast peak demand and right-size commitments.

Quota and usage tell you how many VMs you can and are running. Utilization metrics tell you how hard those VMs are working—critical for forecasting when you'll hit scaling limits.

### Step 2.1: Query CPU metrics across VMs

Query aggregate CPU utilization across all VMs using [VM insights](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/vminsights-overview) data in Log Analytics:

```kusto
InsightsMetrics
| where Origin == "vm.azm.ms"
| where Namespace == "Processor"
| where Name == "UtilizationPercentage"
| where TimeGenerated > ago(30d)
| summarize AvgCPU = avg(Val), MaxCPU = max(Val), P95CPU = percentile(Val, 95) by Computer, bin(TimeGenerated, 1h)
| render timechart
```

Run this in the [Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview) connected to your VMs, or via CLI:

```bash
az monitor log-analytics query \
  --workspace YOUR_WORKSPACE_ID \
  --analytics-query "InsightsMetrics | where Origin == 'vm.azm.ms' | where Namespace == 'Processor' | where Name == 'UtilizationPercentage' | where TimeGenerated > ago(30d) | summarize AvgCPU = avg(Val), MaxCPU = max(Val), P95CPU = percentile(Val, 95) by Computer, bin(TimeGenerated, 1h)" \
  --output table
```

For a single VM's platform metrics (no Log Analytics required):

```bash
az monitor metrics list \
  --resource "/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RG/providers/Microsoft.Compute/virtualMachines/YOUR_VM_NAME" \
  --metrics "Percentage CPU" \
  --interval PT1H \
  --aggregation Average \
  --output table
```

See the [InsightsMetrics table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/insightsmetrics) for the full list of VM insights namespaces and metric names.

Reference the [capacity planning section of the Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning) for guidance on which metrics to track.

### Step 2.2: Identify utilization patterns

Look for:
- **Peak hours:** When does CPU spike? This shows your scaling trigger points.
- **Baseline:** What's the minimum CPU during off-peak? This tells you static vs. variable cost.
- **Trend:** Is utilization growing week-over-week? This informs forecast slope.
- **P95:** 95th percentile tells you the threshold for "normal" workload bursts. Budget capacity for this, not average.

### Step 2.3: Establish growth trends

Track week-over-week utilization changes from your monitoring data. The growth trend feeds directly into your quota increase cadence—if utilization is climbing, schedule quota requests before you hit the 80% threshold from Exercise 1.

---

## Exercise 3: Pull savings plan recommendations

**Objective:** Use Azure Cost Management's Benefit Recommendations API to forecast commitment levels that match your utilization forecast.

A good rate optimization mix targets 80–90% coverage from [Azure Reservations](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations) (which typically offer the deepest discounts), with an additional 5–10% from [savings plans](https://learn.microsoft.com/en-us/azure/cost-management-billing/savings-plan/savings-plan-compute-overview) for workloads that shift across SKUs or regions—targeting roughly 95% total coverage. Bursty workloads may warrant a lower target to avoid waste from unused commitment. This exercise focuses on the savings plan layer of that mix.

### Step 3.1: Query savings plan recommendations

```powershell
.\scripts/rate/Get-BenefitRecommendations.ps1 `
  -BillingScope "/subscriptions/YOUR_SUBSCRIPTION_ID" `
  -LookBackPeriod "Last30Days" `
  -Term "P3Y"
```

Parameters:
- **BillingScope:** billing account (for EA), subscription, or resource group. Narrower scopes give more targeted recommendations.
- **LookBackPeriod:** Last7Days / Last30Days / Last60Days. Use 30+ days for reliable trending.
- **Term:** P1Y (1-year) or P3Y (3-year). 3-year has higher discount but less flexibility.

**Output fields:**
- `commitmentAmount`: The commitment (in currency) the API recommends. Granularity (hourly, monthly) is indicated by a separate `commitmentGranularity` property. This directly maps to VM equivalents.
- `savingsPercentage`: Discount vs. on-demand. Typical range: 25%–55% depending on term and region.
- `coveragePercentage`: % of your historical usage that this commitment covers. Aim for 70%–90%; above 90% risks overspending on unused commitment.
- `averageUtilizationPercentage`: Average utilization of committed resources in the lookback period.
- `overageCost`: Cost of usage beyond commitment at on-demand rates. Should be small relative to savings.
- `wastageCost`: Cost of underutilized commitment. Target <5%.

### Step 3.2: Interpret the recommendation

Example output:
- Hourly commitment: $500
- Coverage: 85%
- Savings: 40%
- Wastage: $12/day

This means:
- Buy $500/hour of compute commitment (1-year or 3-year term)
- This covers 85% of your typical hourly usage
- The remaining 15% runs at on-demand rates, which are 10%–15% higher than the committed rate
- You're leaving ~$12/day on the table to underutilized reserved capacity

**Decision point:** Do you accept 85% coverage to save 40%, or do you need tighter alignment? If your forecast shows 10% growth over the next quarter, and coverage is already 85%, you may want to buy to 90% to avoid overages as utilization climbs.

### Step 3.3: Validate against your forecast

Cross-check the API's recommendation against your capacity forecast from Exercise 2:
- If your forecast growth rate suggests 12% month-over-month increase, and the API recommends 85% coverage, you'll need a commitment increase in 2–3 months.
- Schedule your next forecast refresh accordingly.

Reference the [FinOps Framework planning and estimating guidance](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/quantify/planning) for structuring this decision.

---

## Exercise 4: Assess storage and PaaS costs and forecast

**Objective:** Analyze storage, disk, and PaaS service costs across your estate, then forecast growth based on recent trends.

Storage and PaaS services scale differently from compute. Understanding which resources drive cost—and their growth rate—prevents surprise bill spikes and ensures you allocate capacity correctly across regions. Use [Cost Management cost analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis) to query cost data across service categories.

### Step 4.1: Query storage costs with Cost Management

Use the Azure CLI to pull storage costs grouped by subscription and resource for the last billing period:

```bash
az rest --method POST \
  --url "https://management.azure.com/providers/Microsoft.Billing/billingAccounts/YOUR_BILLING_ACCOUNT_ID/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --body '{
    "type": "ActualCost",
    "timeframe": "TheLastBillingMonth",
    "dataset": {
      "granularity": "None",
      "filter": {
        "dimensions": { "name": "ServiceName", "operator": "In", "values": ["Storage"] }
      },
      "grouping": [
        { "type": "Dimension", "name": "SubscriptionName" },
        { "type": "Dimension", "name": "ResourceId" }
      ],
      "aggregation": { "totalCost": { "name": "Cost", "function": "Sum" } }
    }
  }'
```

Reference the [Cost Management Query API](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage) for request body schema and supported dimensions.

Alternatively, in the Azure portal:
1. Go to **Cost Management** > **Cost analysis**
2. Select **Group by** > **Service name**, then filter to **Storage**
3. Select the **DailyCosts** view to see the trend over the billing period

For recurring analysis, [create a Cost Management export](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-export-acm-data) to automatically deliver cost data to a storage account on a schedule. This gives you a historical dataset for trend analysis without manual queries.

### Step 4.2: Identify growth drivers

For each high-cost storage resource:
- Compare this month's cost to the previous month's cost
- Calculate growth rate: (Current - Previous) / Previous * 100
- If growth > 10% per month, flag for capacity planning

Example: An analytics storage account grew from 500 GB to 600 GB in 30 days = 20% growth. At that rate, it reaches 1 TB in ~4 months. Plan ingestion limits, archival policies, or regional replica targets now.

Storage cost varies by tier (hot, cool, archive), replication (LRS, GRS, RA-GRS), and region. Drill down into high-growth accounts and determine if cost is driven by increasing volume, access pattern shifts, or replication overhead.

### Step 4.3: Forecast Premium SSD v2 disk costs

[Premium SSD v2](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#premium-ssd-v2) disks bill separately for capacity, throughput, and IOPS—each dimension scales independently. This makes forecasting more granular than standard managed disks.

Query disk costs with:

```bash
az rest --method POST \
  --url "https://management.azure.com/subscriptions/YOUR_SUBSCRIPTION_ID/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --body '{
    "type": "ActualCost",
    "timeframe": "TheLastBillingMonth",
    "dataset": {
      "granularity": "None",
      "filter": {
        "dimensions": { "name": "MeterSubCategory", "operator": "In", "values": ["Premium SSD v2"] }
      },
      "grouping": [{ "type": "Dimension", "name": "ResourceId" }],
      "aggregation": { "totalCost": { "name": "Cost", "function": "Sum" } }
    }
  }'
```

When forecasting Premium SSD v2 growth, track three dimensions separately:
- **Capacity (GiB):** Grows with data volume—forecast from ingestion rate
- **Provisioned throughput (MBps):** Grows with workload IO demands—forecast from performance baselines
- **Provisioned IOPS:** Grows with transaction density—forecast from application telemetry

Each dimension has its own per-unit price, so a workload that's IOPS-heavy but storage-light has a different cost profile than one that's capacity-heavy. Model each dimension independently for accurate projections.

### Step 4.4: Forecast Azure Cosmos DB costs

[Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/cost-management) uses request units (RUs) as its primary capacity metric. Forecasting Cosmos DB costs requires tracking RU consumption patterns alongside storage growth.

Query Cosmos DB costs with:

```bash
az rest --method POST \
  --url "https://management.azure.com/subscriptions/YOUR_SUBSCRIPTION_ID/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --body '{
    "type": "ActualCost",
    "timeframe": "TheLastBillingMonth",
    "dataset": {
      "granularity": "None",
      "filter": {
        "dimensions": { "name": "ServiceName", "operator": "In", "values": ["Azure Cosmos DB"] }
      },
      "grouping": [{ "type": "Dimension", "name": "ResourceId" }],
      "aggregation": { "totalCost": { "name": "Cost", "function": "Sum" } }
    }
  }'
```

Key forecasting dimensions for Cosmos DB:
- **Provisioned throughput (RU/s):** If you use [provisioned throughput](https://learn.microsoft.com/en-us/azure/cosmos-db/set-throughput), forecast from peak RU consumption trends in Azure Monitor. Autoscale accounts bill for the max RU/s reached per hour.
- **Serverless consumption:** If you use [serverless](https://learn.microsoft.com/en-us/azure/cosmos-db/serverless), forecast from total RU consumption per billing period. Costs scale linearly with request volume.
- **Storage:** Cosmos DB bills per GB stored. Forecast from data growth rate—partition splits don't change cost, but multi-region writes multiply storage charges per replica.

For stamp-based deployments, Cosmos DB cost often scales with tenant count rather than user count. Track per-tenant RU consumption to forecast when you'll need to increase provisioned throughput or add partitions.

### Step 4.5: Map forecasts to workload types

Combine your storage, disk, and PaaS cost data into a unified forecast:
- **Azure Storage:** Forecast by tier, replication, and transaction volume
- **Premium SSD v2:** Forecast by capacity, throughput, and IOPS independently
- **Azure Cosmos DB:** Forecast by RU consumption pattern and storage growth

Cross-reference these forecasts with your compute stamp projections from Exercise 5—PaaS costs often scale proportionally with stamp count, but the relationship isn't always linear. A new stamp may need pre-provisioned Cosmos DB throughput before tenants migrate to it.

---

## Exercise 5: Map forecasts to scale units

**Objective:** Translate compute and storage forecasts into capacity per deployment stamp or region, identifying when you'll exceed current allocation.

ISVs often deploy multiple independent instances of their platform across regions (the [Deployment Stamps pattern](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/overview#deployment-stamps-pattern)). Forecasting capacity per stamp—not only the aggregate—ensures you don't overload one region.

### Step 5.1: Define your stamp architecture

Document your deployment unit. Example:
- **Stamp composition:**
  - 3 API frontend VMs (Standard_D2s_v3, autoscale 3–10)
  - 1 data platform VM (Standard_D8s_v3, fixed)
  - 1 cache VM (Standard_E4s_v3, fixed)
  - 1 storage account (500 GB hot, 2 TB cool for backups)
- **Stamp capacity limit:** 10,000 concurrent users
- **Deployment regions:** eastus, westus2, and northeurope

### Step 5.2: Forecast per-stamp demand

Use utilization data from Exercise 2 to estimate:
- Concurrent users / peak demand per week
- Storage growth per region

Example forecast:
- **Week 1:** 15,000 users across 2 stamps deployed (1 eastus, 1 westus2)—each stamp handles up to 10,000 users, so you're at 75% capacity
- **Week 12 (end of quarter):** 22,000 users—2 stamps can't cover the load, so deploy a 3rd stamp in northeurope

### Step 5.3: Calculate quota and commitment needs

From Exercise 1, your quota per region: 50 Standard_D2s_v3, 10 Standard_D8s_v3, 10 Standard_E4s_v3.

With 2 stamps fully deployed:
- In-use: 6 D2s, 2 D8s, 2 E4s
- Headroom: 44 D2s, 8 D8s, 8 E4s

Forecast shows you need 3 stamps by week 12 (9 D2s, 3 D8s, 3 E4s in-use). You're safe. But if westus2 is your high-demand region, you may hit quota limits in that region before others—request regional quota increase now.

From Exercise 3, your savings plan commitment is $500/hour. With 2 stamps:
- Compute cost: ~$300/hour at on-demand
- Your commitment covers: $300 / $500 = 60% (acceptable)

At 3 stamps (week 12):
- Compute cost climbs to ~$450/hour
- Commitment covers: $450 / $500 = 90% (tight but viable)

Decision: Buy additional commitment buffer now for the 3rd stamp, or risk overages in week 12.

### Step 5.4: Schedule capacity milestones

Create a table:

| Milestone | Timestamp | Stamps Deployed | Quota Headroom (D2s) | Commitment Buffer | Action |
|-----------|-----------|-----------------|----------------------|-------------------|--------|
| Current | Week 1 | 2 | 44 | $200/hr | Baseline |
| Q1 End | Week 12 | 3 | 41 | $50/hr | Request +10 D2s quota; buy +$200/hr commitment |
| Q2 End | Week 26 | 4 | 38 | Risk | Plan regional expansion |

Reference the [Deployment Stamps pattern](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/overview#deployment-stamps-pattern) and [Well-Architected scaling guidance](https://learn.microsoft.com/en-us/azure/well-architected/reliability/scaling) for stamp-based capacity planning.

---

## Exercise 6: Review the Cost Optimization workbook

**Objective:** Use Azure Advisor's Cost Optimization workbook to surface right-sizing and underutilization recommendations.

Azure Advisor automatically analyzes your workloads and flags cost optimization opportunities. Integrating those signals into your forecast prevents capital waste and ensures you're right-sized at each milestone.

### Step 6.1: Open the workbook

1. In the Azure portal, go to **Azure Advisor**
2. Select **Cost Optimization** tab
3. Open **Cost Optimization workbook** (link in the top toolbar)

Reference the [Cost Optimization workbook documentation](https://learn.microsoft.com/en-us/azure/advisor/advisor-workbook-cost-optimization) for setup details.

### Step 6.2: Review recommendation categories

The workbook typically surfaces:

**Underutilized VMs:**
- VMs where CPU < 5% and network < 5% for 7+ days
- Decision: Right-size (move to smaller SKU), turn off during off-hours, or delete
- Impact on forecast: If 30% of your deployed VMs are underutilized, your effective capacity is higher than apparent VM count suggests. Adjust your per-stamp efficiency assumptions.

**Unattached disks:**
- Disks not connected to any VM, still accruing cost
- Decision: Delete if no snapshot backups rely on them
- Impact: Cost reduction without capacity impact

**Oversized database and storage:**
- Databases and storage accounts with excess reserved capacity
- Decision: Right-size tier or replication settings
- Impact: Reduces storage forecasting headroom; ensure actual growth rate justifies existing allocation

**Unused reservations:**
- Commitments (RI / Savings Plans) with low utilization
- Decision: Evaluate if workload pattern changed; may need to trim commitment or accelerate utilization
- Impact: Informs next commitment purchase decision (Exercise 3)

### Step 6.3: Cross-check against your forecast

For each recommendation:
1. Does it contradict your utilization forecast from Exercise 2?
   - If Advisor flags underutilization but your metrics show growth, the VM may be genuinely slack; size it down and redeploy with auto-scale.
2. Does it reveal an allocation misalignment?
   - If a region has high underutilization despite growing headcount, users may be concentrated in a different region; rebalance stamps.
3. Does it confirm your savings plan coverage?
   - If Advisor shows low utilization on your commitment, you've over-bought and should trim next renewal. If high utilization, you're well-aligned.

### Step 6.4: Feed findings into procurement

Document findings in your capacity planning tracker:
- Right-sizing actions: Save X% per VM by downsizing SKU Y (e.g., D4s → D2s saves 50%)
- Headroom recovery: Consolidation frees X quota units per region; delays next quota increase by N weeks
- Commitment efficiency: Current commitment covers Y% of usage; next purchase should target Z%

---

## Wrap-up: From forecast to procurement

You've now gathered all the signals needed to make infrastructure commitments with confidence:

1. **Quota and usage (Exercise 1):** Know what you're allowed to run and what you're running
2. **Utilization patterns (Exercise 2):** Know the growth rate and peak load patterns
3. **Savings plan recommendations (Exercise 3):** Know the optimal commitment level and discount
4. **Storage and PaaS trends (Exercise 4):** Know which storage, disk, and PaaS resources drive cost and when they'll require scale action
5. **Stamp-level forecasts (Exercise 5):** Know when to deploy new stamps or request regional quota
6. **Advisor recommendations (Exercise 6):** Know where to recover efficiency and trim waste

**Next steps:**
- Refresh these analyses monthly. Create a recurring task to run Exercises 1, 2, and 6 each month.
- Use forecasts to negotiate commitment renewals: present your 3-month utilization trend to your Azure account team when discussing savings plan terms.
- Align stamps with regions: review Exercise 5 data in your billing API to confirm actual per-region deployment matches your forecast assumptions.
- Archive historical CSVs (quota, utilization, storage) to track forecast accuracy and refine your projections for next quarter.

**FOCUS exports and reservation sizing:**
If you use FOCUS (FinOps Open Cost and Usage Specification) exports from Cost Management, map commitment discount utilization to your reservation sizing model. See the [FOCUS exports overview](https://learn.microsoft.com/en-us/cloud-computing/finops/focus/overview) for guidance on structuring cost data for forecasting and commitment planning.

**Operationalization cadence:**
Run utilization analysis (Exercises 1–2) weekly, projection updates (Exercise 5) monthly, and business alignment reviews quarterly. This ensures your forecast stays current with actual trends and your roadmap changes are captured in quota requests before they slip into contingency buffers.

**Release gates:**
Before each stamp deployment, validate three gates:
1. Quota headroom ≥ scale unit requirement (from Exercise 5)
2. CRG reserved quantity ≥ deployment target (if applicable)
3. Budget posture allows the spend increase

These gates prevent quota exhaustion, commitment overages, and budget surprises.

The output of forecasting feeds directly into:
- **Allocation decisions:** How much quota and commitment per region?
- **Procurement timing:** When to renew savings plans or request capacity increases?
- **Architecture reviews:** Are stamp capacities sized correctly, or is one region a bottleneck?

For deeper guidance on the FinOps discipline around forecasting, refer to the [FinOps Framework planning and estimating section](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/quantify/planning).
