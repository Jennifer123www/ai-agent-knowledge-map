# 记忆治理配图说明

- 版本：`0.1.0`；阶段：治理配图已绘制；Git 基线：`7378a4f`（`main`；绘制前 clean）；修改时间：`2026-09-28 CST`。
- 渲染：`scripts/render-memory-context-figures.py`；1536×1024 PNG；标签和删除方向逐项核对。
- `memorygovernance-cover.png`：明确用途、限制读取、删除闭环。
- `memorygovernance-access.png`：用户、租户、用途、日志四层读取边界。
- `memorygovernance-lifecycle.png`：提出、保存、使用、退出的时间线；不杜撰统一保留天数。
- `memorygovernance-delete.png`：定位请求，清理主记录、索引与缓存，再回查结果。
- `memorygovernance-test.png`：越权、过期、删除、审计四类反例。
- `memorygovernance-principle.png`：删除请求先触发失效标记阻断读取，再分叉传播到主记录、检索索引与缓存。各箭头表示需要执行的工程动作，而非承诺任何系统天然具备。

## 原理／规范依据与改绘边界

- 一手依据：[NIST Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework)，Core 的 `Control-P` 数据处理管理目标；另参考 [NIST Privacy Framework 原文 PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf)。这是一份**自愿框架**，不是强制法律条文。
- 保留的治理目标：知道哪些个人信息被处理、能控制使用和退出，并在必要范围内保护数据。图中的请求定位、失效标记与主记录／索引／缓存分叉是为记忆系统设计的工程拓扑，**不是 NIST 原图**。
- 简化：不展示每个备份保留期或各地区法定义务；备份与审计必须另按部署条件处理。删除图要避免“只删界面就完成”的误导。
- 图注：依据 NIST Privacy Framework 的 `Control-P` 目标设计；传播拓扑是工程示意。
