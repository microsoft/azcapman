#!/usr/bin/env bash
# T-30: RTM NFR-11.4
# Adapted from https://github.com/matthansen0/azure-sre-agent-sandbox/tree/main/.devcontainer
# Copyright (c) Matt Hansen and contributors. Licensed under the MIT License.

set -euo pipefail

echo "Configuring Azure capacity management lab dev container..."

git config --global init.defaultBranch main
git config --global core.autocrlf input

mkdir -p "${HOME}/.azure" "${HOME}/.config/powershell"

cat > "${HOME}/.azure/config" <<'EOF'
[core]
collect_telemetry = yes
first_run = no

[cloud]
name = AzureCloud
EOF

if ! grep -q "Azure capacity management lab aliases" "${HOME}/.bashrc"; then
  cat >> "${HOME}/.bashrc" <<'EOF'

# Azure capacity management lab aliases
alias k='kubectl'
alias azlogin='az login --use-device-code'
EOF
fi

cat > "${HOME}/.config/powershell/Microsoft.PowerShell_profile.ps1" <<'EOF'
# T-30: RTM NFR-11.4
Set-Alias -Name k -Value kubectl

function azlogin {
    az login --use-device-code @args
}
EOF

echo "Installed tool versions:"
az version --query '"azure-cli"' -o tsv || true
pwsh -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' || true
kubectl version --client=true --output=yaml | sed -n '1,8p' || true
az bicep version || true
