import { useEffect, useState } from "react";
import axios from "axios";

export default function DocumentsList() {
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  const fetchDocuments = async (query = "") => {
    try {
      const url = query
        ? `http://localhost:8000/api/documents/?search=${encodeURIComponent(query)}`
        : "http://localhost:8000/api/documents/";

      const res = await axios.get(url);
      setDocuments(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch documents");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    fetchDocuments(value);
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">📚 Uploaded Documents</h2>

      <input
        type="text"
        value={searchTerm}
        onChange={handleSearch}
        placeholder="🔍 Search by title or type..."
        className="mb-4 p-2 border w-full rounded"
      />

      {error && <p className="text-red-600">{error}</p>}

      <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-collapse border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="border border-gray-300 px-4 py-2">ID</th>
              <th className="border border-gray-300 px-4 py-2">Title</th>
              <th className="border border-gray-300 px-4 py-2">Type</th>
              <th className="border border-gray-300 px-4 py-2">Pages</th>
              <th className="border border-gray-300 px-4 py-2">Uploaded</th>
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center py-4">
                  No documents found.
                </td>
              </tr>
            ) : (
              documents.map((doc) => (
                <tr key={doc.id} className="hover:bg-gray-50">
                  <td className="border border-gray-300 px-4 py-2">{doc.id}</td>
                  <td className="border border-gray-300 px-4 py-2">{doc.title}</td>
                  <td className="border border-gray-300 px-4 py-2">{doc.file_type}</td>
                  <td className="border border-gray-300 px-4 py-2">
                    {doc.page_count || "–"}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {doc.created_at ? new Date(doc.created_at).toLocaleString() : "N/A"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
