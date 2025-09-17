import ollama
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Summarizer:
    """
    Handles text summarization using Ollama models.
    Follows Single Responsibility Principle by focusing only on summarization tasks.
    """

    def __init__(self, model_config):
        """
        Initialize the Summarizer with model configuration.

        Args:
            model_config: Configuration object containing model settings
        """
        self.model_config = model_config
        self.client = ollama.AsyncClient()
        
    # def _validate_setup_ollama(self) -> None:
    #     # Validate and setup Ollama model
    #     try:
    #         # Test if the configured model is available
    #         test_client = ollama.Client()
    #         available_models = [model['name'] for model in test_client.list()['models']]
            
    #         if self.config.ollama.model not in available_models:
    #             logger.warning(f"Model '{self.config.ollama.model}' not found. Available models: {available_models}")
    #             # Fallback to a known model
    #             fallback_model = "qwen2.5vl:7b" if "qwen2.5vl:7b" in available_models else available_models[0] if available_models else None
    #             if fallback_model:
    #                 logger.info(f"Using fallback model: {fallback_model}")
    #                 self.config.ollama.model = fallback_model
    #             else:
    #                 logger.error("No Ollama models available!")
    #                 return
    #         else:
    #             logger.info(f"Using model: {self.config.ollama.model}")
    #     except Exception as e:
    #         logger.warning(f"Could not validate Ollama models: {e}")
            
    async def _summarize_with_ollama(self, text: str) -> str:
        """
        Generate summary using Ollama model.

        Args:
            text: Text to summarize

        Returns:
            Summary text
        """
        prompt = f"""
                Tu tarea es extraer información clave de las resoluciones municipales proporcionadas
                en formato de texto plano, y devolverla en un texto breve que sea un resumen completo
                y perfecto de lo que se resuelve:
                ## El texto de la reolución es el siguiente:
                {text}"""
        try:
            response = await self.client.generate(
                model=self.model_config.model,
                prompt=prompt,
                format=self.model_config.format,
                options={
                    "temperature": self.model_config.temperature,
                    "top_k": self.model_config.top_k,
                    "top_p": self.model_config.top_p,
                },
            )
            extracted_data: str = response['response']

            # Clean up reasoning model artifacts
            if "thinking" in extracted_data.lower():
                import re
                extracted_data = re.sub(r"<think>.*?</think>", "", extracted_data, flags=re.DOTALL).strip()
                extracted_data = re.sub(r"Thinking.*?done thinking\.", "", extracted_data, flags=re.DOTALL).strip()
    
            return extracted_data
        
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"

    async def generate_summary_async(self, text: str):
        """
        Generate summary asynchronously.

        Args:
            text: Text to summarize

        Returns:
            Summary text
        """
        if not text or not text.strip():
            return "No text available for summarization"
        return await self._summarize_with_ollama(text)

    async def generate_multiple_summaries(self, texts: list[str]) -> list[str]:
        """
        Generate summaries for multiple texts concurrently.

        Args:
            texts: List of texts to summarize

        Returns:
            List of summaries
        """
        tasks = [self.generate_summary_async(text) for text in texts]
        return await asyncio.gather(*tasks, return_exceptions=True)