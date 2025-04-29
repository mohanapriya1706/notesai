from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.environ.get('GOOGLE_GENAI_API_KEY')

if not API_KEY:
    raise ValueError("GOOGLE_GENAI_API_KEY environment variable is not set")

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        client = genai.Client(api_key=API_KEY)
        data = request.json
        print(data)
        if 'key_points' not in data:
            return jsonify({'error': 'Missing required parameter: contents'}), 400
        
        contents = data['key_points']
        model =  'gemini-2.0-flash'
        
        response = client.models.generate_content(model=model, contents=contents)
        print(response.text)
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)