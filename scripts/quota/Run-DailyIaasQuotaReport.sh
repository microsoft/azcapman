#!/usr/bin/env bash
set -euo pipefail

repo_root="/Users/brett/src/azcapman"

pwsh -NoLogo -NoProfile -Command "& '$repo_root/scripts/quota/Get-AzVMQuotaUsage.ps1' -SKUs @('Standard_D2s_v5','Standard_E4s_v5') -Locations @('eastus','westus2')"

report_dir="$repo_root/reports/iaas/$(date +%Y/%m/%d)"
mkdir -p "$report_dir"
cp "$repo_root/QuotaQuery.csv" "$report_dir/QuotaQuery.csv"

echo "Report written: $report_dir/QuotaQuery.csv"
