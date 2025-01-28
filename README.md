# Chatbot_using_LLM
This project is a web-based application that allows users to interact with an AI chatbot capable of two primary functions:

## Text Generation:

Users can input text queries to the chatbot for conversational or generative responses.
The backend processes the text using a language model to generate responses.

## Image Captioning:

Users can upload images, and the application generates descriptive captions.
The backend processes the image using a pre-trained image-to-text model.

## Features:

A visually appealing frontend (HTML/CSS/JavaScript) with options to toggle between text and image input.
Backend services powered by Python (Flask framework) to handle requests, process inputs, and generate outputs.
Integration with modern machine learning tools for natural language processing and computer vision.
Error handling and logging to ensure smooth functionality and easy debugging.

## Use Cases:

Chatbots for customer support.
Educational tools for generating explanations or captions.
Fun or exploratory AI applications for understanding modern machine learning capabilities.
Information About Large Language Models (LLMs)

## LLMs Overview:

Definition: Large Language Models are advanced machine learning models trained on vast amounts of text data to understand and generate human-like language.
Capabilities:
Text understanding and generation.
Summarization, translation, and content creation.
Answering questions and engaging in conversations.
LLM in This Project:

# This project uses OpenAI's API, integrated with the microsoft/Phi-3.5-mini-instruct model.
## Phi-3.5-mini-instruct:
A compact and efficient model for conversational AI and text generation.
Optimized for generating concise and relevant responses within token limits.
Designed to handle instruction-following tasks in natural language.
Text Generation Details:

## Workflow:
User input is collected and sent to the backend.
The backend passes the input to the OpenAI API.
The model generates a response based on the input.
The response is sent back to the frontend and displayed in the chatbox.

## Image Captioning Model:

Uses the Salesforce BLIP (Bootstrapped Language-Image Pretraining) model for generating captions.
Trained on visual and textual data, the model generates descriptive captions by analyzing images.
