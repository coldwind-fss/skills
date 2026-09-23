# 设计令牌

此处区分原工程事实和跨系统的规范化选择。完整 primary/accent 调色板在 `../assets/tailwind.preset.cjs`，全局类在 `../assets/admin-ui.css`。

## 主色与画布

`primary` 是结构靛蓝；`accent` 才是链接、主按钮和选中状态的蓝色。

| 阶 | primary | accent |
| --- | --- | --- |
| 50 | #f0f2f8 | #eff6ff |
| 100 | #d6dceb | #dbeafe |
| 200 | #b4bfd9 | #bfdbfe |
| 300 | #8d9cc2 | #93c5fd |
| 400 | #6f80ad | #60a5fa |
| 500 | #556699 | #3b82f6 |
| 600 | #424f7a | #2563eb |
| 700 | #323b5c | #1d4ed8 |
| 800 | #232943 | #1e40af |
| 900 | #1a1f36 | #1e3a8a |
| 950 | #0f1324 | 未扩展 |

| 用途 | 基线 |
| --- | --- |
| 侧栏 | primary-900；分组线 primary-700/50；用户底板 primary-800/50 |
| 导航默认/悬停 | gray-400 → gray-200，悬停白色 5% |
| 导航选中 | accent-50 底，accent-600 文本 |
| 主按钮 | accent-500，hover accent-600，白字 |
| 页面背景 | gray-50 #f9fafb |
| 卡片/字段/顶栏 | white #ffffff |
| 细分隔线 | gray-100 #f3f4f6 |
| 常规边框 | gray-200 #e5e7eb |
| 标题 | gray-900 #111827 |
| 正文 | gray-700 #374151 或 gray-800 #1f2937 |
| 标签/说明 | gray-500 #6b7280 或 gray-600 #4b5563 |
| 次要时间/占位 | gray-400 #9ca3af；关键说明不要依赖此浅色小字 |

新一些面板使用 slate-50 #f8fafc、slate-200 #e2e8f0、slate-500 #64748b 和 slate-900 #0f172a。两者均出现在源码；新页面通常沿用灰色主体系，沿用 slate 的局部面板无需强制全局替换。

## 语义色

| 语义 | 典型色族 | 典型组合 |
| --- | --- | --- |
| 信息、主操作、选中 | blue/accent | bg-blue-50 + border-blue-100/200 + text-blue-700/800 |
| 成功、完成、上线 | emerald | bg-emerald-50 + border-emerald-100/200 + text-emerald-700/800 |
| 待确认、提醒、期限 | amber | bg-amber-50 + border-amber-100/200 + text-amber-700/800 |
| 错误、阻塞、危险 | rose/red | bg-rose-50 + border-rose-100/200 + text-rose-700/800 |
| 协作、知识、POC | violet | bg-violet-50 + border-violet-100/200 + text-violet-700 |
| AI 能力、迭代、关联 | cyan | bg-cyan-50 + border-cyan-100/200 + text-cyan-700 |
| 未开始、关闭、只读 | gray/slate | bg-gray-100 + text-gray-600 |

主体卡片保持白色，彩色提示常用 30%–80% 浅底。`BusinessCollaborationPanel` 有 `from-violet-50 via-white to-blue-50` 渐变标题条，这是局部强调，不扩展成整页渐变。

原优先级：P0 #ef4444，P1 #f59e0b，P2 #3b82f6，P3 #9ca3af，P4 #cbd5e1。低优先级色用于点/标记；小字号文字需保持可读。

原状态映射（保留用于忠实复现）：

| 状态 | 色值 |
| --- | --- |
| 待处理、维护中 | #64748b |
| 待评估 | #9ca3af |
| 进行中、已排期、已立项 | #3b82f6 |
| 需求确认中 | #6366f1 |
| 设计中 | #8b5cf6 |
| 开发中、待交付 | #f59e0b |
| 联调中 | #06b6d4 |
| 测试中 | #a855f7 |
| 迭代中 | #0ea5e9 |
| 待上线 | #14b8a6 |
| 已上线、已交付 | #10b981 |
| 暂停中 | #f97316 |
| 已关闭 | #6b7280 |
| 已归档 | #94a3b8 |

不同源页面对“开发中”与“进行中”的着色并不完全相同。跨系统时先将业务状态映射到稳定的语义色，不沿用偶然的多套判断函数；颜色不决定流程。

类型色也有新旧两版：新增功能 #2563eb，产品设计 #8b5cf6（成果页 #7c3aed），功能优化 #f59e0b（成果页 #d97706），问题修复 #ef4444（成果页 #dc2626），业务确认 #0ea5e9（成果页 #0284c7），验证交付 #14b8a6（成果页 #0f766e），技术建设 #64748b。较深色适合文字和小标记。

## 排版、间距和密度

字体声明：正文 `"Noto Sans SC", system-ui, sans-serif`，等宽 `"JetBrains Mono", "Fira Code", monospace`。源工程未随包提供字体文件，也未在入口加载这些字体；只有已安装时才显示指定字体，否则使用 fallback。不要把字体声明等同于字体已供应。

| 元素 | 常见规格 |
| --- | --- |
| 顶栏标题 | text-lg 18px / semibold |
| 页标题 | text-xl 20px 或 text-2xl 24px / semibold-bold |
| 业务区块标题 | text-sm 14px 或 text-base 16px / semibold |
| 主正文/字段 | text-sm 14px；紧凑管理行 text-xs 12px |
| 辅助说明 | 11–12px；多行 leading-5 20px |
| 表头/小徽标/时间 | 10–11px，只用于次级高密度信息 |
| 统计数字 | text-xl 到 text-3xl，字号随指标层级而非固定全页放大 |
| 多行内容 | whitespace-pre-wrap + leading-5/6 |
| 长单行标题 | min-w-0 + truncate，并保留 title 或详情入口 |

默认以 Tailwind 4px 间距网格组织：1/2/3/4/5/6 对应 4/8/12/16/20/24px，小标签补用 1.5/2.5（6/10px）。main 外边距 8/12px；卡片 16–20px；筛选栏 12px；主表单组 gap-3/4；紧凑表格单元格 x12/y8px，内层表格 x8/y6px。

| 控件 | 紧凑 | 常规 |
| --- | --- | --- |
| 按钮 | feishu-btn-*：12px 字，x12/y6px，radius 6px | btn-*：14px 字，x16/y8px，radius 8px |
| 输入框 | feishu-input：12px 字，x10/y6px，radius 6px | admin-field：约 13px 字，x11.2/y8.8px，radius 8px |
| 徽标 | feishu-badge：10px 字，x6/y2px，小圆角 | badge：12px 字，x10/y2px，全圆 |
| 图标按钮 | 24px 视觉框 | 触屏场景扩大点击区域，保留图标大小 |

“紧凑”是适合工作密度的选择，不是所有人机界面的固定最小字号。业务确认表单宜使用常规档。

## 形状、图标、层级

圆角：4px 小徽标；6px 紧凑字段；8px 行卡片；12px 主卡片；16px 对话框；圆形用于头像和状态点。表格以线分组，避免给每个单元格加厚边框。

普通面板无阴影或 shadow-sm；悬停可 shadow-md；下拉 shadow-xl；模态 shadow-xl/2xl。标准块边框 1px，特殊业务确认区可 2px 轻色边界。无全屏暗色模式基线。

Lucide 图标：导航 20px、标题/普通操作 16px、紧凑操作 12–14px、空态 32–48px。使用同一笔画风格，不把不同图标库混进一个操作栏。原日志和 favicon 存在少量 emoji，不代表常规控件需要采用 emoji。

源层级：常规模态 z50、图片预览 z70、多选下拉 z80、全局反馈 z100。层叠数值无法解决父容器裁剪或 stacking context；脱离父容器的弹层可 Teleport 到 body，并检查实际叠放。

## 动效与滚动条

普通 hover/边框 150ms，统计卡 hover 200ms，进度条 500ms ease-out；页面 fadeIn 300ms（Y 从 8px 到 0），侧向 slideIn 300ms（X 从 -12px 到 0），scaleIn 200ms（0.95 到 1）；toast 180ms（Y -8px）。主按钮按下缩放 0.98，紧凑版 0.97。

源全局滚动条 6px，透明轨道，thumb #d1d5db，hover #9ca3af，圆角 3px。宽表额外采用 10px 横向滚动条，slate-100 轨道/slate-400 thumb，`scrollbar-gutter: stable`。随包 CSS 另提供 prefers-reduced-motion 适配，属于复用补充。
