const state = {
  docs: [],
  filtered: [],
  selectedDocId: "",
  category: "",
  health: null,
};

const $ = (id) => document.getElementById(id);

function text(value) {
  if (Array.isArray(value)) return value.join(" ");
  return value || "";
}

function commandParts(item) {
  if (typeof item === "string") return { command: item, purpose: "", risk: "" };
  return {
    command: item.command || "",
    purpose: item.purpose || "",
    risk: item.risk || "",
  };
}

async function getJson(url, options) {
  const response = await fetch(url, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body?.error?.message || response.statusText);
  return body;
}

async function loadAll() {
  const [health, index] = await Promise.all([
    getJson("/health"),
    getJson("/api/kb/index"),
  ]);
  state.health = health;
  state.docs = index.documents || [];
  $("healthText").textContent = `${health.documents} 篇 / ${health.vector_model}`;
  renderCategories();
  applyFilters();
  renderStats();
}

function categoryOf(doc) {
  const parts = (doc.path || "").split("/");
  const idx = parts.indexOf("candidate");
  if (idx >= 0 && parts[idx + 1]) return parts[idx + 1];
  return parts.length > 2 ? parts[2] : "other";
}

function renderCategories() {
  const counts = new Map();
  state.docs.forEach((doc) => counts.set(categoryOf(doc), (counts.get(categoryOf(doc)) || 0) + 1));
  const entries = [["", state.docs.length], ...Array.from(counts.entries()).sort()];
  $("categoryList").innerHTML = entries.map(([name, count]) => `
    <button class="category ${state.category === name ? "active" : ""}" data-category="${name}">
      ${name || "全部"} <span class="muted">${count}</span>
    </button>
  `).join("");
  document.querySelectorAll(".category").forEach((button) => {
    button.addEventListener("click", () => {
      state.category = button.dataset.category || "";
      renderCategories();
      applyFilters();
    });
  });
}

function docSearchText(doc) {
  return [
    doc.title,
    doc.doc_id,
    doc.path,
    text(doc.tags),
    text(doc.systems),
    text(doc.asset_types),
    text(doc.issue_types),
    text(doc.steps),
    text(doc.verification),
    (doc.commands || []).map((item) => Object.values(commandParts(item)).join(" ")).join(" "),
    doc.content_preview,
  ].join(" ").toLowerCase();
}

function applyFilters() {
  const keyword = $("searchInput")?.value.trim().toLowerCase() || "";
  const status = $("statusFilter")?.value || "";
  const risk = $("riskFilter")?.value || "";
  state.filtered = state.docs.filter((doc) => {
    if (state.category && categoryOf(doc) !== state.category) return false;
    if (status && doc.status !== status) return false;
    if (risk === "high" && !(doc.risk_level === "high" || doc.review_required)) return false;
    if (risk === "normal" && (doc.risk_level === "high" || doc.review_required)) return false;
    if (keyword && !docSearchText(doc).includes(keyword)) return false;
    return true;
  });
  renderDocList();
}

function renderDocList() {
  $("docList").innerHTML = state.filtered.map((doc) => `
    <article class="doc-card ${state.selectedDocId === doc.doc_id ? "active" : ""}" data-doc-id="${doc.doc_id}">
      <h3>${doc.title}</h3>
      <div class="meta">
        <span class="tag">${doc.status}</span>
        <span class="tag">${categoryOf(doc)}</span>
        ${(doc.risk_level === "high" || doc.review_required) ? '<span class="tag high">高风险</span>' : ""}
        ${(doc.tags || []).slice(0, 4).map((tag) => `<span class="tag">${tag}</span>`).join("")}
      </div>
    </article>
  `).join("") || `<div class="detail empty">没有符合条件的知识。</div>`;
  document.querySelectorAll(".doc-card").forEach((card) => {
    card.addEventListener("click", () => {
      state.selectedDocId = card.dataset.docId;
      renderDocList();
      renderDocDetail(state.docs.find((doc) => doc.doc_id === state.selectedDocId));
    });
  });
  if (!state.selectedDocId && state.filtered[0]) {
    state.selectedDocId = state.filtered[0].doc_id;
    renderDocDetail(state.filtered[0]);
  }
}

function listSection(title, values, ordered = false) {
  if (!values || values.length === 0) return "";
  const tag = ordered ? "ol" : "ul";
  return `<section class="section"><h3>${title}</h3><${tag}>${values.map((item) => `<li>${item}</li>`).join("")}</${tag}></section>`;
}

function commandSection(values) {
  if (!values || values.length === 0) return "";
  return `<section class="section"><h3>常用指令</h3>${values.map((item) => {
    const cmd = commandParts(item);
    return `<div class="command">
      <pre>${cmd.command}</pre>
      ${(cmd.purpose || cmd.risk) ? `<p>${cmd.purpose ? `用途：${cmd.purpose}` : ""}${cmd.purpose && cmd.risk ? " | " : ""}${cmd.risk ? `风险：${cmd.risk}` : ""}</p>` : ""}
    </div>`;
  }).join("")}</section>`;
}

function renderDocDetail(doc) {
  if (!doc) {
    $("docDetail").className = "detail empty";
    $("docDetail").textContent = "选择左侧知识查看步骤、指令和验证方式。";
    return;
  }
  $("docDetail").className = "detail";
  $("docDetail").innerHTML = `
    <h2>${doc.title}</h2>
    <div class="meta">
      <span class="tag">${doc.doc_id}</span>
      <span class="tag">${doc.status}</span>
      <span class="tag">${doc.path}</span>
      ${(doc.risk_level === "high" || doc.review_required) ? '<span class="tag danger">高风险需复核</span>' : ""}
    </div>
    ${listSection("适用范围", doc.applicability)}
    ${listSection("常见现象", doc.symptoms)}
    ${listSection("处理步骤", doc.steps, true)}
    ${commandSection(doc.commands)}
    ${listSection("验证方式", doc.verification)}
    ${listSection("注意事项", doc.notes)}
    <section class="section"><h3>标签</h3><div class="meta">${(doc.tags || []).map((tag) => `<span class="tag">${tag}</span>`).join("")}</div></section>
  `;
}

async function runRecommend() {
  const title = $("ticketTitle").value.trim();
  const description = $("ticketDesc").value.trim();
  if (!title && !description) {
    $("recommendResults").innerHTML = `<div class="result-card">请输入工单标题或问题描述。</div>`;
    return;
  }
  $("recommendResults").innerHTML = `<div class="result-card">匹配中...</div>`;
  const result = await getJson("/api/kb/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticket_id: "manual-ui", title, description, mode: $("modeSelect").value, top_k: 5 }),
  });
  $("recommendResults").innerHTML = (result.recommendations || []).map((doc) => resultCard(doc, result.request_id)).join("") || `<div class="result-card">暂无推荐。</div>`;
  document.querySelectorAll("[data-feedback]").forEach((button) => {
    button.addEventListener("click", async () => {
      await getJson("/api/kb/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticket_id: "manual-ui",
          request_id: result.request_id,
          doc_id: button.dataset.docId,
          action: button.dataset.feedback,
        }),
      });
      button.textContent = "已记录";
      button.disabled = true;
    });
  });
}

function resultCard(doc, requestId) {
  return `<article class="result-card">
    <div class="result-head">
      <div>
        <h3>${doc.title}</h3>
        <div class="meta">
          <span class="tag ${doc.confidence === "high" ? "ok" : doc.confidence === "medium" ? "medium" : ""}">${doc.confidence}</span>
          <span class="tag">综合 ${doc.score}</span>
          <span class="tag">规则 ${doc.rule_score || 0}</span>
          <span class="tag">向量 ${doc.vector_score || 0}</span>
        </div>
      </div>
      <div class="row">
        <button class="button small secondary" data-feedback="useful" data-doc-id="${doc.doc_id}">有用</button>
        <button class="button small secondary" data-feedback="used" data-doc-id="${doc.doc_id}">已参考</button>
        <button class="button small secondary" data-feedback="not_useful" data-doc-id="${doc.doc_id}">无用</button>
      </div>
    </div>
    ${listSection("匹配原因", doc.reason)}
    ${listSection("适用范围", doc.applicability)}
    ${listSection("处理步骤", doc.steps, true)}
    ${commandSection(doc.commands)}
    ${listSection("验证方式", doc.verification)}
    <p class="muted">${doc.doc_id} · ${doc.path} · ${requestId}</p>
  </article>`;
}

function renderStats() {
  const byStatus = state.docs.reduce((acc, doc) => {
    acc[doc.status] = (acc[doc.status] || 0) + 1;
    return acc;
  }, {});
  const highRisk = state.docs.filter((doc) => doc.risk_level === "high" || doc.review_required).length;
  const withCommands = state.docs.filter((doc) => (doc.commands || []).length > 0).length;
  $("statsCards").innerHTML = [
    ["知识总数", state.docs.length],
    ["usable", byStatus.usable || 0],
    ["高风险", highRisk],
    ["含指令", withCommands],
  ].map(([label, value]) => `<div class="stat"><strong>${value}</strong><span>${label}</span></div>`).join("");
}

function setView(name) {
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === name));
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));
  $(`${name}View`).classList.add("active");
  const titles = {
    browse: ["知识浏览", "按分类、关键词、状态筛选知识。"],
    recommend: ["工单推荐", "输入工单或告警内容，查看推荐知识、步骤和指令。"],
    create: ["新增候选知识", "创建 Markdown 候选知识，随后重建索引后进入推荐。"],
    reports: ["治理视图", "查看知识状态和后续治理建议。"],
  };
  $("viewTitle").textContent = titles[name][0];
  $("viewHint").textContent = titles[name][1];
}

async function createDoc(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = Object.fromEntries(form.entries());
  ["applicability", "symptoms", "steps", "verification", "notes"].forEach((key) => {
    payload[key] = (payload[key] || "").split("\n").map((line) => line.trim()).filter(Boolean);
  });
  payload.commands = (payload.commands || "").split("\n").map((line) => line.trim()).filter(Boolean);
  try {
    const result = await getJson("/api/kb/admin/create-doc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    $("createResult").textContent = `已创建：${result.path}。请重建索引后刷新。`;
    event.target.reset();
  } catch (error) {
    $("createResult").textContent = error.message;
  }
}

function bindEvents() {
  document.querySelectorAll(".nav-item").forEach((item) => item.addEventListener("click", () => setView(item.dataset.view)));
  ["searchInput", "statusFilter", "riskFilter"].forEach((id) => $(id).addEventListener("input", applyFilters));
  $("refreshBtn").addEventListener("click", loadAll);
  $("reloadBtn").addEventListener("click", async () => {
    await getJson("/api/kb/admin/reload-index", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
    await loadAll();
  });
  $("recommendBtn").addEventListener("click", runRecommend);
  $("createForm").addEventListener("submit", createDoc);
}

bindEvents();
loadAll().catch((error) => {
  $("healthText").textContent = "连接失败";
  $("docList").innerHTML = `<div class="result-card">${error.message}</div>`;
});
