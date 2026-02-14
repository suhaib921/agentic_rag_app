#!/bin/bash

# Get script directory and compute ENV_FILE relative to it
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

# Accept VECTOR_STORE_ID as command-line argument
VECTOR_STORE_ID="${1:-${OPENAI_VECTOR_STORE_ID}}"

# Validate VECTOR_STORE_ID is provided
if [ -z "$VECTOR_STORE_ID" ]; then
    echo "Error: VECTOR_STORE_ID is required"
    echo "Usage: $0 <vector_store_id>"
    echo "   or: OPENAI_VECTOR_STORE_ID=<id> $0"
    exit 1
fi

# Check if ENV_FILE exists, create if missing
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env file at: $ENV_FILE"
    touch "$ENV_FILE"
fi

# Check if OPENAI_VECTOR_STORE_ID already exists
if grep -q "OPENAI_VECTOR_STORE_ID" "$ENV_FILE"; then
    echo "OPENAI_VECTOR_STORE_ID already exists in .env file"
    # Update existing value
    sed -i "s/^OPENAI_VECTOR_STORE_ID=.*/OPENAI_VECTOR_STORE_ID=$VECTOR_STORE_ID/" "$ENV_FILE"
    echo "✅ Updated OPENAI_VECTOR_STORE_ID to: $VECTOR_STORE_ID"
else
    # Add new line
    echo "" >> "$ENV_FILE"
    echo "OPENAI_VECTOR_STORE_ID=$VECTOR_STORE_ID" >> "$ENV_FILE"
    echo "✅ Added OPENAI_VECTOR_STORE_ID to .env file: $VECTOR_STORE_ID"
fi

echo ""
echo "Done! The backend will reload automatically."
