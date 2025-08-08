<template>
  <div class="login-container">
    <div class="login-card">
      <h1>HyperTrader Login</h1>
      
      <!-- Dev Mode Banner -->
      <div v-if="isDevMode" class="dev-banner">
        <p>🚧 Development Mode Active</p>
        <button @click="handleDevLogin" class="dev-login-btn">
          Skip Auth (Dev Only)
        </button>
      </div>
      
      <!-- Production Auth -->
      <div v-else class="auth-methods">
        <div class="passkey-section">
          <h2>Sign in with Passkey</h2>
          <button @click="handlePasskeyLogin" class="passkey-btn">
            🔐 Use Passkey
          </button>
        </div>
        
        <div class="totp-section">
          <h2>Setup Authentication</h2>
          <form @submit.prevent="handleSetup">
            <input 
              v-model="setupForm.username" 
              placeholder="Username" 
              required 
            />
            <input 
              v-model="setupForm.email" 
              type="email" 
              placeholder="Email" 
              required 
            />
            <button type="submit">Setup Account</button>
          </form>
        </div>
      </div>
      
      <!-- Status Messages -->
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="loading" class="loading">Processing...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { devLogin, setupPasskey, isDevMode } = useAuthCustom()
const router = useRouter()

const setupForm = ref({
  username: '',
  email: ''
})

const error = ref('')
const loading = ref(false)

const handleDevLogin = async () => {
  try {
    loading.value = true
    await devLogin()
    await router.push('/dashboard')
  } catch (err) {
    error.value = 'Dev login failed'
  } finally {
    loading.value = false
  }
}

const handlePasskeyLogin = async () => {
  // Implement passkey authentication
  error.value = 'Passkey login not yet implemented'
}

const handleSetup = async () => {
  try {
    loading.value = true
    await setupPasskey(setupForm.value.username, setupForm.value.email)
    // Redirect to TOTP setup
    await router.push('/setup-totp')
  } catch (err) {
    error.value = 'Setup failed'
  } finally {
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

.auth-methods {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.passkey-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

input {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
}

button[type="submit"] {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
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