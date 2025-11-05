# agents/ui_enrichment_agent.py
"""
UI Enrichment Agent - Creates production-ready frontend interfaces
Optimized for 90+ quality scores with complete implementations
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, List
import json
import re
from config import AppConfig


class UIEnrichmentAgent:
    """Advanced agent for creating production-ready frontend UIs"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp", temperature: float = 0.3):
        self.name = "UI Enrichment Agent"
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_output_tokens=16000,
            google_api_key=AppConfig.GEMINI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an ELITE Full-Stack Frontend Engineer and UI/UX Designer with 15+ years of experience.

Your mission: Generate COMPLETE, FLAWLESS, PRODUCTION-READY single-page HTML applications.

CRITICAL REQUIREMENTS - NON-NEGOTIABLE:

1. COMPLETE HTML STRUCTURE:
   - Proper DOCTYPE and HTML5 structure
   - Complete head with all meta tags
   - Responsive viewport meta tag
   - Page title relevant to application
   - Tailwind CSS CDN (latest version)
   - Google Fonts for professional typography
   - Complete body with all UI elements
   - NO TRUNCATION - code must be complete to closing html tag

2. CSS & STYLING (Embedded in head):
   - Custom CSS variables for theming
   - Modern design principles
   - Smooth transitions and animations
   - Hover effects and interactive feedback
   - Loading states and skeleton loaders
   - Modal and toast notification styles
   - Responsive breakpoints
   - Professional color scheme

3. HTML STRUCTURE (Complete body):
   - Navigation header with logo and menu
   - Main content area with proper sections
   - All forms and input fields needed
   - Buttons with clear actions
   - Data display areas (cards, lists, tables)
   - Loading indicators
   - Empty state messages
   - Modal containers
   - Toast notification area

4. JAVASCRIPT FUNCTIONALITY (Complete in script):
   - API_BASE_URL constant (http://localhost:8080)
   - State management variables
   - DOMContentLoaded event listener
   - API fetch functions with error handling
   - UI update functions
   - Event listeners for all interactions
   - Form submission handlers
   - Modal open/close functions
   - Toast notification system
   - Loading state management
   - Data rendering functions
   - Navigation functions
   - CRUD operations for all features
   - NO TRUNCATION - complete to closing script tag

5. API INTEGRATION:
   - Fetch API for all HTTP requests
   - Proper HTTP methods (GET, POST, PUT, DELETE)
   - JSON content-type headers
   - Error handling with try-catch
   - Loading states during API calls
   - Success/error feedback to user

6. USER EXPERIENCE:
   - Intuitive navigation
   - Clear call-to-action buttons
   - Form validation before submission
   - Immediate visual feedback
   - Loading indicators
   - Success/error messages
   - Smooth transitions
   - Mobile-friendly design

OUTPUT FORMAT - STRICTLY ENFORCE:

DO NOT include:
   - Markdown code blocks (```html, ```)
   - Explanatory text
   - Comments like "Add more features here"
   - Placeholder comments
   - Truncated JavaScript code
   - Incomplete functions
   - Missing closing tags

DO provide:
   - Pure HTML code only
   - Complete from DOCTYPE to closing html
   - All CSS in style tags
   - All JavaScript in script tags
   - Functional, working implementation
   - All features fully implemented
   - Complete event listeners
   - Complete API functions

JAVASCRIPT COMPLETENESS CHECKLIST:

CRITICAL: JavaScript section must include ALL of these:

- Configuration constants (API_BASE_URL, USER_IDs, etc.)
- State variables (currentPage, cart, selectedItems, etc.)
- DOMContentLoaded event listener
- Element reference caching
- API Functions (fetch with error handling)
- UI Update Functions (render/display functions)
- Event Handlers (click, submit, change)
- Helper Functions (modals, toasts, formatting)
- Initialization (load initial data, setup listeners)
- COMPLETE closing script tag

EXAMPLE STRUCTURE:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Name</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
        }}
        .btn-primary {{
            background: #3b82f6;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
    </style>
</head>
<body class="bg-gray-50">
    
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <nav class="container mx-auto px-4 py-4">
            <h1 class="text-2xl font-bold">App Name</h1>
        </nav>
    </header>

    <main class="container mx-auto px-4 py-8">
        <div id="main-view">
            <h2 class="text-xl font-semibold mb-4">Content</h2>
            <div id="items-container"></div>
        </div>
    </main>

    <div id="toast" class="fixed bottom-4 right-4"></div>

    <script>
        const API_BASE_URL = 'http://localhost:8080';
        const CURRENT_USER_ID = 'user_001';
        
        let currentData = [];
        
        document.addEventListener('DOMContentLoaded', () => {{
            initializeApp();
        }});
        
        function initializeApp() {{
            setupEventListeners();
            loadInitialData();
        }}
        
        function setupEventListeners() {{
            document.getElementById('some-btn')?.addEventListener('click', handleClick);
        }}
        
        async function fetchData() {{
            try {{
                const response = await fetch(`${{API_BASE_URL}}/endpoint`);
                if (!response.ok) throw new Error('Failed to fetch');
                const data = await response.json();
                return data;
            }} catch (error) {{
                showToast('Error loading data', 'error');
                console.error(error);
            }}
        }}
        
        async function createItem(itemData) {{
            try {{
                const response = await fetch(`${{API_BASE_URL}}/items`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(itemData)
                }});
                if (!response.ok) throw new Error('Failed to create');
                showToast('Item created', 'success');
                return await response.json();
            }} catch (error) {{
                showToast('Error creating item', 'error');
                console.error(error);
            }}
        }}
        
        function renderItems(items) {{
            const container = document.getElementById('items-container');
            container.innerHTML = '';
            items.forEach(item => {{
                const div = document.createElement('div');
                div.className = 'bg-white p-4 rounded shadow mb-2';
                div.innerHTML = `<h3>${{item.name}}</h3>`;
                container.appendChild(div);
            }});
        }}
        
        function showToast(message, type = 'info') {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = `fixed bottom-4 right-4 p-4 rounded shadow bg-${{type === 'error' ? 'red' : 'green'}}-500 text-white`;
            setTimeout(() => toast.className = 'hidden', 3000);
        }}
        
        async function loadInitialData() {{
            const data = await fetchData();
            if (data) renderItems(data);
        }}
        
    </script>
</body>
</html>

Now generate the COMPLETE, PRODUCTION-READY frontend HTML code following ALL requirements above.
REMEMBER: The JavaScript section must be COMPLETE with NO TRUNCATION!"""),
            ("user", """Application Requirements:
{requirements}

Backend API Information:
{backend_info}

GENERATE THE COMPLETE, PRODUCTION-READY FRONTEND HTML CODE NOW.
Remember: NO markdown, NO explanations, ONLY complete HTML with CSS and JavaScript.""")
        ])
    
    async def generate_ui(self, requirements: Dict, backend_info: Dict) -> Dict:
        """
        Generates complete, production-ready frontend UI
        
        Args:
            requirements: Refined application requirements
            backend_info: Backend code information and endpoints
            
        Returns:
            Dict containing generated frontend code with metadata
        """
        try:
            chain = self.prompt | self.llm
            
            response = await chain.ainvoke({
                "requirements": json.dumps(requirements, indent=2),
                "backend_info": json.dumps(backend_info, indent=2)
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
                    "language": "html",
                    "framework": "HTML/CSS/JS",
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
                    "code": self._generate_fallback_ui(),
                    "language": "html",
                    "framework": "HTML/CSS/JS"
                }
            }
    
    def _clean_code(self, code: str) -> str:
        """Cleans generated code from markdown and extra text"""
        if "```html" in code:
            code = code.split("```html", 1)[1].split("```")[0].strip()
        elif "```" in code:
            parts = code.split("```")
            if len(parts) >= 3:
                code = parts[1].strip()
                if code.startswith('html\n'):
                    code = code[5:]
        
        prefixes_to_remove = ["html", "HTML", "Here's the code:", "Here is the code:", "Code:"]
        for prefix in prefixes_to_remove:
            if code.startswith(prefix):
                code = code[len(prefix):].strip()
        
        code = code.replace('\r\n', '\n')
        
        if not code.startswith('<!DOCTYPE') and not code.startswith('<!doctype'):
            code = '<!DOCTYPE html>\n' + code
        
        return code
    
    def _validate_code(self, code: str) -> Dict:
        """Validates generated code for completeness"""
        issues = []
        
        if '<!DOCTYPE' not in code and '<!doctype' not in code:
            issues.append("Missing DOCTYPE declaration")
        
        if '<html' not in code:
            issues.append("Missing html tag")
        
        if '</html>' not in code:
            issues.append("Missing closing html tag - CODE IS TRUNCATED!")
        
        if '<head>' not in code:
            issues.append("Missing head section")
        
        if '<title>' not in code:
            issues.append("Missing title tag")
        
        if 'tailwindcss' not in code.lower():
            issues.append("Missing Tailwind CSS CDN")
        
        if '<body' not in code:
            issues.append("Missing body tag")
        
        if '<script>' not in code and '<script ' not in code:
            issues.append("Missing script section")
        
        if '</script>' not in code:
            issues.append("Missing closing script tag - JavaScript is TRUNCATED!")
        
        if 'API_BASE_URL' not in code and 'fetch(' not in code:
            issues.append("Missing API integration")
        
        if 'DOMContentLoaded' not in code:
            issues.append("Missing DOMContentLoaded event listener")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "checks_passed": 11 - len(issues),
            "total_checks": 11
        }
    
    def _fix_common_issues(self, code: str, issues: List[str]) -> str:
        """Attempts to fix common issues in generated code"""
        if "Missing closing html" in str(issues) and '</html>' not in code:
            if '</body>' in code:
                code += '\n</html>'
            else:
                code += '\n</body>\n</html>'
        
        if "Missing closing script" in str(issues) and '</script>' not in code:
            code = code.replace('</body>', '</script>\n</body>')
        
        if "Missing DOCTYPE" in str(issues):
            if not code.startswith('<!DOCTYPE'):
                code = '<!DOCTYPE html>\n' + code
        
        return code
    
    def _calculate_quality_score(self, code: str) -> int:
        """Calculates quality score for generated code"""
        score = 0
        
        if all(tag in code for tag in ['<!DOCTYPE', '<html', '</html>', '<head>', '<body>']):
            score += 15
        
        if 'tailwindcss' in code.lower():
            score += 10
        if '<style>' in code:
            score += 5
        
        if '<script>' in code or '<script ' in code:
            score += 10
        if '</script>' in code:
            score += 10
        
        if 'fetch(' in code:
            score += 10
        if 'API_BASE_URL' in code or 'localhost:8080' in code:
            score += 5
        
        if 'addEventListener' in code:
            score += 10
        
        ui_elements = ['button', 'form', 'input', 'modal', 'toast']
        present_elements = sum(1 for el in ui_elements if el in code.lower())
        score += min(10, present_elements * 2)
        
        if 'try' in code and 'catch' in code:
            score += 10
        
        if '</html>' in code and '</script>' in code:
            score += 5
        
        return min(score, 100)
    
    def _generate_fallback_ui(self) -> str:
        """Generates basic fallback UI if generation fails"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-4">Application Running</h1>
        <p class="text-gray-600">Frontend loaded in fallback mode.</p>
        <div id="status" class="mt-4 p-4 bg-white rounded shadow"></div>
    </div>
    
    <script>
        const API_BASE_URL = 'http://localhost:8080';
        
        document.addEventListener('DOMContentLoaded', async () => {
            try {
                const response = await fetch(API_BASE_URL);
                const data = await response.json();
                document.getElementById('status').innerHTML = 
                    `<p class="text-green-600">Backend API is running</p>
                     <pre class="mt-2 text-sm">${JSON.stringify(data, null, 2)}</pre>`;
            } catch (error) {
                document.getElementById('status').innerHTML = 
                    `<p class="text-red-600">Could not connect to backend</p>
                     <p class="text-sm mt-2">Error: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>"""
    
    def get_agent_info(self) -> Dict:
        """Returns detailed agent information"""
        return {
            "name": self.name,
            "model": self.llm.model_name,
            "temperature": self.llm.temperature,
            "max_output_tokens": 16000,
            "purpose": "Generate production-ready frontend UIs with 90+ quality score",
            "capabilities": [
                "Complete HTML5 applications",
                "Responsive Tailwind CSS design",
                "Full JavaScript functionality",
                "API integration",
                "Error handling",
                "Loading states",
                "Toast notifications",
                "Modal dialogs",
                "Form validation",
                "CRUD operations"
            ]
        }