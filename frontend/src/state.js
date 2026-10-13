export const appState = {
  agents: [],
  selectedAgent: null,
  messages: [],
  status: "idle",
  error: null,
  isLoading: false,
};

export function setStatus(nextStatus, nextError = null) {
  appState.status = nextStatus;
  appState.error = nextError;
}

export function setAgents(agents) {
  appState.agents = agents;
  if (!agents.some((agent) => agent.name === appState.selectedAgent)) {
    appState.selectedAgent = agents[0]?.name ?? null;
  }
}

export function setMessages(messages) {
  appState.messages = messages;
}

export function setSelectedAgent(name) {
  appState.selectedAgent = name;
}

export function applyError(message) {
  appState.error = message;
  appState.status = "error";
}
