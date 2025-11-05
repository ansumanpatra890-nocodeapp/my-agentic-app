
"""
Multi-Agent POC Builder - Main Application
Uses LangChain + LangGraph for agent orchestration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from google import genai
from datetime import datetime
import os , traceback
import sys

# Add agents directory to path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'workflow'))

# Import configuration
from config import AppConfig, ModelConfig

# Import agents
from agents.query_refiner_agent import QueryRefinerAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.code_generator_agent import CodeGeneratorAgent
from agents.ui_enrichment_agent import UIEnrichmentAgent
from agents.code_reviewer_agent import CodeReviewerAgent
from agents.deployment_agent import CodeDeploymentAgent

# Import workflow
from workflow.agent_workflow import MultiAgentWorkflow

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent POC Builder",
    description="AI-powered multi-agent system for automated POC development",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class POCRequest(BaseModel):
    requirement: str
    config: Optional[ModelConfig] = None

class POCResponse(BaseModel):
    project_id: str
    status: str
    agent_responses: List[Dict]
    backend_code: str
    frontend_code: str
    review: Dict
    deployment: Dict

# Global storage
running_projects = {}
active_workflows = {}


def initialize_agents(model_config: ModelConfig) -> Dict:
    """Initialize all agents with given configuration"""
    return {
        "query_refiner": QueryRefinerAgent(
            model_name=model_config.query_refiner_model,
            temperature=model_config.temperature
        ),
        "orchestrator": OrchestratorAgent(
            model_name=model_config.orchestrator_model,
            temperature=model_config.temperature
        ),
        "code_generator": CodeGeneratorAgent(
            model_name=model_config.code_generator_model,
            temperature=0.3
        ),
        "ui_enrichment": UIEnrichmentAgent(
            model_name=model_config.ui_enrichment_model,
            temperature=0.4
        ),
        "code_reviewer": CodeReviewerAgent(
            model_name=model_config.code_reviewer_model,
            temperature=model_config.temperature
        ),
        "deployment": CodeDeploymentAgent()
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Multi-Agent POC Builder API",
        "version": "2.0.0",
        "status": "running",
        "framework": "LangChain + LangGraph",
        "agents": 6
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_projects": len(running_projects)
    }


@app.get("/api/agents")
async def list_agents():
    """List all available agents and their configurations"""
    agents = initialize_agents(AppConfig.DEFAULT_MODEL_CONFIG)
    return {
        "agents": [
            agent.get_agent_info() for agent in agents.values() if hasattr(agent, 'get_agent_info')
        ]
    }


@app.get("/api/models")
async def list_models():
    """List available AI models"""
    return {
        "available_models": AppConfig.AVAILABLE_MODELS,
        "default_config": AppConfig.DEFAULT_MODEL_CONFIG.dict()
    }


@app.post("/api/build-poc", response_model=POCResponse)
async def build_poc(request: POCRequest):
    """
    Main endpoint to build POC using multi-agent workflow
    """
    project_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Use provided model config or default
        model_config = request.model_config or AppConfig.DEFAULT_MODEL_CONFIG
        
        # Initialize agents
        agents = initialize_agents(model_config)
        
        # Create workflow
        workflow = MultiAgentWorkflow(agents)
        active_workflows[project_id] = workflow
        
        # Execute workflow
        result = await workflow.execute(request.requirement)
        
        # Check for errors
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Store deployment info
        if result["deployment"]:
            running_projects[project_id] = {
                "deployment_agent": agents["deployment"],
                "created_at": datetime.now().isoformat(),
                "requirement": request.requirement
            }
        
        # Return response
        return POCResponse(
            project_id=project_id,
            status="success",
            agent_responses=result["agent_responses"],
            backend_code=result["backend_code"].get("code", ""),
            frontend_code=result["frontend_code"].get("code", ""),
            review=result["code_review"],
            deployment=result["deployment"]
        )
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects")
async def list_projects():
    """List all running projects"""
    projects = []
    for project_id, info in running_projects.items():
        deployment_agent = info["deployment_agent"]
        status = deployment_agent.get_status()
        projects.append({
            "project_id": project_id,
            "created_at": info["created_at"],
            "requirement": info["requirement"],
            "status": "running" if status["running"] else "stopped",
            "backend_url": "http://localhost:8080" if status["running"] else None
        })
    
    return {"projects": projects, "total": len(projects)}


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get project details"""
    if project_id not in running_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    info = running_projects[project_id]
    status = info["deployment_agent"].get_status()
    
    return {
        "project_id": project_id,
        "created_at": info["created_at"],
        "requirement": info["requirement"],
        "status": "running" if status["running"] else "stopped",
        "backend_url": "http://localhost:8080" if status["running"] else None,
        "temp_dir": status["temp_dir"]
    }


@app.get("/api/projects/{project_id}/frontend")
async def get_frontend(project_id: str):
    """Get frontend HTML for a project"""
    if project_id not in running_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    info = running_projects[project_id]
    status = info["deployment_agent"].get_status()
    
    if status["temp_dir"]:
        frontend_path = os.path.join(status["temp_dir"], "index.html")
        if os.path.exists(frontend_path):
            with open(frontend_path, "r", encoding="utf-8") as f:
                return {"html": f.read(), "path": frontend_path}
    
    raise HTTPException(status_code=404, detail="Frontend file not found")


@app.delete("/api/projects/{project_id}")
async def stop_project(project_id: str):
    """Stop a running project"""
    if project_id not in running_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    info = running_projects[project_id]
    info["deployment_agent"].stop()
    del running_projects[project_id]
    
    if project_id in active_workflows:
        del active_workflows[project_id]
    
    return {
        "message": "Project stopped successfully",
        "project_id": project_id
    }


@app.get("/api/workflow/info")
async def workflow_info():
    """Get workflow structure information"""
    agents = initialize_agents(AppConfig.DEFAULT_MODEL_CONFIG)
    workflow = MultiAgentWorkflow(agents)
    return workflow.get_workflow_info()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    for project_id, info in running_projects.items():
        info["deployment_agent"].stop()
    running_projects.clear()
    active_workflows.clear()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=AppConfig.BACKEND_PORT,
        log_level="info"
    )
