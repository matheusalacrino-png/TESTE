const STORAGE_KEY = "avaliazap_demo_v2";

const state = loadState();

const companyForm = document.getElementById("companyForm");
const requestForm = document.getElementById("requestForm");
const ratingForm = document.getElementById("ratingForm");
const leadForm = document.getElementById("leadForm");
const requestSelect = document.getElementById("requestId");
const historyTable = document.getElementById("historyTable");
const resetButton = document.getElementById("resetData");

companyForm?.addEventListener("submit", handleCompanySubmit);
requestForm?.addEventListener("submit", handleRequestSubmit);
ratingForm?.addEventListener("submit", handleRatingSubmit);
leadForm?.addEventListener("submit", handleLeadSubmit);
resetButton?.addEventListener("click", resetDemoData);

renderAll();

function handleCompanySubmit(event) {
  event.preventDefault();

  const data = new FormData(companyForm);
  state.company = {
    name: String(data.get("companyName") || "").trim(),
    whatsapp: String(data.get("companyWhatsapp") || "").trim(),
    googleUrl: String(data.get("companyGoogle") || "").trim(),
  };

  saveState();
  setMessage("companyMessage", `Empresa ${state.company.name} configurada com sucesso.`);
}

function handleRequestSubmit(event) {
  event.preventDefault();

  if (!state.company.name) {
    setMessage("requestMessage", "Cadastre a empresa antes de criar solicitações.", true);
    return;
  }

  const data = new FormData(requestForm);
  const item = {
    id: crypto.randomUUID(),
    customerName: String(data.get("customerName") || "").trim(),
    customerWhatsapp: String(data.get("customerWhatsapp") || "").trim(),
    serviceName: String(data.get("serviceName") || "").trim(),
    status: "pending",
    stars: null,
    comment: "",
    destination: "Aguardando resposta",
    createdAt: new Date().toISOString(),
  };

  state.requests.unshift(item);
  saveState();
  requestForm.reset();
  renderAll();

  setMessage(
    "requestMessage",
    `Solicitação enviada para ${item.customerName} via WhatsApp (${item.customerWhatsapp}).`
  );
}

function handleRatingSubmit(event) {
  event.preventDefault();

  const data = new FormData(ratingForm);
  const requestId = String(data.get("requestId") || "");
  const stars = Number(data.get("stars"));
  const comment = String(data.get("comment") || "").trim();

  const request = state.requests.find((r) => r.id === requestId);
  if (!request) {
    setMessage("ratingMessage", "Selecione uma solicitação válida.", true);
    return;
  }

  if (!stars || stars < 1 || stars > 5) {
    setMessage("ratingMessage", "Informe uma nota entre 1 e 5.", true);
    return;
  }

  request.stars = stars;
  request.comment = comment;

  if (stars <= 2) {
    request.status = "internal";
    request.destination = "Feedback interno";
    if (!comment) {
      setMessage(
        "ratingMessage",
        "Avaliações até 2 estrelas exigem comentário. Atualize com o motivo.",
        true
      );
      saveState();
      renderAll();
      return;
    }
    setMessage("ratingMessage", "Feedback crítico registrado para ação interna.");
  } else {
    request.status = "google";
    request.destination = state.company.googleUrl || "Google Meu Negócio";
    setMessage(
      "ratingMessage",
      `Cliente satisfeito! Encaminhar para avaliação pública: ${request.destination}`
    );
  }

  saveState();
  ratingForm.reset();
  renderAll();
}

function handleLeadSubmit(event) {
  event.preventDefault();
  const data = new FormData(leadForm);
  const company = String(data.get("empresa") || "sua empresa");
  setMessage("formMessage", `Perfeito! Recebemos o contato da ${company}.`);
  leadForm.reset();
}

function renderAll() {
  renderRequestSelect();
  renderMetrics();
  renderHistory();
}

function renderRequestSelect() {
  if (!requestSelect) return;

  const pending = state.requests.filter((item) => item.status === "pending");
  requestSelect.innerHTML = "";

  const first = document.createElement("option");
  first.value = "";
  first.textContent = pending.length
    ? "Escolha uma solicitação pendente"
    : "Sem solicitações pendentes";
  requestSelect.appendChild(first);

  pending.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = `${item.customerName} • ${item.serviceName}`;
    requestSelect.appendChild(option);
  });
}

function renderMetrics() {
  const total = state.requests.length;
  const rated = state.requests.filter((item) => item.stars !== null);
  const positive = rated.filter((item) => Number(item.stars) >= 3);
  const critical = rated.filter((item) => Number(item.stars) <= 2);
  const pending = state.requests.filter((item) => item.status === "pending");
  const average =
    rated.length > 0
      ? rated.reduce((sum, item) => sum + Number(item.stars), 0) / rated.length
      : 0;

  setText("mTotal", total);
  setText("mRated", rated.length);
  setText("mAverage", average.toFixed(1));
  setText("mPositive", rated.length ? `${Math.round((positive.length / rated.length) * 100)}%` : "0%");
  setText("mCritical", critical.length);
  setText("mPending", pending.length);
}

function renderHistory() {
  if (!historyTable) return;

  if (!state.requests.length) {
    historyTable.innerHTML =
      '<tr><td colspan="6">Nenhuma interação registrada ainda. Use o módulo operacional para iniciar.</td></tr>';
    return;
  }

  historyTable.innerHTML = state.requests
    .map((item) => {
      const statusLabel =
        item.status === "pending"
          ? '<span class="tag pending">Pendente</span>'
          : item.status === "internal"
          ? '<span class="tag internal">Interno</span>'
          : '<span class="tag google">Google</span>';

      return `
        <tr>
          <td>${escapeHtml(item.customerName)}</td>
          <td>${escapeHtml(item.serviceName)}</td>
          <td>${statusLabel}</td>
          <td>${item.stars ? `${item.stars}★` : "-"}</td>
          <td>${
            item.status === "google"
              ? `<a href="${escapeHtml(item.destination)}" target="_blank" rel="noreferrer">Abrir link</a>`
              : escapeHtml(item.destination)
          }</td>
          <td>${escapeHtml(item.comment || "-")}</td>
        </tr>
      `;
    })
    .join("");
}

function resetDemoData() {
  localStorage.removeItem(STORAGE_KEY);
  state.company = { name: "", whatsapp: "", googleUrl: "" };
  state.requests = [];
  renderAll();
  setMessage("requestMessage", "Dados da demonstração foram limpos.");
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = String(value);
}

function setMessage(id, text, isError = false) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = text;
  el.classList.toggle("error", isError);
}

function loadState() {
  const fallback = {
    company: { name: "", whatsapp: "", googleUrl: "" },
    requests: [],
  };

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? { ...fallback, ...JSON.parse(raw) } : fallback;
  } catch {
    return fallback;
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
