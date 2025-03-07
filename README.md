# FashionSense AI Chatbot

A web-based AI fashion stylist chatbot that provides recommendations for color combinations and graphics for clothing. Built with Flask and Ollama, using the Deepseek 7B model.

## Prerequisites

1. Python 3.8 or higher
2. Ollama installed and running on your system
3. The Deepseek model (already installed)

## Setup Instructions

1. Install Ollama if you haven't already:
   - Visit [Ollama's website](https://ollama.ai/) and follow the installation instructions

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure Ollama is running in the background:
   ```bash
   ollama run deepseek-r1:7b
   ```

4. Start the Flask application:
   ```bash
   python app.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Features

- Modern, responsive web interface
- Real-time chat interactions
- Expert recommendations for:
  - Color combinations with specific HEX codes
  - Graphic design elements for clothing
  - Pattern and texture combinations
  - Fashion styling advice

## Usage

Simply type your fashion-related questions into the chat interface. For example:
- "What colors would go well with a navy blue blazer?"
- "Suggest a color palette for a summer casual outfit"
- "What graphic patterns would work for a streetwear t-shirt?"

## Note

The chatbot uses the Ollama API running locally on port 11434. Make sure this port is available and Ollama is running before starting the application.
