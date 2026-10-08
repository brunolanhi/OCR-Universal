from pathlib import Path
import zipfile


def compactar_pasta(
    pasta_origem,
    arquivo_zip
):

    with zipfile.ZipFile(
        arquivo_zip,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for arquivo in Path(
            pasta_origem
        ).rglob("*"):

            if arquivo.is_file():

                zipf.write(
                    arquivo,
                    arquivo.relative_to(
                        pasta_origem
                    )
                )
import zipfile

def extrair_zip(arquivo_zip, destino):

    with zipfile.ZipFile(
        arquivo_zip,
        "r"
    ) as zip_ref:

        zip_ref.extractall(destino)
from pathlib import Path

def localizar_arquivos(caminho):

    extensoes = {
        ".tif",
        ".tiff",
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".pdf"
    }

    resultado = []

    for arquivo in Path(caminho).rglob("*"):

        if arquivo.suffix.lower() in extensoes:
            resultado.append(arquivo)

    return sorted(resultado)

import json


def salvar_status(
    arquivo_status,
    status,
    total,
    atual
):

    dados = {
        "status": status,
        "total": total,
        "atual": atual
    }

    with open(
        arquivo_status,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dados,
            f,
            ensure_ascii=False
        )
from pathlib import Path


def listar_idiomas():

    pasta = Path(
        "/usr/share/tesseract-ocr/5/tessdata"
    )

    idiomas = []

    for arquivo in pasta.glob("*.traineddata"):

        idiomas.append(
            arquivo.stem
        )

    return sorted(idiomas)
