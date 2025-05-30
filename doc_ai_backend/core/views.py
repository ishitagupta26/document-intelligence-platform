from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Document, DocumentChunk,ChatHistory
from .serializers import DocumentUploadSerializer, DocumentDetailSerializer,ChatHistorySerializer
from .utils import process_document, get_full_document_text
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from openai import OpenAI
from django.core.files.storage import default_storage

# ✅ Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

class DocumentUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name
            file_type = uploaded_file.content_type
            file_size = uploaded_file.size

            document = serializer.save(
                title=file_name,
                file_type=file_type,
                size=file_size
            )

            # ✅ Text extraction and chunking
            process_document(document)

            return Response({
                "message": "Document uploaded and processed successfully.",
                "document_id": document.id
            }, status=201)

        return Response(serializer.errors, status=400)

class DocumentListView(APIView):
    def get(self, request):
        query = request.GET.get("search", "")
        documents = Document.objects.filter(title__icontains=query).order_by('-created_at')
        serializer = DocumentDetailSerializer(documents, many=True)
        return Response(serializer.data)


def build_faiss_index(chunks):
    """Optional: not used in current version since we pass full text instead."""
    embeddings = model.encode([chunk.text for chunk in chunks])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings

class QueryView(APIView):
    def post(self, request):
        document_id = request.data.get("document_id")
        question = request.data.get("question")

        if not document_id or not question:
            return Response({"error": "Missing document_id or question"}, status=400)

        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)

        full_text = get_full_document_text(document)

        if not full_text.strip():
            return Response({"error": "Document has no readable content."}, status=400)

        # ✅ Limit prompt size to 12000 characters
        prompt = (
            f"You are a document analysis assistant.\n"
            f"Analyze the following full content and answer accurately:\n\n"
            f"--- DOCUMENT CONTENT START ---\n{full_text[:12000]}\n--- DOCUMENT CONTENT END ---\n\n"
            f"Question: {question}\n"
            f"Give a factual answer based only on the document. If answer not found, say 'Not found in document.'"
        )

        try:
            client = OpenAI(
                api_key="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",  # replace with env variable in prod
                base_url="https://openrouter.ai/api/v1"
            )

            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.5
            )
            answer = response.choices[0].message.content
            ChatHistory.objects.create(
                document=document,
                question=question,
                answer=answer
            )
        except Exception as e:
            import traceback
            print("❌ LLM Error:", traceback.format_exc())
            return Response({"error": str(e)}, status=500)

        return Response({
            "question": question,
            "answer": answer,
            "document_excerpt_used": full_text[:300] + "..."
        })

class DeleteAllDocumentsView(APIView):
    def delete(self, request):
        docs = Document.objects.all()
        for doc in docs:
            # Delete file from storage
            if doc.file and default_storage.exists(doc.file.name):
                default_storage.delete(doc.file.name)

            # Delete the document (cascades to chunks)
            doc.delete()

        return Response({"message": "All documents deleted successfully."})

class ChatHistoryAPI(APIView):
    def get(self, request, document_id):
        chats = ChatHistory.objects.filter(document_id=document_id).order_by("-timestamp")
        serializer = ChatHistorySerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ChatHistoryByDocumentView(generics.ListAPIView):
    serializer_class = ChatHistorySerializer

    def get_queryset(self):
        document_id = self.kwargs.get("document_id")
        return ChatHistory.objects.filter(document_id=document_id).order_by("-timestamp")