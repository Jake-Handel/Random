import google.generativeai as genai

# Configure the Gemini API
def configure_gemini(api_key):
    genai.configure(api_key=api_key)

# Function to get response from Gemini
def get_gemini_response(prompt):
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        response = model.generate_content(prompt)
        
        return {
            "status": "success",
            "message": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
