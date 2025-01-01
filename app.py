import streamlit as st
import os
import zipfile
from PIL import Image
import pytesseract
from io import BytesIO
# Configure the Tesseract executable path (for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Folder paths to save extracted files

uploaded_folder = r"E:\python\TextExtraction\UploadedFolder"
input_images_folder = r"E:\python\TextExtraction\InputImages"
text_output_folder = r"E:\python\TextExtraction\TextOutput"

# Streamlit App Title
st.title("Image to Text Converter")

# File Upload via Streamlit (Single option to upload both ZIP or image)
uploaded_file = st.file_uploader("Upload an image or ZIP file", type=["zip", "png", "jpg", "jpeg", "bmp", "tiff"])

# If a ZIP file is uploaded
if uploaded_file is not None and uploaded_file.name.endswith('.zip'):
    # Save the uploaded ZIP file temporarily in the specified folder
    zip_path = os.path.join(uploaded_folder, uploaded_file.name)
    os.makedirs(uploaded_folder, exist_ok=True)
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract ZIP contents
    extracted_files = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Extract all contents into a folder, preserving the directory structure
            extraction_folder = os.path.join(uploaded_folder, "extracted")
            os.makedirs(extraction_folder, exist_ok=True)
            zip_ref.extractall(extraction_folder)

            # List the extracted files and directories
            extracted_files = []
            for root, dirs, files in os.walk(extraction_folder):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                        extracted_files.append(os.path.join(root, file))

    except zipfile.BadZipFile:
        st.error("The file uploaded is not a valid ZIP file.")
    
    if extracted_files:
        # Display folder icon for ZIP file
        st.subheader("Extracted Images from ZIP File:")
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/26/Folder_icon_%28Black%29.svg", caption="Folder Icon", width=100)

        # Provide download button for the text file
        download_zip_text = []
        for file_path in extracted_files:
            # Get the relative path of the file within the ZIP (preserving directory structure)
            relative_path = os.path.relpath(file_path, extraction_folder)
            base_name = os.path.basename(file_path)

            # Save the image to the InputImages folder (preserving the directory structure)
            image_output_path = os.path.join(input_images_folder, relative_path)
            os.makedirs(os.path.dirname(image_output_path), exist_ok=True)
            
            # Handle file conflicts: Check if the file already exists
            if os.path.exists(image_output_path):
                # If file exists, create a new file name by adding a suffix
                base, ext = os.path.splitext(image_output_path)
                counter = 1
                new_image_output_path = f"{base}_{counter}{ext}"
                while os.path.exists(new_image_output_path):
                    counter += 1
                    new_image_output_path = f"{base}_{counter}{ext}"
                image_output_path = new_image_output_path

            # Move the image to InputImages folder
            os.rename(file_path, image_output_path)

            # Perform OCR to extract text
            image = Image.open(image_output_path)
            extracted_text = pytesseract.image_to_string(image)

            # Save extracted text to TextOutput folder (preserving the directory structure)
            text_output_path = os.path.join(text_output_folder, relative_path + ".txt")
            os.makedirs(os.path.dirname(text_output_path), exist_ok=True)
            with open(text_output_path, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)

            # Add to the list of text files for download
            with open(text_output_path, "r") as text_file:
                download_zip_text.append((relative_path, text_file.read()))
        
        # Provide a download button for the ZIP text files
        if download_zip_text:
            for file_name, text in download_zip_text:
                st.download_button(
                    label=f"Download Extracted Text for {file_name}",
                    data=text,
                    file_name=f"{file_name}.txt",
                    mime="text/plain"
                )
    else:
        st.warning("No image files found in the ZIP archive.")

# If a single image is uploaded
elif uploaded_file is not None and uploaded_file.name.endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
    try:
        # Save the uploaded image to the specified folder
        image_path = os.path.join(uploaded_folder, uploaded_file.name)
        os.makedirs(uploaded_folder, exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Open the uploaded image
        image = Image.open(image_path)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform OCR to extract text
        extracted_text = pytesseract.image_to_string(image)

        # Display extracted text
        st.subheader("Extracted Text:")
        st.text_area("Text from Image", value=extracted_text, height=300)

        # Save extracted text to TextOutput folder
        os.makedirs(text_output_folder, exist_ok=True)
        base_name = os.path.splitext(uploaded_file.name)[0]
        text_file_path = os.path.join(text_output_folder, f"{base_name}.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)

        # Provide download button for the extracted text
        with open(text_file_path, "r") as text_file:
            st.download_button(
                label=f"Download Extracted Text for {uploaded_file.name}",
                data=text_file,
                file_name=f"{base_name}.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"Error processing the image: {e}")