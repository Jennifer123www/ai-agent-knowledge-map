# 知识库子模块配图说明

版本：0.5.0；修订时间：2026-10-10 18:00 CST；依据提交：`82e01bb`（`main`，修改时工作区干净）。图片由 `scripts/render-knowledgebase-figures.mjs` 使用 SVG 确定性绘制并导出为 1536×1024 PNG；无需生成式配图提示词。

## 共同视觉规则

- 沿用暖白底、深灰文字、低饱和蓝绿与橙色；红色只表示失败、受限或撤回，绿色只表示通过或可用。
- 标题保持同一字号且控制在画布高度约 5% 内；不画左侧通高装饰线，不用大色条、渐变、盾牌或无关图标。
- 每张图只解释一项关系。文字、时间、金额和处理状态以正文案例为准，箭头要标清方向；准确文字用确定性排版。
- 主副文各自讲不同问题，不复用一套流程卡。主文解释资料生命周期，副文解释工程建模、故障定位和验收。

## 主文五图

1. `kb-case-scene.png`：开篇场景图。并列两份住宿制度：旧版上限 450 元、适用至 8 月 31 日；新版上限 500 元、9 月 1 日起生效。下方查询条件为 9 月 15 日、北京、A 职级，并指向新版与原文位置。不能用装饰线盖住字段。
2. `kb-principle.png`：知识库原理图。上层展示离线资料整理：正式发布源 → 原件版本 → 解析记录 → 可查索引；下层展示在线取用：查询条件 → 有效期与权限过滤 → 证据记录 → 正式原文。索引是派生查找入口，不是权威原件。
3. `kb-version.png`：区分业务生效时间与系统入库时间，示例新版自 9 月 1 日生效，9 月 5 日才补录；9 月 15 日查询应按住宿日期匹配新版。
4. `kb-access.png`：展示财务审批细则的权限从原件传递到解析记录、索引与缓存；普通员工查询时拒绝受限资料，人员调岗后旧缓存失效。
5. `kb-refresh.png`：更新经解析、字段抽检和候选索引验收后切换；失败时旧构建保持原状态。撤回沿来源 ID 清理派生记录，再反向查询验收。

## 面试副文图

1. `kb-interview-provenance.png`：来源登记、源版本、发布决策、解析产物和索引构建之间可追溯的数据关系。
2. `kb-interview-parser-test.png`：把字段值准确率与字段关系准确率分开；扫描页、跨页表格、脚注和修订页分层抽样。
3. `kb-interview-bitemporal.png`：同一业务日期同时按业务有效时间与系统记录时间查询；新版可追溯生效，但系统在补录前尚未知晓。
4. `kb-interview-acl-cache.png`：当前主体和策略版本参与授权与缓存隔离，撤权后相关缓存失效。
5. `kb-interview-sync.png`：`source_id`、版本和校验和形成幂等登记；重复事件复用结果，失败任务从已持久化检查点恢复。
6. `kb-interview-release.png`：候选索引隔离构建，通过字段、权限和样本查询门槛后原子切换；失败时入口留在旧版。
7. `kb-interview-deletion.png`：撤回事件传播到解析记录、索引和缓存；用原问题及不同身份反向查询，确认派生正文不再返回。

## 一手资料

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)：资料实体、处理活动及派生关系。
- [Microsoft Learn：Azure AI Search 索引器概述](https://learn.microsoft.com/en-us/azure/search/search-indexer-overview)：数据源同步与索引更新的产品实现示例。
- [Microsoft Learn：跟踪 Blob 变更与删除](https://learn.microsoft.com/en-us/azure/search/search-howto-index-changed-deleted-blobs)：删除检测和索引清理边界。
- [Microsoft Learn：Azure AI Search 安全裁剪](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)：按用户权限过滤搜索结果的实现示例。
- [AWS：知识库数据源同步与摄取](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html)：摄取、同步和删除操作的产品示例。

不同厂商接口是实现参考，不代表唯一的知识库架构。最终图片逐张核对中文、字段、金额、时间、箭头和条件关系，并在约 330—345px 手机正文宽度检查可读性。
