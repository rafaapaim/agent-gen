import { createAgent, deleteAgent, fetchAgents, fetchHealth, sendChat } from "./api.js";
import { appState, applyError, setAgents, setMessages, setSelectedAgent, setStatus } from "./state.js";

const app = document.querySelector("#app");
let pendingChatRetry = null;
let isChatPending = false;
let activeChatRequest = 0;

function renderLayout() {
  app.innerHTML = `
    <div class="app-shell">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h1>Agent Manager</h1>
          <button id="refresh-agents" class="secondary">Refresh</button>
        </div>
        <div id="agent-list" class="agent-list"></div>
        <form id="create-agent-form" class="panel-form">
          <h2>Create agent</h2>
          <label>
            Name
            <input id="agent-name" name="name" type="text" placeholder="custom-agent" required />
          </label>
          <label>
            Modelfile path
            <input id="modelfile-path" name="modelfilePath" type="text" placeholder="C:/path/to/Modelfile" required />
          </label>
          <button type="submit">Create</button>
        </form>
      </aside>

      <main class="chat-panel">
        <header class="chat-header">
          <div>
            <h2 id="selected-agent-title">No agent selected</h2>
            <p id="status-message" role="status" aria-live="polite">Ready</p>
          </div>
          <button id="delete-agent" class="danger">Delete</button>
        </header>
        <div id="error-banner" class="error-banner hidden"></div>
        <div id="chat-messages" class="messages"></div>
        <form id="chat-form" class="chat-form">
          <textarea id="chat-input" rows="3" placeholder="Type a message..."></textarea>
          <button id="chat-submit" type="submit">Send</button>
        </form>
      </main>
    </div>
  `;

  const refreshButton = document.querySelector("#refresh-agents");
  refreshButton.addEventListener("click", loadAgents);

  document.querySelector("#delete-agent").addEventListener("click", handleDeleteSelected);
  document.querySelector("#chat-form").addEventListener("submit", handleChatSubmit);
  document.querySelector("#create-agent-form").addEventListener("submit", handleCreateAgent);
}

function renderError() {
  const banner = document.querySelector("#error-banner");
  if (!appState.error) {
    banner.classList.add("hidden");
    banner.textContent = "";
    return;
  }
  banner.classList.remove("hidden");
  banner.textContent = appState.error;
}

function renderAgents() {
  const list = document.querySelector("#agent-list");
  if (!appState.agents.length) {
    list.innerHTML = '<p class="empty-state">No agents available. Create one from the form.</p>';
    return;
  }

  list.innerHTML = appState.agents
    .map(
      (agent) => `
        <button type="button" class="agent-card ${appState.selectedAgent === agent.name ? "selected" : ""}" data-name="${agent.name}" ${isChatPending ? "disabled" : ""}>
          <span class="agent-name">${agent.name}</span>
          <span class="agent-status">${agent.status}</span>
        </button>
      `,
    )
    .join("");

  list.querySelectorAll(".agent-card").forEach((button) => {
    button.addEventListener("click", () => {
      setSelectedAgent(button.dataset.name);
      render();
    });
  });
}

function renderMessages() {
  const container = document.querySelector("#chat-messages");
  if (!appState.messages.length) {
    container.innerHTML = '<div class="empty-chat">No conversation yet. Start with a message.</div>';
    return;
  }

  container.innerHTML = appState.messages
    .map(
      (message) => `
        <div class="message ${message.role === "user" ? "user" : "assistant"}">
          <strong>${message.role === "user" ? "You" : appState.selectedAgent}</strong>
          <p>${message.content}</p>
        </div>
      `,
    )
    .join("");
}

async function loadAgents() {
  setStatus("loading");
  try {
    const [health, agents] = await Promise.all([fetchHealth(), fetchAgents()]);
    if (!health.connected) {
      applyError(health.message);
      setAgents([]);
      render();
      return;
    }
    setAgents(agents);
    setStatus("ready", null);
    if (!appState.selectedAgent && appState.agents.length) {
      setSelectedAgent(appState.agents[0].name);
    }
    render();
  } catch (error) {
    applyError(error.message || "Unable to load agents.");
    setAgents([]);
    render();
  }
}

async function handleCreateAgent(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const name = form.elements.name.value.trim();
  const modelfilePath = form.elements.modelfilePath.value.trim();

  try {
    await createAgent(name, modelfilePath);
    form.reset();
    await loadAgents();
  } catch (error) {
    applyError(error.message);
    renderError();
  }
}

async function handleDeleteSelected() {
  if (!appState.selectedAgent) {
    applyError("Select an agent to delete.");
    renderError();
    return;
  }

  const confirmed = window.confirm(`Delete ${appState.selectedAgent}?`);
  if (!confirmed) {
    return;
  }

  try {
    await deleteAgent(appState.selectedAgent);
    await loadAgents();
  } catch (error) {
    applyError(error.message);
    renderError();
  }
}

async function handleChatSubmit(event) {
  event.preventDefault();
  if (isChatPending) {
    return;
  }

  const input = document.querySelector("#chat-input");
  const message = input.value.trim();
  if (!message || !appState.selectedAgent) {
    applyError("Select an agent and enter a message.");
    renderError();
    return;
  }

  const agentName = appState.selectedAgent;
  const isRetry = pendingChatRetry?.agentName === agentName && pendingChatRetry.message === message;
  const nextMessages = isRetry ? appState.messages : [...appState.messages, { role: "user", content: message }];
  const requestId = ++activeChatRequest;
  isChatPending = true;
  pendingChatRetry = null;
  setMessages(nextMessages);
  setStatus("chatting", null);
  input.value = "";
  render();

  try {
    const response = await sendChat(agentName, message);
    if (requestId !== activeChatRequest || appState.selectedAgent !== agentName) {
      return;
    }
    setMessages([...nextMessages, { role: "assistant", content: response.content }]);
    setStatus("ready", null);
  } catch (error) {
    if (requestId !== activeChatRequest || appState.selectedAgent !== agentName) {
      return;
    }
    pendingChatRetry = { agentName, message };
    input.value = message;
    input.focus();
    applyError(error.message);
  } finally {
    if (requestId === activeChatRequest) {
      isChatPending = false;
      render();
    }
  }
}

function render() {
  const selectedAgent = appState.selectedAgent || "No agent selected";
  const title = document.querySelector("#selected-agent-title");
  const statusMessage = document.querySelector("#status-message");
  if (title) title.textContent = selectedAgent;
  if (statusMessage) {
    statusMessage.textContent = isChatPending
      ? "Waiting for the agent to start and respond..."
      : appState.status === "loading"
        ? "Loading agents..."
        : appState.status === "error"
          ? "Needs attention"
          : "Ready";
    statusMessage.classList.toggle("chat-status-pending", isChatPending);
  }
  const chatInput = document.querySelector("#chat-input");
  const chatSubmit = document.querySelector("#chat-submit");
  if (chatInput) chatInput.disabled = isChatPending;
  if (chatSubmit) chatSubmit.disabled = isChatPending;
  const refreshButton = document.querySelector("#refresh-agents");
  const deleteButton = document.querySelector("#delete-agent");
  const createButton = document.querySelector("#create-agent-form button[type='submit']");
  if (refreshButton) refreshButton.disabled = isChatPending;
  if (deleteButton) deleteButton.disabled = isChatPending;
  if (createButton) createButton.disabled = isChatPending;
  renderAgents();
  renderMessages();
  renderError();
}

renderLayout();
loadAgents();
