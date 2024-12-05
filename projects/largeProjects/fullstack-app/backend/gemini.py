import google.generativeai as genai

# Configure the Gemini API
def configure_gemini(api_key):
    genai.configure(api_key=api_key)

# Function to get response from Gemini
def get_gemini_response(prompt, history=None):
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare conversation history
        if history:
            formatted_history = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in history[:-1]
            ])
            
            # Enhanced prompt with more specific formatting instructions
            full_prompt = (
                "You are a helpful AI assistant. Follow these formatting rules:\n"
                "1. Respond directly without prefixing responses with 'Assistant:', 'Agent:', etc.\n"
                "2. For mathematical expressions:\n"
                "   - Write equations using plain text (e.g., 'x^2' instead of '$x^2$')\n"
                "   - Use ^ for exponents, * for multiplication\n"
                "   - Don't use LaTeX/MathJax delimiters (no $ or $$)\n"
                "   - For functions, write f(x) instead of $f(x)$\n"
                "3. Format mathematical solutions clearly with line breaks and indentation\n\n"
                f"{formatted_history}\n\nUser: {prompt}"
            )
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Clean up response
        response_text = response.text
        
        # Remove prefixes
        prefixes_to_remove = ["Assistant:", "Agent:", "A:"]
        for prefix in prefixes_to_remove:
            if response_text.startswith(prefix):
                response_text = response_text[len(prefix):].strip()
        
        # Remove LaTeX delimiters and clean up mathematical formatting
        response_text = response_text.replace('$', '')  # Remove single $
        response_text = response_text.replace('\\', '')  # Remove LaTeX escape characters
        
        # Clean up common LaTeX commands
        latex_commands = [
            'begin{equation}', 'end{equation}',
            'begin{align}', 'end{align}',
            'text', 'mathbf', 'mathrm'
        ]
        for cmd in latex_commands:
            response_text = response_text.replace(f'{cmd}', '')
        
        return {
            "status": "success",
            "message": response_text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
