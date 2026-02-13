#!/bin/bash

ENV_FILE="/home/suhkth/Desktop/Rag/agentic_rag_app/backend/.env"
VECTOR_STORE_ID="vs_698df86be3d081918dc449d66fb7f552"

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
