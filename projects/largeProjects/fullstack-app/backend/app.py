from flask import Flask, jsonify, request
from flask_cors import CORS
from gemini import configure_gemini, get_gemini_response
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('api_key.env')

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "X-Session-ID"]
    }
})

# Configure Gemini with API key
api_key = os.getenv('GEMINI_API_KEY')
configure_gemini(api_key)

# Store conversations in memory (you might want to use a database in production)
conversations = {}

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route('/api', methods=['GET', 'POST'])
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
            
            # Get response from Gemini
            response = get_gemini_response(message, conversations[session_id])
            
            # Add assistant response to history
            conversations[session_id].append({
                'role': 'assistant',
                'content': response
            })
            
            # Limit conversation history to last 10 messages
            conversations[session_id] = conversations[session_id][-10:]
            
            return jsonify({
                'status': 'success',
                'message': response
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    return jsonify({"message": "Send a POST request with your message"})

@app.route('/api/todos', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        data = request.json
        return jsonify({"status": "success", "data": data})
    return jsonify({"todos": []})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
