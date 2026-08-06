#!/usr/bin/env bash
# Azure SRE Agent v2 plugin and marketplace helper.
# Source: https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sre-agent-plugin.sh <command> [connection options] [command options]

Commands:
  marketplace-add    --name <name> --source-url <owner/repo>
  marketplace-list
  marketplace-get    --name <name>
  marketplace-delete --name <name>
  plugin-install-direct --source-url <owner/repo> [--path-in-repo <path>]
                        [--tool <tool-name>]...
  plugin-list
  plugin-get         --name <installation-name>
  plugin-delete      --name <installation-name>
  skill-list-files   --skill <skill-name>
  skill-read-file    --skill <skill-name> --file-path <path>

Connection options are passed to sre-agent-rest.sh and must include:
  --tenant <tenant-id> --subscription <subscription-id>
  --resource-group <resource-group> --agent <agent-name>

plugin-install-direct binds each supplied --tool to every imported skill after
the install completes. The data-plane PATCH requires the complete skill object.
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
command=$1
shift

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
rest_helper="${script_dir}/sre-agent-rest.sh"
connection_args=()
name=
source_url=
path_in_repo=
skill=
file_path=
tools=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) name=${2:?missing name value}; shift 2 ;;
    --source-url) source_url=${2:?missing source-url value}; shift 2 ;;
    --path-in-repo) path_in_repo=${2:?missing path-in-repo value}; shift 2 ;;
    --skill) skill=${2:?missing skill value}; shift 2 ;;
    --file-path) file_path=${2:?missing file-path value}; shift 2 ;;
    --tool) tools+=("${2:?missing tool value}"); shift 2 ;;
    *) connection_args+=("$1"); shift ;;
  esac
done

require_name() {
  [[ -n "$name" ]] || fail "--name is required for $command"
}

require_source_url() {
  [[ -n "$source_url" ]] || fail "--source-url is required for $command"
}

require_skill() {
  [[ -n "$skill" ]] || fail "--skill is required for $command"
}

require_file_path() {
  [[ -n "$file_path" ]] || fail "--file-path is required for $command"
}

url_encode() {
  python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"
}

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

case "$command" in
  marketplace-add)
    require_name
    require_source_url
    jq -n --arg name "$name" --arg source_url "$source_url" \
      '{metadata: {name: $name}, spec: {sourceUrl: $source_url}}' > "$tmp_dir/body.json"
    "$rest_helper" post "${connection_args[@]}" \
      --path /api/v2/plugins/marketplaces --body "$tmp_dir/body.json"
    ;;
  marketplace-list)
    "$rest_helper" list "${connection_args[@]}" --path /api/v2/plugins/marketplaces
    ;;
  marketplace-get)
    require_name
    "$rest_helper" get "${connection_args[@]}" --path "/api/v2/plugins/marketplaces/${name}"
    ;;
  marketplace-delete)
    require_name
    "$rest_helper" delete "${connection_args[@]}" --path "/api/v2/plugins/marketplaces/${name}"
    ;;
  plugin-install-direct)
    require_source_url
    jq -n --arg source_url "$source_url" --arg path_in_repo "$path_in_repo" \
      '{sourceUrl: $source_url, pathInRepo: $path_in_repo}' > "$tmp_dir/install.json"
    installation=$("$rest_helper" post "${connection_args[@]}" \
      --path /api/v2/plugins/install-direct --body "$tmp_dir/install.json")

    if [[ ${#tools[@]} -gt 0 ]]; then
      tool_json=$(printf '%s\n' "${tools[@]}" | jq -R . | jq -s .)
      while IFS= read -r imported_skill; do
        "$rest_helper" get "${connection_args[@]}" --kind skills --name "$imported_skill" \
          | jq --argjson tools "$tool_json" '.properties.tools = $tools' > "$tmp_dir/skill.json"
        "$rest_helper" patch "${connection_args[@]}" --kind skills --name "$imported_skill" \
          --body "$tmp_dir/skill.json" >/dev/null
      done < <(printf '%s\n' "$installation" | jq -r '.importedSkills[].skillName')
    fi

    printf '%s\n' "$installation"
    ;;
  plugin-list)
    "$rest_helper" list "${connection_args[@]}" --path /api/v2/plugins/installations
    ;;
  plugin-get)
    require_name
    "$rest_helper" get "${connection_args[@]}" --path "/api/v2/plugins/installations/${name}"
    ;;
  plugin-delete)
    require_name
    "$rest_helper" delete "${connection_args[@]}" --path "/api/v2/plugins/installations/${name}"
    ;;
  skill-list-files)
    require_skill
    "$rest_helper" post "${connection_args[@]}" \
      --path "/api/v2/agent/skills/$(url_encode "$skill")/showFileContents"
    ;;
  skill-read-file)
    require_skill
    require_file_path
    "$rest_helper" post "${connection_args[@]}" \
      --path "/api/v2/agent/skills/$(url_encode "$skill")/showFileContents?filePath=$(url_encode "$file_path")"
    ;;
  *)
    fail "unsupported command: $command"
    ;;
esac
