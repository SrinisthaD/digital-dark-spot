
import { useState } from "react";
import "./App.css";
async function analyzeResearch(topic, sources) {
  const response = await fetch("https://digital-dark-spot-unft.onrender.com/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      topic: topic,
      sources: sources,
    }),
  });

  if (!response.ok) {
    throw new Error("The backend could not analyze your research.");
  }

  return await response.json();
}

function App() {
  const [topic, setTopic] = useState("");
  const [sources, setSources] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  return (
    <div className="app">

      {/* Navigation */}
      <nav className="navbar">
        <div className="logo">
          <span className="logo-icon">◈</span>
          DIGITAL DARK SPOT
        </div>

        <div className="nav-right">
          <span>AI Research Platform</span>
          <button className="nav-button">
            Get Started
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-container">

        <div className="hero">
          <div className="tag">
            ✦ AI-POWERED INFORMATION ANALYSIS
          </div>

          <h1>
            Find what the internet
            <br />
            <span>is missing.</span>
          </h1>

          <p>
            Discover information gaps, conflicting claims,
            outdated details and unanswered questions
            before making important decisions.
          </p>
        </div>

        {/* Research Form */}
        <div className="research-card">

          <label>Your Research Question</label>

          <textarea
            placeholder="Example: What should I verify before applying for a scholarship?"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />

          <label>Research Sources</label>

          <textarea
            className="source-input"
            placeholder={"Paste website URLs here, one URL per line...\nhttps://example.com"}
            value={sources}
            onChange={(e) => setSources(e.target.value)}
          />

          
<button
  className="analyze-button"
  disabled={loading}
  onClick={async () => {
    if (!topic.trim() || !sources.trim()) {
      alert("Please enter a research question and at least one source.");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const sourceList = sources
        .split(/\n|,/)
        .map((url) => url.trim())
        .filter((url) => url.length > 0);

      const data = await analyzeResearch(topic, sourceList);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }}
>
  {loading ? "Analyzing..." : "Analyze Information"} <span>→</span>
</button>


{error && (
  <div className="error-message">
    <p>⚠️ {error}</p>
  </div>
)}

{results && (
  <div className="analysis-results">
    <h2>AI Analysis Results</h2>
    
    <button
      className="download-button"
      onClick={() => {
        const report = JSON.stringify(results, null, 2);
        const blob = new Blob([report], {
          type: "application/json",
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = "digital-dark-spot-report.json";
        link.click();

        URL.revokeObjectURL(url);
      }}
    >
      Download Analysis Report
    </button>

    <h3>Summary</h3>
    <p>{results.summary}</p>

    
    <h3>Sources Reviewed</h3>

    {results.source_details?.length > 0 ? (
      results.source_details.map((source) => (
        <div key={source.id} className="gap-card">
          <h4>{source.id}: {source.title}</h4>
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            {source.url}
          </a>
        </div>
      ))
    ) : (
      <p>No source details available.</p>
    )}

    <h3>Information Gaps</h3>
    {results.information_gaps?.length > 0 ? (
      results.information_gaps.map((gap, index) => (
        <div key={index} className="gap-card">
          <h4>{gap.issue}</h4>
          <p>{gap.explanation}</p>
          {gap.evidence && (
            <p>
              <strong>Evidence:</strong> {gap.evidence}
            </p>
          )}

          {gap.confidence && (
            <p>
              <strong>AI Confidence:</strong> {gap.confidence}
            </p>
          )}
          <small>Sources: {gap.source_ids?.join(", ")}</small>
        </div>
      ))
    ) : (
      <p>No potential information gaps identified.</p>
    )}

    <h3>Potential Conflicts</h3>
    {results.conflicts?.length > 0 ? (
      results.conflicts.map((conflict, index) => (
        <div key={index}>
          <h4>{conflict.claim}</h4>
          <p>{conflict.explanation}</p>
        </div>
      ))
    ) : (
      <p>No conflicts identified in the supplied sources.</p>
    )}

    
<h3>Potentially Outdated Information</h3>

{results.outdated_signals?.length > 0 ? (
  results.outdated_signals.map((signal, index) => (
    <div key={index} className="gap-card">
      <h4>{signal.issue}</h4>
      <p>{signal.explanation}</p>
      <small>
        Sources: {signal.source_ids?.join(", ") || "Not specified"}
      </small>
    </div>
  ))
) : (
  <p>No potentially outdated information identified.</p>
)}

<h3>Unanswered Questions</h3>

{results.unanswered_questions?.length > 0 ? (
  results.unanswered_questions.map((question, index) => (
    <div key={index} className="gap-card">
      <p>{question}</p>
    </div>
  ))
) : (
  <p>No unanswered questions identified.</p>
)}

    <h3>Verification Checklist</h3>
    
    {results.verification_checklist?.map((item, index) => (
    <div key={index} className="checklist-card">
        {typeof item === "string" ? (
          <p>{item}</p>
        ) : (
          <>
            <span
              className={`priority-badge priority-${(item.priority || "low").toLowerCase()}`}
            >
              {item.priority || "Low"} Priority
            </span>

            <p><strong>{item.task}</strong></p>

            {item.reason && (
              <p className="checklist-reason">{item.reason}</p>
            )}
          </>
        )}
      </div>
    ))}

  </div>
)}



          <p className="privacy-note">
            Your research. Your evidence. Better decisions.
          </p>

        </div>

        {/* Features */}
        <section className="features">

          <div className="feature-card">
            <div className="feature-icon">⌕</div>
            <h3>Information Gaps</h3>
            <p>Discover what important information is missing.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚖</div>
            <h3>Conflict Detection</h3>
            <p>Compare claims across different sources.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">◷</div>
            <h3>Outdated Information</h3>
            <p>Identify information that may need verification.</p>
          </div>

        </section>

      </main>

      <footer>
        DIGITAL DARK SPOT © 2026 | AI-Assisted Research
      </footer>

    </div>
  );
}

export default App;
