import os
import torch
import streamlit as st
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa

# Load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# Function to transcribe audio file
def transcribe_audio(audio_file_path):
    # Load audio file using librosa (ensure audio is sampled at 16kHz)
    audio_input, _ = librosa.load(audio_file_path, sr=16000)

    # Preprocess audio to be compatible with the model
    input_values = processor(audio_input, return_tensors="pt", padding=True).input_values

    # Get model predictions (logits)
    with torch.no_grad():
        logits = model(input_values).logits

    # Decode the predicted ids to text
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])

    return transcription

# Streamlit UI
st.title("Audio Transcription with Wav2Vec2")
st.write("Upload an audio file, and the transcription will be displayed below:")

# File uploader to upload audio
audio_file = st.file_uploader("Choose an audio file", type=["wav"])

if audio_file:
    # Saving uploaded audio to the specified path
    upload_folder = r"E:\python\TextExtraction\UploadedFolder"
    os.makedirs(upload_folder, exist_ok=True)
    audio_file_path = os.path.join(upload_folder, audio_file.name)

    # Save the audio file
    with open(audio_file_path, "wb") as f:
        f.write(audio_file.getbuffer())

    # Transcribe audio
    transcription = transcribe_audio(audio_file_path)

    # Display transcription on UI
    st.subheader("Transcription:")
    st.write(transcription)

    # Save transcription to the specified output folder
    output_folder = r"E:\python\TextExtraction\TextOutput"
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f"{os.path.splitext(audio_file.name)[0]}.txt")

    # Save transcription as text file
    with open(output_file_path, "w") as f:
        f.write(transcription)

    st.write(f"Transcription saved to: {output_file_path}")
else:
    st.write("Please upload an audio file to begin transcription.")
