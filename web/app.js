const state = {
  docs: [],
  filtered: [],
  selectedDocId: "",
  category: "",
  health: null,
  aiConfig: null,
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
  const [health, index, aiConfig] = await Promise.all([
    getJson("/health"),
    getJson("/api/kb/index"),
    getJson("/api/kb/admin/ai-config"),
  ]);
  state.health = health;
  state.docs = index.documents || [];
  state.aiConfig = aiConfig || null;
  $("healthText").textContent = `${health.documents} 篇 / ${health.chunks || 0} 块 / ${health.vector_model}`;
  renderCategories();
  applyFilters();
  renderStats();
  renderAiConfig();
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

async function runAnswer() {
  const title = $("answerTitle").value.trim();
  const description = $("answerDesc").value.trim();
  if (!title && !description) {
    $("answerResults").innerHTML = `<div class="result-card">请输入问题、告警规则名或工单描述。</div>`;
    return;
  }
  $("answerResults").innerHTML = `<div class="result-card">检索知识块中...</div>`;
  const result = await getJson("/api/kb/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ticket_id: "manual-ui",
      title,
      description,
      mode: $("answerModeSelect").value,
      top_k: 12,
    }),
  });
  $("answerResults").innerHTML = answerCard(result);
}

function answerCard(result) {
  const answer = result.answer || {};
  const commands = answer.commands || [];
  const chunks = answer.retrieved_chunks || [];
  const sources = answer.sources || [];
  return `<article class="result-card">
    <div class="result-head">
      <div>
        <h3>处理建议</h3>
        <p class="muted">${answer.summary || "未召回到足够相关的知识块。"}</p>
      </div>
      <div class="meta">
        <span class="tag">${result.mode}</span>
        <span class="tag">${chunks.length} 个知识块</span>
      </div>
    </div>
    ${listSection("建议步骤", answer.suggested_steps || [], true)}
    ${commands.length ? `<section class="section"><h3>相关指令</h3>${commands.map((cmd) => `<div class="command">
      <pre>${cmd.command || ""}</pre>
      <p>${cmd.purpose ? `用途：${cmd.purpose}` : ""}${cmd.purpose && cmd.risk ? " | " : ""}${cmd.risk ? `风险：${cmd.risk}` : ""}</p>
    </div>`).join("")}</section>` : ""}
    ${listSection("验证方式", answer.verification || [])}
    ${listSection("注意事项", answer.cautions || [])}
    ${sources.length ? `<section class="section"><h3>引用来源</h3>${sources.map((source) => `<div class="source">
      <strong>${source.title}</strong>
      <p class="muted">${source.doc_id} · ${source.path} · score ${source.score}</p>
    </div>`).join("")}</section>` : ""}
    ${chunks.length ? `<section class="section"><h3>召回知识块</h3>${chunks.slice(0, 8).map((chunk) => `<div class="chunk">
      <div class="meta">
        <span class="tag">${chunk.type}</span>
        <span class="tag">综合 ${chunk.score}</span>
        <span class="tag">规则 ${chunk.rule_score || 0}</span>
        <span class="tag">向量 ${chunk.vector_score || 0}</span>
      </div>
      <p>${chunk.title}</p>
      <pre>${chunk.content || ""}</pre>
    </div>`).join("")}</section>` : ""}
    <p class="muted">${result.request_id}</p>
  </article>`;
}

async function submitExperience(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = Object.fromEntries(form.entries());
  $("experienceResultText").textContent = "分析中...";
  $("experienceResult").innerHTML = "";
  try {
    const result = await getJson("/api/kb/experience", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    $("experienceResultText").textContent = "已记录";
    $("experienceResult").innerHTML = experienceCard(result);
  } catch (error) {
    $("experienceResultText").textContent = error.message;
  }
}

function experienceCard(result) {
  const matched = result.matched_doc;
  const candidate = result.suggested_candidate;
  return `<article class="result-card">
    <div class="result-head">
      <div>
        <h3>沉淀结果</h3>
        <div class="meta">
          <span class="tag ${result.quality === "high" ? "ok" : result.quality === "medium" ? "medium" : "danger"}">${result.quality}</span>
          <span class="tag">质量 ${result.quality_score}</span>
          <span class="tag">${result.action}</span>
        </div>
      </div>
      <p class="muted">${result.experience_id}</p>
    </div>
    ${listSection("有效信号", result.signals || [])}
    ${listSection("缺失信息", result.missing_fields || [])}
    ${listSection("建议追问", result.suggested_questions || [])}
    ${matched ? `<section class="section"><h3>匹配已有知识</h3><div class="source">
      <strong>${matched.title}</strong>
      <p class="muted">${matched.doc_id} · score ${matched.score} · ${matched.path}</p>
    </div></section>` : ""}
    ${candidate ? `<section class="section"><h3>候选草稿</h3><div class="source">
      <strong>${candidate.title}</strong>
      <p class="muted">${candidate.candidate_id} · ${candidate.status}</p>
      ${listSection("现象", candidate.symptoms || [])}
      ${listSection("处理步骤", candidate.steps || [], true)}
      ${listSection("待补充", candidate.missing_fields || [])}
    </div></section>` : ""}
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

function renderAiConfig() {
  const config = state.aiConfig || {};
  const mappings = {
    configServiceName: config.service_name || "",
    configModelName: config.model_name || "",
    configHost: config.host || "",
    configPort: config.port || "",
    configBaseUrl: config.base_url || "",
    configApiKey: config.api_key || "",
    configModelsPath: config.models_path || "",
    configChatPath: config.chat_completions_path || "",
    configHealthPath: config.health_path || "",
    configNotes: config.notes || "",
  };
  Object.entries(mappings).forEach(([id, value]) => {
    if ($(id)) $(id).value = value;
  });
  if ($("configRuntime")) {
    $("configRuntime").innerHTML = [
      `当前运行地址：<strong>${config.runtime_base_url || "-"}</strong>`,
      `当前监听：<strong>${config.runtime_host || "-"}:${config.runtime_port || "-"}</strong>`,
      `API Key 已配置：<strong>${config.api_key_configured ? "是" : "否"}</strong>`,
      `端口修改待重启：<strong>${config.port_restart_required ? "是" : "否"}</strong>`,
    ].join("<br>");
  }
}

function setView(name) {
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === name));
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));
  $(`${name}View`).classList.add("active");
  const titles = {
    browse: ["知识浏览", "按分类、关键词、状态筛选知识。"],
    recommend: ["工单推荐", "输入工单或告警内容，查看推荐知识、步骤和指令。"],
    answer: ["智能答案", "按知识块检索步骤、指令和验证方式，生成可引用的处理建议。"],
    experience: ["经验沉淀", "记录关单处理经验，判断质量并决定补充已有知识或生成候选草稿。"],
    create: ["新增候选知识", "创建 Markdown 候选知识，随后重建索引后进入推荐。"],
    config: ["AI服务配置", "维护 AI 服务的默认配置。端口修改保存后需要重启服务才会生效。"],
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

async function loadAiConfig() {
  state.aiConfig = await getJson("/api/kb/admin/ai-config");
  renderAiConfig();
}

async function saveAiConfig(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = Object.fromEntries(form.entries());
  if (payload.port) payload.port = Number(payload.port);
  try {
    const result = await getJson("/api/kb/admin/ai-config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    state.aiConfig = result.config || null;
    renderAiConfig();
    $("configResult").textContent = state.aiConfig?.port_restart_required
      ? "已保存。端口变更需重启服务生效。"
      : "已保存。";
  } catch (error) {
    $("configResult").textContent = error.message;
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
  $("answerBtn").addEventListener("click", runAnswer);
  $("experienceForm").addEventListener("submit", submitExperience);
  $("createForm").addEventListener("submit", createDoc);
  $("configForm").addEventListener("submit", saveAiConfig);
  $("reloadConfigBtn").addEventListener("click", loadAiConfig);
}

bindEvents();
loadAll().catch((error) => {
  $("healthText").textContent = "连接失败";
  $("docList").innerHTML = `<div class="result-card">${error.message}</div>`;
});
