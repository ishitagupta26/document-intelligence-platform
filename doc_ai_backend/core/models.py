from django.db import models
class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=50)
    size = models.IntegerField()
    page_count = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default="processing")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()
    page_number = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    embedding_id = models.CharField(max_length=255, blank=True)  # e.g., FAISS/Chroma identifier

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"

class ChatHistory(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chat_history")
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:30]}..."
