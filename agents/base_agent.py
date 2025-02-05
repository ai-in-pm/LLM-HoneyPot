from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from dotenv import load_dotenv

class BaseAgent(ABC):
    def __init__(self):
        load_dotenv()
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY'),
            'groq': os.getenv('GROQ_API_KEY'),
            'google': os.getenv('GOOGLE_API_KEY'),
            'cohere': os.getenv('COHERE_API_KEY'),
            'emergence': os.getenv('EMERGENCEAI_API_KEY')
        }
        self.validate_api_keys()
        
    def validate_api_keys(self):
        """Validate that all required API keys are present"""
        missing_keys = [k for k, v in self.api_keys.items() if not v]
        if missing_keys:
            raise ValueError(f"Missing API keys for: {', '.join(missing_keys)}")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data and provide insights"""
        pass
    
    @abstractmethod
    def collaborate(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents"""
        pass
