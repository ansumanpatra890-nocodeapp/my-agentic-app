import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

print("My key: ", os.getenv("GOOGLE_API_KEY"))
GEMINI_API_KEY = "AIzaSyDmeHYe0umNa4cm9tBPyM9YvWxr3vBX8hc"

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

response = llm.invoke("Hi , Gemini")
print("Response from Gemini:",response.content)

