
"""
Code Deployment Agent - Deploys code to local server
Handles process management and deployment
"""

import subprocess
import tempfile
import os
import shutil
import asyncio
from typing import Dict


class CodeDeploymentAgent:
    """Agent responsible for deploying and running generated applications"""
    
    def __init__(self):
        self.name = "Code Deployment Agent"
        self.temp_dir = None
        self.process = None
    
    async def deploy(self, backend_code: str, frontend_code: str, project_id: str) -> Dict:
        """
        Deploys the generated code to local server
        
        Args:
            backend_code: Generated backend Python code
            frontend_code: Generated frontend HTML code
            project_id: Unique project identifier
            
        Returns:
            Dict containing deployment information and URLs
        """
        try:
            # Create temporary directory for project
            self.temp_dir = tempfile.mkdtemp(prefix=f"poc_{project_id}_")
            
            # Save backend code
            backend_file = os.path.join(self.temp_dir, "main.py")
            with open(backend_file, "w", encoding="utf-8") as f:
                # Ensure code runs on port 8080
                if "uvicorn" in backend_code and "uvicorn.run" not in backend_code:
                    backend_code += '\n\nif __name__ == "__main__":\n    import uvicorn\n    uvicorn.run(app, host="0.0.0.0", port=8080)'
                f.write(backend_code)
            
            # Save frontend code
            frontend_file = os.path.join(self.temp_dir, "index.html")
            with open(frontend_file, "w", encoding="utf-8") as f:
                f.write(frontend_code)
            
            # Install dependencies
            await self._install_dependencies()
            
            # Start the backend server
            self.process = subprocess.Popen(
                ["python", backend_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.temp_dir,
                text=True
            )
            
            # Wait for server to start
            await asyncio.sleep(3)
            
            # Check if server is running
            if self.process.poll() is None:
                return {
                    "status": "success",
                    "agent": self.name,
                    "output": {
                        "backend_url": "http://localhost:8080",
                        "frontend_path": frontend_file,
                        "temp_dir": self.temp_dir,
                        "process_id": self.process.pid,
                        "message": "Application deployed successfully on port 8080",
                        "project_id": project_id
                    }
                }
            else:
                # Server failed to start
                stderr = self.process.stderr.read() if self.process.stderr else "Unknown error"
                return {
                    "status": "error",
                    "agent": self.name,
                    "output": {
                        "message": f"Server failed to start: {stderr}",
                        "project_id": project_id
                    }
                }
                
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "output": {
                    "message": f"Deployment failed: {str(e)}",
                    "project_id": project_id
                }
            }
    
    async def _install_dependencies(self):
        """Install required Python dependencies"""
        try:
            requirements = ["fastapi", "uvicorn", "pydantic"]
            process = await asyncio.create_subprocess_exec(
                "pip", "install", "-q", *requirements,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except Exception as e:
            print(f"Warning: Failed to install dependencies: {e}")
    
    def stop(self):
        """Stop the running process"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
        
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def get_status(self) -> Dict:
        """Get current deployment status"""
        if self.process:
            is_running = self.process.poll() is None
            return {
                "running": is_running,
                "pid": self.process.pid if is_running else None,
                "temp_dir": self.temp_dir
            }
        return {"running": False, "pid": None, "temp_dir": None}
    
    def get_agent_info(self) -> Dict:
        """Returns agent information"""
        return {
            "name": self.name,
            "purpose": "Deploy and manage application instances"
        }