from pathlib import Path


def gerar_txt(texto, destino):

    with open(
        destino,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(texto)

from docx import Document


def gerar_docx(texto, arquivo_saida):

    doc = Document()

    doc.add_paragraph(texto)

    doc.save(arquivo_saida)
