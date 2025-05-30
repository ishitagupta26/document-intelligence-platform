from django.urls import path
from .views import DocumentUploadView, QueryView,DocumentListView,DeleteAllDocumentsView,ChatHistoryAPI,ChatHistoryByDocumentView

urlpatterns = [
    path("upload/", DocumentUploadView.as_view(), name="upload-doc"),
    path("query/", QueryView.as_view(), name="query"),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path("documents/delete_all/", DeleteAllDocumentsView.as_view(), name="delete-all-docs"),
    path("chat-history/<int:document_id>/", ChatHistoryByDocumentView.as_view(), name="chat-history"),  # ✅ NEW
]
