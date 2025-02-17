from langchain_google_genai import GoogleGenerativeAI
import os

class LLMBuilder(object):
    _instance = None

    def __init__(self):
        raise RuntimeError("Call build_llm() instead")

    @staticmethod
    def build_llm():
        if LLMBuilder._instance is None:
            # Set the environment variable for Google API key
            LLMBuilder._instance = GoogleGenerativeAI(
                temperature=0.1,
                model="gemini-2.0-flash-001",
                api_key=os.getenv("GOOGLE_API_KEY")
            )

        return LLMBuilder._instance