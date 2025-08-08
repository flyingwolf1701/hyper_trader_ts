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
        <hr style="margin: 1rem 0;">
      </div>
      
      <!-- Login Form -->
      <div class="auth-methods">
        <form @submit.prevent="handleLogin">
          <input 
            v-model="loginForm.username" 
            placeholder="Username" 
            required 
          />
          
          <div v-if="showTotpInput">
            <input 
              v-model="loginForm.totpCode" 
              placeholder="TOTP Code (6 digits)" 
              maxlength="6"
              pattern="[0-9]{6}"
            />
          </div>
          
          <div class="auth-options">
            <label>
              <input 
                type="checkbox" 
                v-model="showTotpInput"
              /> 
              Use TOTP (more secure)
            </label>
          </div>
          
          <button type="submit" :disabled="loading">
            {{ showTotpInput ? '🔐 Login with Passkey + TOTP' : '🔐 Login with Passkey' }}
          </button>
        </form>
        
        <div class="setup-link">
          <router-link to="/register">Need to set up authentication?</router-link>
        </div>
      </div>
      
      <!-- Status Messages -->
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="loading" class="loading">Processing...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { devLogin, loginWithPasskey, loginWithFull, isDevMode } = useAuth()
const router = useRouter()

const loginForm = ref({
  username: '',
  totpCode: ''
})

const showTotpInput = ref(false)
const error = ref('')
const loading = ref(false)

const handleDevLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    await devLogin()
    await router.push('/dashboard')
  } catch (err: any) {
    error.value = err.message || 'Dev login failed'
  } finally {
    loading.value = false
  }
}

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    if (showTotpInput.value) {
      if (!loginForm.value.totpCode || loginForm.value.totpCode.length !== 6) {
        throw new Error('Please enter a 6-digit TOTP code')
      }
      await loginWithFull(loginForm.value.username, loginForm.value.totpCode)
    } else {
      await loginWithPasskey(loginForm.value.username)
    }
    
    await router.push('/dashboard')
  } catch (err: any) {
    error.value = err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Your existing styles... */
.auth-options {
  margin: 0.5rem 0;
}

.setup-link {
  text-align: center;
  margin-top: 1rem;
}

.setup-link a {
  color: #3b82f6;
  text-decoration: none;
}
</style>