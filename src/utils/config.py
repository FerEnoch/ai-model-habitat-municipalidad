"""
Configuration loader for PDF Data Extraction
"""
import yaml
import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class FileProcessingConfig:
    input_folder: str
    output_file: str
    supported_formats: List[str]
    ocr_method: str
    test_limit: Optional[int]

@dataclass
class OllamaConfig:
    model: str
    temperature: float
    top_k: int
    top_p: float
    format: str

@dataclass
class ExtractionConfig:
    required_fields: List[str]

@dataclass
class LoggingConfig:
    level: str
    format: str

@dataclass
class TimezoneConfig:
    name: str

@dataclass
class AppConfig:
    file_processing: FileProcessingConfig
    ollama: OllamaConfig
    extraction: ExtractionConfig
    logging: LoggingConfig
    timezone: TimezoneConfig


# Global config instance
_config: Optional[AppConfig] = None


def load_config(config_path: str = None) -> AppConfig:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file. If None, uses default location.
        
    Returns:
        AppConfig object with loaded configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
        ValueError: If required config values are missing
    """
    if config_path is None:
        # Default to config/config.yaml relative to the script
        script_dir = Path(__file__).parent
        config_path = script_dir / "config.yaml"
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in config file: {e}")
    
    if not config_data:
        raise ValueError("Configuration file is empty")
    
    try:
        # Create configuration objects
        file_processing = FileProcessingConfig(**config_data['file_processing'])
        ollama = OllamaConfig(**config_data['ollama'])
        extraction = ExtractionConfig(**config_data['extraction'])
        logging_config = LoggingConfig(**config_data['logging'])
        timezone = TimezoneConfig(**config_data['timezone'])
        
        return AppConfig(
            file_processing=file_processing,
            ollama=ollama,
            extraction=extraction,
            logging=logging_config,
            timezone=timezone
        )
        
    except KeyError as e:
        raise ValueError(f"Missing required configuration section: {e}")
    except TypeError as e:
        raise ValueError(f"Invalid configuration format: {e}")

def validate_config(config: AppConfig) -> None:
    """
    Validate configuration values
    
    Args:
        config: Configuration object to validate
        
    Raises:
        ValueError: If configuration values are invalid
    """
    # Validate file processing
    if not config.file_processing.input_folder:
        raise ValueError("Input folder cannot be empty")
    
    if not config.file_processing.output_file:
        raise ValueError("Output file cannot be empty")
    
    if config.file_processing.test_limit is not None and config.file_processing.test_limit < 1:
        raise ValueError("Test limit must be positive or null")
    
    # Validate Ollama settings
    if not config.ollama.model:
        raise ValueError("Ollama model cannot be empty")
    
    if not (0.0 <= config.ollama.temperature <= 2.0):
        raise ValueError("Temperature must be between 0.0 and 2.0")
    
    if config.ollama.top_k < 1:
        raise ValueError("Top K must be positive")
    
    if not (0.0 <= config.ollama.top_p <= 1.0):
        raise ValueError("Top P must be between 0.0 and 1.0")
    
    # Validate extraction
    if not config.extraction.required_fields:
        raise ValueError("Required fields list cannot be empty")
    
    print(f"✓ Configuration validated successfully")
    print(f"  - Method: {config.file_processing.ocr_method}")
    print(f"  - Model: {config.ollama.model}")
    print(f"  - Temperature: {config.ollama.temperature}")
    print(f"  - Input folder: {config.file_processing.input_folder}")
    print(f"  - Test limit: {config.file_processing.test_limit or 'All files'}")

def get_config() -> AppConfig:
    """
    Get the global configuration instance
    
    Returns:
        AppConfig object
    """
    global _config
    if _config is None:
        # get main dir path:
        main_dir = Path(__file__).parent.parent.parent
        _config = load_config(main_dir / "config.yaml")
        validate_config(_config)
    return _config