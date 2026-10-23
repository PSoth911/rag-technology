import React, { useState } from "react";

export interface Citation {
  id: string;
  docId: string;
  pageNumber: number;
  snippet: string;
  score: number;
}

export const RAGSearchComponent: React.FC = () => {
  const [query, setQuery] = useState("");
  const [language, setLanguage] = useState<"auto" | "en" | "km">("auto");
  const [topK, setTopK] = useState(3);
  const [isLoading, setIsLoading] = useState(false);
  const [answer, setAnswer] = useState<string | null>(null);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [activeCitation, setActiveCitation] = useState<Citation | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setAnswer(null);
    setCitations([]);
    setActiveCitation(null);

    // Simulate RAG retrieval & LLM generation response
    setTimeout(() => {
      const isKhmer = /[\u1780-\u17FF]/.test(query);
      if (isKhmer) {
        setAnswer(
          "ប្រព័ន្ធ RAG រួមបញ្ចូលការស្វែងរកឯកសារយោងជាមួយនឹង LLM ដើម្បីផ្តល់ចម្លើយត្រឹមត្រូវ និងទប់ស្កាត់ការឆ្លើយខុស [DOC-KM-01, P.2]។"
        );
        setCitations([
          {
            id: "cit-1",
            docId: "DOC-KM-01",
            pageNumber: 2,
            snippet: "ឯកសារស្រាវជ្រាវស្តីពីបច្ចេកវិទ្យាបញ្ញាសិប្បនិម្មិត និងប្រព័ន្ធស្វែងរកទិន្នន័យ។",
            score: 0.94,
          },
        ]);
      } else {
        setAnswer(
          "Retrieval-Augmented Generation grounds model responses in retrieved passages, providing verifiable citations [DOC-EN-01, P.1]."
        );
        setCitations([
          {
            id: "cit-1",
            docId: "DOC-EN-01",
            pageNumber: 1,
            snippet: "RAG optimizes the output of an LLM by referencing an authoritative external knowledge base.",
            score: 0.96,
          },
        ]);
      }
      setIsLoading(false);
    }, 600);
  };

  return (
    <div style={{ maxWidth: 720, margin: "20px auto", fontFamily: "Segoe UI, sans-serif" }}>
      <header style={{ borderBottom: "1px solid #e2e8f0", paddingBottom: 12, marginBottom: 20 }}>
        <h2 style={{ margin: "0 0 6px 0", color: "#0f172a" }}>RAG Multilingual Assistant</h2>
        <p style={{ margin: 0, color: "#64748b", fontSize: 14 }}>
          Search documents in English and Khmer with verifiable citations.
        </p>
      </header>

      <form onSubmit={handleSearch} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question (e.g. 'What is RAG?' or 'តើអ្វីជា RAG?')..."
          style={{
            padding: "12px 16px",
            fontSize: 15,
            border: "1px solid #cbd5e1",
            borderRadius: 8,
            outline: "none",
          }}
        />

        <div style={{ display: "flex", gap: 16, alignItems: "center", fontSize: 14 }}>
          <label>
            Language:
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as any)}
              style={{ marginLeft: 6, padding: "4px 8px", borderRadius: 4 }}
            >
              <option value="auto">Auto-detect</option>
              <option value="en">English (EN)</option>
              <option value="km">Khmer (KM - ភាសាខ្មែរ)</option>
            </select>
          </label>

          <label>
            Top K: {topK}
            <input
              type="range"
              min={1}
              max={10}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              style={{ marginLeft: 8, verticalAlign: "middle" }}
            />
          </label>

          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            style={{
              marginLeft: "auto",
              padding: "8px 20px",
              backgroundColor: isLoading ? "#94a3b8" : "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: 6,
              cursor: isLoading ? "not-allowed" : "pointer",
              fontWeight: 600,
            }}
          >
            {isLoading ? "Searching..." : "Ask Assistant"}
          </button>
        </div>
      </form>

      {answer && (
        <div style={{ marginTop: 24, padding: 18, backgroundColor: "#f8fafc", borderRadius: 8 }}>
          <h4 style={{ margin: "0 0 8px 0", color: "#1e293b" }}>Grounded Response</h4>
          <p style={{ margin: "0 0 16px 0", fontSize: 15, lineHeight: 1.6, color: "#334155" }}>
            {answer}
          </p>

          <h5 style={{ margin: "0 0 8px 0", color: "#475569" }}>Document Citations:</h5>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {citations.map((c) => (
              <button
                key={c.id}
                onClick={() => setActiveCitation(c)}
                style={{
                  padding: "6px 12px",
                  fontSize: 13,
                  backgroundColor: activeCitation?.id === c.id ? "#dbeafe" : "#ffffff",
                  border: `1px solid ${activeCitation?.id === c.id ? "#2563eb" : "#cbd5e1"}`,
                  borderRadius: 6,
                  cursor: "pointer",
                }}
              >
                📄 {c.docId} (Page {c.pageNumber}) — Score: {(c.score * 100).toFixed(0)}%
              </button>
            ))}
          </div>

          {activeCitation && (
            <div
              style={{
                marginTop: 12,
                padding: 12,
                backgroundColor: "#ffffff",
                borderLeft: "4px solid #2563eb",
                fontSize: 13,
                color: "#1e293b",
              }}
            >
              <strong>Excerpt from {activeCitation.docId} [P.{activeCitation.pageNumber}]:</strong>
              <div style={{ marginTop: 4, fontStyle: "italic" }}>"{activeCitation.snippet}"</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RAGSearchComponent;
