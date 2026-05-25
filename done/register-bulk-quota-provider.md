# Register-BulkQuotaProvider.ps1

## Goal

Create `scripts/quota/Register-BulkQuotaProvider.ps1` — a script that registers the `Microsoft.Quota` resource provider on all subscriptions in a management group.

## Why

Quota groups, quota alerts, and the `az quota` CLI all require the `Microsoft.Quota` resource provider to be registered on each subscription. ISVs with hundreds of subscriptions need a bulk operation that follows the same patterns as the existing budget deployment scripts.

## Reference pattern

`scripts/budgets/Deploy-BulkBudgets.ps1` — follow this file's structure exactly for:

- Shebang line (`#!/usr/bin/env pwsh`)
- Copyright header
- Comment-based help (`.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`, `.NOTES`)
- `param()` block structure and validation attributes
- ARG pagination loop (`Search-AzGraph` with `-First 1000` / `-Skip`)
- Subscription listing with first-10 preview + "and N more"
- Confirmation prompt (unless `-Force`)
- Per-subscription `try/catch` with `✅`/`❌` emoji output
- Success/fail counters and summary

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `-ManagementGroup` | Yes | — | Management group name to query for subscriptions |
| `-WhatIf` | No | — | Preview which subscriptions would be registered without making changes |
| `-Quiet` | No | — | Suppress Azure PowerShell warning messages |
| `-Force` | No | — | Skip confirmation prompt |

## Core logic per subscription

```powershell
Set-AzContext -SubscriptionId $sub.subscriptionId -WarningAction SilentlyContinue | Out-Null
$existing = Get-AzResourceProvider -ProviderNamespace "Microsoft.Quota" -ErrorAction SilentlyContinue
if ($existing -and $existing.RegistrationState -eq "Registered") {
    Write-Host "⏭️  Already registered: $($sub.name)" -ForegroundColor Gray
    $skipCount++
} else {
    if ($WhatIf) {
        Write-Host "🔍 Would register: $($sub.name)" -ForegroundColor Cyan
    } else {
        Register-AzResourceProvider -ProviderNamespace "Microsoft.Quota" | Out-Null
        Write-Host "✅ Registered: $($sub.name)" -ForegroundColor Green
    }
    $successCount++
}
```

## Summary output

Track and display four counts: registered, already registered (skipped), failed, total.

## Acceptance criteria

1. Script runs without errors when sourced in PowerShell 7+
2. `-WhatIf` produces output but makes no ARM calls beyond `Get-AzResourceProvider`
3. Already-registered subscriptions are skipped with `⏭️` indicator and counted separately
4. ARG pagination works for >1000 subscriptions
5. Script follows the repository's documentation style guide in all comments and help text
6. Copyright header matches existing scripts
7. No prohibited words (utilize, leverage, powerful, seamless, etc.)
