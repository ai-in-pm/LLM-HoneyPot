from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Agent Configuration
AGENT_CONFIG = {
    "architect": {
        "name": "Dr. Sarah Chen",
        "role": "Lead Architect",
        "expertise": "System Architecture and LLM Integration",
        "model": "claude-3-opus-20240229"
    },
    "llm_specialist": {
        "name": "Dr. James Rodriguez",
        "role": "LLM Specialist",
        "expertise": "Large Language Models and Fine-tuning",
        "model": "gpt-4-turbo-preview"
    },
    "honeypot_expert": {
        "name": "Dr. Aisha Patel",
        "role": "Honeypot Expert",
        "expertise": "Advanced Honeypot Systems",
        "model": "claude-3-sonnet-20240229"
    },
    "security_analyst": {
        "name": "Dr. Marcus Weber",
        "role": "Security Analyst",
        "expertise": "Threat Analysis and Pattern Recognition",
        "model": "gemini-1.0-pro"
    },
    "infrastructure_engineer": {
        "name": "Dr. Elena Popov",
        "role": "Infrastructure Engineer",
        "expertise": "Cloud Infrastructure and Scaling",
        "model": "command-nightly"
    },
    "data_scientist": {
        "name": "Dr. Kai Yamamoto",
        "role": "Data Scientist",
        "expertise": "ML Operations and Data Analysis",
        "model": "command"
    }
}

# API Configuration
API_CONFIG = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "organization": None
    },
    "anthropic": {
        "api_key": os.getenv("ANTHROPIC_API_KEY")
    },
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY")
    },
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY")
    },
    "cohere": {
        "api_key": os.getenv("COHERE_API_KEY")
    },
    "emergence": {
        "api_key": os.getenv("EMERGENCEAI_API_KEY")
    }
}

# System Configuration
SYSTEM_CONFIG = {
    "log_level": "INFO",
    "max_retries": 3,
    "timeout": 30,
    "batch_size": 10
}

def validate_config():
    """Validate the configuration settings"""
    # Check API keys
    missing_keys = []
    for provider, config in API_CONFIG.items():
        if not config["api_key"]:
            missing_keys.append(provider)
    
    if missing_keys:
        raise ValueError(f"Missing API keys for: {', '.join(missing_keys)}")
    
    # Validate agent configuration
    for agent, config in AGENT_CONFIG.items():
        required_fields = ["name", "role", "expertise", "model"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required fields for agent {agent}: {', '.join(missing_fields)}")

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Get configuration for a specific agent"""
    if agent_name not in AGENT_CONFIG:
        raise ValueError(f"Unknown agent: {agent_name}")
    return AGENT_CONFIG[agent_name]

def get_api_config(provider: str) -> Dict[str, Any]:
    """Get configuration for a specific API provider"""
    if provider not in API_CONFIG:
        raise ValueError(f"Unknown API provider: {provider}")
    return API_CONFIG[provider]
