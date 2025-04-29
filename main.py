from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import parser_ocrspace as parser

app = FastAPI(title="Lab OCR via OCR.Space")

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    # Read the uploaded bytes
    img_bytes = await file.read()
    if not img_bytes:
        raise HTTPException(400, "Empty file upload")
    # Use the original filename so OCR.Space knows the extension
    filename = file.filename or "image.png"
    try:
        raw_text = parser.ocr_via_ocr_space(img_bytes, filename)
    except Exception as e:
        raise HTTPException(502, f"OCR service error: {e}")
    # Parse the OCR output
    data = parser.parse_text(raw_text)
    return JSONResponse({"is_success": True, "data": data})
