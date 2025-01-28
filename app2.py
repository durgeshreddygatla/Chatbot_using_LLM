from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
import logging
import pyttsx3
import os
import warnings
import speech_recognition as sr
from io import BytesIO
from openai import OpenAI

# Suppress specific warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client for text generation
try:
    client = OpenAI(
        base_url="https://api-inference.huggingface.co/v1/",
        api_key="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"
    )
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

# Load image captioning model
try:
    from transformers import pipeline
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    logger.info("Image captioning model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load image captioning model: {e}")
    image_to_text = None

@app.route('/')
def home():
    """Render home page with input options."""
    return render_template("index2.html")  # Ensure `index2.html` is in the `templates` folder

@app.route('/process', methods=['POST'])
def process_input():
    """Process input based on the selected method."""
    method = request.form.get('method') or request.json.get('method')

    if not method:
        return jsonify({'error': 'No method provided. Please specify "chat" or "caption-image".'}), 400

    if method == 'text-generation':
        text = request.form.get('text') or request.json.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        if not client:
            return jsonify({'error': 'OpenAI client is not available.'}), 500

        try:
            messages = [{"role": "user", "content": text}]
            completion = client.chat.completions.create(
                model="microsoft/Phi-3.5-mini-instruct",
                messages=messages,
                max_tokens=4069
            )
            generated_content = completion.choices[0].message.content

            # Check for incomplete sentence
            if not generated_content.endswith(('.', '!', '?')):
                generated_content = generated_content.rsplit('.', 1)[0] + '.'

            return jsonify({'Generated text': generated_content})
        except Exception as e:
            logger.error(f"Chat Error: {str(e)}")
            return jsonify({'error': 'Chat processing failed. Please try again later.'}), 500

    elif method == 'caption-image':
        if 'image' not in request.files:
            return jsonify({'error': 'No image file uploaded.'}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected.'}), 400

        if not image_to_text:
            return jsonify({'error': 'Image captioning pipeline is not available.'}), 500

        try:
            # Open the image file
            image = Image.open(image_file)

            # Validate the image format
            if image.format not in ["JPEG", "PNG", "BMP", "GIF"]:
                return jsonify({'error': 'Unsupported image format. Please upload JPEG, PNG, BMP or GIF.'}), 400

            # Generate a caption for the image
            result = image_to_text(image)
            caption = result[0]['generated_text'] if result else "No caption could be generated."
            caption = caption.capitalize()
            return jsonify({'caption': caption})
        except Exception as e:
            logger.error(f"Image Captioning Error: {str(e)}")
            return jsonify({'error': 'Failed to generate a caption. Please try again later.'}), 500

    else:
        return jsonify({'error': f'Invalid method "{method}". Please select "chat" or "caption-image".'}), 400

if __name__ == '__main__':
    app.run(debug=True)
