<template>
  <AdminShell title="记录管理" subtitle="同一套视觉规范下的列表、状态与表单" system-name="后台组件示例">
    <template #navigation>
      <p class="hidden px-3 pb-2 text-[10px] font-semibold tracking-wider text-primary-400 md:block">示例区域</p>
      <a href="#records" class="nav-item nav-item-active justify-center px-2 md:justify-start md:px-4" title="记录列表">
        <ListChecks class="h-5 w-5 shrink-0" aria-hidden="true" /><span class="sr-only md:not-sr-only">记录列表</span>
      </a>
      <a href="#record-form" class="nav-item nav-item-inactive mt-1 justify-center px-2 md:justify-start md:px-4" title="记录表单">
        <FilePenLine class="h-5 w-5 shrink-0" aria-hidden="true" /><span class="sr-only md:not-sr-only">记录表单</span>
      </a>
    </template>
    <template #sidebar-footer>
      <div class="flex items-center justify-center gap-2 rounded-lg bg-primary-800/50 px-1 py-2 md:justify-start md:px-3">
        <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent-500 text-xs text-white">示</span>
        <span class="hidden text-xs text-primary-200 md:block">本地视觉示例</span>
      </div>
    </template>
    <template #header-actions><span class="badge bg-gray-100 text-gray-600">仅示例数据</span></template>

    <div class="space-y-4 p-1 md:p-2">
      <div class="flex flex-wrap items-start justify-between gap-3">
        <div><h2 class="text-xl font-semibold text-gray-900">业务记录</h2><p class="mt-1 text-xs text-gray-500">搜索记录或编辑内容。刷新后恢复示例数据。</p></div>
        <button type="button" class="btn-primary" @click="startCreate"><Plus class="h-4 w-4" aria-hidden="true" />新建记录</button>
      </div>

      <section class="grid grid-cols-2 gap-3 xl:grid-cols-4" aria-label="记录统计">
        <div v-for="metric in metrics" :key="metric.label" class="feishu-card">
          <p class="text-xs text-gray-500">{{ metric.label }}</p><p class="mt-2 text-2xl font-semibold" :class="metric.color">{{ metric.value }}</p>
        </div>
      </section>

      <div class="grid items-start gap-4 xl:grid-cols-[minmax(0,1fr)_360px]">
        <section id="records" class="feishu-section min-w-0 scroll-mt-3">
          <div class="flex flex-wrap items-center gap-2 border-b border-gray-100 p-3">
            <label class="relative min-w-0 flex-1">
              <span class="sr-only">搜索记录</span><Search class="pointer-events-none absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" aria-hidden="true" />
              <input v-model="query" type="search" class="feishu-input w-full pl-8" placeholder="搜索名称或负责人" />
            </label>
            <label><span class="sr-only">状态筛选</span><select v-model="statusFilter" class="feishu-input"><option value="all">全部状态</option><option v-for="option in statuses" :key="option.key" :value="option.key">{{ option.label }}</option></select></label>
          </div>
          <div class="flex items-center justify-between gap-2 border-b border-gray-100 px-2">
            <div class="flex overflow-x-auto" aria-label="记录范围">
              <button v-for="view in views" :key="view.key" type="button" class="feishu-tab" :class="scope === view.key ? 'feishu-tab-active' : 'feishu-tab-inactive'" :aria-pressed="scope === view.key" @click="scope = view.key">{{ view.label }}</button>
            </div>
            <span class="shrink-0 pr-1 text-[11px] text-gray-500">{{ filteredRows.length }} 条</span>
          </div>
          <div class="admin-table-scroll" tabindex="0" aria-label="业务记录表，可横向滚动">
            <table class="feishu-table min-w-[620px]">
              <caption class="sr-only">业务记录、负责人、状态、进度和操作</caption>
              <thead><tr><th scope="col">记录名称</th><th scope="col">负责人</th><th scope="col">状态</th><th scope="col">进度</th><th scope="col">操作</th></tr></thead>
              <tbody>
                <tr v-for="row in filteredRows" :key="row.id" class="feishu-row" :class="editingId === row.id ? 'bg-accent-50/50' : ''">
                  <td><span class="block max-w-[240px] truncate font-medium text-gray-800" :title="row.title">{{ row.title }}</span></td>
                  <td class="whitespace-nowrap text-gray-600">{{ row.owner }}</td>
                  <td><span class="feishu-badge whitespace-nowrap" :class="statusInfo(row.status).className">{{ statusInfo(row.status).label }}</span></td>
                  <td><div class="flex min-w-[100px] items-center gap-2"><div class="progress-bar min-w-0 flex-1" role="progressbar" :aria-label="row.title + '进度'" :aria-valuenow="row.progress" aria-valuemin="0" aria-valuemax="100"><div class="progress-fill bg-accent-500" :style="{ width: row.progress + '%' }" /></div><span class="text-[11px] text-gray-500">{{ row.progress }}%</span></div></td>
                  <td><button type="button" class="feishu-btn-ghost text-accent-600" :aria-label="'编辑' + row.title" @click="edit(row)">编辑</button></td>
                </tr>
                <tr v-if="!filteredRows.length"><td colspan="5" class="text-center"><div class="py-10"><Inbox class="mx-auto h-8 w-8 text-gray-300" aria-hidden="true" /><p class="mt-2 text-sm text-gray-500">暂无匹配记录</p><button type="button" class="feishu-btn-ghost mt-2" @click="clearFilters">清空筛选</button></div></td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section id="record-form" class="feishu-card scroll-mt-3">
          <h3 class="text-sm font-semibold text-gray-900">{{ editingId ? '编辑记录' : '新建记录' }}</h3>
          <p class="mt-1 text-xs leading-5 text-gray-500">独立表单搭配列表。仅在当前页面内存中保存。</p>
          <p v-if="notice" role="status" class="admin-notice admin-notice-success mt-3">{{ notice }}</p>
          <form class="mt-4 space-y-3" @submit.prevent="save">
            <label class="block"><span class="admin-form-label">记录名称 <b>*</b></span><input ref="titleInput" v-model="draft.title" class="admin-field" required maxlength="120" :aria-invalid="!!error" aria-describedby="name-error" /></label>
            <p v-if="error" id="name-error" role="alert" class="text-xs text-rose-700">{{ error }}</p>
            <label class="block"><span class="admin-form-label">负责人</span><input v-model="draft.owner" class="admin-field" placeholder="可稍后补充" /></label>
            <div class="grid grid-cols-2 gap-3">
              <label><span class="admin-form-label">状态</span><select v-model="draft.status" class="admin-field"><option v-for="option in statuses" :key="option.key" :value="option.key">{{ option.label }}</option></select></label>
              <label><span class="admin-form-label">进度（%）</span><input v-model.number="draft.progress" class="admin-field" type="number" min="0" max="100" required /></label>
            </div>
            <details class="rounded-lg border border-gray-200 p-3"><summary class="cursor-pointer text-xs font-medium text-gray-600">补充说明（可选）</summary><label class="mt-3 block"><span class="sr-only">补充说明</span><textarea v-model="draft.note" rows="3" class="admin-field" placeholder="记录背景或补充信息" /></label></details>
            <div class="flex justify-end gap-2"><button type="button" class="btn-ghost" @click="reset">重置</button><button type="submit" class="btn-primary">保存</button></div>
          </form>
        </section>
      </div>

      <section class="grid gap-3 md:grid-cols-2" aria-label="其他视觉模式">
        <div class="feishu-card"><h3 class="text-sm font-semibold">状态标签</h3><div class="mt-3 flex flex-wrap gap-2"><span class="badge bg-blue-50 text-blue-700">处理中</span><span class="badge bg-emerald-50 text-emerald-700">已完成</span><span class="badge bg-amber-50 text-amber-800">待确认</span><span class="badge bg-rose-50 text-rose-700">需处理</span><span class="badge bg-violet-50 text-violet-700">知识沉淀</span></div></div>
        <div class="admin-notice admin-notice-info"><p class="font-semibold">使用说明</p><p class="mt-1">此示例展示通用视觉和本地交互。实际项目可按业务选择所需区块。</p></div>
      </section>
    </div>
  </AdminShell>
</template>

<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import { FilePenLine, Inbox, ListChecks, Plus, Search } from 'lucide-vue-next'
import AdminShell from './AdminShell.vue'

type Status = 'pending' | 'active' | 'done'
interface RecordItem { id: number; title: string; owner: string; status: Status; progress: number; note: string }
const rows = ref<RecordItem[]>([
  { id: 1, title: '客户资料查询优化', owner: '业务组', status: 'active', progress: 60, note: '用于展示长标题与编辑。' },
  { id: 2, title: '每月业务数据汇总与自动校验', owner: '数据组', status: 'pending', progress: 0, note: '' },
  { id: 3, title: '统一业务入口', owner: '产品组', status: 'done', progress: 100, note: '示例已完成记录。' },
])
const statuses: { key: Status; label: string; className: string }[] = [
  { key: 'pending', label: '待开始', className: 'bg-gray-100 text-gray-600' },
  { key: 'active', label: '进行中', className: 'bg-blue-50 text-blue-700' },
  { key: 'done', label: '已完成', className: 'bg-emerald-50 text-emerald-700' },
]
const views = [{ key: 'all', label: '全部记录' }, { key: 'open', label: '未完成' }]
const query = ref(''), scope = ref('all'), statusFilter = ref<Status | 'all'>('all')
const editingId = ref<number | null>(null), notice = ref(''), error = ref('')
const titleInput = ref<HTMLInputElement | null>(null)
const newDraft = (): Omit<RecordItem, 'id'> => ({ title: '', owner: '', status: 'pending', progress: 0, note: '' })
const draft = ref(newDraft())
let nextId = 4
const filteredRows = computed(() => rows.value.filter(row =>
  (scope.value === 'all' || row.status !== 'done') &&
  (statusFilter.value === 'all' || row.status === statusFilter.value) &&
  (row.title + row.owner).toLowerCase().includes(query.value.trim().toLowerCase()),
))
const metrics = computed(() => [
  { label: '全部记录', value: rows.value.length, color: 'text-accent-600' },
  { label: '待开始', value: rows.value.filter(r => r.status === 'pending').length, color: 'text-gray-600' },
  { label: '进行中', value: rows.value.filter(r => r.status === 'active').length, color: 'text-amber-600' },
  { label: '已完成', value: rows.value.filter(r => r.status === 'done').length, color: 'text-emerald-600' },
])
function statusInfo(status: Status) { return statuses.find(item => item.key === status)! }
function clearFilters() { query.value = ''; scope.value = 'all'; statusFilter.value = 'all' }
function reset() { editingId.value = null; draft.value = newDraft(); notice.value = ''; error.value = '' }
async function focusForm() { await nextTick(); titleInput.value?.focus(); titleInput.value?.scrollIntoView({ block: 'nearest' }) }
function startCreate() { reset(); void focusForm() }
function edit(row: RecordItem) { editingId.value = row.id; draft.value = { title: row.title, owner: row.owner, status: row.status, progress: row.progress, note: row.note }; notice.value = ''; error.value = ''; void focusForm() }
function save() {
  if (!draft.value.title.trim()) { error.value = '请填写记录名称'; return }
  const item: RecordItem = {
    ...draft.value, id: editingId.value ?? nextId++, title: draft.value.title.trim(),
    owner: draft.value.owner.trim() || '未指定', progress: Math.max(0, Math.min(100, Number(draft.value.progress) || 0)),
  }
  const index = rows.value.findIndex(row => row.id === item.id)
  if (index >= 0) rows.value[index] = item
  else rows.value.unshift(item)
  editingId.value = item.id
  draft.value = { ...item }
  error.value = ''; notice.value = '已保存到当前页面内存；刷新后恢复示例数据。'
  clearFilters()
}
</script>
