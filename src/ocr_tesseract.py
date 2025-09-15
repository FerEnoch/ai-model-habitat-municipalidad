"""
OCR implementations for PDF data extraction.
"""

import io
import logging
from typing import Dict, Literal
import fitz  # PyMuPDF for PDF to image conversion
import cv2
import numpy as np
from PIL import Image
import pytesseract
from os import path


logger = logging.getLogger(__name__)

class OCR_tesseract:
    """ Local OCR implementation using Tesseract """
    
    def __init__(self):
        """Initialize local OCR."""
        self.tesseract_cmd = "tesseract"
        self.zoom_factor = 2.0  # Default zoom for better OCR quality

    def _pdf_to_images(self, file_path: str) -> list[Image.Image]:
        """
        Convert PDF pages to PIL Images.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of PIL Images, one per page
        """
        images = []
        pdf_document = fitz.open(file_path)
        
        try:
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                images.append(img)
        finally:
            pdf_document.close()
            
        return images

    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results.
        
        Args:
            img: Input PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply threshold for better contrast
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Convert back to PIL
        return Image.fromarray(thresh)

    def _extract_text_from_image(self, img: Image.Image) -> tuple[str, list[int]]:
        """
        Extract text and confidence scores from a single image.
        
        Args:
            img: PIL Image to process
            
        Returns:
            Tuple of (extracted_text, confidence_scores)
        """
        # Get OCR data with confidence scores
        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Extract text and confidence scores
        page_text = ""
        confidences = []
        
        for i in range(len(ocr_data['text'])):
            conf = int(ocr_data['conf'][i])
            if conf > 0:  # Only include text with confidence > 0
                word = ocr_data['text'][i].strip()
                if word:
                    page_text += word + " "
                    confidences.append(conf)
        
        return page_text.strip(), confidences

    def _calculate_average_confidence(self, all_confidences: list[int]) -> float:
        """
        Calculate average confidence score.
        
        Args:
            all_confidences: List of confidence scores
            
        Returns:
            Average confidence as float between 0-1
        """
        if not all_confidences:
            return 0.0
        confidence_average = sum(all_confidences) / len(all_confidences) / 100.0
        return round(confidence_average, 2)

    def _format_extraction_text_result(self, page_texts: list[str]) ->  Dict[
        Literal["text"],
        str
        ]:
        """
        Format the final extraction result.
        
        Args:
            page_texts: List of extracted text per page
            page_count: Total number of pages
            avg_confidence: Average confidence score
            
        Returns:
            Formatted result dictionary
        """
        # Combine all page texts
        full_text = ""
        for i, text in enumerate(page_texts):
            if text:
                full_text += f"Page {i + 1}:\n{text}\n\n"
        
        return {
            "text": full_text.strip(),
        }

    def extract_with_tesseract(self, file_path: str) -> Dict[
        Literal["method", "text", "page_count", "confidence"],
        str | int | float
        ]:
        """
        Extract text using Tesseract OCR by converting PDF pages to images.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted data dictionary
        """
        try:
            # Convert PDF to images
            images = self._pdf_to_images(file_path)
            
            # Process each image
            page_texts = []
            all_confidences = []
            
            for img in images:
                # Preprocess image
                processed_img = self._preprocess_image(img)
                
                # Extract text and confidence
                page_text, confidences = self._extract_text_from_image(processed_img)
                
                page_texts.append(page_text)
                all_confidences.extend(confidences)
            
            # Format result
            text_result = self._format_extraction_text_result(page_texts)
            confidence = self._calculate_average_confidence(all_confidences)
            
            return {
                "method": "tesseract",
                "file": path.basename(file_path),
                "page_count": len(images),
                "text": text_result["text"],
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"Tesseract OCR extraction failed: {str(e)}")
            return {"error": str(e), "method": "tesseract"}
    
    # def extract_with_tesseract_simple(self, file_path: str) -> Dict[str, Any]:
    #     """
    #     Simple fallback Tesseract extraction without preprocessing.
        
    #     Args:
    #         file_path: Path to PDF file
            
    #     Returns:
    #         Extracted data dictionary
    #     """
    #     try:
    #         images = self._pdf_to_images(file_path)
    #         page_texts = []
            
    #         for img in images:
    #             # Direct OCR without preprocessing
    #             text = pytesseract.image_to_string(img)
    #             page_texts.append(text.strip())
            
    #         result = self._format_extraction_result(page_texts, len(images), 0.5)  # Default confidence
    #         return result
            
    #     except Exception as e:
    #         logger.error(f"Simple Tesseract OCR extraction failed: {str(e)}")
    #         return {"error": str(e), "method": "tesseract_simple"}

    # def extract_text(self, file_path: str, method: Optional[str] = None) -> Dict[str, Any]:
    #     """
    #     Extract text using the best available method.
        
    #     Args:
    #         file_path: Path to PDF file
    #         method: Specific method to use (optional)
            
    #     Returns:
    #         Extracted data dictionary
    #     """
    #     target_method = method or "tesseract"
    #     logger.info(f"Using {target_method} for text extraction")
        
    #     # Execute extraction
    #     if target_method == "tesseract":
    #         # Try advanced Tesseract first, fallback to simple
    #         result = self.extract_with_tesseract(file_path)
    #         if "error" in result:
    #             logger.info("Advanced Tesseract failed, trying simple method...")
    #             return self.extract_with_tesseract_simple(file_path)
    #         return result
    #     else:
    #         return {"error": f"Method {target_method} not implemented"}