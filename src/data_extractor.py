import logging
from threading import Thread, Event
import os
from datetime import datetime
from typing import Dict, List, Literal
from zoneinfo import ZoneInfo
import ollama
from ocr_tesseract import OCR_tesseract
from utils.config import get_config
from utils.index import print_loading_animation

logger = logging.getLogger(__name__)

class Data_Extractor:
    """
    Process extracted data to find specific information.
    """
    
    def __init__(self):
        """Initialize the data exractor."""
        # Load configuration
        self.config = get_config()
        # Initialize OCR
        self.ocr = OCR_tesseract()

    def _validate_setup_ollama(self) -> None:
        # Validate and setup Ollama model
        try:
            # Test if the configured model is available
            test_client = ollama.Client()
            available_models = [model['name'] for model in test_client.list()['models']]
            
            if self.config.ollama.model not in available_models:
                logger.warning(f"Model '{self.config.ollama.model}' not found. Available models: {available_models}")
                # Fallback to a known model
                fallback_model = "qwen2.5vl:7b" if "qwen2.5vl:7b" in available_models else available_models[0] if available_models else None
                if fallback_model:
                    logger.info(f"Using fallback model: {fallback_model}")
                    self.config.ollama.model = fallback_model
                else:
                    logger.error("No Ollama models available!")
                    return
            else:
                logger.info(f"Using model: {self.config.ollama.model}")
        except Exception as e:
            logger.warning(f"Could not validate Ollama models: {e}")

    def _get_dataset_files_to_analyze(self) -> List[str]:
        # Get list of files to analyze based on config
        from utils.index import get_files_from_folder
        
        pdf_files = get_files_from_folder(self.config.file_processing.input_folder)
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Determine how many files to process
        files_to_process = pdf_files
        if self.config.file_processing.test_limit:
            files_to_process = pdf_files[:self.config.file_processing.test_limit]
            logger.info(f"Processing only {self.config.file_processing.test_limit} files for testing")
        
        return files_to_process
    
    def extract_text_from_dataset(self) -> List[Dict[
        Literal["method", "text", "page_count", "confidence"],
        str | int | float
        ]]:
        """
        Extract text using tesseract.

        Returns:
            Extracted data dictionary list
        """
        files_to_process = self._get_dataset_files_to_analyze()
        extracted_data = []

        try:
            for file_path in files_to_process:
                # successAnalisisResult, successTask, analisisErrorResult = {}, False, {}
                
                file_name = os.path.basename(file_path)
                logger.info(f"Extracting text with ocr from: {file_name}")
                
                try:
                    # Extract text from PDF
                    extractionOCRResult = self.ocr.extract_with_tesseract(file_path)
                    
                    if not extractionOCRResult.get('text'):
                        logger.warning(f"No text extracted from {file_name}")
                        continue

                    extracted_data.append(extractionOCRResult)
                except:
                    logger.error(f"OCR extraction failed for {file_name}")
                    continue
            return extracted_data
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return {"error": str(e)}