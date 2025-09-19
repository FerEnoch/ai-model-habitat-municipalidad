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
- **🔄 Streaming Output**: Real-time JSONL file writing.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running
- UV package manager (or pip)

### OCR Issues

```bash
# Install Tesseract if missing
sudo apt-get install tesseract-ocr

# Verify Tesseract installation
python -c "from src.ocr_tesseract import OCR_tesseract; ocr = OCR_tesseract(); print('Tesseract is working')"
```