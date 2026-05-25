#!/usr/bin/env bash
# T-30: RTM NFR-11.4
# Adapted from https://github.com/matthansen0/azure-sre-agent-sandbox/tree/main/.devcontainer
# Copyright (c) Matt Hansen and contributors. Licensed under the MIT License.

set -euo pipefail

echo ""
echo "Azure capacity management lab"
echo "  - Run 'az login --use-device-code' to authenticate."
echo "  - Use 'pwsh' for PowerShell 7+ commands."
echo "  - Use 'kubectl' and 'az bicep' for cluster and deployment tasks."

if az account show >/dev/null 2>&1; then
  account_name="$(az account show --query 'name' -o tsv)"
  echo "  - Azure CLI is authenticated for: ${account_name}"
else
  echo "  - Azure CLI is not authenticated yet."
fi

echo ""
