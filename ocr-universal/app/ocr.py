from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def imagem_para_texto(
    arquivo,
    idioma
):

    imagem = Image.open(arquivo)

    return pytesseract.image_to_string(
        imagem,
        lang=idioma
    )
