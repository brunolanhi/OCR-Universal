# OCR Universal

OCR Universal is a web-based OCR platform built with FastAPI, Tesseract OCR and OCRmyPDF.

The application supports image files, TIFF/TIF collections, ZIP archives and searchable PDF generation.

---

# Features

- TIFF / TIF OCR
- JPG / JPEG OCR
- PNG OCR
- BMP OCR
- ZIP support
- Searchable PDF generation
- DOCX generation
- TXT generation
- Job history
- Background job processing
- Progress tracking
- Automatic cleanup
- Dynamic Tesseract language detection
- Downloadable result packages

---

# Supported Input Formats

- PDF
- TIFF
- TIF
- JPG
- JPEG
- PNG
- BMP
- ZIP

---

# Supported Output Formats

- TXT
- DOCX
- Searchable PDF
- ZIP package

---

# Tested Environment

This project has been developed and tested on:

- Debian GNU/Linux 13 (Trixie)
- Python 3.13
- Tesseract OCR 5.x
- OCRmyPDF 17.x

---

# System Requirements

Recommended:

- 4 vCPU
- 8 GB RAM
- 100 GB SSD

Large OCR workloads:

- 8 vCPU or more
- 16 GB RAM or more

---

# Install System Packages

Update system:

bash

apt update
apt upgrade -y

Install required packages:

bash

apt install -y \
python3 \
python3-pip \
python3-venv \
tesseract-ocr \
tesseract-ocr-por \
tesseract-ocr-ita \
tesseract-ocr-eng \
tesseract-ocr-spa \
tesseract-ocr-fra \
ocrmypdf \
libreoffice \
nginx

Verify installation:

bash

tesseract --version
ocrmypdf --version
libreoffice --version

---

# Clone Project

bash

git clone https://github.com/brunolanhi/ocr-universal.git

cd ocr-universal

---

# Create Virtual Environment

bash

python3 -m venv venv

source venv/bin/activate

---

# Install Python Dependencies

bash

pip install -r requirements.txt

---

# Project Structure

text
ocr-universal/
 
app/
├── cleanup.py
├── generators.py
├── main.py
├── ocr.py
├── pdf_generator.py
├── utils.py
├── worker.py
│
├── templates/
│ ├── index.html
│ ├── jobs.html
│ ├── progresso.html
│ └── sucesso.html
│
├── uploads/
├── outputs/
├── temp/
├── static/
│
└── __pycache__/
 
requirements.txt
README.md
.gitignore

---

# Run Manually

Activate environment:

bash

source venv/bin/activate

Start application:
bash

cd app

uvicorn main:app --host 0.0.0.0 --port 8000

Open browser:

text
http://SERVER_IP:8000

---

# Systemd Service

Create:

bash

nano /etc/systemd/system/ocr-universal.service

Content:

ini
[Unit]
Description=OCR Universal
After=network.target

[Service]

User=root

WorkingDirectory=/opt/ocr-universal/app

Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ocr-universal/venv/bin"
Environment="TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata"

ExecStart=/opt/ocr-universal/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000

Restart=always

[Install]

WantedBy=multi-user.target

Enable service:

bash

systemctl daemon-reload

systemctl enable ocr-universal

systemctl start ocr-universal

Check status:

bash

systemctl status ocr-universal

---

# Nginx Reverse Proxy

Create:

bash

nano /etc/nginx/sites-available/ocr-universal

Content:

server {
    
    listen 80;

    server_name _;

    client_max_body_size 10G;

    location / {

        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

Enable:

bash

ln -s \
/etc/nginx/sites-available/ocr-universal \
/etc/nginx/sites-enabled/

Remove default:

bash

rm -f /etc/nginx/sites-enabled/default

Validate:

bash

nginx -t

Restart:

bash

systemctl restart nginx

---

# Automatic Cleanup

Edit crontab:

bash

crontab -e

Add:

cron
0 3 * * * /opt/ocr-universal/venv/bin/python /opt/ocr-universal/app/cleanup.py

This removes old files automatically.

---

# Progress Tracking

The application creates:

text
status.json

for each job.

Example:

json
{
    "status": "processando",
    "total": 840,
    "atual": 325
}

Status API:

text
/status/JOB_ID

---
## OCR Languages

OCR Universal automatically detects installed Tesseract language packs.

To list installed languages:

bash

tesseract --list-langs

To install additional languages:

bash

apt install tesseract-ocr-deu

Available examples:

bash

apt install tesseract-ocr-por
apt install tesseract-ocr-eng
apt install tesseract-ocr-ita
apt install tesseract-ocr-spa
apt install tesseract-ocr-fra
apt install tesseract-ocr-deu
apt install tesseract-ocr-rus
apt install tesseract-ocr-jpn

After installation, languages automatically appear in the OCR Universal interface without code changes.

# brunolanhi

Created and maintained by Bruno Lanhi Teixeira.
