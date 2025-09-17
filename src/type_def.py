"""
Type definitions for the PDF Data Extraction project.

This module contains type aliases and custom types used throughout the project
to ensure type safety and consistency.
"""

from typing import Dict, List, Literal, TypeAlias, Any

# OCR-related types
OCRExtractionResult: TypeAlias = Dict[
    Literal["method", "file_name", "text", "page_count", "confidence"],
    str | int | float
]

# Processing result types
ProcessingResult: TypeAlias = Dict[
    Literal[
        "source_file", "error", "summary", "ocr_confidence",
        "processed_at", "processing_time_seconds"
    ],
    str | float | None
]

# Dataset processing types
DatasetResults: TypeAlias = List[ProcessingResult]

# Configuration types
ModelConfig: TypeAlias = Dict[str, Any]

# File processing types
FilePathList: TypeAlias = List[str]
SupportedFormat: TypeAlias = Literal["pdf", "txt"]