from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import os
load_dotenv()

llm=GoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)