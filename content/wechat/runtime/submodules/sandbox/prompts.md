# 沙箱执行环境配图提示词与校验记录

- 版本：0.1.0
- 阶段：第九模块公众号推文初稿
- Git 状态：基于 9b4282c（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:38 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“沙箱执行环境”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：sandbox-principle.png

- 用途：解释“沙箱隔离的多层边界”。
- 资料来源：
- Kubernetes：RuntimeClass：https://kubernetes.io/docs/concepts/containers/runtime-class/
- Kubernetes：Pod Security Standards：https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Kubernetes：Restrict a Container's Syscalls with seccomp：https://kubernetes.io/docs/tutorials/security/seccomp/
- 保留节点：任务材料（只读输入与校验）；隔离运行时（独立进程或容器边界）；系统调用限制（seccomp 与最小内核能力）；网络与文件策略（白名单、临时目录、只读挂载）；资源与回收（CPU、内存、时间、输出上限）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- sandbox-inputs.png：五类输入——代码来源、文件权限、网络目的、系统能力、资源预算。
- sandbox-failure.png：三类失效——把容器等同于绝对安全边界；把宿主凭据和 Docker socket 挂进沙箱；只设超时却不限制内存、进程和网络。
- sandbox-controls.png：控制组合——独立低权限运行时、只读根文件系统和临时工作区、seccomp、能力删除和网络默认拒绝、镜像来源、依赖扫描和执行后销毁。
- sandbox-verification.png：验证闭环与指标——越界访问拦截数、沙箱逃逸测试通过率、资源超限终止率、残留文件与凭据事件数。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
