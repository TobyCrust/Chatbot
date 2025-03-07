from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import requests
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Custom system prompt for the fashion stylist persona
SYSTEM_PROMPT = """You are FashionSense AI, an expert fashion stylist with a keen eye for color combinations and graphic design in clothing. 
You specialize in:
- Creating harmonious color palettes for outfits
- Suggesting graphic design elements for clothing
- Providing modern and trendy fashion advice
- Understanding color theory and its application in fashion
- Recommending complementary patterns and textures

Always provide specific, actionable advice with exact color codes (HEX) when discussing colors.
Keep responses concise but informative, and maintain a friendly, professional tone.
Keep responses under 3 sentences.
Never explain your thinking process, just provide the answer directly."""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Combine system prompt with user message
    prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
    
    def generate():
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": prompt,
                    "stream": True
                },
                stream=True
            )
            response.raise_for_status()
            
            # Skip initial thinking/processing text
            buffer = ""
            started_response = False
            
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        current_text = json_response['response']
                        buffer += current_text
                        
                        # Only start yielding once we have a complete sentence or substantial content
                        if not started_response and ('.' in buffer or len(buffer) > 20):
                            started_response = True
                        
                        if started_response:
                            yield f"data: {json.dumps({'response': current_text})}\n\n"
                            
                    if json_response.get('done', False):
                        break
                        
        except requests.exceptions.ConnectionError:
            logging.error("Could not connect to Ollama API. Please ensure Ollama is installed and running.")
            yield f"data: {json.dumps({'error': 'Could not connect to Ollama. Please make sure Ollama is installed and running with the command: ollama run deepseek-r1:1.5b'})}\n\n"
            
        except requests.exceptions.Timeout:
            logging.error("Request to Ollama API timed out")
            yield f"data: {json.dumps({'error': 'Request to Ollama timed out. Please try again.'})}\n\n"
        
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            yield f"data: {json.dumps({'error': f'An unexpected error occurred: {str(e)}'})}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
