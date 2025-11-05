
"""
Query Refiner Agent - Clarifies and refines user requirements
Uses LangChain for structured processing
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import json
from config import AppConfig

class TechnicalRequirements(BaseModel):
    """Technical requirements structure"""
    backend: List[str] = Field(description="Backend requirements")
    frontend: List[str] = Field(description="Frontend requirements")
    database: str = Field(description="Database type needed")
    apis: List[str] = Field(description="APIs needed")


class RefinedRequirement(BaseModel):
    """Refined requirement output structure"""
    clarified_requirement: str = Field(description="Clear and detailed requirement")
    identified_ambiguities: List[str] = Field(description="List of ambiguities found")
    technical_requirements: TechnicalRequirements
    clarifying_questions: List[str] = Field(description="Questions for clarification")
    is_clear: bool = Field(description="Whether requirement is clear")


class QueryRefinerAgent:
    """Agent responsible for refining and clarifying user requirements"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        self.name = "Query Refiner Agent"
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=AppConfig.GEMINI_API_KEY
        )
        self.parser = PydanticOutputParser(pydantic_object=RefinedRequirement)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Query Refiner Agent specialized in analyzing and clarifying software requirements.
Your job is to:
1. Identify any ambiguities or missing information
2. Clarify the core functionality needed
3. Extract specific technical requirements
4. Suggest clarifying questions if needed
5. Output a clear, detailed, and unambiguous requirement specification

{format_instructions}"""),
            ("user", "Requirement: {requirement}")
        ])
    
    async def refine(self, requirement: str) -> Dict:
        """
        Refines and clarifies user requirements
        
        Args:
            requirement: User's initial requirement description
            
        Returns:
            Dict containing refined requirements and analysis
        """
        try:
            # Create the chain
            chain = self.prompt | self.llm
            
            # Generate response
            response = await chain.ainvoke({
                "requirement": requirement,
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
                    "clarified_requirement": requirement,
                    "identified_ambiguities": [],
                    "technical_requirements": {
                        "backend": ["REST API"],
                        "frontend": ["Web UI"],
                        "database": "none",
                        "apis": []
                    },
                    "clarifying_questions": [],
                    "is_clear": True
                }
            }
    
    def get_agent_info(self) -> Dict:
        """Returns agent information"""
        return {
            "name": self.name,
            "model": self.llm.model_name,
            "temperature": self.llm.temperature,
            "purpose": "Refine and clarify user requirements"
        }