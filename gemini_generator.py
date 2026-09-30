import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_document(document_type, parties, terms, effective_date):

    prompt = f"""
Create a simple professional legal document.

Document Type: {document_type}

Parties: {parties}

Terms and Conditions:
{terms}

Effective Date:
{effective_date}

Requirements:
- Give a clear title.
- Use simple professional language.
- Organize the document with headings and clauses.
- Do not invent personal information.
- Add a note that the document should be reviewed by a qualified legal professional.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as error:
            error_text = str(error)

            if "503" in error_text or "UNAVAILABLE" in error_text:
                if attempt < 2:
                    time.sleep(5)
                    continue

                return "Gemini is temporarily busy. Please wait a few seconds and click Generate again."

            raise