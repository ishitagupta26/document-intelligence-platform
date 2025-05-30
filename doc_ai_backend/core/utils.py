from .models import DocumentChunk
import os
import uuid
import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("❌ Error reading PDF:", e)
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print("❌ Error reading DOCX:", e)
        return ""

def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("❌ Error reading TXT:", e)
        return ""

def chunk_with_overlap(text, chunk_size=500, overlap=100):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def process_document(document):
    print(f"🟢 Processing: {document.title}")
    ext = os.path.splitext(document.file.name)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(document.file.path)
    elif ext == ".docx":
        text = extract_text_from_docx(document.file.path)
    elif ext == ".txt":
        text = extract_text_from_txt(document.file.path)
    elif ext == ".md":  # ✅ New condition
        text = extract_text_from_md(document.file.path)
    else:
        print("❌ Unsupported file type:", ext)
        return

    if not text.strip():
        print("❌ No text extracted from the document.")
        return

    print("📄 Total characters extracted:", len(text))

    chunks = chunk_with_overlap(text, chunk_size=500, overlap=100)
    print("🧩 Overlapping chunks created:", len(chunks))

    for idx, chunk in enumerate(chunks):
        DocumentChunk.objects.create(
            document=document,
            chunk_index=idx,
            text=chunk,
            embedding_id=str(uuid.uuid4())
        )

    document.status = "processed"
    document.save()
    print("✅ Document processed and chunks saved.")

def get_full_document_text(document):
    """Return full extracted text for entire document (used for whole-document QA)."""
    ext = os.path.splitext(document.file.name)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(document.file.path)
    elif ext == ".docx":
        return extract_text_from_docx(document.file.path)
    elif ext == ".txt":
        return extract_text_from_txt(document.file.path)
    else:
        print("❌ Unsupported file type:", ext)
        return ""
def extract_text_from_md(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("❌ Error reading MD file:", e)
        return ""
