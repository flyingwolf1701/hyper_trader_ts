<template>
  <div class="login-container">
    <div class="login-card">
      <h1>HyperTrader Login</h1>
      
      <div class="dev-banner">
        <p>🚧 Development Mode Active</p>
        <button @click="handleDevLogin" class="dev-login-btn">
          Skip Auth (Dev Only)
        </button>
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="loading" class="loading">Processing...</div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const error = ref('')
const loading = ref(false)

const handleDevLogin = async () => {
  try {
    loading.value = true
    await new Promise(resolve => setTimeout(resolve, 1000))
    alert('Dev login successful!')
    loading.value = false
  } catch (err) {
    error.value = 'Login failed'
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background: #f9fafb;
}

.login-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.dev-banner {
  background: #fef3cd;
  border: 1px solid #fecba1;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  text-align: center;
}

.dev-login-btn {
  background: #f59e0b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
}

.error {
  color: #ef4444;
  text-align: center;
  margin-top: 1rem;
}

.loading {
  text-align: center;
  margin-top: 1rem;
}
</style>