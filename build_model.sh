#!/bin/bash

# Build custom Ollama model for PDF extraction
echo "Building custom Ollama model for municipal resolution extraction..."

# Create the custom model
ollama create resolution-summarizer -f Modelfile

# Verify the model was created
if ollama list | grep -q "resolution-summarizer"; then
    echo "✓ Custom model 'resolution-summarizer' created successfully!"
    echo ""
    echo "Model details:"
    ollama show resolution-summarizer
    echo ""
    echo "To use this model, update your config.yaml:"
    echo "ollama:"
    echo "  model: \"resolution-summarizer\""
    echo ""
else
    echo "✗ Failed to create custom model"
    exit 1
fi