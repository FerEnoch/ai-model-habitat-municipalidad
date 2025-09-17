"""
Data Processor module for handling PDF extraction and analysis workflow.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo
import ollama
from data_extractor import Data_Extractor
from summarizer import Summarizer
from utils.config import get_config
from utils.index import dump_json
from type_def import ProcessingResult, DatasetResults

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Handles the complete data processing workflow.
    Follows Single Responsibility Principle by orchestrating the extraction,
    analysis, and summarization processes.
    """

    def __init__(self):
        """Initialize the data processor with all necessary components."""
        self.config = get_config()
        self.data_extractor = Data_Extractor(dataset_folder=self.config.file_processing.input_folder)
        self.summarizer = Summarizer(self.config.ollama)
        self.timezone = ZoneInfo(self.config.timezone.name)
        self.client = ollama.AsyncClient()

    async def _process_single_file(self, ocr_result: Dict[str, Any]) -> ProcessingResult:
        """
        Process a single OCR result through analysis and summarization.

        Args:
            ocr_result: OCR extraction result

        Returns:
            Complete processing result

        Notes:
            The summary_json returned from the summarizer is expected to be a JSON string
            with at least a "summary" key, e.g. '{"summary": "Summary text here."}'.
        """
        file_name = ocr_result.get('file_name', 'unknown')
        text = ocr_result.get('text', '')

        start_time = datetime.now(self.timezone)

        try:
            # Step 1: Generate summary
            # summary_json is expected to be a JSON string with a "summary" key.
            summary_plaintext = await self.summarizer.generate_summary_async(text)
            # summary_obj = json.loads(summary_json)

            parsed_data = {
                "source_file": ocr_result.get('file_name', 'unknown'),
                "error": None,
                "summary": summary_plaintext,
                "ocr_confidence": ocr_result.get('confidence', 0.0),
            }
            
            end_time = datetime.now(self.timezone)
            parsed_data["processed_at"] = end_time.isoformat()
            parsed_data['processing_time_seconds'] = round((end_time - start_time).total_seconds(), 2)

            # Return error result if analysis failed
            return parsed_data

        except Exception as e:
            file_name = ocr_result.get('file_name', 'unknown')
            logger.error(f"Error processing {file_name}: {e}")
            end_time = datetime.now(self.timezone)
            return {
                "source_file": file_name,
                "error": str(e),
                "summary": "Error occurred during processing",
                "ocr_confidence": ocr_result.get('confidence', 0.0),
                "processed_at": end_time.isoformat(),
                "processing_time_seconds": round((end_time - start_time).total_seconds(), 2)             
            }

    async def process_dataset(self) -> DatasetResults:
        """
        Process the entire dataset through OCR, analysis, and summarization.

        Returns:
            List of processing results
        """
        logger.info("Starting dataset processing...")

        # Step 1: Extract text from all PDFs
        ocr_results = await self.data_extractor.extract_text_from_dataset()
        logger.info(f"Extracted text from {len(ocr_results)} documents.")

        # Step 2: Process each file concurrently
        tasks = [self._process_single_file(ocr_result) for ocr_result in ocr_results]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Step 3: Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Exception during processing: {result}")
            else:
                valid_results.append(result)

        return valid_results

    def save_results(self, results: DatasetResults) -> None:
        """
        Save processing results to output files.

        Args:
            results: List of processing results to save
        """
        try:
            # Save to dataset.json
            dump_json(results=results)
            logger.info(f"Saved {len(results)} results to {self.config.file_processing.output_file}")

        except Exception as e:
            logger.error(f"Error saving results: {e}")