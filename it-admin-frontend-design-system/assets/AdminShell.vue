<template>
  <div class="app-shell">
    <aside class="flex h-full min-h-0 w-16 shrink-0 flex-col overflow-y-auto bg-primary-900 md:w-52" aria-label="主导航">
      <div class="px-3 pb-3 pt-5 md:px-4">
        <slot name="brand">
          <div class="flex items-center gap-2.5" :title="systemName">
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent-500 text-white">
              <Layers class="h-5 w-5" aria-hidden="true" />
            </span>
            <div class="hidden min-w-0 md:block">
              <p class="truncate text-sm font-semibold text-white">{{ systemName }}</p>
              <p class="mt-0.5 truncate text-xs text-primary-300">{{ systemSubtitle }}</p>
            </div>
          </div>
        </slot>
      </div>
      <nav class="flex-1 px-2 py-2"><slot name="navigation" /></nav>
      <div v-if="$slots['sidebar-footer']" class="border-t border-primary-700/50 px-2 py-4 md:px-4">
        <slot name="sidebar-footer" />
      </div>
    </aside>

    <div class="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
      <header class="flex min-h-16 shrink-0 flex-wrap items-center justify-between gap-2 border-b border-gray-200 bg-white px-4 py-2">
        <div class="min-w-0">
          <h1 class="truncate text-lg font-semibold text-gray-900">{{ title }}</h1>
          <p v-if="subtitle" class="mt-0.5 text-xs text-gray-500">{{ subtitle }}</p>
        </div>
        <div v-if="$slots['header-actions']" class="flex items-center gap-2"><slot name="header-actions" /></div>
      </header>
      <main class="app-main-scroll min-h-0 min-w-0 flex-1 overflow-auto p-2 md:p-3">
        <div class="mx-auto min-h-0 w-full min-w-0 max-w-none page-transition" :class="fillHeight ? 'h-full' : ''">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Layers } from 'lucide-vue-next'

withDefaults(defineProps<{
  title: string
  subtitle?: string
  systemName?: string
  systemSubtitle?: string
  fillHeight?: boolean
}>(), {
  subtitle: '',
  systemName: '管理系统',
  systemSubtitle: '业务协作空间',
  fillHeight: false,
})
</script>
