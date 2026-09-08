from pathlib import Path
from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs" / "aws_s3"


PDF_FILES = [
    "glacier-dg.pdf",
    "s3-api.pdf",
    "s3-devguide.pdf",
    "s3-userguide.pdf",
]


def load() -> str:
    texts = []

    for pdf_name in PDF_FILES:
        pdf_path = DOCS_DIR / pdf_name

        if not pdf_path.exists():
            print(f"Warning: Missing PDF, skipping: {pdf_path}")
            continue

        reader = PdfReader(str(pdf_path))
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        texts.append(text)

    return "\n".join(texts)
