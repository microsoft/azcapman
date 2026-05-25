#!/usr/bin/env pwsh

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

<#
.SYNOPSIS
    Register the Microsoft.Quota resource provider across subscriptions in a management group.

.DESCRIPTION
    Register the Microsoft.Quota resource provider on all enabled subscriptions in the
    specified management group. The script uses Azure Resource Graph to find
    subscriptions in batches and registers the provider one subscription at a time.
    Assumes you're already authenticated via Connect-AzAccount.

    Registration is asynchronous—Azure completes it in the background after the call
    returns. Allow a few minutes before running quota API calls on newly registered
    subscriptions.

.PARAMETER ManagementGroup
    Management group name to query for subscriptions.

.PARAMETER WhatIf
    Preview which subscriptions would be registered without making changes.

.PARAMETER Quiet
    Suppress Azure PowerShell warning messages for cleaner output.

.PARAMETER Force
    Skip the confirmation prompt.

.EXAMPLE
    ./Register-BulkQuotaProvider.ps1 -ManagementGroup "ALZ"

    Register Microsoft.Quota on all enabled subscriptions in the ALZ management group.

.EXAMPLE
    ./Register-BulkQuotaProvider.ps1 -ManagementGroup "ALZ" -WhatIf

    Preview which subscriptions would be registered without making changes.

.EXAMPLE
    ./Register-BulkQuotaProvider.ps1 -ManagementGroup "ALZ" -Quiet -Force

    Register Microsoft.Quota without a confirmation prompt and suppress warning output.

.NOTES
    - Requires Azure PowerShell and Azure Resource Graph modules.
    - Supports pagination for thousands of subscriptions.
    - Automatically handles Azure Resource Graph's 1,000 result limit.
    - You must have permission to read subscriptions and register resource providers.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ManagementGroup,

    [switch]$WhatIf,

    [switch]$Quiet,

    [switch]$Force
)

Write-Host "=== Bulk quota provider registration ===" -ForegroundColor Cyan
Write-Host "Target: $ManagementGroup management group" -ForegroundColor Yellow
Write-Host "Provider: Microsoft.Quota" -ForegroundColor Yellow
Write-Host "Mode: $(if ($WhatIf) { 'What-if (preview)' } else { 'Register' })" -ForegroundColor Yellow

# Suppress Azure PowerShell warnings if Quiet mode is enabled
if ($Quiet) {
    $WarningPreference = 'SilentlyContinue'
}

# Verify Azure connection (assume already logged in)
$context = Get-AzContext
if (-not $context) {
    Write-Host "Not connected to Azure. Please run 'Connect-AzAccount' first." -ForegroundColor Red
    exit 1
}

# Get subscriptions
Write-Host "Finding subscriptions in $ManagementGroup management group..." -ForegroundColor Yellow

# Handle pagination for large result sets
$allSubscriptions = @()
$skip = 0
$pageSize = 1000

do {
    Write-Host "Querying subscriptions (page $([math]::Floor($skip / $pageSize) + 1))..." -ForegroundColor Gray

    $query = "ResourceContainers | where type =~ 'microsoft.resources/subscriptions' | where properties.state == 'Enabled' | project subscriptionId, name"

    if ($skip -eq 0) {
        $pageResults = Search-AzGraph -Query $query -ManagementGroup $ManagementGroup -First $pageSize
    } else {
        $pageResults = Search-AzGraph -Query $query -ManagementGroup $ManagementGroup -First $pageSize -Skip $skip
    }

    if ($pageResults) {
        $allSubscriptions += $pageResults
        $skip += $pageResults.Count
        Write-Host "Found $($pageResults.Count) subscriptions in this page (total: $($allSubscriptions.Count))" -ForegroundColor Gray
    }

    # Continue if we got a full page (indicating there might be more)
} while ($pageResults -and $pageResults.Count -eq $pageSize)

$subscriptions = $allSubscriptions
Write-Host "Total subscriptions found: $($subscriptions.Count)" -ForegroundColor Green

if (!$subscriptions -or $subscriptions.Count -eq 0) {
    Write-Host "No subscriptions found!" -ForegroundColor Red
    exit 1
}

Write-Host "Subscriptions to register on:" -ForegroundColor Green
foreach ($sub in $subscriptions | Select-Object -First 10) {
    Write-Host "  - $($sub.name)" -ForegroundColor White
}

if ($subscriptions.Count -gt 10) {
    Write-Host "  ... and $($subscriptions.Count - 10) more" -ForegroundColor Gray
}

# Confirm registration
if (!$WhatIf -and !$Force) {
    Write-Host ""
    $confirm = Read-Host "Register Microsoft.Quota on all subscriptions? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Register on each subscription
Write-Host ""
Write-Host "Starting registration..." -ForegroundColor Green

$successCount = 0
$skipCount = 0
$failCount = 0

foreach ($sub in $subscriptions) {
    Write-Host "Processing: $($sub.name)" -ForegroundColor Cyan

    try {
        if ($Quiet) {
            Set-AzContext -SubscriptionId $sub.subscriptionId -WarningAction SilentlyContinue | Out-Null
        } else {
            Set-AzContext -SubscriptionId $sub.subscriptionId | Out-Null
        }

        $existing = Get-AzResourceProvider -ProviderNamespace "Microsoft.Quota" -ErrorAction SilentlyContinue

        if ($existing -and ($existing | Where-Object { $_.RegistrationState -ne "Registered" }).Count -eq 0) {
            Write-Host "⏭️  Already registered: $($sub.name)" -ForegroundColor Gray
            $skipCount++
        } else {
            if ($WhatIf) {
                Write-Host "🔍 Would register: $($sub.name)" -ForegroundColor Cyan
                $successCount++
            } else {
                if ($Quiet) {
                    Register-AzResourceProvider -ProviderNamespace "Microsoft.Quota" -WarningAction SilentlyContinue | Out-Null
                } else {
                    Register-AzResourceProvider -ProviderNamespace "Microsoft.Quota" | Out-Null
                }

                Write-Host "✅ Registration initiated: $($sub.name)" -ForegroundColor Green
                $successCount++
            }
        }
    }
    catch {
        Write-Host "❌ Failed: $($sub.name) - $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "Registration complete!" -ForegroundColor Green
Write-Host "  $(if ($WhatIf) { 'Would register' } else { 'Registered (new)' }): $successCount" -ForegroundColor Green
Write-Host "  Already registered (skipped): $skipCount" -ForegroundColor Gray
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { 'Red' } else { 'Green' })
Write-Host "  Total processed: $($subscriptions.Count)" -ForegroundColor Cyan
