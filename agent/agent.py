import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Import tools from the local file (assuming tools.py is in the same directory)
try:
    from .tools import tool_retrieve, tool_answer, tool_evaluate
except ImportError:
    # Fallback if running directly without package structure
    from tools import tool_retrieve, tool_answer, tool_evaluate

# Load environment variables
load_dotenv()

class SimpleAgent:
    def __init__(self):
        """
        Initialize the agent with the API client and model configuration.
        """
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not api_key:
            print("Error: HUGGINGFACE_API_KEY not found in .env file.")
            sys.exit(1)

        self.client = InferenceClient(api_key=api_key)
        # Using Llama 3.1 Instruct
        self.model = "meta-llama/Llama-3.1-8B-Instruct"

    def ask(self, question: str, language: str = "en"):
        """
        The main workflow: Retrieve -> Answer -> Evaluate.
        
        Args:
            question (str): The user's query.
            language (str): 'ar' for Arabic, 'en' for English.
        """
        print(f"--- Processing Query (Language: {language}) ---")
        
        # 1. Retrieve
        passages = tool_retrieve(question)
        
        if not passages:
            return "No relevant context found.", "Score: 0\nReason: No context retrieved."
        
        context = "\n\n".join(passages)
        
        # 2. Answer
        answer = tool_answer(question, context, self.client, self.model, language)
        
        # 3. Evaluate
        evaluation = tool_evaluate(question, answer, self.client, self.model, language)

        return answer, evaluation

# Optional: Simple test block if you run this file directly
if __name__ == "__main__":
    agent = SimpleAgent()
    ans, ev = agent.ask("What is the main topic?", language="en")
    print(f"\nAnswer:\n{ans}")
    print(f"\nEvaluation:\n{ev}")