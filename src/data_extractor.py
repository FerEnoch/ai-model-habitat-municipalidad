import asyncio
import logging
from os import path
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor
from ocr_tesseract import OCR_tesseract
from utils.config import get_config
from utils.index import print_loading_animation
from type_def import OCRExtractionResult

logger = logging.getLogger(__name__)

class Data_Extractor:
    """
    Process extracted data to find specific information.
    """
    
    def __init__(self, dataset_folder: str = ""):
        """Initialize the data extractor."""
        # Load configuration
        self.config = get_config()
        self.dataset_folder = dataset_folder or self.config.file_processing.input_folder
        # Initialize OCR
        self.ocr = OCR_tesseract()
        self.thread_pool = ThreadPoolExecutor(max_workers=self.config.file_processing.max_concurrent_tasks)

    def _get_processing_files(self, files_detected) -> List[str]:
            files_to_process = files_detected
            # Determine how many files to process
            if self.config.file_processing.test_limit is None:
                logger.info("Processing all detected files")
            else:
                try :
                    self.config.file_processing.test_limit = int(self.config.file_processing.test_limit)
                except ValueError:
                    logger.warning("test_limit in config is not a valid integer. Processing all files.")
                    self.config.file_processing.test_limit = None
                if self.config.file_processing.test_limit < 1:
                    logger.warning("test_limit in config is less than 1. Processing all files.")
                    self.config.file_processing.test_limit = None
            if self.config.file_processing.test_limit is not None:
                files_to_process = files_detected[:self.config.file_processing.test_limit]
                logger.info(f"Processing only {self.config.file_processing.test_limit} files for testing")
            
            return files_to_process 

    def _get_dataset_files_to_analyze(self) -> List[str]:
        # Get list of files to analyze based on config
        from utils.index import get_files_from_folder
        
        files_detected = get_files_from_folder(self.dataset_folder, self.config.file_processing.supported_formats)
        # Log detected files according to file extentions
        for ext in self.config.file_processing.supported_formats:
            count = len([f for f in files_detected if f.lower().endswith(f".{ext.lower()}")])
            logger.info(f"Detected {count} .{ext} files detected")
        
        return self._get_processing_files(files_detected)
    
    async def extract_text_from_dataset(self) -> List[OCRExtractionResult]:
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
                
                file_name = path.basename(file_path)
                logger.info(f"Extracting text from: {file_name}")
                
                try:
                    # Extract text from PDF
                    loop = asyncio.get_event_loop()
                    extractionOCRResult = await loop.run_in_executor(self.thread_pool, self.ocr.extract_with_tesseract, file_path)
                    # extractionOCRResult = self.ocr.extract_with_tesseract(file_path)
                    
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