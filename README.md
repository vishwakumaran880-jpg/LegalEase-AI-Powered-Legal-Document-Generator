# LegalEase — AI-Powered Legal Document Generator
github link: https://github.com/Lakshetha2014/LegalEase.git

LegalEase is a FastAPI web application for creating editable AI-assisted drafts of:
- Employment Contracts
- Non-Disclosure Agreements (NDAs)
- Residential Lease Agreements

It supports:
- FastAPI backend
- HTML/CSS/JavaScript frontend
- Optional Gemini API integration
- Local fallback templates when no API key is configured
- Editable preview
- Automatic key-term table
- PDF export
- DOCX export
- TXT export
- Optional company name and logo
- No database required for the starter version

## 1. Recommended project setup

Python 3.12 is a conservative choice for third-party package compatibility. If Python 3.14 is already installed on your computer, try it first; if a package installation reports a compatibility/build error, use Python 3.12 for this project.

Open the project folder in VS Code.

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can use Command Prompt:

```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run without Gemini first

The project has a built-in template fallback, so you can test the application without an API key.

```powershell
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI API documentation:

```text
http://127.0.0.1:8000/docs
```

## 3. Enable Gemini AI

Create a Gemini API key and set it as an environment variable.

PowerShell for the current terminal session:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
$env:GEMINI_MODEL="gemini-3.8-flash"
uvicorn app:app --reload
```

Alternatively create a `.env` file from `.env.example` and load it before starting the application, or set the environment variable through Windows.

Do not put a real API key into GitHub or into frontend JavaScript.

## 4. Main workflow

1. Select Employment Contract, NDA, or Lease Agreement.
2. Enter party information.
3. Enter the effective date.
4. Add document-specific details.
5. Add key terms/custom instructions.
6. Optionally add company name and logo.
7. Click Generate Document.
8. Edit the generated preview.
9. Export PDF, DOCX, or TXT.

## 5. Important legal limitation

This application is an educational/product prototype for AI-assisted drafting. Generated text can contain errors, omissions, or jurisdiction-specific issues. It must be reviewed by an appropriately qualified legal professional before use or signing.

## 6. Production improvements

For a real deployment, add:
- User authentication and role-based access
- Database with encryption at rest
- Audit logs
- Rate limiting
- CSRF/security controls appropriate to the deployment
- Malware/file scanning for uploads
- Secure secret management
- Data retention/deletion policies
- Jurisdiction-specific clause libraries reviewed by lawyers
- Version history
- Digital signatures through a compliant provider
- Background jobs for long document generation
- Automated tests and CI/CD
