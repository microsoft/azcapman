#!/usr/bin/env bash
# Azure SRE Agent data-plane CRUD helper.
# Source: https://learn.microsoft.com/en-us/azure/sre-agent/api-reference
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sre-agent-rest.sh <list|get|put|patch|delete|post> \
    --tenant <tenant-id> --subscription <subscription-id> \
    --resource-group <resource-group> --agent <agent-name> \
    (--kind <extended-agent-kind> [--name <name>] | --path <data-plane-path>) \
    [--body <json-file>]

--kind builds /api/v2/extendedAgent/<kind>[/<name>].
--path uses a data-plane path verbatim, for example:
  /api/v2/plugins/marketplaces
  /api/v2/plugins/installations

put, patch, and post require --body. The script verifies the supplied tenant
matches the supplied subscription before requesting the SRE Agent endpoint.
EOF
}

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

[[ $# -ge 1 ]] || { usage; exit 2; }
case "$1" in
  -h|--help) usage; exit 0 ;;
esac
operation=$1
shift

tenant=
subscription=
resource_group=
agent=
kind=
name=
path=
body=

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tenant) tenant=${2:?missing tenant value}; shift 2 ;;
    --subscription) subscription=${2:?missing subscription value}; shift 2 ;;
    --resource-group) resource_group=${2:?missing resource-group value}; shift 2 ;;
    --agent) agent=${2:?missing agent value}; shift 2 ;;
    --kind) kind=${2:?missing kind value}; shift 2 ;;
    --name) name=${2:?missing name value}; shift 2 ;;
    --path) path=${2:?missing path value}; shift 2 ;;
    --body) body=${2:?missing body value}; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) fail "unknown argument: $1" ;;
  esac
done

case "$operation" in
  list|get|put|patch|delete|post) ;;
  *) fail "unsupported operation: $operation" ;;
esac

[[ -n "$tenant" && -n "$subscription" && -n "$resource_group" && -n "$agent" ]] ||
  fail "--tenant, --subscription, --resource-group, and --agent are required"
[[ -z "$kind" || -z "$path" ]] || fail "use either --kind or --path, not both"
[[ -n "$kind" || -n "$path" ]] || fail "--kind or --path is required"

if [[ "$operation" == put || "$operation" == patch || "$operation" == post ]]; then
  [[ -n "$body" && -f "$body" ]] || fail "--body must name an existing JSON file"
fi

actual_tenant=$(az account show --subscription "$subscription" --query tenantId -o tsv)
[[ "$actual_tenant" == "$tenant" ]] ||
  fail "subscription $subscription belongs to tenant $actual_tenant, not $tenant"

agent_resource="https://management.azure.com/subscriptions/${subscription}/resourceGroups/${resource_group}/providers/Microsoft.App/agents/${agent}?api-version=2025-05-01-preview"
endpoint=$(az rest --method get --subscription "$subscription" --url "$agent_resource" \
  --query properties.agentEndpoint -o tsv)
[[ -n "$endpoint" && "$endpoint" != "null" ]] || fail "agent endpoint was empty"

if [[ -n "$kind" ]]; then
  path="/api/v2/extendedAgent/${kind}"
  if [[ -n "$name" ]]; then
    encoded_name=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$name")
    path+="/${encoded_name}"
  fi
fi

if [[ "$operation" == get || "$operation" == put || "$operation" == patch || "$operation" == delete ]]; then
  [[ -n "$name" || -z "$kind" || "$operation" == list ]] ||
    fail "--name is required for $operation with --kind"
fi

token=$(az account get-access-token --tenant "$tenant" --resource https://azuresre.dev \
  --query accessToken -o tsv)
[[ -n "$token" ]] || fail "could not acquire an Azure SRE Agent data-plane token"

method=$(printf '%s' "$operation" | tr '[:lower:]' '[:upper:]')
[[ "$operation" == list ]] && method=GET
[[ "$operation" == get ]] && method=GET

curl_args=(
  --silent --show-error --fail-with-body
  --request "$method"
  --header "Authorization: Bearer $token"
  --header "Accept: application/json"
)
if [[ -n "$body" ]]; then
  curl_args+=(--header "Content-Type: application/json" --data-binary "@$body")
fi

curl "${curl_args[@]}" "${endpoint%/}${path}"
