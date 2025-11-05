
"""
Orchestrator Agent - Decides architecture and coordinates development
Uses LangChain for decision making
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import json
from config import AppConfig

class TechStack(BaseModel):
    """Technology stack structure"""
    backend: str = Field(description="Backend framework")
    frontend: str = Field(description="Frontend framework")
    database: str = Field(description="Database type")


class ArchitectureDecision(BaseModel):
    """Architecture decision output structure"""
    app_type: str = Field(description="Type of application")
    tech_stack: TechStack
    architecture: str = Field(description="Architecture pattern")
    components: List[str] = Field(description="Components to develop")
    development_order: List[str] = Field(description="Order of development")
    estimated_complexity: str = Field(description="Complexity level")


class OrchestratorAgent:
    """Agent responsible for orchestrating the development process"""
    
    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.7):
        self.name = "Orchestrator Agent"
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=AppConfig.GEMINI_API_KEY
        )
        self.parser = PydanticOutputParser(pydantic_object=ArchitectureDecision)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an Orchestrator Agent specialized in software architecture decisions.
Based on refined requirements, you must decide:
1. What type of application to build (REST API, Web App, etc.)
2. Technology stack to use
3. Architecture pattern
4. Which components need to be developed
5. Development priority order

{format_instructions}"""),
            ("user", "Refined Requirements:\n{requirements}")
        ])
    
    async def orchestrate(self, refined_requirements: Dict) -> Dict:
        """
        Decides the architecture and coordinates development
        
        Args:
            refined_requirements: Output from Query Refiner Agent
            
        Returns:
            Dict containing architecture decisions
        """
        try:
            # Create the chain
            chain = self.prompt | self.llm
            
            # Generate response
            response = await chain.ainvoke({
                "requirements": json.dumps(refined_requirements, indent=2),
                "format_instructions": self.parser.get_format_instructions()
            })
            
            # Parse the response
            result_text = response.content
            
            # Try to extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            # Parse to dict
            result_dict = json.loads(result_text)
            
            return {
                "status": "success",
                "agent": self.name,
                "output": result_dict
            }
            
        except Exception as e:
            # Fallback response
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "output": {
                    "app_type": "web_app",
                    "tech_stack": {
                        "backend": "FastAPI",
                        "frontend": "HTML/CSS/JS",
                        "database": "None"
                    },
                    "architecture": "simple_mvc",
                    "components": ["backend_api", "frontend_ui"],
                    "development_order": ["backend", "frontend", "integration"],
                    "estimated_complexity": "medium"
                }
            }
    
    def get_agent_info(self) -> Dict:
        """Returns agent information"""
        return {
            "name": self.name,
            "model": self.llm.model_name,
            "temperature": self.llm.temperature,
            "purpose": "Orchestrate development and decide architecture"
        }