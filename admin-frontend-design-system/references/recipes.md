# 实施配方

## 随包模板

- `../assets/tailwind.preset.cjs`：原 primary/accent 和字体映射，Tailwind 3。
- `../assets/admin-ui.css`：原全局 CSS 类；追加命名为 admin-* 的表单/弹层/反馈配方。
- `../assets/AdminShell.vue`：通用壳层，brand/navigation/sidebar-footer/header-actions/default slots。
- `../assets/AdminUiExample.vue`：可运行的内存示例，展示导航、统计、搜索、页签、表格、状态、进度、表单和保存反馈。依赖 Vue、Lucide 和同级 AdminShell。

复用示例组件前先阅读代码，接到实际业务后移除示例数据及“仅保存到内存”的说明。全局类是可复制样式约定，不是发布好的 npm UI 包。

## 按钮、表单与状态

```vue
<form class="grid gap-3 sm:grid-cols-2" @submit.prevent="save">
  <label class="block sm:col-span-2">
    <span class="admin-form-label">记录名称 <b>*</b></span>
    <input v-model="draft.title" required class="admin-field"
      :aria-invalid="!!errors.title" aria-describedby="title-error" />
    <p v-if="errors.title" id="title-error" class="mt-1 text-xs text-rose-700">{{ errors.title }}</p>
  </label>
  <label class="block sm:col-span-2">
    <span class="admin-form-label">补充说明 <em>可选</em></span>
    <textarea v-model="draft.note" rows="3" class="admin-field resize-y" />
  </label>
  <div class="flex justify-end gap-2 sm:col-span-2">
    <button type="button" class="btn-ghost" @click="cancel">取消</button>
    <button type="submit" class="btn-primary" :disabled="saving">{{ saving ? '保存中…' : '保存' }}</button>
  </div>
</form>
```

此片段需由目标页面提供 draft/errors/save/cancel/saving。字段是否必填由业务约束决定；UI风格不新增数据门禁。保存失败保留草稿，恢复操作；成功刷新对应视图并告知结果。`disabled` 既需要逻辑阻止重复提交，也需要可见的降低强调。

标准字段的焦点为蓝边框和轻蓝 ring。不要复制源个别页面 `outline:none` 却没有替代焦点的写法。紧凑原生 select 如果使用 appearance-none，应保留 ChevronDown 或改回原生箭头。页面新增图标按钮提供 aria-label，不只依赖图案。

## 表格

```vue
<section class="feishu-section">
  <div class="flex flex-wrap items-center gap-2 border-b border-gray-100 p-3">
    <!-- 搜索、筛选和已选范围 -->
  </div>
  <div class="admin-table-scroll" tabindex="0" aria-label="记录表格，可横向滚动">
    <table class="feishu-table min-w-[760px]">
      <caption class="sr-only">业务记录列表</caption>
      <thead><tr><th scope="col">名称</th><th scope="col">状态</th><th scope="col">操作</th></tr></thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id" class="feishu-row">
          <td><span class="block max-w-sm truncate font-medium" :title="row.title">{{ row.title }}</span></td>
          <td><span class="feishu-badge bg-emerald-50 text-emerald-700">{{ row.statusLabel }}</span></td>
          <td><button type="button" class="feishu-btn-ghost" @click="open(row)">详情</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

示例绿色标签仅示意，需要根据真实状态映射。真实表的名称列保留空间，状态/日期/动作短列适度固定。源 RequirementsList 的12列百分比分配和1320/1480px布局参数属于该页；新表按自身内容确定宽度。避免整页被表格撑宽。

层级行复用 `.feishu-l1-header`、`.feishu-l3-row`、`.feishu-l3-table`；展开按钮带 aria-expanded。父行与子表通过边界/缩进区分。源码某些`.feishu-l3-row-item`是脚本选择钩子，不是有独立 CSS 定义的视觉类。

可排序 th 放真正的 button，当前排序用 aria-sort；图标显示方向。批量操作只针对明确选择范围，避免“当前页”与“所有查询结果”混淆。密集屏幕上的hover可以轻，不将必需动作完全隐藏。

## 标签、进度、卡片

```html
<span class="badge bg-amber-50 text-amber-800">待确认</span>
<div class="feishu-card">普通内容卡</div>
<div class="l2-progress l2-progress-active">
  <div class="mb-2 flex justify-between text-xs"><span>进行中</span><span>60%</span></div>
  <div class="progress-bar" role="progressbar" aria-label="处理进度" aria-valuemin="0" aria-valuemax="100" aria-valuenow="60">
    <div class="progress-fill bg-accent-500" style="width:60%"></div>
  </div>
</div>
```

百分比先限定在0–100，空值显示“未设置/暂无数据”，不伪装成0%。卡片是可交互时才增加cursor/键盘操作；纯统计卡的浮起动画可省略。

## 列表加详情

普通文档流用 `grid gap-3 xl:grid-cols-[360px_minmax(0,1fr)]`。全高工作区用 `flex min-h-0 flex-1 flex-col xl:flex-row`，列表与详情分别设置 `min-h-0 overflow-y-auto`。窄屏应恢复自然流或一层可返回的详情，避免两个不足一屏高的嵌套滚动区。

选中行：`border-accent-400 bg-accent-50/50`；默认：`border-gray-100 bg-white hover:bg-gray-50 hover:border-gray-300`。标题14px，摘要12px，时间11px。用稳定id记住选中项，刷新后该项不存在时展示清晰空态。

## 弹层与图片

源常见模态：`fixed inset-0 z-50`，slate遮罩，白卡，宽度上限 md/3xl/6xl，圆角12/16px。头/尾固定，正文 `min-h-0 overflow-y-auto`；最大高度90dvh或`calc(100dvh - 2rem)`。

随包 `.admin-dialog-backdrop/card/header/body/footer` 是视觉样式，不包含可访问弹窗逻辑。优先使用目标工程已具备焦点管理的弹窗组件，套用本样式。自建时使用 dialog语义、aria-modal/标题关联、打开聚焦、关闭恢复焦点、Escape和Tab循环，并明确点击遮罩是否允许关闭未保存草稿。

媒体预览保持object-contain，工具条给出文件名与缩放/页码，缩略图object-cover。放大后需要可以平移或滚动查看完整边缘；仅transform并不自动获得正确滚动边界。空图片数组、无效索引和加载失败应有退路。

## 反馈、附件、时间线

反馈使用 `.admin-notice` 配合 `.admin-notice-info/success/warning/error`；错误用 role=alert，成功等异步状态用 role=status。Toast参照原FeedbackHost：右上、max-w-sm、z100、轻阴影、关闭按钮。非必须阅读的信息可短时隐藏，关键失败留在字段/面板内。

源main全局覆盖window.alert是历史兼容方式，复用时优先显式调用项目反馈服务；确认不能被换成仅提示的toast。并发确认需排队或限制，避免覆盖未结束Promise。

附件区沿用虚线灰底、紫色回形针、可删除文件chip。保留完整文件名title、大小、进度/失败；文件选择和上传是两件事。粘贴只拦截实际文件，成功/部分成功分别反馈；创建的object URL在移除或组件卸载时释放。大小/类型限制使用目标项目实际配置，不硬编码50MB为所有系统规则。

动态条目使用头像 + 操作人/类型/时间 + 正文 + 附件 + 评论；评论缩进和淡边线，不需要给每条记录全套高亮。正文保留换行，默认按纯文本渲染；富文本沿用项目的清洗和显示方式。

## CSS 扩展和一致性

`admin-ui.css` 保留源 `.feishu-*` 名称以便对照，名称不构成第三方产品依赖。新项目如有同名类，应合并/改前缀后再引入。源scoped字段样式被归纳到admin-field/form-label；业务协作渐变和聊天气泡直接在模板用utilities。

不要为了复制所有样式而引入所有页面、业务接口或mockData。新增复用组件优先提取已出现的视觉组合，并保持API与视觉层分离。样例未包含真实请求或权限模型。

## 验收

对本包可运行 `node scripts/check-assets.cjs --project <project>` 做静态链接、SFC和CSS编译检查。对实现后的页面还需验证：筛选/切换/提交有结果，空态和请求失败不混淆；长标题及宽表仍可使用；弹窗不被transform/overflow裁剪；键盘焦点可见。使用真实浏览器做过的验证才计为视觉/交互验证。
