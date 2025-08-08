<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Header with back navigation -->
      <div class="header">
        <NuxtLink to="/" class="back-link">
          <span class="back-icon">←</span>
          <span>Back to Home</span>
        </NuxtLink>
        <h1>Welcome Back</h1>
        <p class="subtitle">Sign in to your HyperTrader account</p>
      </div>

      <!-- Development Mode Banner -->
      <div v-if="isDevMode" class="dev-banner">
        <div class="dev-content">
          <span class="dev-icon">🚧</span>
          <div>
            <p class="dev-title">Development Mode Active</p>
            <p class="dev-description">Skip authentication for testing</p>
          </div>
        </div>
        <button @click="handleDevLogin" class="dev-login-btn" :disabled="loading">
          <span v-if="loading" class="btn-spinner"></span>
          <span v-else>Skip Auth (Dev Only)</span>
        </button>
      </div>

      <!-- OAuth Options -->
      <div class="oauth-section">
        <h3>Quick Sign In</h3>
        <div class="oauth-buttons">
          <button @click="handleOAuthLogin('google')" class="oauth-btn google" :disabled="loading">
            <span class="oauth-icon">🔴</span>
            <span>Continue with Google</span>
          </button>
          <button @click="handleOAuthLogin('github')" class="oauth-btn github" :disabled="loading">
            <span class="oauth-icon">⚫</span>
            <span>Continue with GitHub</span>
          </button>
          <button @click="handleOAuthLogin('discord')" class="oauth-btn discord" :disabled="loading">
            <span class="oauth-icon">🟣</span>
            <span>Continue with Discord</span>
          </button>
        </div>
        
        <div class="divider">
          <span>or</span>
        </div>
      </div>

      <!-- Email/Password Login Form -->
      <div class="login-form">
        <h3>Sign in with Email</h3>
        <form @submit.prevent="handleEmailLogin" class="form">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="your.email@example.com"
              :class="{ error: errors.email }"
              required
            />
            <div v-if="errors.email" class="field-error">{{ errors.email }}</div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-input">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter your password"
                :class="{ error: errors.password }"
                required
              />
              <button 
                type="button" 
                @click="showPassword = !showPassword"
                class="password-toggle"
              >
                {{ showPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
            <div v-if="errors.password" class="field-error">{{ errors.password }}</div>
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe">
              <span class="checkmark"></span>
              Remember me
            </label>
            <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">
              Forgot password?
            </a>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="loading || !formData.email || !formData.password"
          >
            <span v-if="loading" class="btn-spinner"></span>
            <span v-else>Sign In</span>
          </button>
        </form>
      </div>

      <!-- Passkey Login Option -->
      <div v-if="showPasskeyOption" class="passkey-section">
        <div class="divider">
          <span>or</span>
        </div>
        
        <div class="passkey-info">
          <h4>🔐 Sign in with Passkey</h4>
          <p>Use your biometric authentication for faster, more secure login</p>
          <button @click="handlePasskeyLogin" class="btn btn-secondary" :disabled="loading">
            <span v-if="loading" class="btn-spinner"></span>
            <span v-else>Use Passkey</span>
          </button>
        </div>
      </div>

      <!-- Error and loading states -->
      <div v-if="error" class="error-banner">
        <span class="error-icon">⚠️</span>
        <span>{{ error }}</span>
        <button @click="error = ''" class="error-close">×</button>
      </div>

      <!-- Register link -->
      <div class="register-link">
        <p>Don't have an account? 
          <NuxtLink to="/register" class="link">Create one here</NuxtLink>
        </p>
      </div>

      <!-- Quick actions (for development) -->
      <div v-if="isDevMode" class="quick-actions">
        <h4>Quick Actions (Dev Mode)</h4>
        <div class="action-buttons">
          <NuxtLink to="/register" class="btn btn-outline">
            Test Registration
          </NuxtLink>
          <NuxtLink to="/dashboard" class="btn btn-outline">
            View Dashboard
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Background decorative elements -->
    <div class="background-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const { devLogin, loginWithPasskey, isDevMode } = useAuthCustom()

// Reactive state
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)
const rememberMe = ref(false)
const showPasskeyOption = ref(true)

const formData = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

// Page meta
useHead({
  title: 'Sign In - HyperTrader',
  meta: [
    { name: 'description', content: 'Sign in to your HyperTrader account with secure authentication' }
  ]
})

// Methods
const validateForm = () => {
  errors.email = ''
  errors.password = ''

  if (!formData.email || !isValidEmail(formData.email)) {
    errors.email = 'Please enter a valid email address'
    return false
  }

  if (!formData.password) {
    errors.password = 'Please enter your password'
    return false
  }

  return true
}

const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const handleDevLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    await devLogin()
    
    // Show success and redirect
    await new Promise(resolve => setTimeout(resolve, 1000))
    router.push('/dashboard')
  } catch (err) {
    console.error('Dev login failed:', err)
    error.value = 'Dev login failed. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleOAuthLogin = async (provider) => {
  loading.value = true
  error.value = ''

  try {
    // Placeholder for OAuth login
    console.log(`OAuth login with ${provider}`)
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // For now, just show success
    alert(`${provider} login coming soon!`)
  } catch (err) {
    error.value = `Failed to sign in with ${provider}. Please try again.`
  } finally {
    loading.value = false
  }
}

const handleEmailLogin = async () => {
  if (!validateForm()) return

  loading.value = true
  error.value = ''

  try {
    // Simulate email/password login
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Placeholder for actual authentication
    console.log('Email login:', { email: formData.email, rememberMe: rememberMe.value })
    
    // For now, simulate success
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Invalid email or password. Please try again.'
  } finally {
    loading.value = false
  }
}

const handlePasskeyLogin = async () => {
  if (!formData.email) {
    error.value = 'Please enter your email address first'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Use the username part of email for passkey
    const username = formData.email.split('@')[0]
    await loginWithPasskey(username)
    
    router.push('/dashboard')
  } catch (err) {
    console.error('Passkey login failed:', err)
    if (err.message.includes('NotSupportedError')) {
      error.value = 'Your device or browser doesn\'t support passkeys.'
    } else if (err.message.includes('NotAllowedError')) {
      error.value = 'Passkey authentication was cancelled.'
    } else {
      error.value = 'Passkey login failed. Please try password login instead.'
    }
  } finally {
    loading.value = false
  }
}

const handleForgotPassword = () => {
  // Placeholder for forgot password functionality
  alert('Forgot password functionality coming soon!')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 100%;
  max-width: 450px;
  position: relative;
  z-index: 1;
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 2rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.back-link:hover {
  color: #374151;
  background: #f3f4f6;
}

.back-icon {
  margin-right: 0.5rem;
  font-size: 1rem;
}

.header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #6b7280;
  margin: 0;
}

/* Dev Banner */
.dev-banner {
  background: linear-gradient(45deg, #fef3cd, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.dev-content {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.dev-icon {
  font-size: 1.5rem;
  margin-right: 1rem;
}

.dev-title {
  font-weight: 600;
  color: #92400e;
  margin: 0 0 0.25rem 0;
}

.dev-description {
  font-size: 0.875rem;
  color: #a16207;
  margin: 0;
}

.dev-login-btn {
  width: 100%;
  background: #f59e0b;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dev-login-btn:hover:not(:disabled) {
  background: #d97706;
  transform: translateY(-1px);
}

.dev-login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* OAuth Section */
.oauth-section {
  margin-bottom: 2rem;
}

.oauth-section h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
  text-align: center;
}

.oauth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.oauth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.oauth-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #d1d5db;
}

.oauth-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.oauth-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.oauth-btn.google:hover:not(:disabled) {
  border-color: #ea4335;
  background: rgba(234, 67, 53, 0.05);
}

.oauth-btn.github:hover:not(:disabled) {
  border-color: #333;
  background: rgba(51, 51, 51, 0.05);
}

.oauth-btn.discord:hover:not(:disabled) {
  border-color: #5865f2;
  background: rgba(88, 101, 242, 0.05);
}

.divider {
  text-align: center;
  position: relative;
  margin: 1.5rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e5e7eb;
}

.divider span {
  background: white;
  padding: 0 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

/* Login Form */
.login-form {
  margin-bottom: 2rem;
}

.login-form h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
  text-align: center;
}

.form {
  space-y: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group input.error {
  border-color: #ef4444;
}

.field-error {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Password Input */
.password-input {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: #6b7280;
}

.password-toggle:hover {
  color: #374151;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.remember-me {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.875rem;
  color: #374151;
}

.remember-me input[type="checkbox"] {
  margin-right: 0.5rem;
  width: auto;
}

.forgot-password {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
}

.forgot-password:hover {
  text-decoration: underline;
}

/* Passkey Section */
.passkey-section {
  margin-bottom: 2rem;
}

.passkey-info {
  text-align: center;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.passkey-info h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.passkey-info p {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  margin: 0.25rem;
  width: 100%;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-outline {
  background: transparent;
  color: #374151;
  border: 1px solid #d1d5db;
  width: auto;
}

.btn-outline:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.btn-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

/* Error Banner */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fca5a5;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  color: #991b1b;
}

.error-icon {
  margin-right: 0.5rem;
}

.error-close {
  margin-left: auto;
  background: none;
  border: none;
  color: #991b1b;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0;
}

/* Register Link */
.register-link {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
  margin-bottom: 1.5rem;
}

.register-link p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

/* Quick Actions */
.quick-actions {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
}

.quick-actions h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
  text-align: center;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Background Decoration */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(1px);
}

.circle-1 {
  width: 200px;
  height: 200px;
  top: -100px;
  right: -100px;
  animation: float 6s ease-in-out infinite;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  left: -150px;
  animation: float 8s ease-in-out infinite reverse;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: -75px;
  animation: float 10s ease-in-out infinite;
}

/* Responsive Design */
@media (max-width: 640px) {
  .login-card {
    padding: 1.5rem;
    margin: 0.5rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .form-options {
    flex-direction: column;
    gap: 0.75rem;
  }

  .oauth-buttons {
    gap: 0.5rem;
  }
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}
</style>