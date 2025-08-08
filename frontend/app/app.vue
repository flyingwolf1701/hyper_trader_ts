<template>
  <div class="app">
    <!-- Global loading indicator -->
    <div v-if="pending" class="global-loading">
      <div class="loading-spinner"></div>
    </div>

    <!-- Main app content -->
    <NuxtRouteAnnouncer />
    <NuxtPage />
    
    <!-- Global notifications/toasts could go here -->
  </div>
</template>

<script setup>
// Global meta tags
useHead({
  title: 'HyperTrader',
  meta: [
    { name: 'description', content: 'Personal trading application with advanced authentication' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  ]
})

// Global loading state (optional)
const { pending } = useLazyAsyncData('app-init', () => Promise.resolve())
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  background: #fafafa;
}

.app {
  min-height: 100vh;
  position: relative;
}

.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive utilities */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }
}
</style>