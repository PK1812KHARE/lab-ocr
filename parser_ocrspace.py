import re
import requests

API_KEY = "helloworld"   # ← swap in your real OCR.Space key
OCR_URL = "https://api.ocr.space/parse/image"

def ocr_via_ocr_space(image_bytes: bytes, filename: str = "image.png") -> str:
    """
    Sends the image bytes along with its filename and correct mime-type
    so OCR.Space can recognize it.
    """
    # Determine mime from extension
    mime = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
    # files expects a tuple: (filename, content, content_type)
    files = {
        "file": (filename, image_bytes, mime)
    }
    data = {
        "apikey": API_KEY,
        "language": "eng",
        "OCREngine": 2
    }
    resp = requests.post(OCR_URL, files=files, data=data)
    resp.raise_for_status()
    result = resp.json()
    if result.get("IsErroredOnProcessing"):
        err = result.get("ErrorMessage", ["Unknown OCR error"])[0]
        raise RuntimeError(err)
    return result["ParsedResults"][0]["ParsedText"]

def parse_text(text: str) -> list[dict]:
    """
    Extracts test records from the raw OCR text.
    """
    pattern = re.compile(
        r'([A-Za-z0-9 \(\)%]+?)\s+'          # test name
        r'([\d.]+)\s+'                       # test value
        r'(\d+\.?\d*[-–]\d+\.?\d*)\s*'       # reference range
        r'([A-Za-z/%μµ]+)'                   # unit
    )
    records = []
    for line in text.splitlines():
        m = pattern.search(line)
        if not m:
            continue
        name, val, rng, unit = m.groups()
        low, high = map(float, rng.replace('–','-').split('-'))
        v = float(val)
        records.append({
            "test_name":             name.strip().upper(),
            "test_value":            val,
            "bio_reference_range":   rng,
            "test_unit":             unit,
            "lab_test_out_of_range": not (low <= v <= high)
        })
    return records
