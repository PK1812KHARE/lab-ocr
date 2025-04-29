# Lab-OCR

A FastAPI service that extracts lab-test data from report images using the OCR.Space API.

## Quickstart

```bash
git clone https://github.com/PK1812KHARE/lab-ocr.git
cd lab-ocr

# 1) Create & activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Run locally
uvicorn main:app --reload

# 4) Hit it
curl -F "file=@data/sample1.png" http://127.0.0.1:8000/get-lab-tests
