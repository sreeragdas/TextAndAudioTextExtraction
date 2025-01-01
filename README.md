# Image to Text Converter

This application allows users to upload an image or a ZIP file containing images. It processes the images using Optical Character Recognition (OCR) to extract text from them. The extracted text is then available for download as `.txt` files.

## Features
- Upload images (PNG, JPG, JPEG, BMP, TIFF) or ZIP files containing image files.
- Extract text from images using Tesseract OCR.
- Download extracted text as `.txt` files.
- Handle ZIP files by extracting and processing images inside.

## Requirements
- Python 3.x
- Tesseract OCR
- Streamlit
- Pillow (PIL Fork)
- pytesseract

## Installation

### Step 1: Install Dependencies

Clone the repository and install the required dependencies using `pip`:

```bash
git clone https://github.com/your-username/image-to-text-converter.git
cd image-to-text-converter
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
pip install -r requirements.txt
