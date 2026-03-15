import os
from openai import OpenAI

def get_explanation(bug_info, code_snippet, api_key):
    """
    Uses GPT to explain the bug and suggest a fix.
    """
    if not api_key:
        return "Error: OpenAI API Key is missing.", None

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an expert ML Code Auditor.
    You found this bug in a user's Jupyter Notebook:
    Bug Type: {bug_info['type']}
    Severity: {bug_info['severity']}
    Message: {bug_info['message']}
    
    Here is the relevant code snippet:
    {code_snippet}
    
    Please provide:
    1. A simple explanation of why this is a problem.
    2. The CORRECTED code snippet only (no extra text).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful senior ML engineer."},
                {"role": "user", "content": prompt}
            ]
        )
        full_response = response.choices[0].message.content
        
        # Simple logic to split explanation and code
        # We assume the last code block in the response is the fix
        parts = full_response.split("```python")
        explanation = parts[0].strip()
        
        fixed_code = None
        if len(parts) > 1:
            code_part = parts[1].split("```")[0].strip()
            fixed_code = code_part
            
        return explanation, fixed_code

    except Exception as e:
        return f"Could not generate explanation (API Error): {str(e)}", None
    
    