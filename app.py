# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# from flask import Flask, render_template, request, jsonify

# load_dotenv()
# genai.configure(api_key=os.getenv("Gemini_Api_Key"))

# # Create the model
# generation_config = {
#     "temperature": 1.2,
#     "top_p": 0.95,
#     "top_k": 60,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config,
# )

# def GenerateResponse(input_text):
#     response = model.generate_content([
#         "You are a puzzle solver AI",
#         f"input: {input_text}",
#         "output: ",
#     ])
#     return response.text

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     input_text = request.form['input_text']
#     print(f"Received input: {input_text}")  # Debugging line
#     output = GenerateResponse(input_text)
#     return jsonify({'response': output})


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini AI API key
genai.configure(api_key=os.getenv("Gemini_Api_Key"))

# Flask App
app = Flask(__name__)

# Create the model configuration
generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 60,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the AI model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# To store the conversation history (globally)
conversation_history = []

def GenerateResponse(input_text):
    # Include previous conversation history in the prompt
    prompt = "You are an AI designed to solve puzzles. Please only respond with answers to puzzles and refrain from answering non-puzzle-related questions. If a question is not a puzzle, kindly reply with 'Please give me a puzzle.' For puzzle-related queries, provide answers in a clear, courteous, and well-structured manner. Here is the conversation history:[Include previous conversation here]\n"
    # Add previous conversation to the prompt (if any)
    for user_input, ai_response in conversation_history:
        prompt += f"User: {user_input}\nAI: {ai_response}\n"
    
    # Add the current user input
    prompt += f"User: {input_text}\nAI:"
    
    # Generate the AI's response
    response = model.generate_content([prompt])
    return response.text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.form['input_text']
    print(f"Received input: {input_text}")  # Debugging line to check input
    # Get AI response based on the current conversation history
    output = GenerateResponse(input_text)
    
    # Store the user input and AI output to the conversation history
    conversation_history.append((input_text, output))
    
    # Return the response
    return jsonify({'response': output})

if __name__ == '__main__':
    app.run(debug=True)
