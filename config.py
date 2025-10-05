"""Configuration Management for TalentScout Hiring Assistant

Centralized configuration handling with environment variable support
and validation for required settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class with environment variable support."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    
    # Application Settings
    APP_TITLE = os.getenv("APP_TITLE", "TalentScout Hiring Assistant")
    APP_ICON = os.getenv("APP_ICON", "🤖")
    
    # Interview Configuration
    MAX_BASIC_QUESTIONS = int(os.getenv("MAX_BASIC_QUESTIONS", "7"))
    MAX_TECH_QUESTIONS = int(os.getenv("MAX_TECH_QUESTIONS", "5"))
    MIN_ANSWER_LENGTH = int(os.getenv("MIN_ANSWER_LENGTH", "10"))
    MAX_EXPERIENCE_YEARS = int(os.getenv("MAX_EXPERIENCE_YEARS", "50"))
    
    # Data Storage Configuration
    DATA_DIR = os.getenv("DATA_DIR", "data")
    CSV_FILENAME = os.getenv("CSV_FILENAME", "candidate_data.csv")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file")
        return True