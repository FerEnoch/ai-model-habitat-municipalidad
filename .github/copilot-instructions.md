# Copilot Instructions for PDF Data Extraction Project

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Context
This is a Python project for extracting specific data from PDF files using OCR techniques.

## Code Style and Conventions
- Use Python type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include comprehensive docstrings for all classes and functions
- Use logging instead of print statements for debugging and information
- Handle exceptions gracefully with try-catch blocks

## Project Structure
- `src/`: Main source code directory
  - `pdf_extractor.py`: Main extractor class and file validation
  - `local_ocr.py`: Local OCR implementations using Tesseract and OpenCV
- `main.py`: Entry point for the application
- `requirements.txt`: Project dependencies

## Key Dependencies
- pytesseract, opencv-python: Image-based OCR
- Pillow, numpy: Image processing

## Development Guidelines
1. **Error Handling**: Always include fallback mechanisms when cloud APIs fail
2. **Logging**: Use the logging module with appropriate levels (INFO, WARNING, ERROR)
3. **Type Safety**: Use Optional types for parameters that might be None
4. **Configuration**: Use environment variables for API keys and sensitive data
5. **Testing**: Include validation checks and example data for testing
6. **Documentation**: Provide clear examples in docstrings

## Common Patterns
- Validate file existence and format before processing
- Return standardized data structures (Dict[str, Any]) for consistency
- Include confidence scores when available

## Testing Approach
- Create sample data for testing when real PDFs aren't available
- Test each extraction method independently
- Validate entity recognition patterns
- Check error handling with invalid inputs
