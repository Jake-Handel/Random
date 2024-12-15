from flask import Flask, jsonify, request
from flask_cors import CORS
from gemini import configure_gemini, get_gemini_response
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('api_key.env')

app = Flask(__name__)
CORS(app)

# Configure Gemini with API key
api_key = os.getenv('GEMINI_API_KEY')
configure_gemini(api_key)

# Store conversations in memory (you might want to use a database in production)
conversations = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        try:
            data = request.json
            message = data.get('message', '')
            session_id = request.headers.get('X-Session-ID', 'default')
            
            # Initialize conversation history if it doesn't exist
            if session_id not in conversations:
                conversations[session_id] = []
            
            # Add user message to history
            conversations[session_id].append({
                'role': 'user',
                'content': message
            })
                        
            # Get response from Gemini with conversation history
            response = get_gemini_response(message, conversations[session_id])
            
            # Add assistant response to history
            conversations[session_id].append({
                'role': 'assistant',
                'content': response['message']
            })
            
            # Limit conversation history to last 10 messages
            conversations[session_id] = conversations[session_id][-10:]
            
            return jsonify(response)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Server error: {str(e)}"
            }), 500
    
    return jsonify({
        "message": "Hello! Send me a message using POST request.",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
