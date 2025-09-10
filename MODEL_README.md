# Custom Ollama Model for Municipal Resolution Extraction

## Overview
This Modelfile creates a specialized AI model optimized for extracting structured data from Santa Fe municipal resolutions in JSON format.

## Features
- **Deterministic output**: Temperature 0.0 for consistent results
- **Focused sampling**: top_p 0.1, top_k 1 for precise responses
- **Stop tokens**: Prevents model from continuing beyond JSON
- **Specialized system prompt**: Trained specifically for your extraction task

## How to Build and Use

### 1. Build the Custom Model
```bash
# From the project root directory
ollama create resolution-extractor -f Modelfile
```

### 2. Verify Model Creation
```bash
ollama list | grep resolution-extractor
```

### 3. Update Configuration
Edit `config.yaml`:
```yaml
ollama:
  model: "resolution-extractor"
```

### 4. Test the Model
```bash
ollama run resolution-extractor "Extract data from: Resolution 0001-25 from Santa Fe Hábitat about property regularization dated 15 ene. 2025"
```

## Model Parameters Explained

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `temperature` | 0.0 | Completely deterministic output |
| `top_k` | 1 | Only consider the most likely token |
| `top_p` | 0.1 | Very focused nucleus sampling |
| `repeat_penalty` | 1.0 | No penalty for repetition |
| `stop` | "```", "\n\n" | Stop at code blocks or double newlines |

## System Prompt Strategy

The model uses a **template-completion approach** rather than instruction-following:
- Provides exact JSON template to complete
- Uses concrete examples instead of abstract rules
- Enforces strict field constraints
- Prevents over-extraction of unnecessary data

## Expected Output Format
```json
{
  "numero_resolucion": "0004-25",
  "fecha_resolucion": "20 ago. 2024",
  "area_emisora": "Santa Fe Hábitat, Agencia para el Desarrollo Social y Urbano",
  "descripcion": "Rescisión de boleto de compraventa y adjudicación de lote municipal.",
  "tema": "Regularización dominial"
}
```

## Troubleshooting

### Model Not Found
If you get "model not found" errors:
```bash
# Rebuild the model
ollama create resolution-extractor -f Modelfile

# Check if base model exists
ollama list | grep qwen2.5vl
```

### JSON Parsing Errors
If output is not valid JSON:
- Check that stop tokens are properly set
- Verify the system prompt is loading correctly
- Try increasing temperature slightly (0.1) for variation

### Fallback Option
If custom model fails, update config.yaml:
```yaml
ollama:
  model: "qwen2.5vl:7b"  # Use base model
```

## Performance Benefits

Compared to the base model, this custom model should provide:
- ✅ More consistent JSON structure
- ✅ Reduced over-extraction of unnecessary fields  
- ✅ Better adherence to field naming conventions
- ✅ Faster inference (fewer tokens generated)
- ✅ Higher success rate for JSON parsing
