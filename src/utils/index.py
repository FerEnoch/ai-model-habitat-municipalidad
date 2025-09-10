import logging
import os, json
from time import sleep
from itertools import cycle
from sys import stdout as terminal
from anyio import Path

from utils.config import get_config

logger = logging.getLogger(__name__)

def get_files_from_folder(folder: str) -> list:
    '''Recursively scans a folder and returns a list of all PDF files found within it.'''
    files = []
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.pdf'):
                files.append(os.path.join(root, filename))
    return files

# def load_prompt_template() -> str:
#     '''Load the prompt template from the markdown file.'''
#     try:
#         with open("prompts/res_generic_extraction_prompt.md", "r", encoding="utf-8") as f:
#             content = f.read()
#             return content
#     except FileNotFoundError:
#         return "Just say: 'Error loading the prompt template. Please check the file path.'"

def dump_json(results, filename: str = get_config().file_processing.output_file, append: bool = False):
    '''Writes the output in a JSON file with UTF-8 encoding.'''
    if append and os.path.exists(filename):
        # Read existing data
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []
        
        # Append new result
        existing_data.append(results)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

def print_loading_animation(stop_event):
    '''Print a cycling loading animation until stop_event is set'''
    for c in cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        terminal.write('\rloading ' + c)
        terminal.flush()
        sleep(0.1)
    # terminal.write('\r' + ' ' * 20 + '\r')  # Clear the loading line
    # terminal.flush()

def validate_file(self, file_path: str) -> bool:
        """
        Validate if the file exists and is a supported format.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            bool: True if file is valid, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return False
            
        if path.suffix.lower() not in self.supported_formats:
            logger.error(f"Unsupported file format: {path.suffix}")
            return False
            
        return True