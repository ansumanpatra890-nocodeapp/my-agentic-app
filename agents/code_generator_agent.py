# agents/code_generator_agent.py
"""
Code Generator Agent - Generates production-ready backend code
Optimized for 90+ quality scores with comprehensive error handling
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, List
import json
import re
from config import AppConfig


class CodeGeneratorAgent:
    """Advanced agent for generating production-ready backend code"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp", temperature: float = 0.2):
        self.name = "Code Generator Agent"
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=AppConfig.GEMINI_API_KEY,
            max_output_tokens=16000
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an ELITE Backend Software Engineer with 15+ years of experience in building production-grade APIs.

Your mission: Generate COMPLETE, FLAWLESS, PRODUCTION-READY FastAPI backend code.

CRITICAL REQUIREMENTS - NON-NEGOTIABLE:

1. CODE STRUCTURE & COMPLETENESS:
   - Include ALL necessary imports at the top
   - Proper FastAPI app initialization with metadata
   - CORS middleware configured for all origins (development mode)
   - Complete Pydantic models for ALL data structures
   - Comprehensive error handling with proper HTTP status codes
   - Input validation using Pydantic Field validators
   - In-memory data storage with proper initialization
   - Seed data for immediate testing (if applicable)
   - Helper functions for common operations
   - Must run on port 8080

2. API ENDPOINT REQUIREMENTS:
   - RESTful design principles
   - Proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
   - Clear, descriptive endpoint paths
   - Response models for type safety
   - Status code specifications
   - API tags for documentation organization
   - Comprehensive docstrings for all endpoints

3. ERROR HANDLING & VALIDATION:
   - Try-catch blocks where needed
   - HTTPException with proper status codes (400, 404, 409, 422, 500)
   - Descriptive error messages
   - Data validation before operations

4. DATA MODELS & STORAGE:
   - BaseModel classes for inheritance
   - Separate Create/Update/Response models
   - Proper field types and constraints
   - Default values where appropriate
   - Example values in Field definitions
   - Enums for status fields
   - Organized in-memory database structure

5. CODE QUALITY:
   - Clear, descriptive variable names
   - Proper indentation (4 spaces)
   - Logical code organization
   - DRY principle (Don't Repeat Yourself)
   - Type hints throughout
   - PEP 8 compliance

6. EXECUTION:
   - Must include: if __name__ == "__main__":
   - uvicorn.run(app, host="0.0.0.0", port=8080)
   - Code must be immediately executable

OUTPUT FORMAT - STRICTLY ENFORCE:

DO NOT include:
   - Markdown code blocks (```python, ```)
   - Explanatory text before or after code
   - Placeholder comments like "# Add more endpoints here"
   - Incomplete sections

DO provide:
   - Pure Python code only
   - Complete, working implementation
   - All features fully implemented
   - Proper imports and dependencies
   - Executable code from line 1

EXAMPLE STRUCTURE:

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import uuid

app = FastAPI(title="App Name", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Status(str, Enum):
    ACTIVE = "active"

class ItemBase(BaseModel):
    name: str = Field(..., example="Item")

class Item(ItemBase):
    id: str
    created_at: datetime

db = {{"items": {{}}}}

def seed_data():
    pass

seed_data()

@app.get("/")
def root():
    return {{"message": "API running"}}

@app.get("/items", response_model=List[Item])
def list_items():
    return list(db["items"].values())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

Now generate the COMPLETE, PRODUCTION-READY backend code following ALL requirements above."""),
            ("user", """Application Requirements:
{requirements}

Architecture Details:
{architecture}

GENERATE THE COMPLETE, PRODUCTION-READY BACKEND CODE NOW.
Remember: NO markdown, NO explanations, ONLY executable Python code.""")
        ])
    
    async def generate_backend(self, requirements: Dict, architecture: Dict) -> Dict:
        """
        Generates complete, production-ready backend code
        
        Args:
            requirements: Refined application requirements
            architecture: Architecture decisions and technical stack
            
        Returns:
            Dict containing generated backend code with metadata
        """
        try:
            chain = self.prompt | self.llm
            
            response = await chain.ainvoke({
                "requirements": json.dumps(requirements, indent=2),
                "architecture": json.dumps(architecture, indent=2)
            })
            
            code = response.content.strip()
            code = self._clean_code(code)
            validation_result = self._validate_code(code)
            
            if not validation_result["valid"]:
                code = self._fix_common_issues(code, validation_result["issues"])
            
            return {
                "status": "success",
                "agent": self.name,
                "output": {
                    "code": code,
                    "language": "python",
                    "framework": "FastAPI",
                    "port": 8080,
                    "lines": len(code.split('\n')),
                    "validation": validation_result,
                    "quality_score": self._calculate_quality_score(code)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "output": {
                    "code": self._generate_fallback_code(),
                    "language": "python",
                    "framework": "FastAPI",
                    "port": 8080
                }
            }
    
    def _clean_code(self, code: str) -> str:
        """Cleans generated code from markdown and extra text"""
        if "```python" in code:
            code = code.split("```python", 1)[1].split("```")[0].strip()
        elif "```" in code:
            parts = code.split("```")
            if len(parts) >= 3:
                code = parts[1].strip()
        
        prefixes_to_remove = ["python", "Python", "Here's the code:", "Here is the code:", "Code:"]
        for prefix in prefixes_to_remove:
            if code.startswith(prefix):
                code = code[len(prefix):].strip()
        
        code = code.replace('\r\n', '\n')
        return code
    
    def _validate_code(self, code: str) -> Dict:
        """Validates generated code for completeness"""
        issues = []
        
        required_imports = ['uvicorn', 'FastAPI', 'CORSMiddleware']
        for imp in required_imports:
            if imp not in code:
                issues.append(f"Missing import: {imp}")
        
        if 'app = FastAPI' not in code:
            issues.append("Missing FastAPI app initialization")
        
        if 'add_middleware' not in code or 'CORSMiddleware' not in code:
            issues.append("Missing CORS middleware configuration")
        
        if 'uvicorn.run' not in code:
            issues.append("Missing uvicorn.run() execution block")
        
        if '@app.' not in code:
            issues.append("No API endpoints defined")
        
        if 'BaseModel' not in code:
            issues.append("No Pydantic models defined")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "checks_passed": 6 - len(issues),
            "total_checks": 6
        }
    
    def _fix_common_issues(self, code: str, issues: List[str]) -> str:
        """Attempts to fix common issues in generated code"""
        if "Missing uvicorn.run()" in str(issues) and 'uvicorn.run' not in code:
            if 'if __name__ == "__main__"' not in code:
                code += '\n\nif __name__ == "__main__":\n    uvicorn.run(app, host="0.0.0.0", port=8080)\n'
        
        return code
    
    def _calculate_quality_score(self, code: str) -> int:
        """Calculates quality score for generated code"""
        score = 0
        
        if 'import uvicorn' in code and 'from fastapi import' in code:
            score += 10
        
        if 'CORSMiddleware' in code and 'add_middleware' in code:
            score += 10
        
        if 'BaseModel' in code and 'Field' in code:
            score += 15
        
        if 'HTTPException' in code and 'status_code' in code:
            score += 15
        
        endpoint_count = code.count('@app.')
        score += min(20, endpoint_count * 4)
        
        if 'db = {' in code or 'database' in code.lower():
            score += 10
        
        if 'uvicorn.run' in code and 'if __name__' in code:
            score += 10
        
        lines = len(code.split('\n'))
        if lines > 100:
            score += 10
        elif lines > 50:
            score += 5
        
        return min(score, 100)
    
    def _generate_fallback_code(self) -> str:
        """Generates basic fallback code if generation fails"""
        return """import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fallback API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API running in fallback mode"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
"""
    
    def get_agent_info(self) -> Dict:
        """Returns detailed agent information"""
        return {
            "name": self.name,
            "model": self.llm.model_name,
            "temperature": self.llm.temperature,
            "max_output_tokens": 16000,
            "purpose": "Generate production-ready backend code with 90+ quality score",
            "capabilities": [
                "FastAPI application generation",
                "Complete API endpoint creation",
                "Pydantic model generation",
                "Error handling implementation",
                "CORS configuration",
                "Data validation",
                "In-memory database setup"
            ]
        }