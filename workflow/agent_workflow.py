# workflow/agent_workflow.py
"""
LangGraph Workflow for Multi-Agent POC Builder
Orchestrates the flow between different agents
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Dict
from typing_extensions import TypedDict
import operator


# Define the state structure
class AgentState(TypedDict):
    """State shared across all agents"""
    requirement: str
    refined_requirement: Dict
    architecture: Dict
    backend_code: Dict
    frontend_code: Dict
    code_review: Dict
    deployment: Dict
    agent_responses: Annotated[List[Dict], operator.add]
    error: str


class MultiAgentWorkflow:
    """LangGraph-based workflow for multi-agent collaboration"""
    
    def __init__(self, agents: Dict):
        """
        Initialize workflow with agent instances
        
        Args:
            agents: Dictionary of agent instances
        """
        self.agents = agents
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("query_refiner", self._refine_query)
        workflow.add_node("orchestrator", self._orchestrate)
        workflow.add_node("code_generator", self._generate_code)
        workflow.add_node("ui_enrichment", self._enrich_ui)
        workflow.add_node("code_reviewer", self._review_code)
        workflow.add_node("deployment", self._deploy_code)
        
        # Define the flow
        workflow.set_entry_point("query_refiner")
        workflow.add_edge("query_refiner", "orchestrator")
        workflow.add_edge("orchestrator", "code_generator")
        workflow.add_edge("code_generator", "ui_enrichment")
        workflow.add_edge("ui_enrichment", "code_reviewer")
        workflow.add_edge("code_reviewer", "deployment")
        workflow.add_edge("deployment", END)
        
        return workflow
    
    async def _refine_query(self, state: AgentState) -> AgentState:
        """Query Refiner Agent node"""
        result = await self.agents["query_refiner"].refine(state["requirement"])
        state["refined_requirement"] = result["output"]
        state["agent_responses"].append({
            "agent": "Query Refiner",
            "status": result["status"],
            "output": result["output"]
        })
        return state
    
    async def _orchestrate(self, state: AgentState) -> AgentState:
        """Orchestrator Agent node"""
        result = await self.agents["orchestrator"].orchestrate(state["refined_requirement"])
        state["architecture"] = result["output"]
        state["agent_responses"].append({
            "agent": "Orchestrator",
            "status": result["status"],
            "output": result["output"]
        })
        return state
    
    async def _generate_code(self, state: AgentState) -> AgentState:
        """Code Generator Agent node"""
        result = await self.agents["code_generator"].generate_backend(
            state["refined_requirement"],
            state["architecture"]
        )
        state["backend_code"] = result["output"]
        state["agent_responses"].append({
            "agent": "Code Generator",
            "status": result["status"],
            "output": {"code_length": len(result["output"].get("code", ""))}
        })
        return state
    
    async def _enrich_ui(self, state: AgentState) -> AgentState:
        """UI Enrichment Agent node"""
        result = await self.agents["ui_enrichment"].generate_ui(
            state["refined_requirement"],
            state["backend_code"]
        )
        state["frontend_code"] = result["output"]
        state["agent_responses"].append({
            "agent": "UI Enrichment",
            "status": result["status"],
            "output": {"code_length": len(result["output"].get("code", ""))}
        })
        return state
    
    async def _review_code(self, state: AgentState) -> AgentState:
        """Code Reviewer Agent node"""
        result = await self.agents["code_reviewer"].review(
            state["backend_code"].get("code", ""),
            state["frontend_code"].get("code", "")
        )
        state["code_review"] = result["output"]
        state["agent_responses"].append({
            "agent": "Code Reviewer",
            "status": result["status"],
            "output": result["output"]
        })
        return state
    
    async def _deploy_code(self, state: AgentState) -> AgentState:
        """Deployment Agent node"""
        from datetime import datetime
        project_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = await self.agents["deployment"].deploy(
            state["backend_code"].get("code", ""),
            state["frontend_code"].get("code", ""),
            project_id
        )
        state["deployment"] = result["output"]
        state["agent_responses"].append({
            "agent": "Code Deployment",
            "status": result["status"],
            "output": result["output"]
        })
        return state
    
    async def execute(self, requirement: str) -> Dict:
        """
        Execute the complete workflow
        
        Args:
            requirement: User's requirement description
            
        Returns:
            Final state with all agent outputs
        """
        initial_state = {
            "requirement": requirement,
            "refined_requirement": {},
            "architecture": {},
            "backend_code": {},
            "frontend_code": {},
            "code_review": {},
            "deployment": {},
            "agent_responses": [],
            "error": ""
        }
        
        try:
            result = await self.app.ainvoke(initial_state)
            return result
        except Exception as e:
            initial_state["error"] = str(e)
            return initial_state
    
    def get_workflow_info(self) -> Dict:
        """Get information about the workflow structure"""
        return {
            "nodes": ["query_refiner", "orchestrator", "code_generator", 
                     "ui_enrichment", "code_reviewer", "deployment"],
            "flow": "query_refiner → orchestrator → code_generator → ui_enrichment → code_reviewer → deployment",
            "framework": "LangGraph"
        }