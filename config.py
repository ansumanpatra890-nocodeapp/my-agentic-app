"""
Configuration file for Multi-Agent POC Builder
Manages model configurations and environment settings
"""

from pydantic import BaseModel

class ModelConfig(BaseModel):
    """Configuration for AI models used by agents"""
    query_refiner_model: str = "gemini-2.5-flash"
    orchestrator_model: str = "gemini-2.5-flash"
    code_generator_model: str = "gemini-2.5-pro"
    ui_enrichment_model: str = "gemini-2.5-pro"
    code_reviewer_model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_tokens: int = 8000

class AppConfig:
    """Application configuration"""
    GEMINI_API_KEY = "AIzaSyDmeHYe0umNa4cm9tBPyM9YvWxr3vBX8hc"
    BACKEND_PORT = 5000
    DEPLOYMENT_PORT = 8080
    
    # Model configurations
    DEFAULT_MODEL_CONFIG = ModelConfig()
    
    # Available models
    AVAILABLE_MODELS = [
        "gemini-2.5-flash"
    ]