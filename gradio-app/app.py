"""
Gradio Text Classification Demo
This script demonstrates a Gradio interface for text classification using a provided prediction API.

It allows users to input text and get predictions for whether the input text is related to a natural disaster or not.

Dependencies:
- gradio: A library for creating interactive UI components.
- requests: A library for making HTTP requests.

Environment Variables:
- PREDICT_API_URL: The URL of the prediction API.

Usage:
- Set the PREDICT_API_URL environment variable to the URL of your prediction API.
- Run this script to launch the Gradio interface.

Note: The API should expect a 'data' parameter with the text to predict on and return a JSON response with a 'prediction' key.

Author: Sushant Khattar
"""

import os

import gradio as gr
import requests

API_URL = os.getenv('PREDICT_API_URL')


def predict(text):
    """
    Predict Function
    Make a prediction using the prediction API.

    Args:
        text (str): Input text to predict on.

    Returns:
        str: Prediction result indicating whether the text is sarcastic or not.
    """
    query_params = {'data': text}
    response = requests.get(API_URL, params=query_params, timeout=60).json()
    return response['prediction']



with gr.Blocks() as demo:
    with gr.Row(equal_height=False):
        with gr.Column():
            text = gr.Textbox(
                lines=3, label="Text Input", info="Enter you input text here..."
            )
            predict_btn = gr.Button("Predict")
        output = gr.Textbox(lines=1, label="Output prediction")

    predict_btn.click(fn=predict, inputs=text, outputs=output)

    examples = gr.Examples(
        [
            "Wow, I just love being stuck in traffic for hours!",
            "Great, another software update that will totally not ruin everything.",
            "Oh sure, I'd love to work overtime on a Friday night.",
        ],
        inputs=text,
    )


demo.launch()
