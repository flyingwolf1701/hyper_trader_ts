<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Header with back navigation -->
      <div class="header">
        <div class="nav-links">
          <NuxtLink to="/" class="back-link">
            <span class="back-icon">←</span>
            <span>Back to Home</span>
          </NuxtLink>
          <NuxtLink to="/login" class="login-link">
            <span>Sign In</span>
            <span class="login-icon">→</span>
          </NuxtLink>
        </div>
        <h1>Create Your HyperTrader Account</h1>
        
        <!-- Progress indicator -->
        <div class="progress-indicator">
          <div class="step" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
            <div class="step-number">1</div>
            <span>Account Info</span>
          </div>
          <div class="step-divider"></div>
          <div class="step" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
            <div class="step-number">2</div>
            <span>Setup Passkey</span>
          </div>
          <div class="step-divider"></div>
          <div class="step" :class="{ active: currentStep === 3 }">
            <div class="step-number">3</div>
            <span>Complete</span>
          </div>
        </div>
      </div>

      <!-- OAuth Options -->
      <div v-if="currentStep === 1" class="oauth-section">
        <h3>Quick Sign Up</h3>
        <div class="oauth-buttons">
          <button @click="handleOAuthSignup('google')" class="oauth-btn google" :disabled="loading">
            <span class="oauth-icon">🔴</span>
            <span>Continue with Google</span>
          </button>
          <button @click="handleOAuthSignup('github')" class="oauth-btn github" :disabled="loading">
            <span class="oauth-icon">⚫</span>
            <span>Continue with GitHub</span>
          </button>
          <button @click="handleOAuthSignup('discord')" class="oauth-btn discord" :disabled="loading">
            <span class="oauth-icon">🟣</span>
            <span>Continue with Discord</span>
          </button>
        </div>
        
        <div class="divider">
          <span>or</span>
        </div>
      </div>

      <!-- Step 1: Account Information -->
      <div v-if="currentStep === 1" class="step-content">
        <h2>Create Account</h2>
        <p class="step-description">Enter your account details to get started</p>
        
        <form @submit.prevent="handleAccountInfo" class="form">
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
                placeholder="Create a strong password"
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
            
            <!-- Password strength indicator -->
            <div class="password-strength">
              <div class="strength-bar">
                <div 
                  class="strength-fill" 
                  :class="passwordStrength.class"
                  :style="{ width: passwordStrength.width }"
                ></div>
              </div>
              <span class="strength-text" :class="passwordStrength.class">
                {{ passwordStrength.text }}
              </span>
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              placeholder="Confirm your password"
              :class="{ error: errors.confirmPassword }"
              required
            />
            <div v-if="errors.confirmPassword" class="field-error">{{ errors.confirmPassword }}</div>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="loading || !formData.email || !formData.password || !formData.confirmPassword"
          >
            <span v-if="loading" class="btn-spinner"></span>
            Continue to Passkey Setup
          </button>
        </form>
      </div>

      <!-- Step 2: Passkey Setup -->
      <div v-if="currentStep === 2" class="step-content">
        <h2>Setup Your Passkey</h2>
        <p class="step-description">Add an extra layer of security with a passkey (optional but recommended)</p>
        
        <div class="passkey-info">
          <div class="info-card">
            <div class="info-icon">🔐</div>
            <div class="info-content">
              <h3>Why Add a Passkey?</h3>
              <ul>
                <li>Faster login with biometrics</li>
                <li>More secure than passwords alone</li>
                <li>Resistant to phishing attacks</li>
                <li>Works across all your devices</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="device-info">
          <h4>Your device supports:</h4>
          <div class="supported-methods">
            <div class="method" v-if="supportInfo.fingerprint">
              <span class="method-icon">👆</span>
              <span>Fingerprint</span>
            </div>
            <div class="method" v-if="supportInfo.faceId">
              <span class="method-icon">🫥</span>
              <span>Face ID</span>
            </div>
            <div class="method" v-if="supportInfo.pin">
              <span class="method-icon">🔢</span>
              <span>PIN</span>
            </div>
            <div class="method" v-if="supportInfo.securityKey">
              <span class="method-icon">🔑</span>
              <span>Security Key</span>
            </div>
          </div>
        </div>

        <div class="button-group">
          <button 
            @click="handlePasskeySetup" 
            class="btn btn-primary"
            :disabled="loading"
          >
            <span v-if="loading" class="btn-spinner"></span>
            <span v-else>Setup Passkey</span>
          </button>

          <button 
            @click="skipPasskey" 
            class="btn btn-secondary"
            :disabled="loading"
          >
            Skip for Now
          </button>

          <button 
            @click="currentStep = 1" 
            class="btn btn-outline"
            :disabled="loading"
          >
            Back
          </button>
        </div>
      </div>

      <!-- Step 3: Success -->
      <div v-if="currentStep === 3" class="step-content">
        <div class="success-content">
          <div class="success-icon">✅</div>
          <h2>Account Created Successfully!</h2>
          <p class="success-message">
            Welcome to HyperTrader! Your account has been created and 
            <span v-if="passkeySetup">your passkey is ready to use</span>
            <span v-else>you can always add a passkey later for enhanced security</span>.
          </p>
          
          <div class="account-summary">
            <div class="summary-item">
              <span class="summary-icon">📧</span>
              <span>{{ formData.email }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-icon">🔐</span>
              <span>{{ passkeySetup ? 'Passkey Enabled' : 'Password Only' }}</span>
            </div>
          </div>
          
          <div class="next-steps">
            <h3>What's Next?</h3>
            <div class="step-list">
              <div class="next-step">
                <span class="step-icon">🏠</span>
                <span>Access your dashboard</span>
              </div>
              <div class="next-step" v-if="!passkeySetup">
                <span class="step-icon">🔒</span>
                <span>Set up passkey for faster login</span>
              </div>
              <div class="next-step">
                <span class="step-icon">📈</span>
                <span>Start trading on HyperLiquid</span>
              </div>
            </div>
          </div>

          <div class="action-buttons">
            <button @click="goToDashboard" class="btn btn-primary">
              Go to Dashboard
            </button>
            <button @click="goToLogin" class="btn btn-secondary">
              Go to Login
            </button>
            <NuxtLink to="/" class="btn btn-outline">
              Back to Home
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Error display -->
      <div v-if="error" class="error-banner">
        <span class="error-icon">⚠️</span>
        <span>{{ error }}</span>
        <button @click="error = ''" class="error-close">×</button>
      </div>

      <!-- Footer links -->
      <div v-if="currentStep !== 3" class="footer-links">
        <p>Already have an account? 
          <NuxtLink to="/login" class="link">Sign in here</NuxtLink>
        </p>
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
const { setupPasskey, isDevMode } = useAuthCustom()

// Reactive state
const currentStep = ref(1)
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const passkeySetup = ref(false)

const formData = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

// Device capability detection
const supportInfo = reactive({
  fingerprint: false,
  faceId: false,
  pin: false,
  securityKey: false
})

// Password strength computation
const passwordStrength = computed(() => {
  const password = formData.password
  if (!password) return { width: '0%', class: '', text: '' }

  let score = 0
  let feedback = []

  // Length check
  if (password.length >= 8) score += 1
  else feedback.push('At least 8 characters')

  // Character variety
  if (/[a-z]/.test(password)) score += 1
  else feedback.push('Lowercase letter')

  if (/[A-Z]/.test(password)) score += 1
  else feedback.push('Uppercase letter')

  if (/\d/.test(password)) score += 1
  else feedback.push('Number')

  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1
  else feedback.push('Special character')

  // Return strength info
  if (score === 0) return { width: '0%', class: '', text: '' }
  if (score <= 2) return { width: '25%', class: 'weak', text: 'Weak' }
  if (score <= 3) return { width: '50%', class: 'fair', text: 'Fair' }
  if (score <= 4) return { width: '75%', class: 'good', text: 'Good' }
  return { width: '100%', class: 'strong', text: 'Strong' }
})

// Page meta
useHead({
  title: 'Register - HyperTrader',
  meta: [
    { name: 'description', content: 'Create your HyperTrader account with secure authentication' }
  ]
})

onMounted(async () => {
  await detectDeviceCapabilities()
})

// Methods
const validateForm = () => {
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''

  if (!formData.email || !isValidEmail(formData.email)) {
    errors.email = 'Please enter a valid email address'
    return false
  }

  if (!formData.password || formData.password.length < 8) {
    errors.password = 'Password must be at least 8 characters long'
    return false
  }

  if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    return false
  }

  return true
}

const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const handleOAuthSignup = async (provider) => {
  loading.value = true
  error.value = ''

  try {
    // Placeholder for OAuth signup
    console.log(`OAuth signup with ${provider}`)
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // For now, just show success
    alert(`${provider} signup coming soon!`)
  } catch (err) {
    error.value = `Failed to sign up with ${provider}. Please try again.`
  } finally {
    loading.value = false
  }
}

const handleAccountInfo = async () => {
  if (!validateForm()) return

  loading.value = true
  error.value = ''

  try {
    // Simulate account creation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Here you would create the account with email + password
    console.log('Creating account:', { email: formData.email })
    
    currentStep.value = 2
  } catch (err) {
    error.value = 'Failed to create account. Please try again.'
  } finally {
    loading.value = false
  }
}

const handlePasskeySetup = async () => {
  loading.value = true
  error.value = ''

  try {
    // Generate username from email for passkey
    const username = formData.email.split('@')[0]
    await setupPasskey(username, formData.email)
    passkeySetup.value = true
    currentStep.value = 3
  } catch (err) {
    console.error('Passkey setup failed:', err)
    if (err.message.includes('NotSupportedError')) {
      error.value = 'Your device or browser doesn\'t support passkeys. You can continue without one.'
    } else if (err.message.includes('NotAllowedError')) {
      error.value = 'Passkey creation was cancelled. You can try again or continue without one.'
    } else {
      error.value = 'Failed to create passkey. You can continue without one.'
    }
  } finally {
    loading.value = false
  }
}

const skipPasskey = () => {
  passkeySetup.value = false
  currentStep.value = 3
}

const detectDeviceCapabilities = async () => {
  if (!process.client) return

  try {
    // Check if WebAuthn is available
    if (!window.PublicKeyCredential) {
      return
    }

    // Check for various authenticator types
    if (window.PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable) {
      const available = await window.PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable()
      if (available) {
        // Platform authenticator available (Touch ID, Face ID, Windows Hello, etc.)
        supportInfo.fingerprint = true
        supportInfo.faceId = true
        supportInfo.pin = true
      }
    }

    // Security keys are generally supported if WebAuthn is available
    supportInfo.securityKey = true
  } catch (err) {
    console.warn('Could not detect device capabilities:', err)
  }
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 100%;
  max-width: 500px;
  position: relative;
  z-index: 1;
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 2rem;
}

.nav-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.back-link, .login-link {
  display: inline-flex;
  align-items: center;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.875rem;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.back-link:hover, .login-link:hover {
  color: #374151;
  background: #f3f4f6;
}

.back-icon {
  margin-right: 0.5rem;
  font-size: 1rem;
}

.login-icon {
  margin-left: 0.5rem;
  font-size: 1rem;
}

.header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

/* Progress Indicator */
.progress-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.step-number {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: #e5e7eb;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: #3b82f6;
  color: white;
}

.step.completed .step-number {
  background: #10b981;
  color: white;
}

.step span {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.step-divider {
  width: 3rem;
  height: 1px;
  background: #e5e7eb;
  margin: 0 1rem;
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

/* Form Styles */
.step-content {
  margin-bottom: 1.5rem;
}

.step-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.step-description {
  color: #6b7280;
  margin-bottom: 1.5rem;
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

/* Password Strength */
.password-strength {
  margin-top: 0.5rem;
}

.strength-bar {
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.strength-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 2px;
}

.strength-fill.weak {
  background: #ef4444;
}

.strength-fill.fair {
  background: #f59e0b;
}

.strength-fill.good {
  background: #3b82f6;
}

.strength-fill.strong {
  background: #10b981;
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 500;
}

.strength-text.weak {
  color: #ef4444;
}

.strength-text.fair {
  color: #f59e0b;
}

.strength-text.good {
  color: #3b82f6;
}

.strength-text.strong {
  color: #10b981;
}

/* Passkey Info */
.passkey-info {
  margin-bottom: 1.5rem;
}

.info-card {
  display: flex;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.info-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.info-content h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.info-content ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.info-content li {
  color: #4b5563;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  position: relative;
  padding-left: 1rem;
}

.info-content li::before {
  content: '✓';
  color: #10b981;
  font-weight: bold;
  position: absolute;
  left: 0;
}

/* Device Info */
.device-info {
  margin-bottom: 1.5rem;
}

.device-info h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
}

.supported-methods {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.method {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: #ecfdf5;
  color: #065f46;
  border-radius: 6px;
  font-size: 0.875rem;
  border: 1px solid #a7f3d0;
}

.method-icon {
  margin-right: 0.5rem;
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
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
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

.button-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Success Content */
.success-content {
  text-align: center;
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.success-content h2 {
  color: #10b981;
  margin-bottom: 1rem;
}

.success-message {
  color: #4b5563;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.account-summary {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  color: #4b5563;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.next-steps {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.next-steps h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.step-list {
  text-align: left;
}

.next-step {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  color: #4b5563;
}

.step-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
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

/* Footer Links */
.footer-links {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.footer-links p {
  color: #6b7280;
  font-size: 0.875rem;
}

.link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
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
  .register-card {
    padding: 1.5rem;
    margin: 0.5rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
  }

  .progress-indicator {
    flex-direction: column;
    gap: 1rem;
  }

  .step-divider {
    width: 1px;
    height: 2rem;
    margin: 0.5rem 0;
  }

  .supported-methods {
    flex-direction: column;
  }

  .action-buttons, .button-group {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    margin: 0.25rem 0;
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