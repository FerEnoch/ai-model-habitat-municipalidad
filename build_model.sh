#!/bin/bash

# Build custom Ollama model for PDF extraction
echo "Building custom Ollama model for municipal resolution extraction..."

# Create the custom model
ollama create resolution-extractor -f Modelfile

# Verify the model was created
if ollama list | grep -q "resolution-extractor"; then
    echo "✓ Custom model 'resolution-extractor' created successfully!"
    echo ""
    echo "Model details:"
    ollama show resolution-extractor
    echo ""
    echo "To use this model, update your config.yaml:"
    echo "ollama:"
    echo "  model: \"resolution-extractor\""
    echo ""
else
    echo "✗ Failed to create custom model"
    exit 1
fi

echo "Testing the model with a simple prompt..."
echo '{"test": "ping"}' | ollama run resolution-extractor "Archivo: 0004-25 Aguilay y Ojeda.pdf
Texto de la resolución:
RESOLUCIÓN N° 0004-25
Santa Fe, 20 de agosto de 2024
VISTO: La Ordenanza N° 11.631 y;
CONSIDERANDO: Que el señor Aguilar Mirian y Ojeda Alejandro han solicitado la rescisión del boleto de compraventa del lote municipal.
POR ELLO: EL INTENDENTE MUNICIPAL RESUELVE:
ARTÍCULO 1°: Rescindiendo el boleto de compraventa y adjudicando nuevamente el lote.
Santa Fe Hábitat, Agencia para el Desarrollo Social y Urbano"
