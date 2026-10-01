from io import BytesIO
from pathlib import Path
import re

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.ai_service import generate_document
from services.document_service import build_docx, build_pdf, build_txt, extract_terms

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="LegalEase", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

DOCUMENT_TYPES = {
    "employment": "Employment Contract",
    "nda": "Non-Disclosure Agreement",
    "lease": "Residential Lease Agreement",
}

def clean_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value or "document")
    return value.strip("._") or "document"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"document_types": DOCUMENT_TYPES},
    )

@app.post("/api/generate")
async def generate(
    document_type: str = Form(...),
    party_a: str = Form(...),
    party_b: str = Form(...),
    effective_date: str = Form(...),
    key_terms: str = Form(""),
    address: str = Form(""),
    role: str = Form(""),
    compensation: str = Form(""),
    confidentiality_scope: str = Form(""),
    lease_term: str = Form(""),
    monthly_rent: str = Form(""),
    custom_instructions: str = Form(""),
    company_name: str = Form(""),
    logo: UploadFile | None = File(default=None),
):
    if document_type not in DOCUMENT_TYPES:
        return {"error": "Invalid document type."}

    logo_bytes = None
    logo_name = None
    if logo and logo.filename:
        allowed = {".png", ".jpg", ".jpeg"}
        suffix = Path(logo.filename).suffix.lower()
        if suffix not in allowed:
            return {"error": "Logo must be PNG, JPG, or JPEG."}
        logo_bytes = await logo.read()
        if len(logo_bytes) > 2 * 1024 * 1024:
            return {"error": "Logo must be 2 MB or smaller."}
        logo_name = logo.filename

    data = {
        "document_type": DOCUMENT_TYPES[document_type],
        "party_a": party_a.strip(),
        "party_b": party_b.strip(),
        "effective_date": effective_date.strip(),
        "key_terms": key_terms.strip(),
        "address": address.strip(),
        "role": role.strip(),
        "compensation": compensation.strip(),
        "confidentiality_scope": confidentiality_scope.strip(),
        "lease_term": lease_term.strip(),
        "monthly_rent": monthly_rent.strip(),
        "custom_instructions": custom_instructions.strip(),
        "company_name": company_name.strip(),
    }

    content = generate_document(data)
    terms = extract_terms(data)

    return {
        "document_type": data["document_type"],
        "content": content,
        "terms": terms,
        "company_name": data["company_name"],
        "logo_name": logo_name,
        "notice": "AI-generated draft for review. It is not a substitute for advice from a qualified lawyer.",
    }

def make_document_response(
    content: str,
    terms: list[dict],
    company_name: str,
    fmt: str,
    logo_bytes: bytes | None = None,
    filename_stem: str = "legalease_document",
):
    if fmt == "docx":
        payload = build_docx(content, terms, company_name, logo_bytes)
        media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = clean_filename(filename_stem) + ".docx"
    elif fmt == "pdf":
        payload = build_pdf(content, terms, company_name, logo_bytes)
        media = "application/pdf"
        filename = clean_filename(filename_stem) + ".pdf"
    else:
        payload = build_txt(content, terms, company_name)
        media = "text/plain; charset=utf-8"
        filename = clean_filename(filename_stem) + ".txt"

    return StreamingResponse(
        BytesIO(payload),
        media_type=media,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

@app.post("/api/export")
async def export_document(
    content: str = Form(...),
    terms_json: str = Form("[]"),
    company_name: str = Form(""),
    fmt: str = Form(...),
    filename_stem: str = Form("legalease_document"),
):
    import json
    try:
        terms = json.loads(terms_json)
        if not isinstance(terms, list):
            terms = []
    except json.JSONDecodeError:
        terms = []

    return make_document_response(
        content=content,
        terms=terms,
        company_name=company_name,
        fmt=fmt,
        filename_stem=filename_stem,
    )

@app.get("/health")
async def health():
    return {"status": "ok", "service": "LegalEase"}
