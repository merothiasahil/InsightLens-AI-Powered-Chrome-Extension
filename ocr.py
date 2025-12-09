import os
import os
os.environ["DISPLAY"] = ":0"  


import matplotlib
matplotlib.use('Agg')  

from PIL import Image
Image.Image.show = lambda self, *args, **kwargs: None  
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import io
import base64

def extract_text_from_image_base64(base64_str):
    try:
        # Decode base64 → bytes → image
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))

        # PREPROCESSING 
        image = image.convert("L")  # Convert to grayscale
        image = image.resize((image.width * 2, image.height * 2))  # Resize to improve clarity

       

        # OCR
        text = pytesseract.image_to_string(image)

        return {
            "text": text.strip()
        }

    except Exception as e:
        return {
            "error": str(e)}
