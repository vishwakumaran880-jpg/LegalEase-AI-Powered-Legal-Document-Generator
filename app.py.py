import uuid
import os

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse

from ai_core.gemini_generator import generate_document
from main import create_pdf
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LegalEase</title>
        <style>
            body {
                font-family: Arial;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
            }

            h1 {
                text-align: center;
            }

            input, textarea, button {
                width: 100%;
                padding: 10px;
                margin: 8px 0 15px;
                box-sizing: border-box;
            }

            button {
                cursor: pointer;
                font-size: 16px;
            }
        </style>
    </head>

    <body>

        <h1>LegalEase</h1>

        <h2>AI Legal Document Generator</h2>

        <form action="/generate" method="post">

            <label>Document Type</label>
            <input
                type="text"
                name="document_type"
                placeholder="Example: Rental Agreement"
                required
            >

            <label>Parties</label>
            <textarea
                name="parties"
                placeholder="Example: Landlord and Tenant"
                required
            ></textarea>

            <label>Terms and Conditions</label>
            <textarea
                name="terms"
                placeholder="Enter agreement terms"
                required
            ></textarea>

           
               <label>Effective Date</label>
<input
    type="date"
    name="effective_date"
    required
>


            <button type="submit">
                Generate Legal Document
            </button>
<p style="font-size: 13px; color: gray; margin-top: 20px;">
    Disclaimer: This document is AI-generated for reference purposes only.
    Please consult a qualified legal professional before using it for legal purposes.
</p>
        </form>

    </body>
    </html>
    """


@app.post("/generate")
def generate(
    document_type: str = Form(...),
    parties: str = Form(...),
    terms: str = Form(...),
    effective_date: str = Form(...)
):

    document = generate_document(
        document_type,
        parties,
        terms,
        effective_date
    )

    if document.startswith("Gemini is temporarily busy"):
        return HTMLResponse(
            f"""
            <h2>{document}</h2>
            <p>Please go back and try again.</p>
            """
        )

    filename = os.path.join("documents", f"legal_document_{uuid.uuid4().hex[:8]}.pdf")

    create_pdf(document, filename)

    return FileResponse(
    filename,
    media_type="application/pdf",
    headers={"Content-Disposition": "inline"}
)
