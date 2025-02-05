#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
from loguru import logger
import asyncio
from datetime import datetime

# Import our agent modules
from agents import (
    ArchitectAgent,
    LLMAgent,
    HoneypotAgent,
    SecurityAgent,
    InfrastructureAgent,
    DataAgent
)

# Import configuration
from config import validate_config, SYSTEM_CONFIG

# Initialize FastAPI app
app = FastAPI(
    title="LLM Honeypot System",
    description="Advanced cybersecurity system integrating LLMs with Honeypot systems",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
class AgentManager:
    def __init__(self):
        self.architect = ArchitectAgent()
        self.llm_specialist = LLMAgent()
        self.honeypot_expert = HoneypotAgent()
        self.security_analyst = SecurityAgent()
        self.infrastructure_engineer = InfrastructureAgent()
        self.data_scientist = DataAgent()
        
        self.agents = {
            "architect": self.architect,
            "llm_specialist": self.llm_specialist,
            "honeypot_expert": self.honeypot_expert,
            "security_analyst": self.security_analyst,
            "infrastructure_engineer": self.infrastructure_engineer,
            "data_scientist": self.data_scientist
        }
        
    async def process_with_agent(self, agent_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if agent_name not in self.agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        return await asyncio.to_thread(self.agents[agent_name].process, data)

# Initialize agent manager
agent_manager = AgentManager()

# Pydantic models for request/response validation
class ProcessRequest(BaseModel):
    agent: str
    data: Dict[str, Any]

class SystemStatus(BaseModel):
    status: str
    agent_status: Dict[str, str]
    last_check: str

# Routes
@app.get("/")
async def root():
    """Root endpoint returning system information"""
    return {
        "name": "LLM Honeypot System",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def get_status() -> SystemStatus:
    """Get system status including all agents"""
    return SystemStatus(
        status="operational",
        agent_status={
            name: "active" for name in agent_manager.agents.keys()
        },
        last_check=datetime.now().isoformat()
    )

@app.post("/process")
async def process_request(request: ProcessRequest) -> Dict[str, Any]:
    """Process a request using the specified agent"""
    try:
        result = await agent_manager.process_with_agent(
            request.agent,
            request.data
        )
        return {
            "status": "success",
            "agent": request.agent,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/analyze")
async def analyze_threat(
    data: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Analyze potential threats using multiple agents"""
    try:
        # Start with security analysis
        security_result = await agent_manager.process_with_agent(
            "security_analyst",
            data
        )
        
        # Add background tasks for deeper analysis
        background_tasks.add_task(
            agent_manager.process_with_agent,
            "data_scientist",
            {"security_result": security_result}
        )
        
        return {
            "status": "success",
            "initial_analysis": security_result,
            "message": "Detailed analysis running in background",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in threat analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Main entry point for the application"""
    try:
        # Validate configuration
        validate_config()
        
        # Configure logging
        logger.add(
            "logs/llm_honeypot.log",
            rotation="500 MB",
            retention="10 days",
            level=SYSTEM_CONFIG["log_level"]
        )
        
        # Start the server
        uvicorn.run(
            "main:app",  
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

if __name__ == "__main__":
    main()
