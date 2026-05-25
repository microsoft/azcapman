# Lab 2 forecasting action register template

Use this template to track technical forecasting signals, evidence, thresholds, and Azure control actions, aligned to [capacity planning](https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/capacity-planning) and [workload supply chain controls](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/workload-supply-chain).

## How to use this template

1. Add one row per measurable forecasting signal that you monitor through Azure quota and monitoring surfaces, as described in [quota monitoring and alerting](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting).
2. Record the exact metric, query, or API output that crossed a threshold so the trigger is auditable, and tie the evidence to supported quota APIs such as [`az quota usage list`](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest#az-quota-usage-list).
3. Document the specific Azure action to take, and the technical decision required, using the matching control path for [per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests), [quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups), [capacity reservations](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview), [region access requests](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process), or [zonal enablement requests](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series).
4. Keep evidence links and validation timestamps current so handoffs and promotion gates stay traceable under [workload supply chain guidance](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/workload-supply-chain).

## Forecasting technical action register

| Service/workload | Region | Measured signal | Threshold crossed | Recommended Azure action | API/query evidence link | Validation timestamp (UTC) | Escalation trigger condition (technical) | Decision needed (technical) |
|---|---|---|---|---|---|---|---|---|
| `<service or stamp>` | `<region>` | `<metric name + current value>` | `<threshold definition + breach window>` | `<quota request, quota group adjustment, CRG update, region access request, zonal enablement request>` | `<Resource Graph query, Azure Monitor query, workbook link, az CLI output, support request link>` | `<yyyy-mm-ddThh:mm:ssZ>` | `<example: projected vCPU usage >80% family quota within 14 days>` | `<example: increase StandardDSv3Family quota to 1500 in eastus>` |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

## Technical references

- [Per-VM quota requests](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests)
- [Quota groups](https://learn.microsoft.com/en-us/azure/quotas/quota-groups)
- [Quota monitoring and alerting](https://learn.microsoft.com/en-us/azure/quotas/how-to-guide-monitoring-alerting)
- [Capacity reservation overview](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview)
- [Region access request process](https://learn.microsoft.com/en-us/troubleshoot/azure/general/region-access-request-process)
- [Zonal enablement request for restricted VM series](https://learn.microsoft.com/en-us/troubleshoot/azure/general/zonal-enablement-request-for-restricted-vm-series)

**Source**: `docs/labs/lab-02-forecasting.md`
**Source**: `references/docs/operations/quota/README.md`
**Source**: `references/docs/operations/quota-groups/README.md`
**Source**: `references/docs/operations/monitoring-alerting/README.md`
**Source**: `references/docs/operations/capacity-reservations/README.md`
