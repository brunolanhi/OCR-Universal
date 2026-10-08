import uuid

from pathlib import Path

from ocr import imagem_para_texto
from generators import gerar_txt
from generators import gerar_docx

from pdf_generator import (
    gerar_pdf_pesquisavel,
    imagens_para_pdf
)

from utils import (
    compactar_pasta,
    extrair_zip,
    localizar_arquivos,
    salvar_status
)

from pathlib import Path

import time

def processar_job(
    job_id,
    destino,
    idioma
):

    destino = Path(destino)

    output_dir = Path(
        f"/opt/ocr-universal/app/outputs/{job_id}"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    status_file = (
        output_dir
        / "status.json"
    )

    #
    # ZIP
    #

    if destino.suffix.lower() == ".zip":

        pasta_extraida = Path(
            f"/opt/ocr-universal/app/temp/{job_id}"
        )

        pasta_extraida.mkdir(
            parents=True,
            exist_ok=True
        )

        extrair_zip(
            destino,
            pasta_extraida
        )

        arquivos = localizar_arquivos(
            pasta_extraida
        )

        salvar_status(
            status_file,
            "processando",
            len(arquivos),
            0
        )

        texto = ""

        for indice, arq in enumerate(
            arquivos,
            start=1
        ):

            texto += imagem_para_texto(
                arq,
                idioma
            )

            texto += "\n\n"

            salvar_status(
                status_file,
                "processando",
                len(arquivos),
                indice
            )

        saida_txt = (
            output_dir
            / "resultado.txt"
        )

        gerar_txt(
            texto,
            saida_txt
        )

        saida_docx = (
            output_dir
            / "resultado.docx"
        )

        gerar_docx(
            texto,
            saida_docx
        )

        pdf_original = (
            output_dir
            / "original.pdf"
        )

        imagens_para_pdf(
            arquivos,
            pdf_original
        )

        saida_pdf = (
            output_dir
            / "resultado.pdf"
        )

        gerar_pdf_pesquisavel(
            pdf_original,
            saida_pdf,
            idioma
        )

        if pdf_original.exists():
            pdf_original.unlink()

        zip_saida = Path(
            f"/opt/ocr-universal/app/outputs/{job_id}.zip"
        )

        compactar_pasta(
            output_dir,
            zip_saida
        )

        salvar_status(
            status_file,
            "concluido",
            len(arquivos),
            len(arquivos)
        )

        return

    #
    # TIFF / JPG / PNG
    #

    salvar_status(
        status_file,
        "processando",
        1,
        0
    )

    texto = imagem_para_texto(
        destino,
        idioma
    )

    salvar_status(
        status_file,
        "processando",
        1,
        1
    )

    saida_txt = (
        output_dir
        / "resultado.txt"
    )

    gerar_txt(
        texto,
        saida_txt
    )

    saida_docx = (
        output_dir
        / "resultado.docx"
    )

    gerar_docx(
        texto,
        saida_docx
    )

    saida_pdf = (
        output_dir
        / "resultado.pdf"
    )

    gerar_pdf_pesquisavel(
        destino,
        saida_pdf,
        idioma
    )

    zip_saida = Path(
        f"/opt/ocr-universal/app/outputs/{job_id}.zip"
    )

    compactar_pasta(
        output_dir,
        zip_saida
    )

    salvar_status(
        status_file,
        "concluido",
        1,
        1
    )

    print(f"PROCESSANDO JOB {job_id}")

    # por enquanto apenas criar um status

    output_dir = Path(
        f"/opt/ocr-universal/app/outputs/{job_id}"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    status_file = (
        output_dir
        / "status.json"
    )

    salvar_status(
        status_file,
        "processando",
        100,
        0
    )

    import time

    for indice, arq in enumerate(
        arquivos,
        start=1
    ):

        texto += imagem_para_texto(
            arq,
            idioma
        )

        salvar_status(
            status_file,
            "processando",
            len(arquivos),
            indice
        )

    salvar_status(
        status_file,
        "concluido",
        100,
        100
    )

    log = Path(
        f"/opt/ocr-universal/app/uploads/{job_id}.log"
    )

    with open(log, "w") as f:

        f.write(
            f"JOB={job_id}\n"
        )

        f.write(
            f"ARQUIVO={destino}\n"
        )

        f.write(
            f"IDIOMA={idioma}\n"
        )

    time.sleep(5)
