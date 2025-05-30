import { useState, useEffect } from "react";
import axios from "axios";

export default function QuestionForm() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/documents/")
      .then(res => setDocuments(res.data))
      .catch(() => alert("Failed to fetch documents"));
  }, []);

  useEffect(() => {
    if (selectedDocId) {
      axios.get(`http://localhost:8000/api/chat-history/${selectedDocId}/`)
        .then(res => setChatHistory(res.data))
        .catch(() => setChatHistory([]));
    }
  }, [selectedDocId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedDocId || !question) return alert("Please select a document and enter a question");

    setLoading(true);
    setAnswer(""); setContext("");

    try {
      const res = await axios.post("http://localhost:8000/api/query/", {
        document_id: selectedDocId,
        question
      });

      setAnswer(res.data.answer || "No answer returned");
      setContext(res.data.document_excerpt_used || "");

      // Refresh chat history
      const chatRes = await axios.get(`http://localhost:8000/api/chat-history/${selectedDocId}/`);
      setChatHistory(chatRes.data);
    } catch (err) {
      console.error(err);
      setAnswer("❌ Error fetching answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">❓ Ask a Question</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          value={selectedDocId}
          onChange={(e) => setSelectedDocId(e.target.value)}
          className="border p-2 w-full"
        >
          <option value="">-- Select Document --</option>
          {documents.map(doc => (
            <option key={doc.id} value={doc.id}>
              {doc.title}
            </option>
          ))}
        </select>
        <textarea
          className="border p-2 w-full"
          rows="3"
          placeholder="Type your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Thinking..." : "Get Answer"}
        </button>
      </form>

      {answer && (
        <>
          <div className="mt-6">
            <h3 className="font-semibold mb-2">Answer:</h3>
            <p className="bg-gray-100 p-3 rounded">{answer}</p>
          </div>
          {context && (
            <div className="mt-4">
              <h4 className="font-semibold mb-1">Context Used:</h4>
              <pre className="bg-gray-100 p-3 text-sm overflow-x-auto whitespace-pre-wrap">{context}</pre>
            </div>
          )}
        </>
      )}

      {chatHistory.length > 0 && (
        <div className="mt-6">
          <h3 className="font-semibold mb-2">Chat History:</h3>
          <ul className="space-y-2 text-sm">
            {chatHistory.map(chat => (
              <li key={chat.id} className="bg-gray-50 p-3 border rounded">
                <p className="font-medium text-gray-800">Q: {chat.question}</p>
                <p className="text-gray-600">A: {chat.answer}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

    </div>
  );
}
