from typing import Dict, Any
from .base_agent import BaseAgent
from cohere import Client
from loguru import logger

class InfrastructureAgent(BaseAgent):
    """Dr. Elena Popov - Infrastructure Engineer
    Expertise: Cloud Infrastructure and Scaling
    Role: System deployment and infrastructure management"""
    
    def __init__(self):
        super().__init__()
        self.client = Client(api_key=self.api_keys['cohere'])
        self.model = "command-nightly"
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process infrastructure and deployment tasks"""
        try:
            response = self.client.chat(
                message=str(input_data),
                model=self.model,
                temperature=0.7,
                preamble="You are Dr. Elena Popov, a PhD-level expert in Cloud Infrastructure and Scaling. Analyze the input and provide infrastructure-specific insights."
            )
            return {"status": "success", "response": response.text}
        except Exception as e:
            logger.error(f"Error in infrastructure processing: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze infrastructure performance and provide scaling recommendations"""
        try:
            response = self.client.chat(
                message=str(data),
                model=self.model,
                temperature=0.7,
                preamble="Analyze the infrastructure data and provide detailed scaling and optimization recommendations."
            )
            return {"status": "success", "analysis": response.text}
        except Exception as e:
            logger.error(f"Error in infrastructure analysis: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def collaborate(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other team members on infrastructure decisions"""
        try:
            response = self.client.chat(
                message=str(agent_input),
                model=self.model,
                temperature=0.7,
                preamble="Collaborate with team members to optimize infrastructure deployment and scaling."
            )
            return {"status": "success", "collaboration": response.text}
        except Exception as e:
            logger.error(f"Error in infrastructure collaboration: {str(e)}")
            return {"status": "error", "message": str(e)}
