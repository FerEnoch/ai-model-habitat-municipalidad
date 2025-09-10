# Municipal Resolution Data Extractor

A specialized AI-powered system for extracting structured data from Santa Fe municipal resolution PDFs using custom Ollama models and OCR technology.

## 🎯 Overview

This project automatically extracts key information from municipal resolutions and outputs structured JSON data with fields like:
- Resolution number
- Date
- Issuing area
- Description  
- Topic classification

## ✨ Key Features

- **🤖 Custom AI Model**: Specialized Ollama model trained for municipal document extraction
- **📄 OCR Integration**: Tesseract OCR for PDF text extraction
- **⚙️ YAML Configuration**: Easy parameter tuning without code changes
- **🔄 Streaming Output**: Real-time JSONL file writing
- **🌍 Timezone Support**: Buenos Aires timezone with proper ISO formatting
- **🎛️ Template-Completion**: Deterministic JSON structure enforcement
- **🔧 Fallback Support**: Automatic model fallback and error handling

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running
- UV package manager (or pip)

### 1. Installation

```bash
# Clone and navigate to project
cd /root/projects/mis_proyectos/pdf-data-extraction

# Install dependencies
uv sync
# or with pip: pip install -r requirements.txt
```

### 2. Build Custom Model

**Important**: You must build the custom model before running the extractor.

```bash
# Build the specialized extraction model
ollama create resolution-extractor -f Modelfile

# Verify model creation
ollama list | grep resolution-extractor
```

### 3. Configure Settings

Edit `config.yaml` to customize:

```yaml
ollama:
  model: "resolution-extractor"  # Use your custom model
  temperature: 0.0               # Deterministic output
  
file_processing:
  input_folder: "data/"
  test_limit: 1                  # Start with 1 file for testing
```

### 4. Run Extraction

```bash
# Process PDFs
uv run src/main.py

# Check output
cat output.json
```

## 📁 Project Structure

```
pdf-data-extraction/
├── src/
│   ├── main.py              # Main extraction pipeline
│   ├── local_ocr.py         # OCR processing
│   └── utils/               # Utility functions
├── config/
│   ├── config.yaml          # Main configuration
│   └── config.py            # Configuration loader
├── prompts/
│   └── res_generic_extraction_prompt.md  # Prompt templates
├── data/                    # Input PDF files
├── Modelfile               # Custom Ollama model definition
├── build_model.sh          # Model building script
└── output.json             # Extracted data (JSONL format)
```

## 🔧 Configuration Options

### Model Settings (`config.yaml`)

```yaml
ollama:
  model: "resolution-extractor"    # Custom model name
  temperature: 0.0                 # 0.0 = deterministic, 0.1+ = creative
  top_k: 1                         # Number of tokens to consider
  top_p: 0.1                       # Nucleus sampling threshold
```

### Processing Settings

```yaml
file_processing:
  input_folder: "data/"            # PDF source directory
  output_file: "output.json"      # Results file
  test_limit: null                 # null = all files, number = limit
```

### Extraction Fields

```yaml
extraction:
  required_fields:
    - "numero_resolucion"          # Resolution number
    - "fecha_resolucion"           # Date (dd mmm. yyyy format)
    - "area_emisora"               # Issuing department
    - "descripcion"                # Brief description
    - "tema"                       # Topic classification
```

## 🎯 Template-Completion Approach

### Why Custom Models?

Instead of sending instructions every time:

```python
# ❌ INEFFICIENT: Repeat instructions for every request
ollama.generate(
    model="qwen2.5vl:7b",
    prompt="You are an expert... extract JSON... follow these rules..."
)
```

We use a specialized model with built-in instructions:

```python
# ✅ EFFICIENT: Instructions are built into the model
ollama.generate(
    model="resolution-extractor", 
    prompt="Resolution text here..."
)
```

### Benefits

- **🎯 Consistency**: Same behavior every time
- **⚡ Efficiency**: 5x fewer tokens, faster processing  
- **🔒 Reliability**: Instructions can't be accidentally modified
- **💰 Cost-effective**: Less API usage

## 📊 Output Format

Each processed file generates a JSON line in `output.json`:

```json
{
  "numero_resolucion": "0004-25",
  "fecha_resolucion": "20 ago. 2024",
  "area_emisora": "Santa Fe Hábitat, Agencia para el Desarrollo Social y Urbano",
  "descripcion": "Rescisión de boleto de compraventa y adjudicación de lote municipal.",
  "tema": "Regularización dominial",
  "source_file": "Res 0004-25 Aguilar Mirian y Ojeda Alejandro.pdf",
  "processed_at": "2025-08-14T10:30:45.123456-03:00",
  "processing_time_seconds": 145.67
}
```

## 🔍 Advanced Usage

### Processing Multiple Files

```bash
# Process all PDFs in data/ folder
# Edit config.yaml: test_limit: null
uv run src/main.py
```

### Custom Model Parameters

```bash
# Rebuild model with different parameters
# Edit Modelfile, then:
ollama create resolution-extractor -f Modelfile
```

### Different Base Models

```dockerfile
# In Modelfile, change base model:
FROM llama2:7b              # Alternative base model
PARAMETER temperature 0.0   # Your custom parameters
SYSTEM "Your instructions..." 
```

## 🚨 Troubleshooting

### Model Not Found

```bash
# Check available models
ollama list

# Rebuild if missing
ollama create resolution-extractor -f Modelfile
```

### JSON Parsing Errors

1. **Check model output**:
   ```python
   # Enable debug mode in main.py
   print(f"Model response: {ollama_result}")
   ```

2. **Verify Modelfile**:
   ```bash
   ollama show resolution-extractor
   ```

3. **Test model directly**:
   ```bash
   ollama run resolution-extractor "Test prompt"
   ```

### OCR Issues

```bash
# Install Tesseract if missing
sudo apt-get install tesseract-ocr

# Verify Tesseract installation
python -c "from src.ocr_tesseract import OCR_tesseract; ocr = OCR_tesseract(); print('Tesseract is working')"
```

## �️ Development

### Adding New Fields

1. **Update config.yaml**:
   ```yaml
   extraction:
     required_fields:
       - "numero_resolucion"
       - "new_field"  # Add your field
   ```

2. **Update Modelfile**:
   ```dockerfile
   SYSTEM """
   Template:
   {
     "numero_resolucion": "...",
     "new_field": "..."
   }
   """
   ```

3. **Rebuild model**:
   ```bash
   ollama create resolution-extractor -f Modelfile
   ```

### Testing Changes

```bash
# Test with single file
# config.yaml: test_limit: 1
uv run src/main.py

# Check results
cat dataset.json | jq .
```

## � Performance Tips

- **Use deterministic settings** (`temperature: 0.0`) for consistent results
- **Process in batches** to monitor progress
- **Monitor `processing_time_seconds`** to optimize performance
- **Use SSD storage** for faster PDF processing

## 📄 License

This project is licensed under the GPL v3 License.
This project is for educational and municipal administration purposes.
