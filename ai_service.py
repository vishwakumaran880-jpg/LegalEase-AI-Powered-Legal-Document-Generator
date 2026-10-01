import os
from textwrap import dedent

try:
    from google import genai
except ImportError:
    genai = None

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

def _fallback(data: dict) -> str:
    dtype = data["document_type"]
    a, b, date = data["party_a"], data["party_b"], data["effective_date"]

    if dtype == "Employment Contract":
        return dedent(f"""
        EMPLOYMENT CONTRACT

        This Employment Contract is made between {a} ("Employer") and {b} ("Employee"),
        effective from {date}.

        1. POSITION AND RESPONSIBILITIES
        The Employee will serve in the role of {data["role"] or "[Role]"} and will perform
        the duties reasonably assigned to that role.

        2. COMPENSATION
        The compensation is {data["compensation"] or "[Compensation]"}, subject to applicable
        law and the agreed payroll terms.

        3. CONFIDENTIALITY
        The Employee shall protect confidential business information and use it only for
        legitimate work purposes.

        4. TERM AND TERMINATION
        The employment continues according to the agreed terms and applicable law.
        Termination, notice, and final settlement shall follow the applicable employment rules.

        5. GOVERNING LAW
        The parties should specify the applicable jurisdiction and legal requirements.

        ADDITIONAL TERMS
        {data["key_terms"] or "[Insert additional agreed terms]"}

        IMPORTANT: This is an AI-assisted draft and must be reviewed for the applicable
        jurisdiction before signing.
        """).strip()

    if dtype == "Non-Disclosure Agreement":
        return dedent(f"""
        NON-DISCLOSURE AGREEMENT

        This Agreement is between {a} ("Disclosing Party") and {b} ("Receiving Party"),
        effective from {date}.

        1. PURPOSE
        The parties may exchange information for a legitimate business or professional purpose.

        2. CONFIDENTIAL INFORMATION
        Confidential information includes information identified as confidential or that a
        reasonable person would understand to be confidential in the circumstances.

        3. SCOPE
        {data["confidentiality_scope"] or "[Describe the confidential information and permitted use]"}

        4. EXCLUSIONS
        Information that is publicly available without breach, already lawfully known, or
        independently developed may be excluded as permitted by applicable law.

        5. DURATION
        {data["key_terms"] or "[Specify confidentiality period]"}

        6. GOVERNING LAW
        The parties should specify the applicable jurisdiction.

        IMPORTANT: This is an AI-assisted draft and must be reviewed by a qualified lawyer
        before signing.
        """).strip()

    return dedent(f"""
    RESIDENTIAL LEASE AGREEMENT

    This Lease Agreement is between {a} ("Landlord") and {b} ("Tenant"),
    effective from {date}.

    1. PROPERTY
    Property address: {data["address"] or "[Property Address]"}

    2. TERM
    {data["lease_term"] or "[Lease term]"}

    3. RENT
    Monthly rent: {data["monthly_rent"] or "[Monthly Rent]"}

    4. USE AND MAINTENANCE
    The property shall be used for lawful residential purposes. Maintenance and repair
    responsibilities should be specified by the parties.

    5. SECURITY DEPOSIT
    The parties should specify the deposit amount, permitted deductions, and return procedure.

    6. TERMINATION
    Notice and termination shall follow the agreed terms and applicable law.

    7. GOVERNING LAW
    The parties should specify the applicable jurisdiction.

    ADDITIONAL TERMS
    {data["key_terms"] or "[Insert additional agreed terms]"}

    IMPORTANT: This is an AI-assisted draft and must be reviewed for the applicable
    jurisdiction before signing.
    """).strip()

def generate_document(data: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        return _fallback(data)

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a legal-document drafting assistant. Generate a structured FIRST DRAFT,
not legal advice. Do not claim that the document is legally valid or enforceable.
Use neutral placeholders where information is missing. Avoid inventing facts.

Document type: {data["document_type"]}
Party A: {data["party_a"]}
Party B: {data["party_b"]}
Effective date: {data["effective_date"]}
Address: {data["address"]}
Role: {data["role"]}
Compensation: {data["compensation"]}
Confidentiality scope: {data["confidentiality_scope"]}
Lease term: {data["lease_term"]}
Monthly rent: {data["monthly_rent"]}
Key terms: {data["key_terms"]}
Company name: {data["company_name"]}
Custom instructions: {data["custom_instructions"]}

Requirements:
- Professional headings and numbered clauses.
- Include only clauses relevant to the document type.
- Do not fabricate jurisdiction-specific law.
- Flag missing legal details using [PLACEHOLDER].
- End with: "AI-assisted draft — professional legal review recommended before signing."
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    text = getattr(response, "text", None)
    return text.strip() if text else _fallback(data)
