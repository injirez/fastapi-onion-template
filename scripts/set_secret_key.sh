#!/bin/bash

# Check if the SECRET_KEY environment variable is set
if [ -z "$SECRET_KEY" ]; then
  SECRET_KEY=$(openssl rand -hex 32)
  echo "Generated SECRET_KEY: $SECRET_KEY"
else
  echo "Using SECRET_KEY from environment: $SECRET_KEY"
fi

sed -i.bak "s/^\(secret_key *= *\).*/\1$SECRET_KEY/" "app.conf"

echo "Configuration file updated with secret key: $SECRET_KEY"
