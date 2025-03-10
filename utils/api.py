# utils/api.py
from google import genai

def configure_api(api_key):
    """Configure the Gemini API with the provided key."""
    return api_key is not None and api_key != ""

def call_gemini_api(prompt, api_key):
    """
    Call the Gemini 2.0 Flash model with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the model
        api_key (str): The API key for Gemini
        
    Returns:
        str: The generated text response
    """
    if not configure_api(api_key):
        return None
    
    try:
        # Create a client with the user's API key
        client = genai.Client(api_key=api_key)
        
        # Call the Gemini 2.0 Flash model specifically
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Return the text response
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"
