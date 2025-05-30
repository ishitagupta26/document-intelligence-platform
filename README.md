Document Intelligence Platform
An AI-powered document intelligence web app that allows users to upload documents and ask natural language questions about their content using RAG (Retrieval-Augmented Generation).

-->Tech Stack

- Backend: Django + Django REST Framework  
- Frontend: ReactJS + Tailwind CSS  
- Embeddings: Sentence Transformers (MiniLM)  
- Vector Store: FAISS  
- LLM: OpenAI via OpenRouter API  
- File Support: `.pdf`, `.docx`, `.txt`, `.md`  
- Database: SQLite (can be configured to MySQL/Postgres)

-->Features

- Upload and parse documents (`.pdf`, `.docx`, `.txt`, `.md`)
- Automatic chunking with overlapping strategy
- FAISS-based similarity search with sentence embeddings
- RAG-style question answering with OpenAI
- Document list & metadata (title, type, pages, upload time)
- Q&A chat history per document
- Search and delete documents



-->Setup Instructions

--Backend

```bash
cd doc_ai_backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

--Frontend
cd doc-intel-frontend
npm install
npm start

-->API Endpoints

GET	     /api/documents/	     List all uploaded documents
POST     /api/upload/	         Upload a new document
POST     /api/query/	         Ask a question on a document
GET	     /api/chat-history/<id>/ Get Q&A chat history
DELETE   /api/documents/<id>/	 Delete document

-->Sample Questions
Upload a resume and ask:

What is the candidate’s name?
What is their GitHub profile?
What is their education background?
Has the candidate done any internships?
What are the projects mentioned?

-->Sample Documents
Include some test documents in /documents/ folder:
resume25.pdf

-->Deployment
Local only. Optional deployment instructions (Render / Vercel) can be added later.