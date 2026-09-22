# 技术与布局

## 源码基线与适用边界

依据：2026-09-22 的 IT 项目协作空间工作区。主要来源为 `package.json`、`.env/vite.config.ts`、`.env/tailwind.config.js`、`.env/tsconfig.json`、`src/main.ts`、`src/router/index.ts`、`src/index.css`、`src/components/` 和代表性页面。下文的源路径用于追溯，不要求目标项目存在这些文件。

版本号是源工程声明范围，不代表最新版本推荐；实际安装版本由其 lockfile 决定。新项目采用其他版本时核对兼容性；已有工程无需为视觉复用升级依赖。

| 层 | 源工程实现 | 复用方式 |
| --- | --- | --- |
| 视图 | Vue `^3.4.0`，SFC，`<script setup lang="ts">` | 新建同栈项目的基线 |
| 类型 | TypeScript `^5.5.0`，strict，ES2020，bundler resolution | 定义 props、emits、页面模型 |
| 路由 | Vue Router `^4.3.0`，Hash history，懒加载页面 | 壳层嵌套路由与外部单页分开 |
| 全局状态 | Pinia `^2.1.0` 已在入口注册 | 源码无独立 stores 目录；按实际共享状态需要使用 |
| 构建 | Vite `^5.4.0`，plugin-vue `^5.0.0` | 现有脚本显式指定 `.env/vite.config.ts` |
| 样式 | Tailwind `^3.4.0`、PostCSS `^8.4.0`、Autoprefixer `^10.4.0` | utilities + 全局 `@layer components` + 少量 scoped CSS |
| 图标 | lucide-vue-next `^0.441.0` | 小尺寸线性 SVG，按组件导入 |
| 类型检查工具 | vue-tsc `^2.0.0` | 源 `build` 只调用 Vite；类型检查另行执行 |
| UI/图表依赖 | 未声明 Element Plus、Ant Design、ECharts 等 | 原视觉由自建模板和 CSS 组成，不假设存在商业/第三方组件库 |

原工程别名 `@ → src`，构建输出 `dist`，生产 base 为 `/pm/`；后端代理、钉钉脚本和登录不随本 Skill 迁移。新工程的 base、root、认证、路由守卫和构建输出由目标工程决定。

## 页面壳层

```text
App（错误恢复 + 路由内容 + 全局反馈）
├─ 管理区 Layout：100dvh，flex，overflow hidden
│  ├─ Sidebar：208px，深靛蓝，内部可滚动
│  │  ├─ 标识 / 系统名
│  │  ├─ 按用途分组的导航
│  │  └─ 用户 / 系统入口
│  └─ 主列：flex-1，min-width/height 0
│     ├─ Header：64px，白色，标题说明 + 操作
│     └─ main：flex-1，overflow auto，8/12px 内边距
│        └─ 路由页：使用完整可用宽度
└─ 外部业务页：无管理侧栏，居中表单，自然页面滚动
```

关键点是给主列和嵌套可滚动区域明确收缩边界。全高列表加详情页可以各自滚动；普通详情页直接沿 main 滚动。不要每多一张卡片就添加一个滚动区。

原 `index.html` 挂载节点是 `#root`，全局 CSS 却保留了 `#app` 选择器。随包 CSS 同时涵盖两个常用 ID。源 `body overflow:hidden` 不适合所有独立表单，随包版本将滚动限制留在 `.app-shell`，外部页自然滚动。

`AdminShell.vue` 保留桌面尺寸，额外提供窄屏 64px 图标栏；这属于模板的适配增强，原 `Sidebar.vue` 是固定 208px。导航图标栏需提供文字 `title`/`aria-label`。目标项目若使用抽屉导航，应复用其已有方案。

## 页面骨架的选择

| 任务 | 骨架 | 源码示例 |
| --- | --- | --- |
| 总览 | 简短工具栏 → 2/4 列指标 → 分组卡片、进度条及下钻 | DashboardOverview、PostLaunchDashboard |
| 管理大量记录 | 标题/操作 → 筛选 → tabs → 层级表格 | RequirementsList、ProductOverview |
| 按条处理 | 标题/少量计数 → 左侧列表 → 右侧详情/表单 | PocWorkbench、DemandPool、PostLaunchOperations |
| 理解一个对象 | 返回/对象标题 → 状态和摘要 → 分组详情 → 动态/附件 | ProjectDetail、RequirementDetail |
| 业务参与 | 提交入口 → 与我有关的事项 → 确实待我处理的动作 | BusinessIntake |
| 设置 | 设置分组 → 说明 → 字段 → 保存/结果 | NotificationSettings、SystemManagement |
| 外部回复 | 精简标题 → 当前事项上下文 → 必要字段 → 单一提交动作 | 各 Entry 页面 |

常见响应式网格：`grid-cols-1 sm:grid-cols-2` 用于字段，`grid-cols-2 xl:grid-cols-4` 用于指标；列表/详情在 `xl` 才并列。POC 列表为 420px，业务协作右侧摘要为 360px，这些是页面选择，不是所有后台必须保留的宽度。

## 目录建议与状态流

已有工程保留原组织方式。新建同栈项目可将壳层及通用组件放 `components/`、路由页放 `pages/`、令牌及共享 CSS 放 `styles/`、请求适配放 `api/`。项目级共享状态放 Pinia，单页筛选、弹窗和编辑草稿放页面局部状态。

原项目使用集中的 `src/api/index.ts`，若干业务组件直接请求 API。跨系统提取时，将这类组件改为接收数据与状态、通过事件或注入的适配器提交；不要把原 API、用户姓名或通知行为嵌入模板。

动态颜色类要使用完整字符串映射，例如 `{ success: 'bg-emerald-50 text-emerald-700' }`。不要拼接 `bg-${color}-50` 导致 Tailwind 扫描不到。数据驱动的真实色值可经验证后传入 style/CSS 变量。

## 同栈接入

将 `assets/tailwind.preset.cjs` 放到项目样式目录，在 Tailwind 3 配置的 `presets` 中导入。保留项目自己的 `content`，覆盖全部 Vue/TS 文件。将 `admin-ui.css` 作为一次性的入口样式引入；它含 Tailwind 三条指令，应与已有入口合并，避免重复 preflight。

```js
// 例如项目根部 tailwind.config.cjs
const adminPreset = require('./src/styles/tailwind.preset.cjs')
module.exports = {
  presets: [adminPreset],
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
}
```

Tailwind 4 或其他 CSS 工具需要翻译令牌与组件样式，不能直接假设 Tailwind 3 的配置和 `@apply` 接法兼容。视觉基线保持一致即可。

示例壳层使用 slots，不依赖 Router、Pinia 或原 API。实际项目可在 default slot 放 `router-view`，在 navigation slot 放自己的 RouterLink。

## 验证范围

检查主侧栏、顶栏、列表、长中文标题及编辑区在桌面和窄屏能否使用；表格水平滚动不应推动整页；弹层按钮应可见。复用时使用目标工程已有构建、类型检查命令，不能把 `vite build` 成功当成所有类型或交互均已验证。

原入口提供路由加载失败提示、一次性 chunk 刷新恢复和全局反馈。这些说明“失败仍有可操作页面”是体验的一部分；恢复逻辑须按目标部署方式实现，避免无限刷新。此 Skill 不携带原生产日志接口。
