import { useState, useRef } from "react";
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [q, setQ] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const controllerRef = useRef(null);

  async function search() {
    if (!q.trim()) return;
    setLoading(true);
    setAnswer("");
    setSources([]);
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;

    try {
      const res = await fetch(`${API_BASE}/api/personal_research/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, max_web_results: 5, use_rag: true }),
        signal: controller.signal,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      if (!reader) throw new Error("No stream");

      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        const txt = decoder.decode(value, { stream: true });
        for (const line of txt.split("\n").filter(Boolean)) {
          try {
            const data = JSON.parse(line);
            if (data.type === "token") setAnswer((a) => a + data.text);
            else if (data.type === "sources") setSources(data.items || []);
          } catch { /* ignore */ }
        }
      }
    } catch (e) {
      setAnswer(`⚠️ ${e?.message || "Request failed"}`);
    } finally {
      setLoading(false);
    }
  }

    return (
      <>
        <div style={{ maxWidth: 900, margin: "40px auto", padding: 16, fontFamily: "ui-sans-serif,system-ui" }}>
          <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8 }}>Personal Research Assistant (LangChain)</h1>
          <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e)=>{ if (e.key === "Enter") search(); }}
              placeholder="Ask a research question…"
              style={{ flex: 1, padding: "10px 12px", borderRadius: 12, border: "1px solid #e2e8f0" }}
            />
            <button
              onClick={search}
              disabled={loading || !q.trim()}
              style={{ padding: "10px 16px", borderRadius: 12, border: "1px solid #0ea5e9", background: loading ? "#e2e8f0" : "#0ea5e9", color: "white" }}
            >
              {loading ? "Searching…" : "Search"}
            </button>
          </div>

          {!!answer && (
            <div
              style={{
                whiteSpace: "pre-wrap",
                background: "var(--answer-bg, #f8fafc)",
                color: "var(--answer-color, #1e293b)",
                border: "1px solid #cbd5e1",
                padding: 16,
                borderRadius: 12,
                marginBottom: 16,
              }}
            >
              {answer}
            </div>
          )}

          <div>
            <div style={{ fontWeight: 600, marginBottom: 8 }}>Sources</div>
            {sources.length === 0 ? (
              <div style={{ color: "#64748b" }}>No sources yet.</div>
            ) : (
              <ul style={{ display: "grid", gap: 10, listStyle: "none", padding: 0 }}>
                {sources.map((s, i) => (
                  <li key={i} style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 12 }}>
                    <a href={s.url} target="_blank" rel="noreferrer" style={{ fontWeight: 600, textDecoration: "underline" }}>
                      {s.title}
                    </a>
                    {s.snippet && <div style={{ color: "#475569", marginTop: 6 }}>{s.snippet}</div>}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
        <style>{`
          :root {
            --answer-bg: #f8fafc;
            --answer-color: #1e293b;
          }
          @media (prefers-color-scheme: dark) {
            :root {
              --answer-bg: #1e293b;
              --answer-color: #f8fafc;
            }
          }
        `}</style>
      </>
    );
}
