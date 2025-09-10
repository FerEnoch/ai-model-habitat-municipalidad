from ocr_tesseract import OCR_tesseract
from datetime import datetime
import ollama
import os, json, asyncio
from threading import Thread, Event
import logging
from zoneinfo import ZoneInfo
from utils.index import dump_json, print_loading_animation
import sys
from pathlib import Path
from data_extractor import Data_Extractor

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent))
from utils.config import get_config

logger = logging.getLogger(__name__)

async def main():
    # Validate and setup Ollama model
    data_extractor = Data_Extractor()
    
    all_results = []
    
    # Configure timezone from config
    timezone = ZoneInfo(config.timezone.name)
    
    # Start timing
    start_time = datetime.now(timezone)
    
    extractionOCRResult = data_extractor.extract_text_from_dataset()

    print(f"Extracted text from {len(extractionOCRResult)} documents.")
    
    dump_json(results=extractionOCRResult)

    #### Thread and time initialization
    # Create a stop event for the loading animation
    # stop_event = Event()
    # thread = Thread(target=print_loading_animation, args=(stop_event,))
    # thread.start()
#############################################################
########## Initialize ollama client and prepare for analyze
#############################################################
            # Use Ollama for analysis
            # ollama_async_client = ollama.AsyncClient()
            
            # The model already has built-in instructions
#             if config.ollama.model == "resolution-extractor":
#                 # Template-completion approach: model knows what to do
#                 simple_prompt = f"""Nombre de archivo: {file_name}

# Texto de la resolución:
# {extractionOCRResult}"""
#             else:
#                 # Fallback for general models: provide explicit instructions  
#                 simple_prompt = f"""Extrae información de esta resolución en formato JSON con estos campos exactos:
# - numero_resolucion
# - fecha_resolucion  
# - area_emisora
# - descripcion
# - tema

# Archivo: {file_name}
# Texto: {extractionOCRResult}"""
            
#             ollama_result = await ollama_async_client.generate(
#                 model=config.ollama.model,
#                 prompt=simple_prompt,
#                 format=config.ollama.format,
#                 options={
#                     "temperature": config.ollama.temperature,
#                     "top_k": config.ollama.top_k,
#                     "top_p": config.ollama.top_p,
#                 },
#             )
            
#             # Extract the response text from the GenerateResponse object
#             extracted_data: str = ollama_result['response']

#             # Clean up any model-specific artifacts (e.g., thinking tokens)
#             if "thinking" in extracted_data.lower():
#                 # Remove thinking process for reasoning models
#                 import re
#                 extracted_data = re.sub(r"<think>.*?</think>", "", extracted_data, flags=re.DOTALL).strip()
#                 extracted_data = re.sub(r"Thinking.*?done thinking\.", "", extracted_data, flags=re.DOTALL).strip()
#############################################################
########## End ollama analizing 
#############################################################
    
    ### Thread and time finalization
    # Stop the loading animation
    # stop_event.set()
    # thread.join()  # Wait for the thread to finish
    # End timing
    # end_time = datetime.now(timezone)
    # elapsed_time = (end_time - start_time).total_seconds()
    # logger.info(f"Processing time for {file_name}: {elapsed_time:.2f} seconds")

    ################################
    ### Process and validate model results
    ################################

    # Try to parse the JSON response from Ollama
    # parsed_data = {}
    # try:
    #     parsed_data = json.loads(extracted_data)
    
    #     # Validate required fields
    #     required_fields = config.extraction.required_fields
    #     if all(field in parsed_data for field in required_fields):
    #         successTask = True
    #         parsed_data['source_file'] = file_name  # Add source file info
    #         parsed_data['processed_at'] = end_time.isoformat()
    #         parsed_data['processing_time_seconds'] = f"{elapsed_time:.2f}"

    #         successAnalisisResult = parsed_data.copy()  # Create a copy for success result
            
    #         all_results.append(parsed_data)
                    
    #         logger.info(f"Successfully processed {file_name}")
    #     else:
    #         logger.warning(f"Missing required fields in response for {file_name}")
    #         analisisErrorResult = {
    #             "source_file": file_name,
    #             "error": "Missing required fields in AI response",
    #             "raw_response": parsed_data,
    #             "processed_at": end_time.isoformat(),
    #             "processing_time_seconds": f"{elapsed_time:.2f}"
    #         }
    #         all_results.append(analisisErrorResult)

    # except json.JSONDecodeError as e:
    #     logger.warning(f"Error parsing JSON response for {file_name}: {e}")
    #     # Store the raw response if JSON parsing fails
    #     analisisErrorResult = {
    #         "source_file": file_name,
    #         "error": f"JSON parsing failed: {str(e)}",
    #         "raw_response": parsed_data,
    #         "processed_at": end_time.isoformat(),
    #         "processing_time_seconds": f"{elapsed_time:.2f}"
    #     }
    #     all_results.append(analisisErrorResult)

    # except Exception as e:
    #     # Stop the loading animation in case of error
    #     stop_event.set()
    #     thread.join()  # Wait for the thread to finish
        
    #     logger.error(f"Error processing {file_path}: {e}")
    #     analisisErrorResult = {
    #         "source_file": os.path.basename(file_path),
    #         "error": str(e),
    #         "processed_at": datetime.now(timezone).isoformat(),
    #         "processing_time_seconds": None
    #     }
    #     all_results.append(analisisErrorResult)
    
    ######################
    ### write results to json
    #####################
    # Write result to output.json in streaming mode (append as a line-delimited JSON)
    # write_json_file(results=successAnalisisResult if successTask else analisisErrorResult)

if __name__ == "__main__":
    global config
    try:
        # Load configuration first
        config = get_config()
        
        # Configure logging using config
        logging.basicConfig(
            level=getattr(logging, config.logging.level),
            format=config.logging.format
        )
        
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.error("Process interrupted by user...")
    except Exception as e:
        logger.error(f"Fatal error occurred: {e}")
