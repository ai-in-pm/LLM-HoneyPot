from typing import Dict, Any
from .base_agent import BaseAgent
from cohere import Client
from loguru import logger

class DataAgent(BaseAgent):
    """Dr. Kai Yamamoto - Data Scientist
    Expertise: ML Operations and Data Analysis
    Role: Model evaluation and performance optimization"""
    
    def __init__(self):
        super().__init__()
        self.client = Client(api_key=self.api_keys['cohere'])
        self.model = "command"
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data analysis and ML optimization tasks"""
        try:
            response = self.client.chat(
                message=str(input_data),
                model=self.model,
                temperature=0.7,
                preamble="You are Dr. Kai Yamamoto, a PhD-level expert in ML Operations and Data Analysis. Analyze the input and provide ML-specific insights."
            )
            return {"status": "success", "response": response.text}
        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ML model performance and provide optimization insights"""
        try:
            response = self.client.chat(
                message=str(data),
                model=self.model,
                temperature=0.7,
                preamble="Analyze the ML model performance data and provide detailed optimization recommendations."
            )
            return {"status": "success", "analysis": response.text}
        except Exception as e:
            logger.error(f"Error in data analysis: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def collaborate(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other team members on ML and data analysis"""
        try:
            response = self.client.chat(
                message=str(agent_input),
                model=self.model,
                temperature=0.7,
                preamble="Collaborate with team members to optimize ML models and data analysis."
            )
            return {"status": "success", "collaboration": response.text}
        except Exception as e:
            logger.error(f"Error in data collaboration: {str(e)}")
            return {"status": "error", "message": str(e)}
