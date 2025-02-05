from typing import Dict, Any
from .base_agent import BaseAgent
import anthropic
from loguru import logger

class ArchitectAgent(BaseAgent):
    """Dr. Sarah Chen - Lead Architect
    Expertise: System Architecture and LLM Integration
    Role: Overall project leadership and architecture design"""
    
    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic(api_key=self.api_keys['anthropic'])
        self.model = "claude-3-opus-20240229"
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process architectural decisions and system design"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                system="You are Dr. Sarah Chen, a PhD-level cybersecurity expert specializing in System Architecture and LLM Integration. Analyze the input and provide architectural insights.",
                messages=[
                    {
                        "role": "user",
                        "content": str(input_data)
                    }
                ]
            )
            return {"status": "success", "response": message.content}
        except Exception as e:
            logger.error(f"Error in architect processing: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze system architecture and provide recommendations"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                system="Analyze the current system architecture and provide detailed recommendations for improvement.",
                messages=[
                    {
                        "role": "user",
                        "content": str(data)
                    }
                ]
            )
            return {"status": "success", "analysis": message.content}
        except Exception as e:
            logger.error(f"Error in architect analysis: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def collaborate(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other team members"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                system="Collaborate with team members to integrate their expertise into the system architecture.",
                messages=[
                    {
                        "role": "user",
                        "content": str(agent_input)
                    }
                ]
            )
            return {"status": "success", "collaboration": message.content}
        except Exception as e:
            logger.error(f"Error in architect collaboration: {str(e)}")
            return {"status": "error", "message": str(e)}
