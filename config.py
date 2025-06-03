import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    JINA_API_KEY = os.getenv("JINA_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    
    # API Endpoints
    JINA_SEARCH_URL = "https://s.jina.ai/"
    GROK_API_URL = "https://api.x.ai/v1"
    
    # Search Settings
    MAX_SEARCH_RESULTS = 10
    MAX_SOCIAL_RESULTS = 5
    
    # Report Settings
    REPORT_TEMPLATE_PATH = "templates/"
    OUTPUT_PATH = "reports/"
    
    @classmethod
    def validate(cls):
        """Validate that all required API keys are present"""
        required_keys = [cls.GEMINI_API_KEY, cls.JINA_API_KEY]
        missing_keys = [key for key in required_keys if not key]
        
        if missing_keys:
            raise ValueError(f"Missing required API keys. Please check your .env file.")
        
        return True