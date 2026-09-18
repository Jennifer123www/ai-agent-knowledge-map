(() => {
  const pathParts = decodeURIComponent(location.pathname).split('/').filter(Boolean);
  const section = pathParts.at(-2);
  const inLearn = section === 'learn';
  const inInterview = section === 'interview';
  const beginner = inLearn ? '' : inInterview ? '../learn/' : 'learn/';
  const interview = inInterview ? '' : inLearn ? '../interview/' : 'interview/';

  const modules = [
    ['foundation', '基础模型与推理', '大语言模型 多模态 向量嵌入 重排序 模型适配 LLM'],
    ['context', '知识检索与检索增强生成', 'RAG 知识库 分段 召回 引用 向量检索'],
    ['improvement', '记忆与上下文工程', '短期状态 长期记忆 记忆写入 上下文构造 记忆治理'],
    ['core', '智能体与工作流', 'Agent 提示词 推理 规划 路由 反思 循环'],
    ['capabilities', '工具、技能与协议', 'Skill 工具调用 Function Calling MCP 连接器 插件'],
    ['orchestration', '多智能体协作', '工作流 状态图 多 Agent Handoff 人工参与'],
    ['evaluation', '评测、可观测性与持续优化', 'Trace 链路追踪 离线评测 线上监控 反馈 实验'],
    ['governance', '安全、权限与治理', '身份认证 授权 密钥 Guardrail 护栏 隐私 审计 提示词注入'],
    ['runtime', '系统设计、运行时与成本', '运行时 沙箱 事件 消息队列 缓存 存储 A2A 成本 时延'],
    ['applications', '应用落地与项目实践', '研究智能体 编程智能体 数据分析智能体 流程智能体 具身智能体 项目']
  ];

  const children = [
    ['foundation', 'llm', '大语言模型', 'LLM 词元 注意力 采样'], ['foundation', 'multimodal', '多模态模型', 'VLM 图像 视觉 语音'], ['foundation', 'embedding', '向量嵌入模型', 'Embedding 向量 相似度 HNSW'], ['foundation', 'reranker', '重排序模型', 'Reranker ColBERT'], ['foundation', 'adaptation', '模型适配', 'LoRA QLoRA 微调'],
    ['context', 'knowledgebase', '知识库', '文档 版本 权限'], ['context', 'knowledgegraph', '知识源、知识图谱与 GraphRAG', '文档 Wiki 数据库 数仓 向量数据库 图谱 实体 关系 多跳检索'], ['context', 'rag', '检索增强生成', 'RAG 检索 引用'], ['context', 'chunking', '分段与元数据', 'Chunking 切分'], ['context', 'retrieval', '召回、重排序与引用', '检索 混合召回'],
    ['improvement', 'shortterm', '短期状态', '状态 检查点'], ['improvement', 'longterm', '长期记忆', 'Memory 偏好'], ['improvement', 'memorytypes', '记忆类型与用户画像', '工作记忆 情景记忆 语义记忆 用户画像 偏好'], ['improvement', 'memorywrite', '记忆写入与更新', '冲突 合并 删除'], ['improvement', 'contextbuild', '上下文构造', 'Context Token 窗口'], ['improvement', 'memorygovernance', '记忆治理', '隐私 保留期'],
    ['core', 'persona', '角色与职责设定', 'Role 边界'], ['core', 'prompt', '系统指令与提示词', 'Prompt 提示词 注入'], ['core', 'reasoning', '基于证据的推理', 'Reasoning ReAct'], ['core', 'planning', '任务规划', 'Planning 计划'], ['core', 'routing', '模型与能力路由', 'Routing 模型路由'], ['core', 'reflection', '反思与纠错', 'Reflection 复盘'], ['core', 'loop', '智能体执行循环', 'Agent Loop 停止条件'],
    ['capabilities', 'skill', '技能', 'Skill 标准作业'], ['capabilities', 'toolcalling', '工具调用', 'Function Calling 函数调用'], ['capabilities', 'execution', 'API、代码与浏览器执行', 'API Code 执行 沙箱 Browser 浏览器 Computer Use'], ['capabilities', 'mcp', '模型上下文协议', 'MCP 协议 工具 资源'], ['capabilities', 'mcpobjects', 'MCP Client、Server 与三类能力', 'Client Server Tools Resources Prompts'], ['capabilities', 'connector', '连接器与插件', 'Connector Plugin'],
    ['orchestration', 'workflow', '工作流', 'Workflow 流程'], ['orchestration', 'stategraph', '状态与任务图', 'State Graph 状态机'], ['orchestration', 'multiagent', '多智能体协作', 'Multi-Agent 多 Agent'], ['orchestration', 'supervisor', '主管调度与 Agent 通信', 'Supervisor 委派 通信 专家 协作'], ['orchestration', 'handoff', '交接与人工参与', 'Handoff Human in the loop 人工'],
    ['evaluation', 'trace', '链路追踪', 'Trace Span 可观测性'], ['evaluation', 'offlineeval', '离线评测', 'Evaluation Evals'], ['evaluation', 'monitoring', '线上监控', 'Monitoring 告警'], ['evaluation', 'release', '版本、实验与发布管理', '版本 灰度 A/B 回滚 Release'], ['evaluation', 'feedback', '反馈与实验', 'Feedback A/B'],
    ['governance', 'identity', '身份认证', 'Authentication 登录'], ['governance', 'authorization', '授权与最小权限', 'Authorization RBAC'], ['governance', 'approval', '审批机制与人类把关', 'Approval Human Oversight 审批 人工确认'], ['governance', 'secrets', '密钥与凭据管理', 'Secrets API Key'], ['governance', 'guardrail', '安全护栏', 'Guardrail 内容安全 提示词注入'], ['governance', 'audit', '隐私与审计', 'Privacy Audit'],
    ['runtime', 'runtime', '智能体运行时', 'Agent Runtime'], ['runtime', 'sandbox', '沙箱执行环境', 'Sandbox 隔离'], ['runtime', 'gateway', '模型网关与流量治理', 'Model Gateway 路由 限流 配额'], ['runtime', 'schedule', '定时任务与事件触发', 'Schedule 定时 事件 触发器'], ['runtime', 'event', '事件与消息队列', 'Event Queue Kafka'], ['runtime', 'storage', '状态存储与缓存', 'Storage Cache Redis'], ['runtime', 'delivery', '部署、扩缩容与发布', 'Deployment Scaling 灰度 回滚'], ['runtime', 'a2a', '智能体对智能体协议', 'A2A Agent2Agent'],
    ['applications', 'researchagent', '研究型智能体', 'Research Agent 调研'], ['applications', 'codingagent', '编程智能体', 'Coding Agent 代码'], ['applications', 'dataagent', '数据分析智能体', 'Data Agent 数据'], ['applications', 'processagent', '业务流程智能体', 'Business Process Agent'], ['applications', 'officeagent', '办公、客服与销售智能体', 'Office Customer Service Sales 客服销售 客服 销售 办公'], ['applications', 'embodied', '具身智能体', 'Embodied Agent 机器人']
  ];

  const interviewTopic = {foundation: 'foundation', context: 'rag', improvement: 'memory', core: 'agent', capabilities: 'tools', orchestration: 'multiagent', evaluation: 'evaluation', governance: 'safety', runtime: 'system', applications: 'project'};
  const entries = [
    {title: '初学者总览', meta: '初学者 · 全景知识图谱', words: 'AI Agent 智能体 知识图谱 学习地图 总览', href: `${beginner}index.html`},
    {title: '初学者概念下钻', meta: '初学者 · 子模块图解与大话系列', words: '初学者 下钻 大话 机制加餐 图解', href: `${beginner}concepts.html?topic=foundation`},
    {title: '面试图谱', meta: '面向面试 · 高频主题与答题结构', words: '面试 高频 题库 答题 记忆点', href: `${interview}index.html`},
    {title: '面试题下钻', meta: '面向面试 · 原理、答题点与追问', words: '面试题 原理 追问 图解', href: `${interview}questions.html?topic=foundation`}
  ];

  modules.forEach(([topic, title, words]) => {
    entries.push({title, meta: '初学者 · 模块下钻', words, href: `${beginner}concepts.html?topic=${topic}`});
    entries.push({title: `${title}面试题`, meta: '面向面试 · 高频练习', words: `${words} 面试 高频 答题`, href: `${interview}questions.html?topic=${interviewTopic[topic]}`});
  });
  children.forEach(([topic, child, title, words]) => entries.push({title, meta: '初学者 · 子模块图解、大话与机制加餐', words: `${words} ${modules.find(item => item[0] === topic)[1]}`, href: `${beginner}concepts.html?topic=${topic}&child=${child}`}));

  const style = document.createElement('style');
  style.textContent = `
    .site-search .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0, 0, 0, 0); white-space:nowrap; border:0; }
    .site-search { position:relative; flex:0 1 224px; width:224px; color:var(--ink); }
    .site-search input { width:100%; height:31px; padding:0 10px; border:1px solid var(--line); border-radius:4px; background:var(--paper); color:var(--ink); font:inherit; font-size:12px; outline:0; }
    .site-search input::placeholder { color:var(--muted); }
    .site-search input:focus { border-color:var(--accent, var(--green)); box-shadow:0 0 0 2px color-mix(in srgb, var(--accent, var(--green)) 18%, transparent); }
    .site-search-results { position:absolute; right:0; top:calc(100% + 7px); z-index:20; display:none; width:min(420px,calc(100vw - 24px)); max-height:min(470px,calc(100vh - 90px)); overflow:auto; border:1px solid var(--line); background:var(--surface); box-shadow:var(--shadow); }
    .site-search-results[data-open="true"] { display:block; }
    .site-search-result { display:block; padding:10px 12px; border-bottom:1px solid var(--line); color:var(--ink); text-decoration:none; }
    .site-search-result:last-child { border-bottom:0; }
    .site-search-result:hover, .site-search-result[aria-selected="true"] { background:var(--soft, var(--surface-soft)); }
    .site-search-result strong { display:block; font-size:13px; line-height:1.35; }
    .site-search-result span { display:block; margin-top:2px; color:var(--muted); font-size:11px; line-height:1.35; }
    .site-search-empty { padding:12px; color:var(--muted); font-size:12px; }
    @media (max-width:720px) { .site-search { width:min(100%,420px); flex-basis:auto; } .site-search input { height:34px; } .site-search-results { left:0; right:auto; width:100%; } }
    @media print { .site-search { display:none; } }
  `;
  document.head.append(style);

  document.querySelectorAll('[data-site-search]').forEach(host => {
    host.classList.add('site-search');
    host.innerHTML = '<label><span class="sr-only">搜索页面</span><input type="search" autocomplete="off" placeholder="搜索模块、术语或面试题" aria-label="搜索页面" aria-controls="siteSearchResults"></label><div class="site-search-results" id="siteSearchResults" role="listbox"></div>';
    const input = host.querySelector('input');
    const results = host.querySelector('.site-search-results');
    let activeIndex = -1;
    let visible = [];

    const close = () => { results.dataset.open = 'false'; activeIndex = -1; };
    const render = () => {
      const query = input.value.trim().toLowerCase();
      if (!query) { close(); results.replaceChildren(); return; }
      const terms = query.split(/\s+/).filter(Boolean);
      visible = entries.map(entry => {
        const haystack = `${entry.title} ${entry.meta} ${entry.words}`.toLowerCase();
        const matched = terms.every(term => haystack.includes(term));
        const score = matched ? terms.reduce((total, term) => total + (entry.title.toLowerCase().includes(term) ? 4 : 1), 0) : -1;
        return {...entry, score};
      }).filter(entry => entry.score >= 0).sort((a, b) => b.score - a.score || a.title.localeCompare(b.title, 'zh-CN')).slice(0, 8);
      activeIndex = -1;
      results.replaceChildren();
      if (!visible.length) {
        results.innerHTML = '<p class="site-search-empty">没有找到匹配页面</p>';
      } else {
        visible.forEach((entry, index) => {
          const link = document.createElement('a');
          link.className = 'site-search-result';
          link.href = entry.href;
          link.setAttribute('role', 'option');
          link.setAttribute('aria-selected', 'false');
          link.dataset.index = String(index);
          link.innerHTML = `<strong>${entry.title}</strong><span>${entry.meta}</span>`;
          results.append(link);
        });
      }
      results.dataset.open = 'true';
    };
    const setActive = index => {
      const links = [...results.querySelectorAll('.site-search-result')];
      if (!links.length) return;
      activeIndex = (index + links.length) % links.length;
      links.forEach((link, i) => link.setAttribute('aria-selected', String(i === activeIndex)));
      links[activeIndex].scrollIntoView({block: 'nearest'});
    };
    input.addEventListener('input', render);
    input.addEventListener('keydown', event => {
      if (event.key === 'ArrowDown') { event.preventDefault(); setActive(activeIndex + 1); }
      if (event.key === 'ArrowUp') { event.preventDefault(); setActive(activeIndex - 1); }
      if (event.key === 'Enter' && activeIndex >= 0 && visible[activeIndex]) { window.location.href = visible[activeIndex].href; }
      if (event.key === 'Escape') { input.value = ''; close(); input.blur(); }
    });
    document.addEventListener('pointerdown', event => { if (!host.contains(event.target)) close(); });
  });
})();
