import os
from typing import List, Optional
from huggingface_hub import InferenceClient

# Assuming this import works in your local environment based on your description
try:
    from rag.retriever import retrieve_relevant_passages
except ImportError:
    # Fallback for testing if the module is missing
    print("Warning: 'rag.retriever' not found. Using dummy retriever.")
    def retrieve_relevant_passages(query):
        return ["Context passage 1 placeholder", "Context passage 2 placeholder"]

def tool_retrieve(query: str) -> List[str]:
    """
    Retrieves relevant passages based on the query.
    """
    try:
        results = retrieve_relevant_passages(query)
        # Ensure results is a list of strings
        if not results:
            return []
        return results
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

def tool_answer(question: str, context: str, client: InferenceClient, model_name: str, language: str) -> str:
    """
    Generates an answer using the LLM based on context and language.
    """
    
    # تعليمات أكثر ذكاءً للتعامل مع التحيات والنصوص غير المرتبطة
    system_instruction = (
        f"You are a helpful academic assistant using a specific knowledge base (Context). "
        f"The user requires the answer in: {language}. "
        f"Instructions: "
        f"1. If the user says a greeting (like 'hello', 'hi'), ignore the context and reply with a polite greeting in {language} offering help. "
        f"2. Use the provided Context ONLY if it answers the specific question. "
        f"3. If the Context is not relevant to the Question, say 'I cannot find information about this in my documents' in {language}. "
        f"4. Do NOT say 'You provided text', refer to it as 'the available information'. "
    )

    user_message = f"Context provided by system:\n{context}\n\nUser Question:\n{question}"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1024,
            temperature=0.3,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def tool_evaluate(question: str, answer: str, client: InferenceClient, model_name: str, language: str) -> str:
    """
    Evaluates the generated answer for accuracy and relevance.
    """
    
    system_instruction = (
        f"You are an evaluator. Evaluate the answer provided. "
        f"Output must be in this language: {language}. "
        f"Format strictly:\n"
        f"Score: [1-5]\n"
        f"Reason: [Short explanation]"
    )

    user_message = f"Original Question: {question}\nGenerated Answer: {answer}"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            max_tokens=512,
            temperature=0.1,  # Low temperature for strict evaluation
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating evaluation: {str(e)}"