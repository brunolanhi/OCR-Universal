from worker import processar_job
from fastapi import BackgroundTasks
from pdf_generator import (
    gerar_pdf_pesquisavel,
    imagens_para_pdf
)
from datetime import datetime
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.responses import FileResponse
from utils import compactar_pasta
from ocr import imagem_para_texto
from generators import gerar_txt, gerar_docx
from utils import (
    compactar_pasta,
    extrair_zip,
    localizar_arquivos,
    salvar_status
)
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
import shutil
import uuid

app = FastAPI(title="OCR Universal")

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    jobs = []

    outputs = BASE_DIR / "outputs"

    for arquivo in sorted(
        outputs.glob("*.zip"),
        reverse=True
    ):

        data = datetime.fromtimestamp(
            arquivo.stat().st_mtime
        )

        jobs.append(
            {
                "nome": arquivo.name,
                "data": data.strftime("%d/%m/%Y %H:%M")
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "jobs": jobs[:10]
        }
    )

@app.post("/upload")
async def upload_file(
    request: Request,
    background_tasks: BackgroundTasks,
    arquivo: UploadFile = File(...),
    idioma: str = Form(...)
):

    job_id = str(uuid.uuid4())

    destino = UPLOAD_DIR / f"{job_id}_{arquivo.filename}"

    with open(destino, "wb") as buffer:
        background_tasks.add_task(
            processar_job,
            job_id,
            destino,
            idioma
        )
        shutil.copyfileobj(
            arquivo.file,
            buffer
        )
    if destino.suffix.lower() == ".zip":

        pasta_extraida = (
            BASE_DIR
            / "temp"
            / job_id
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

        print(
            f"Arquivos encontrados: {len(arquivos)}"
        )
        job_dir = (
            BASE_DIR
            / "outputs"
            / job_id
        )

        job_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        status_file = (
            job_dir
            / "status.json"
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
            print(
                f"Processando: {arq}"
            )

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
            job_dir
            / "resultado.txt"
        )

        gerar_txt(
            texto,
            saida_txt
        )

        saida_docx = (
            job_dir
            / "resultado.docx"
        )

        gerar_docx(
            texto,
            saida_docx
        )
        pdf_original = (
            job_dir
            / "original.pdf"
        )

        imagens_para_pdf(
            arquivos,
            pdf_original
        )

        saida_pdf = (
            job_dir
            / "resultado.pdf"
        )

        gerar_pdf_pesquisavel(
            pdf_original,
            saida_pdf,
            idioma
        )

        if pdf_original.exists():
            pdf_original.unlink()

        zip_saida = (
            BASE_DIR
            / "outputs"
            / f"{job_id}.zip"
        )

        compactar_pasta(
            job_dir,
            zip_saida
        )
        salvar_status(
            status_file,
            "concluido",
            len(arquivos),
            len(arquivos)
        )
        return templates.TemplateResponse(
            request=request,
            name="sucesso.html",
            context={
                "request": request,
                "arquivo": arquivo.filename,
                "job_id": job_id
            }
        )
    texto = imagem_para_texto(
        destino,
        idioma
    )

    job_dir = (
        BASE_DIR
        / "outputs"
        / job_id
    )

    job_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    saida_txt = (
        job_dir
        / "resultado.txt"
    )

    gerar_txt(
        texto,
        saida_txt
    )

    saida_docx = (
        job_dir
        / "resultado.docx"
    )

    gerar_docx(
        texto,
        saida_docx
    )

    saida_pdf = (
        job_dir
        / "resultado.pdf"
    )

    gerar_pdf_pesquisavel(
        destino,
        saida_pdf,
        idioma
    )

    zip_saida = (
        BASE_DIR
        / "outputs"
        / f"{job_id}.zip"
    )

    compactar_pasta(
        job_dir,
        zip_saida
    )

    return templates.TemplateResponse(
        request=request,
        name="sucesso.html",
        context={
            "request": request,
            "arquivo": arquivo.filename,
            "job_id": job_id
        }
    )
@app.get("/download/{job_id}")
async def download(job_id: str):

    arquivo = (
        BASE_DIR
        / "outputs"
        / f"{job_id}.zip"
    )

    if not arquivo.exists():
        return {
            "erro": "arquivo nao encontrado"
        }

    return FileResponse(
        path=str(arquivo),
        filename=f"{job_id}.zip",
        media_type="application/zip"
    )
@app.get("/jobs")
async def jobs(request: Request):

    lista = []

    outputs = BASE_DIR / "outputs"

    for arquivo in sorted(
        outputs.glob("*.zip"),
        reverse=True
    ):

        data = datetime.fromtimestamp(
            arquivo.stat().st_mtime
        )

        lista.append(
            {
                "nome": arquivo.name,
                "data": data.strftime("%d/%m/%Y %H:%M")
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "request": request,
            "jobs": lista
        }
    )
import json


@app.get("/status/{job_id}")
async def status(job_id: str):

    arquivo = (
        BASE_DIR
        / "outputs"
        / job_id
        / "status.json"
    )

    if not arquivo.exists():

        return {
            "erro": "status nao encontrado"
        }

    with open(
        arquivo,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
@app.get("/progresso/{job_id}")
async def progresso(
    request: Request,
    job_id: str
):

    return templates.TemplateResponse(
        request=request,
        name="progresso.html",
        context={
            "request": request,
            "job_id": job_id
        }
    )
