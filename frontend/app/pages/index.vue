<template>
  <div class="home-container">
    <div class="hero-section">
      <!-- Header with logo/brand -->
      <header class="header">
        <div class="brand">
          <h1 class="logo">HyperTrader</h1>
          <p class="tagline">Advanced Trading Platform</p>
        </div>
      </header>

      <!-- Main hero content -->
      <div class="hero-content">
        <div class="hero-text">
          <h2 class="hero-title">
            Trade Smarter with 
            <span class="gradient-text">Advanced Authentication</span>
          </h2>
          <p class="hero-description">
            Experience secure, passwordless trading with cutting-edge passkey technology. 
            Connect to HyperLiquid and manage your portfolio with enterprise-grade security.
          </p>
          
          <!-- Features list -->
          <div class="features">
            <div class="feature">
              <span class="feature-icon">🔐</span>
              <span>Passkey Authentication</span>
            </div>
            <div class="feature">
              <span class="feature-icon">📈</span>
              <span>HyperLiquid Integration</span>
            </div>
            <div class="feature">
              <span class="feature-icon">⚡</span>
              <span>Real-time Trading</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🛡️</span>
              <span>TOTP Security</span>
            </div>
          </div>
        </div>

        <!-- Call-to-action buttons -->
        <div class="cta-section">
          <div class="cta-buttons">
            <NuxtLink to="/register" class="btn btn-primary">
              <span class="btn-icon">🚀</span>
              Create Account
            </NuxtLink>
            <NuxtLink to="/login" class="btn btn-secondary">
              <span class="btn-icon">🔑</span>
              Sign In
            </NuxtLink>
          </div>
          
          <!-- Development mode indicator -->
          <div v-if="isDevMode" class="dev-notice">
            <span class="dev-icon">🚧</span>
            <span>Development Mode Active</span>
          </div>
        </div>
      </div>

      <!-- Visual elements -->
      <div class="hero-visual">
        <div class="trading-card">
          <div class="card-header">
            <div class="status-indicator active"></div>
            <span>Live Trading</span>
          </div>
          <div class="card-content">
            <div class="metric">
              <span class="metric-label">Portfolio Value</span>
              <span class="metric-value">$125,840.32</span>
              <span class="metric-change positive">+2.34%</span>
            </div>
            <div class="metric">
              <span class="metric-label">24h P&L</span>
              <span class="metric-value">+$2,984.15</span>
              <span class="metric-change positive">+2.4%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Security features section -->
    <section class="security-section">
      <div class="container">
        <h3 class="section-title">Bank-Grade Security</h3>
        <div class="security-grid">
          <div class="security-feature">
            <div class="security-icon">🔐</div>
            <h4>Passkey Authentication</h4>
            <p>Use biometric authentication or security keys for passwordless login</p>
          </div>
          <div class="security-feature">
            <div class="security-icon">🔢</div>
            <h4>TOTP Protection</h4>
            <p>Two-factor authentication with time-based one-time passwords</p>
          </div>
          <div class="security-feature">
            <div class="security-icon">🛡️</div>
            <h4>Zero Trust</h4>
            <p>Every action verified with modern cryptographic standards</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const isDevMode = computed(() => config.public.devMode)

// Page meta
useHead({
  title: 'HyperTrader - Advanced Trading Platform',
  meta: [
    { 
      name: 'description', 
      content: 'Secure trading platform with passkey authentication and HyperLiquid integration' 
    }
  ]
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.hero-section {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

/* Header */
.header {
  padding: 2rem;
  text-align: center;
}

.brand {
  margin-bottom: 2rem;
}

.logo {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.tagline {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.125rem;
  margin: 0.5rem 0 0 0;
  font-weight: 300;
}

/* Hero Content */
.hero-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  gap: 4rem;
}

.hero-text {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.gradient-text {
  background: linear-gradient(45deg, #fbbf24, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin-bottom: 2rem;
  font-weight: 300;
}

/* Features */
.features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 3rem;
}

.feature {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.feature-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

/* CTA Section */
.cta-section {
  margin-top: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.125rem;
  text-decoration: none;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  text-align: center;
}

.btn-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.btn-primary {
  background: linear-gradient(45deg, #3b82f6, #1d4ed8);
  color: white;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* Dev Notice */
.dev-notice {
  display: inline-flex;
  align-items: center;
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.dev-icon {
  margin-right: 0.5rem;
}

/* Hero Visual */
.hero-visual {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trading-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
  width: 300px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  color: white;
  font-weight: 600;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.status-indicator.active {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
}

.card-content {
  space-y: 1.5rem;
}

.metric {
  margin-bottom: 1.5rem;
}

.metric-label {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.metric-value {
  display: block;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.metric-change {
  font-size: 0.875rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

/* Security Section */
.security-section {
  background: white;
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 3rem;
}

.security-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.security-feature {
  text-align: center;
  padding: 2rem;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.security-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.security-feature h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.security-feature p {
  color: #6b7280;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .trading-card {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .header, .hero-content {
    padding: 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-description {
    font-size: 1.125rem;
  }

  .features {
    grid-template-columns: 1fr;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .security-grid {
    grid-template-columns: 1fr;
  }

  .container {
    padding: 0 1rem;
  }
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-text > * {
  animation: fadeInUp 0.8s ease-out forwards;
}

.hero-text > *:nth-child(2) {
  animation-delay: 0.2s;
}

.hero-text > *:nth-child(3) {
  animation-delay: 0.4s;
}

.cta-section {
  animation: fadeInUp 0.8s ease-out 0.6s forwards;
  opacity: 0;
}
</style>