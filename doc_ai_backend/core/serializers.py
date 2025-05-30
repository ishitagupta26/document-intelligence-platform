from rest_framework import serializers
from .models import Document,ChatHistory

# ✅ For POST /api/upload/
class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['file']  # Only expect file from frontend

    def create(self, validated_data):
        file = validated_data["file"]
        return Document.objects.create(
            file=file,
            title=file.name,
            file_type=file.content_type,
            size=file.size,
        )

# ✅ For GET /api/documents/
class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'  # Return full metadata to frontend

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = '__all__'