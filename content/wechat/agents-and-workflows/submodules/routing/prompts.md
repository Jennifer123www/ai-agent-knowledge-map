# 模型与能力路由配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 1536×1024 中文 PNG。路由选择须先满足权限与风险约束，再比较质量、时延和成本；不写固定比例或虚构跑分。
- `routing-cover.png`：日历查询、房间查询、草拟、人工确认四种不同路径。
- `routing-features.png`：请求类型、时限、权限、风险四项输入特征。
- `routing-paths.png`：硬规则分流后，候选路径分别进入工具、轻量模型、强模型和人工。
- `routing-fallback.png`：日历服务失效时明确“暂停给出确定时间”，不冒充查询成功。
- `routing-test.png`：误分流、服务超时、风险升级、成本约束四类测试。
- `routing-principle.png`：复现 Anthropic 路由工作流的主要拓扑：输入→分类→专用处理路径→统一结果校验；本图在分类前加权限过滤，在输出后加失败回退。

## 原理图依据与改绘边界

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 中 “Workflow: Routing” 图及对应文字。保留分类器决定专用路径的核心；会议工具、人工确认与权限闸门是本案例扩展，不是原文固定配置。
- 图注建议：“依据 Anthropic Routing 工作流结构改绘；风险闸门与回退路径为会议案例补充。”
