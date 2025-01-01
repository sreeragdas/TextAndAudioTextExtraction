# Image to Text & Audio to Text Converter

This application allows users to upload images or audio files for transcription. It processes images using Optical Character Recognition (OCR) to extract text and audio files using the Wav2Vec2 model (from Hugging Face) for speech-to-text conversion. The extracted or transcribed text is then available for download as `.txt` files.

The audio transcription uses the **Wav2Vec2 Large 960h model** for converting speech to text.

## Features
- Upload images (PNG, JPG, JPEG, BMP, TIFF) or audio files (WAV) for transcription.
- Extract text from images using Tesseract OCR.
- Transcribe audio to text using the **Wav2Vec2 Large 960h model**.
- Download extracted or transcribed text as `.txt` files.

## Requirements
- Python 3.x
- Tesseract OCR (for image-to-text functionality)
- Hugging Face `transformers` library (for audio-to-text functionality)
- Streamlit (for UI)
- Pillow (PIL Fork)
- pytesseract
- librosa (for audio processing)
- torch (PyTorch)

## Installation

### Step 1: Install Dependencies

Clone the repository and install the required dependencies using `pip`:

```bash
git clone https://github.com/your-username/image-to-text-and-audio-to-text.git
cd image-to-text-and-audio-to-text
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
pip install -r requirements.txt
