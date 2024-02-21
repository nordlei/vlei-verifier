#!/bin/bash
set -e

verifier_name=${VERIFIER_NAME:-"verifier"}
port=${HTTP_PORT:-"7676"}
config_file="/usr/local/var/keri/cf/$verifier_name.json"

if [[ -f $config_file ]];
then
  echo "Config file already exists at $config_file"
  cat "$config_file"
else
  echo "Creating new config file at $config_file"
  mkdir -p "$(dirname "$config_file")"
  python3 print_config.py | tee "$config_file"
fi

verifier --config-file "$verifier_name" --name "$verifier_name" --http "$port"
