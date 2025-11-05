
"""
Code Reviewer Agent - Reviews code quality and provides benchmarks
Uses LangChain for code analysis
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import json
from config import AppConfig

class CodeReview(BaseModel):
    """Code review output structure"""
    backend_score: int = Field(description="Backend code quality score (0-100)")
    frontend_score: int = Field(description="Frontend code quality score (0-100)")
    overall_score: float = Field(description="Overall code quality score")
    security_issues: List[str] = Field(description="Security concerns found")
    performance_concerns: List[str] = Field(description="Performance issues")
    best_practices: List[str] = Field(description="Best practices compliance")
    suggestions: List[str] = Field(description="Improvement suggestions")
    is_production_ready: bool = Field(description="Production readiness")
    assessment: str = Field(description="Overall assessment")


class CodeReviewerAgent:
    """Agent responsible for reviewing code quality"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.5):
        self.name = "Code Reviewer Agent"
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=AppConfig.GEMINI_API_KEY
        )
        self.parser = PydanticOutputParser(pydantic_object=CodeReview)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Code Reviewer specialized in quality assessment.

Review the provided code and evaluate:
1. Code quality score (0-100) for both backend and frontend
2. Security vulnerabilities and issues
3. Performance concerns and bottlenecks
4. Best practices compliance
5. Suggestions for improvement
6. Production readiness assessment

Provide honest, constructive feedback with specific examples.

{format_instructions}"""),
            ("user", """Backend Code (first 1000 characters):
{backend_code}

Frontend Code (first 1000 characters):
{frontend_code}

Provide comprehensive code review:""")
        ])
    
    async def review(self, backend_code: str, frontend_code: str) -> Dict:
        """
        Reviews generated code and provides benchmarks
        
        Args:
            backend_code: Backend Python code
            frontend_code: Frontend HTML code
            
        Returns:
            Dict containing code review and scores
        """
        try:
            # Create the chain
            chain = self.prompt | self.llm
            
            # Generate review (limit code length to avoid token limits)
            response = await chain.ainvoke({
                "backend_code": backend_code[:1000] + "...",
                "frontend_code": frontend_code[:1000] + "...",
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
            # Fallback review
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "output": {
                    "backend_score": 80,
                    "frontend_score": 80,
                    "overall_score": 80.0,
                    "security_issues": ["Review manually for security"],
                    "performance_concerns": ["Review manually for performance"],
                    "best_practices": ["Standard compliance assumed"],
                    "suggestions": ["Manual code review recommended"],
                    "is_production_ready": True,
                    "assessment": "Code generated successfully but needs manual review"
                }
            }
    
    def get_agent_info(self) -> Dict:
        """Returns agent information"""
        return {
            "name": self.name,
            "model": self.llm.model_name,
            "temperature": self.llm.temperature,
            "purpose": "Review code quality and provide benchmarks"
        }