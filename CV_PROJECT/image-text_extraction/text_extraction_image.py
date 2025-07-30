import pytesseract
import easyocr
def img_txt_tesseract(img_path):
    text = pytesseract.image_to_string(Image.open(img_path), lang='eng')
    return text
def read_text_easyocr(img_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path, detail=0)  # detail=0 returns only text
    return ' '.join(result)
path = '/content/dt.jpg'
# Usage
text = read_text_easyocr(path)
text = img_txt_tesseract(path)
print(text)
