import os
import gradio as gr
import requests
import random
import speech_recognition as sr

API_URL = os.getenv('PREDICT_API_URL')

# List of fun responses for sarcastic and non-sarcastic predictions
sarcastic_responses = [
    "Oh, how delightfully sarcastic! You must be a joy at parties.",
    "Sarcasm detected! Your wit is as sharp as a butter knife.",
    "Congratulations! You've mastered the art of not saying what you mean.",
    "Ah, sarcasm - the body's natural defense against stupidity.",
    "Warning: Sarcasm levels are off the charts!"
]

non_sarcastic_responses = [
    "No sarcasm detected. How refreshingly honest!",
    "Straight talk, no chaser. I appreciate your directness.",
    "A sarcasm-free zone. How rare and wonderful!",
    "No hidden meanings here. You're as clear as a summer sky.",
    "Zero sarcasm found. Are you feeling alright?"
]

def predict(text):
    """
    Predict Function
    Make a prediction using the prediction API.

    Args:
        text (str): Input text to predict on.

    Returns:
        tuple: (Original prediction, Fun response)
    """
    query_params = {'data': text}
    response = requests.get(API_URL, params=query_params, timeout=60).json()
    prediction = response['prediction']
    
    if prediction == "sarcastic":
        pred="Sarcastic"
        fun_response = random.choice(sarcastic_responses)
    else:
        pred="Non-sarcastic"
        fun_response = random.choice(non_sarcastic_responses)
    
    return f"Prediction: {pred}", fun_response

def transcribe(audio):
    """
    Transcribe Function
    Transcribe audio input to text using Google's Speech Recognition.

    Args:
        audio: Audio input from Gradio.

    Returns:
        str: Transcribed text.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"

def process_audio(audio):
    """
    Process Audio Function
    Transcribe audio and then predict sarcasm.

    Args:
        audio: Audio input from Gradio.

    Returns:
        tuple: (Original prediction, Fun response, Transcribed text)
    """
    text = transcribe(audio)
    prediction, fun_response = predict(text)
    return prediction, fun_response, f"Transcribed: {text}"

with gr.Blocks() as demo:
    gr.Markdown("# 🎭 Sarcasm Detector Extraordinaire")
    gr.Markdown("Unleash your wit and let's see if we can catch that sarcasm!")
    
    with gr.Tabs() as tabs:
        with gr.TabItem("Text Input") as text_tab:
            text_input = gr.Textbox(
                lines=3, label="Your Potentially Sarcastic Text", 
                placeholder="Type your sarcastic (or not) message here..."
            )
            text_button = gr.Button("Analyze Text")
        
        with gr.TabItem("Voice Input") as audio_tab:
            audio_input = gr.Audio(type="filepath", label="Speak Your Sarcasm")
            audio_button = gr.Button("Analyze Speech")
            transcription_output = gr.Textbox(lines=2, label="Transcription")
    
    with gr.Row():
        prediction_output = gr.Textbox(lines=1, label="Prediction")
        fun_output = gr.Textbox(lines=2, label="Sarcasm Analysis")
    
        
    text_button.click(fn=predict, inputs=text_input, outputs=[prediction_output, fun_output])
    audio_button.click(fn=process_audio, inputs=audio_input, outputs=[prediction_output, fun_output, transcription_output])
    
    
    gr.Markdown("## Examples to Get You Started")
    examples = gr.Examples(
        [
            "Wow, I just love being stuck in traffic for hours!",
            "Great, another software update that will totally not ruin everything.",
            "The weather is perfect for a picnic today.",
            "Your outfit looks amazing today!",
            "Oh, just what I wanted—a flat tire on my way to work!",
            "Oh sure, I'd love to work overtime on a Friday night.",
        ],
        inputs=text_input,
    )

demo.launch()
