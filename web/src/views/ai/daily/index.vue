<template>
  <div class="daily-report-page">
    <div class="report-status-row">
      <span class="report-status" :class="{ error: loadError, ready: frameLoaded && !loadError }">
        {{ loadError ? '加载失败' : frameLoaded ? '完整日报已加载' : '正在加载完整日报' }}
      </span>
    </div>

    <div class="report-shell">
      <div v-if="!loadError && !frameLoaded" class="report-overlay loading-overlay">
        <div class="loading-ring" />
        <p>正在载入完整日报内容...</p>
      </div>

      <div v-if="loadError" class="report-overlay error-overlay">
        <div class="error-mark">!</div>
        <h3>日报内容暂时不可用</h3>
        <p>当前内嵌页面未成功返回内容，你可以重新加载，或直接在新窗口中查看完整日报。</p>
        <div class="error-actions">
          <ElButton type="primary" @click="refreshIframe">重新加载</ElButton>
          <ElButton @click="openNewWindow">外部打开</ElButton>
        </div>
      </div>

      <iframe
        v-show="!loadError"
        ref="dailyFrame"
        :src="articleUrl"
        class="report-frame"
        frameborder="0"
        @load="onFrameLoad"
        @error="onFrameError"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineOptions({ name: 'AiDaily' })

const dailyFrame = ref<HTMLIFrameElement>()
const loadError = ref(false)
const frameLoaded = ref(false)
const articleUrl = 'https://rudygo8.github.io/AI_Daily_Paper/ai-daily/'

function refreshIframe() {
  loadError.value = false
  frameLoaded.value = false

  if (dailyFrame.value) {
    dailyFrame.value.src = articleUrl
  }
}

function openNewWindow() {
  window.open(articleUrl, '_blank', 'noopener,noreferrer')
}

function onFrameLoad() {
  loadError.value = false
  frameLoaded.value = true
}

function onFrameError() {
  loadError.value = true
  frameLoaded.value = false
}
</script>

<style lang="scss" scoped>
.daily-report-page {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
}

.report-status-row {
  display: flex;
  align-items: center;
  padding-top: 2px;
}

.report-status {
  width: fit-content;
  padding: 6px 10px;
  font-size: 12px;
  color: #80671f;
  background: #fff7df;
  border: 1px solid #f3e2a5;
  border-radius: 999px;

  &.ready {
    color: #23744d;
    background: #eaf8f1;
    border-color: #bfe7ce;
  }

  &.error {
    color: #bf4f47;
    background: #fff1ef;
    border-color: #f0c6c2;
  }
}

.report-shell {
  position: relative;
  overflow: hidden;
  min-height: 1400px;
  height: calc(100vh + 700px);
  background: #fff;
  border: 1px solid #dbe6f3;
  border-radius: 20px;
  box-shadow: 0 14px 32px rgba(34, 73, 116, 0.08);
}

.report-frame {
  width: 100%;
  height: 100%;
  border: none;
  background: #fff;
}

.report-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  text-align: center;
}

.loading-overlay {
  gap: 14px;
  color: #66727e;
  background: rgba(248, 250, 252, 0.88);

  p {
    margin: 0;
    font-size: 14px;
  }
}

.loading-ring {
  width: 34px;
  height: 34px;
  border: 3px solid #dce4ec;
  border-top-color: #445e78;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

.error-overlay {
  gap: 12px;
  background: rgba(255, 255, 255, 0.96);

  h3 {
    margin: 0;
    font-size: 22px;
    color: #18212a;
  }

  p {
    max-width: 560px;
    margin: 0;
    font-size: 14px;
    line-height: 1.7;
    color: #68737d;
  }
}

.error-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 58px;
  height: 58px;
  font-size: 24px;
  font-weight: 700;
  color: #ce5a4f;
  background: #fff2ef;
  border: 1px solid #ffd5cf;
  border-radius: 50%;
}

.error-actions {
  display: flex;
  gap: 10px;
  margin-top: 6px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 900px) {
  .report-shell {
    min-height: 1100px;
    height: calc(100vh + 520px);
  }
}

@media (max-width: 640px) {
  .report-shell {
    min-height: 900px;
    height: calc(100vh + 380px);
    border-radius: 16px;
  }

  .error-actions {
    flex-direction: column;
    width: 100%;
  }
}
</style>
