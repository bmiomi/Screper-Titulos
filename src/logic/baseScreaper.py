import io
from requests_html import HTMLSession
from PIL import Image, ImageFilter, ImageEnhance
from requests.packages import urllib3
import pytesseract
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BaseScrapper(HTMLSession):

    def __init__(self):
         super().__init__()
        

    def processar_capchar(self,s):
        img_capchar= Image.open(io.BytesIO(s.content))
        img = img_capchar.convert('L')

        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.convert('1') 
        captcha_text = pytesseract.image_to_string(img_capchar)
        return  ''.join(char for char in captcha_text if char.isalnum())
    
    def buscar_tesesseract(self):
        tesseract_cmd = None
        for path in os.getenv('PATH', '').split(os.pathsep):
            tesseract_path = os.path.join(path, 'tesseract.exe')
            if os.path.exists(tesseract_path):
                tesseract_cmd = tesseract_path
                return tesseract_cmd
        if tesseract_cmd is None:
                raise Exception("No se encontró el ejecutable de Tesseract en el PATH")

        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
