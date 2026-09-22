# 组件与页面目录

以下覆盖 2026-09-22 源工程 `src/components` 的全部 13 个 Vue 组件。它们并非全部都是独立 UI 库组件：业务面板直接依赖原接口。跨系统复用其视觉和交互结构，使用新项目的数据模型与事件。

## 全量独立组件

| 原组件 | 结构 / 视觉 | 原接口或依赖 | 跨系统复用 |
| --- | --- | --- | --- |
| Layout.vue | 侧栏 + 顶栏 + 主区，视口高度，主区独立滚动 | Sidebar、Header、router-view | 用随包 AdminShell 或保留目标壳层 |
| Sidebar.vue | 深靛蓝、208px、分组导航、浅蓝激活项、底部用户卡 | 路由、用户、业务导航与可见规则 | 导航/身份由目标项目提供 |
| Header.vue | 白色64px，左标题/说明，右搜索/通知/头像 | 路由标题、搜索、待办、登录 | 通过 slots 或配置组合 |
| AttachmentPicker.vue | 虚线灰底、回形针、添加入口、文件 chip、删除 | files: File[]；add(File[])、remove(index)；粘贴 | 提取选择视图；源50MB限制由父层校验，并非组件自身已强制 |
| SearchableMultiSelect.vue | 有计数的字段 + 搜索 + checkbox 列表 + 清空/完成 | modelValue 为逗号分隔 string，options string[]，disabled；update:modelValue | 人员字段可适配 id[]；选中摘要截断，列表高224px，z80 |
| ImagePreviewModal.vue | 深色遮罩、工具条、原图、缩放、前后翻页、缩略图 | modelValue、images、startIndex；update:modelValue；图片可为 URL 或 data/url 对象 | 统一图片适配接口；补 alt、键盘关闭、焦点管理 |
| FeedbackHost.vue | 右上 toast，语义浅底，确认/输入框对话框 | utils/feedback：showFeedback/showConfirm/showPrompt；源 toast 默认3600ms | 宿主只挂一次；反馈事件由目标项目连接 |
| PriorityAssessment.vue | 浅蓝折叠面板，问题行/选项按钮，结果与采用动作 | assessment、priority、projectPriority；update:modelValue、adopt | 复用“选项评估 + 可解释结果”结构，不复制评分规则 |
| DeliveryBaselinePanel.vue | 绿色边框区，当前版本摘要 + 新版编辑 + 专项details | requirement；交付模板、版本、确认接口 | 复用“已生效摘要/编辑草稿/历史”层次，业务表单另配 |
| RequirementLifecycle.vue | 分组操作入口、资料/验证表单、记录时间线、回执、来源折叠区 | requirement、revision、deliveryOnly、readOnly；changed；生命周期API | 复用阶段与证据布局，不默认生成通知或自动流转 |
| RequirementPhases.vue | 两列阶段卡、状态选择、备注；选中后展示详情 | requirement、revision；阶段API；权限 | 复用 selectable card + detail；键盘 Enter/Space 已有参考 |
| BusinessCollaborationPanel.vue | 紫色轻渐变标题、折叠主题、左右消息气泡、附件/回复 | requirementId；原协作API、用户身份、附件 | 复用讨论UI，发消息/通知由业务适配器提供 |
| SharedActivityFeed.vue | 动态卡、头像、类型/时间、评论树、附件、发布区 | scopeType(project/requirement)、scopeId、compact、title/subtitle、allowCompose、enableCollaboration、recipient/title；activity-created | 复用事件流；展示权限与发送权限分别处理 |

## 原页面内联的通用 UI

这些目前常由模板片段实现，没有对应独立 `.vue` 文件。复用时按频率提取，避免误以为源码已经有完整 UI 库。

| 模式 | 组成 | 样式/行为 |
| --- | --- | --- |
| 标题工具栏 | 标题说明 + 一个主动作 + 少量次动作 | flex-wrap/gap；窄屏换行 |
| 指标卡 | 名称、数值、解释、可选趋势/图标 | stat-card 或浅色边框卡；点击可下钻时提供明确交互 |
| 分类统计 | 分组卡、计数、进度条、细分柱条 | CSS宽度驱动；保留标签及数值，不只显示颜色 |
| 搜索筛选 | 搜索图标字段、状态/类型下拉、清空 | feishu-input/select；active filter 需可见 |
| 页签/分段切换 | tabs、计数、选中态 | feishu-tab-*；横向可滚，选中不能只靠 hover |
| 层级表格 | 分组头 → 父行 → 展开的子表 | feishu-section/table/l1-header/l3-table |
| 行操作 | 编辑、详情、删除、更多 | 紧凑按钮/图标；危险动作与主要动作分开 |
| 批量操作 | 选择框、已选计数、工具栏 | 表头全选与部分选中；操作范围明确 |
| 列表/详情 | 可搜索列表、选中卡、详情编辑 | 选中浅蓝边框/底色；列表和详情可独立滚动 |
| 进度 | 彩色填充、百分比、状态文字 | progress-bar/fill；l2-progress-* |
| 阶段步骤 | 编号/名称、状态、摘要、可选动作 | 完成绿、当前蓝、待开始灰；横排或窄屏可滚 |
| 表单 | label、必填/可选说明、字段、帮助、错误 | 1/2列；长文本通栏；details容纳低频专项字段 |
| 详情摘要 | label/value两行，分组网格 | 标签浅灰小字，值深色、长文换行 |
| 标签/身份 | 状态chip、类型标签、优先级、头像 | badge/feishu-badge；初始字头像，20/28/32px等 |
| 折叠块 | summary/title + ChevronDown + 内容 | 默认收起低频细节；保留当前状态摘要 |
| 模态/侧详情 | 遮罩、标题、关闭、滚动正文、操作尾部 | 源多为居中大模态；需右侧抽屉时沿用同样层次 |
| 附件/媒体 | 文件chip、缩略图、预览、下载 | 图像object-contain，列表缩略图object-cover |
| 动态/时间线 | 时间、操作者、事件类型、内容、评论 | timeline-dot/change-dot；左线/节点；内容pre-wrap |
| 通知与提示 | inline notice、toast、confirm、未读点 | 成功绿、信息蓝、提醒黄、错误红 |
| 看板 | 列标题计数 + 工作卡 + 状态标签 | kanban-column/card；源码样式不等于已实现拖拽 |
| 分页/更多 | 列表总量、加载更多或分页动作 | 源码没有统一分页组件；沿用同一按钮与边框密度，按目标数据量选择 |
| 加载/空态/错误 | 旋转圈或文字、空态图标与说明、重试 | 加载/失败与零条数据分别渲染 |

## 页面的视觉覆盖范围

源 `pages` 共30个文件；其中部分仅为历史页面或兼容跳转，不代表都在当前导航可见。

| 家族 | 原页面文件（省略.vue） | 可提取结构 |
| --- | --- | --- |
| 成果和管理看板 | DashboardOverview、Dashboard、ManagementDashboard、PostLaunchDashboard、PerformanceWorkbench | 指标卡、分组统计、进度与下钻 |
| 日常管理 | Workspace、TodoCenter、RequirementsList、ProductOverview、Kanban、Sprints | 工具栏、分组列表、表格、工作卡、期限 |
| 需求处理与沉淀 | DemandPool、PocWorkbench、PostLaunchOperations | 列表/详情、阶段、表单、关联对象、结果 |
| 对象详情 | ProjectDetail、RequirementDetail | 返回栏、概览、分阶段面板、历史/附件 |
| 业务参与 | BusinessIntake | 简化入口、自己的事项、确认动作 |
| 内容/记录/配置 | KnowledgeBase、Changelog、OperationRecords、NotificationSettings、SystemManagement | 文档分类卡、时间线、设置表单、表格 |
| 外部任务表单 | CollaborationLinkEntry、CollaborationUpload、DemandEntry、DemandConfirmEntry、DemandOutcomeEntry、DemandReviewEntry、DemandSupplementEntry、DemandPocEntry | 独立任务上下文、表单、提交后回执 |

路由事实：`/dashboard` 使用 DashboardOverview；`/management` 重定向；`/requirements/kanban` 跳转产品视图；`/todos` 跳转工作台。不要从历史文件存在推导当前导航应展示它们。

## 常见组合

库存/订单管理可组合“标题工具栏 + 筛选 + 紧凑表格 + 详情弹层”；客户反馈可组合“列表/详情 + 状态卡 + 动态/附件”；知识/AI模型可组合“分类标签 + 搜索 + 记录详情 + 关联对象”；审批可组合“当前阶段 + 已确认摘要 + 本人动作 + 历史记录”。只携带本次任务需要的组成部分。
