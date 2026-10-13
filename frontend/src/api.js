const API_BASE = "http://127.0.0.1:8000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let message = "Request failed.";
    try {
      const payload = await response.json();
      message = payload.error || message;
    } catch {
      // Ignore invalid JSON responses and fall back to the default error message.
    }
    throw new Error(message);
  }

  return response.status === 204 ? null : response.json();
}

export async function fetchAgents() {
  return apiRequest("/agents");
}

export async function createAgent(name, modelfilePath) {
  return apiRequest("/agents", {
    method: "POST",
    body: JSON.stringify({ name, modelfilePath }),
  });
}

export async function deleteAgent(agentName) {
  return apiRequest(`/agents/${encodeURIComponent(agentName)}`, {
    method: "DELETE",
  });
}

export async function sendChat(agentName, message) {
  return apiRequest("/chat", {
    method: "POST",
    body: JSON.stringify({ agentName, message }),
  });
}

export async function fetchHealth() {
  return apiRequest("/health");
}
