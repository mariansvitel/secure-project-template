const form = document.querySelector("#decision-form");
const submitButton = document.querySelector("#submit-button");
const statusElement = document.querySelector("#service-status");
const emptyState = document.querySelector("#empty-state");
const resultState = document.querySelector("#result-state");
const errorState = document.querySelector("#error-state");

function updateCount(fieldId, counterId, maximum) {
  const field = document.querySelector(fieldId);
  const counter = document.querySelector(counterId);
  const render = () => { counter.textContent = `${field.value.length} / ${maximum}`; };
  field.addEventListener("input", render);
  render();
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error("Health check failed");
    const health = await response.json();
    statusElement.classList.add(health.ai_configured ? "ready" : "offline");
    statusElement.lastChild.textContent = health.ai_configured ? " AI ready" : " AI key not configured";
  } catch {
    statusElement.classList.add("offline");
    statusElement.lastChild.textContent = " Server unavailable";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorState.hidden = true;
  resultState.hidden = true;
  emptyState.hidden = false;
  submitButton.disabled = true;
  submitButton.textContent = "Creating bounded draft…";
  const payload = {
    mode: document.querySelector("#mode").value,
    objective: document.querySelector("#objective").value,
    context: document.querySelector("#context").value,
    confirmed_safe_input: document.querySelector("#confirmed-safe-input").checked,
  };

  try {
    const response = await fetch("/api/assist", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(typeof data.detail === "string" ? data.detail : "Request failed.");
    }
    document.querySelector("#result-text").textContent = data.advice;
    document.querySelector("#result-model").textContent = data.model;
    document.querySelector("#result-redactions").textContent = String(data.redactions_applied);
    document.querySelector("#result-request").textContent = data.request_id.slice(0, 10);
    emptyState.hidden = true;
    resultState.hidden = false;
  } catch (error) {
    emptyState.hidden = true;
    errorState.textContent = error instanceof Error ? error.message : "Unexpected error.";
    errorState.hidden = false;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Create review draft";
  }
});

updateCount("#objective", "#objective-count", 1500);
updateCount("#context", "#context-count", 2500);
checkHealth();
