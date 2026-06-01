import { useState, useEffect, useRef } from "react";

const API_BASE = "http://localhost:8000";

const styles = `
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #202123; color: white; font-family: Arial, sans-serif; height: 100vh; overflow: hidden; }
.app { display: flex; height: 100vh; }
.sidebar { width: 300px; background: #171717; border-right: 1px solid #2f2f2f; display: flex; flex-direction: column; }
.sidebar-header { padding: 20px; border-bottom: 1px solid #2f2f2f; display: flex; justify-content: space-between; align-items: center; }
.sidebar-header h2 { font-size: 18px; }
.sidebar-header button { background: #2f2f2f; border: none; color: white; padding: 10px 14px; border-radius: 10px; cursor: pointer; }
.workflow-list { flex: 1; overflow-y: auto; padding: 12px; }
.workflow-item { background: #202123; border: 1px solid #2f2f2f; padding: 14px; border-radius: 12px; margin-bottom: 10px; cursor: pointer; transition: 0.2s; }
.workflow-item:hover { background: #2a2b32; }
.workflow-item.active { border-color: #3b82f6; }
.workflow-item h4 { font-size: 14px; margin-bottom: 6px; }
.workflow-item p { font-size: 12px; color: #9ca3af; }
.main { flex: 1; overflow-y: auto; padding: 40px; }
.top-section { max-width: 900px; margin: 0 auto 30px; }
.top-section h1 { font-size: 42px; margin-bottom: 24px; }
.query-box { background: #2a2b32; border: 1px solid #3a3a3a; border-radius: 18px; padding: 20px; }
.query-box textarea { width: 100%; min-height: 140px; background: transparent; border: none; outline: none; resize: none; color: white; font-size: 16px; }
.query-box button { margin-top: 16px; background: #10a37f; border: none; padding: 14px 20px; border-radius: 12px; color: white; cursor: pointer; font-weight: bold; }
.workflow-section { max-width: 900px; margin: 0 auto; }
.workflow-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.status-badge { background: #374151; padding: 10px 18px; border-radius: 999px; text-transform: capitalize; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px; }
.card { background: #2a2b32; border: 1px solid #3a3a3a; padding: 20px; border-radius: 16px; }
.card h3 { margin-bottom: 10px; color: #9ca3af; }
.output-card { background: #2a2b32; border: 1px solid #3a3a3a; padding: 20px; border-radius: 16px; margin-bottom: 20px; }
.output-card h3 { margin-bottom: 14px; }
pre { white-space: pre-wrap; overflow-x: auto; color: #d1d5db; }
.actions { display: flex; gap: 14px; }
.actions button { border: none; padding: 14px 20px; border-radius: 12px; color: white; cursor: pointer; font-weight: bold; }
.approve-btn { background: #16a34a; }
.reject-btn { background: #dc2626; }
`;

function getStoredWorkflows() {
  return JSON.parse(localStorage.getItem("workflows") || "[]");
}

function saveStoredWorkflows(workflows) {
  localStorage.setItem("workflows", JSON.stringify(workflows));
}

export default function App() {
  const [query, setQuery] = useState("");
  const [workflows, setWorkflows] = useState(getStoredWorkflows);
  const [currentId, setCurrentId] = useState(null);
  const [workflowData, setWorkflowData] = useState(null);
  const socketRef = useRef(null);

  const connectWebSocket = (requestId) => {
    if (socketRef.current) socketRef.current.close();
    const ws = new WebSocket(`ws://localhost:8000/ws/${requestId}`);
    ws.onmessage = (e) => setWorkflowData(JSON.parse(e.data));
    socketRef.current = ws;
  };

  const loadWorkflow = async (requestId) => {
    try {
      const res = await fetch(`${API_BASE}/workflow/${requestId}`);
      if (!res.ok) throw new Error("Not found");
      const data = await res.json();
      setCurrentId(requestId);
      setWorkflowData(data);
      connectWebSocket(requestId);
    } catch (err) {
      console.error(err);
    }
  };

  const startWorkflow = async () => {
    const q = query.trim();
    if (!q) return alert("Enter workflow query");
    try {
      const res = await fetch(`${API_BASE}/workflow/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      const data = await res.json();
      const updated = [...getStoredWorkflows(), { request_id: data.request_id, query: q }];
      saveStoredWorkflows(updated);
      setWorkflows(updated);
      setQuery("");
      loadWorkflow(data.request_id);
    } catch (err) {
      console.error(err);
      alert("Failed to start workflow");
    }
  };

  const approve = async () => {
    if (!currentId) return;
    await fetch(`${API_BASE}/workflow/${currentId}/approve`, { method: "POST" }).catch(console.error);
  };

  const reject = async () => {
    if (!currentId) return;
    await fetch(`${API_BASE}/workflow/${currentId}/reject`, { method: "POST" }).catch(console.error);
  };

  const w = workflowData;

  return (
    <>
      <style>{styles}</style>
      <div className="app">
        <aside className="sidebar">
          <div className="sidebar-header">
            <h2>Workflows</h2>
            <button onClick={() => setWorkflowData(null)}>+ New</button>
          </div>
          <div className="workflow-list">
            {[...workflows].reverse().map((wf) => (
              <div
                key={wf.request_id}
                className={`workflow-item${wf.request_id === currentId ? " active" : ""}`}
                onClick={() => loadWorkflow(wf.request_id)}
              >
                <h4>{wf.query}</h4>
                <p>{wf.request_id}</p>
              </div>
            ))}
          </div>
        </aside>

        <main className="main">
          <div className="top-section">
            <h1>Workflow Console</h1>
            <div className="query-box">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Describe your workflow..."
              />
              <button onClick={startWorkflow}>Start Workflow</button>
            </div>
          </div>

          {w && (
            <div className="workflow-section">
              <div className="workflow-top">
                <div>
                  <h2>Workflow Execution</h2>
                  <p>{w.request_id}</p>
                </div>
                <div className="status-badge">{w.status || "pending"}</div>
              </div>

              <div className="grid">
                <div className="card"><h3>Status</h3><p>{w.status || "-"}</p></div>
                <div className="card"><h3>Approval</h3><p>{w.approval_status || "-"}</p></div>
                <div className="card"><h3>Retries</h3><p>{w.retry_count || 0}</p></div>
              </div>

              <div className="output-card">
                <h3>Final Output</h3>
                <pre>{w.final_output ? JSON.stringify(w.final_output["document"], null, 2) : "No output yet"}</pre>
              </div>

              <div className="output-card">
                <h3>Error</h3>
                <pre>{w.error || "No errors"}</pre>
              </div>

              <div className="actions">
                <button className="approve-btn" onClick={approve}>Approve</button>
                <button className="reject-btn" onClick={reject}>Reject</button>
              </div>
            </div>
          )}
        </main>
      </div>
    </>
  );
}