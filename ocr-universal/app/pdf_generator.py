import subprocess
import img2pdf


def gerar_pdf_pesquisavel(
    arquivo_entrada,
    arquivo_saida,
    idioma
):

    resultado = subprocess.run(
        [
            "/usr/bin/ocrmypdf",
            "--force-ocr",
            "-l",
            idioma,
            str(arquivo_entrada),
            str(arquivo_saida)
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:

        raise Exception(
            f"""
OCRMYPDF FALHOU

STDOUT:
{resultado.stdout}

STDERR:
{resultado.stderr}
"""
        )


def imagens_para_pdf(
    arquivos,
    pdf_saida
):

    with open(pdf_saida, "wb") as f:

        f.write(
            img2pdf.convert(
                [str(arq) for arq in arquivos]
            )
        )
