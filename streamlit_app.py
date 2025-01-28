import streamlit as st
from PIL import Image
import logging
import warnings
from openai import OpenAI
from transformers import pipeline

# Suppress specific warnings
warnings.filterwarnings("ignore")

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
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    logger.info("Image captioning model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load image captioning model: {e}")
    image_to_text = None

# Streamlit App
st.title("Chat and Image Captioning App")

# Sidebar options
st.sidebar.title("Choose an option")
method = st.sidebar.selectbox("Select a method", ["Chat (Text Generation)", "Image Captioning"])

if method == "Chat (Text Generation)":
    st.header("Text Generation")
    text_input = st.text_area("Enter your text:")
    if st.button("Generate"):
        if client and text_input:
            try:
                messages = [{"role": "user", "content": text_input}]
                completion = client.chat.completions.create(
                    model="microsoft/Phi-3.5-mini-instruct",
                    messages=messages,
                    max_tokens=4069
                )
                generated_content = completion.choices[0].message.content

                # Ensure complete sentence
                if not generated_content.endswith(('.', '!', '?')):
                    generated_content = generated_content.rsplit('.', 1)[0] + '.'

                st.success("Generated Text:")
                st.write(generated_content)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Text input is empty or OpenAI client is unavailable.")

elif method == "Image Captioning":
    st.header("Image Captioning")
    uploaded_image = st.file_uploader("Upload an image", type=["jpeg", "jpg", "png", "bmp", "gif"])
    if st.button("Generate Caption"):
        if uploaded_image and image_to_text:
            try:
                # Open the image file
                image = Image.open(uploaded_image)

                # Validate and generate caption
                if image.format not in ["JPEG", "PNG", "BMP", "GIF"]:
                    st.error("Unsupported image format. Please upload JPEG, PNG, BMP, or GIF.")
                else:
                    result = image_to_text(image)
                    caption = result[0]['generated_text'] if result else "No caption could be generated."
                    st.success("Generated Caption:")
                    st.write(caption.capitalize())
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("No image uploaded or captioning pipeline unavailable.")
