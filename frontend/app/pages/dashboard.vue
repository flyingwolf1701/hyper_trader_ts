<template>
  <div class="dashboard">
    <!-- Navigation Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="brand">
          <h1 class="logo">HyperTrader</h1>
          <div class="status-indicator">
            <span class="status-dot live"></span>
            <span class="status-text">Live Trading</span>
          </div>
        </div>
        
        <nav class="nav-menu">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="nav-tab"
            :class="{ active: activeTab === tab.id }"
          >
            <span class="tab-icon">{{ tab.icon }}</span>
            <span>{{ tab.label }}</span>
          </button>
        </nav>

        <div class="header-actions">
          <div class="user-info">
            <div class="user-avatar">
              <span>{{ userInitials }}</span>
            </div>
            <div class="user-details">
              <span class="user-name">{{ user.name || user.email }}</span>
              <span class="user-status">{{ authMethod }}</span>
            </div>
          </div>
          
          <div class="action-buttons">
            <button @click="showSettings = true" class="btn btn-icon" title="Settings">
              ⚙️
            </button>
            <button @click="handleSignOut" class="btn btn-icon" title="Sign Out">
              🚪
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Dashboard Content -->
    <main class="dashboard-main">
      <!-- Portfolio Overview Tab -->
      <div v-if="activeTab === 'portfolio'" class="tab-content">
        <div class="dashboard-grid">
          <!-- Portfolio Summary -->
          <div class="card portfolio-summary">
            <div class="card-header">
              <h2>Portfolio Overview</h2>
              <div class="portfolio-actions">
                <button class="btn btn-sm btn-primary">
                  <span>📈</span>
                  Deposit
                </button>
                <button class="btn btn-sm btn-secondary">
                  <span>📉</span>
                  Withdraw
                </button>
              </div>
            </div>
            <div class="card-content">
              <div class="portfolio-stats">
                <div class="stat">
                  <span class="stat-label">Total Value</span>
                  <span class="stat-value">${{ formatNumber(portfolioData.totalValue) }}</span>
                  <span class="stat-change" :class="portfolioData.totalChange >= 0 ? 'positive' : 'negative'">
                    {{ portfolioData.totalChange >= 0 ? '+' : '' }}{{ portfolioData.totalChange.toFixed(2) }}%
                  </span>
                </div>
                <div class="stat">
                  <span class="stat-label">24h P&L</span>
                  <span class="stat-value">{{ portfolioData.dailyPnl >= 0 ? '+' : '' }}${{ formatNumber(Math.abs(portfolioData.dailyPnl)) }}</span>
                  <span class="stat-change" :class="portfolioData.dailyPnl >= 0 ? 'positive' : 'negative'">
                    {{ portfolioData.dailyPnlPercent >= 0 ? '+' : '' }}{{ portfolioData.dailyPnlPercent.toFixed(2) }}%
                  </span>
                </div>
                <div class="stat">
                  <span class="stat-label">Available Balance</span>
                  <span class="stat-value">${{ formatNumber(portfolioData.availableBalance) }}</span>
                  <span class="stat-change neutral">USDC</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Top Holdings -->
          <div class="card holdings">
            <div class="card-header">
              <h2>Top Holdings</h2>
              <button class="btn btn-sm btn-outline">View All</button>
            </div>
            <div class="card-content">
              <div class="holdings-list">
                <div 
                  v-for="holding in portfolioData.topHoldings" 
                  :key="holding.symbol"
                  class="holding-item"
                >
                  <div class="holding-info">
                    <div class="holding-symbol">{{ holding.symbol }}</div>
                    <div class="holding-name">{{ holding.name }}</div>
                  </div>
                  <div class="holding-amount">
                    <div class="holding-quantity">{{ holding.quantity }}</div>
                    <div class="holding-value">${{ formatNumber(holding.value) }}</div>
                  </div>
                  <div class="holding-change" :class="holding.change >= 0 ? 'positive' : 'negative'">
                    {{ holding.change >= 0 ? '+' : '' }}{{ holding.change.toFixed(2) }}%
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="card activity">
            <div class="card-header">
              <h2>Recent Activity</h2>
              <div class="activity-filters">
                <button class="filter-btn active">All</button>
                <button class="filter-btn">Trades</button>
                <button class="filter-btn">Transfers</button>
              </div>
            </div>
            <div class="card-content">
              <div class="activity-list">
                <div 
                  v-for="activity in portfolioData.recentActivity" 
                  :key="activity.id"
                  class="activity-item"
                >
                  <div class="activity-icon" :class="activity.type">
                    {{ activity.icon }}
                  </div>
                  <div class="activity-details">
                    <div class="activity-title">{{ activity.title }}</div>
                    <div class="activity-time">{{ activity.time }}</div>
                  </div>
                  <div class="activity-amount" :class="activity.type">
                    {{ activity.amount }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="card quick-actions">
            <div class="card-header">
              <h2>Quick Actions</h2>
            </div>
            <div class="card-content">
              <div class="actions-grid">
                <button class="action-button">
                  <span class="action-icon">⚡</span>
                  <span class="action-label">Quick Trade</span>
                </button>
                <button class="action-button">
                  <span class="action-icon">📊</span>
                  <span class="action-label">Market Analysis</span>
                </button>
                <button class="action-button">
                  <span class="action-icon">🔔</span>
                  <span class="action-label">Set Alerts</span>
                </button>
                <button class="action-button">
                  <span class="action-icon">📋</span>
                  <span class="action-label">View Reports</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Trading Tab -->
      <div v-if="activeTab === 'trading'" class="tab-content">
        <div class="trading-layout">
          <div class="trading-placeholder">
            <div class="placeholder-content">
              <div class="placeholder-icon">📈</div>
              <h2>Advanced Trading Interface</h2>
              <p>Full HyperLiquid trading integration coming soon</p>
              <div class="placeholder-features">
                <div class="feature">
                  <span class="feature-icon">⚡</span>
                  <span>Real-time market data</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">📊</span>
                  <span>Advanced charting tools</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🎯</span>
                  <span>Order management</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🔄</span>
                  <span>Automated strategies</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Tab -->
      <div v-if="activeTab === 'security'" class="tab-content">
        <div class="security-grid">
          <!-- Authentication Methods -->
          <div class="card auth-methods">
            <div class="card-header">
              <h2>Authentication Methods</h2>
              <span class="security-badge">🛡️ Secure</span>
            </div>
            <div class="card-content">
              <div class="auth-method" :class="{ enabled: securityData.passkey }">
                <div class="method-info">
                  <div class="method-icon">🔐</div>
                  <div class="method-details">
                    <h3>Passkey Authentication</h3>
                    <p>Biometric authentication for secure, passwordless login</p>
                  </div>
                </div>
                <div class="method-status">
                  <span v-if="securityData.passkey" class="status enabled">Enabled</span>
                  <button v-else @click="handleSetupPasskey" class="btn btn-sm btn-primary">Setup</button>
                </div>
              </div>

              <div class="auth-method" :class="{ enabled: securityData.totp }">
                <div class="method-info">
                  <div class="method-icon">🔢</div>
                  <div class="method-details">
                    <h3>Two-Factor Authentication</h3>
                    <p>Time-based one-time passwords for additional security</p>
                  </div>
                </div>
                <div class="method-status">
                  <span v-if="securityData.totp" class="status enabled">Enabled</span>
                  <button v-else @click="handleSetupTOTP" class="btn btn-sm btn-primary">Setup</button>
                </div>
              </div>

              <div class="auth-method enabled">
                <div class="method-info">
                  <div class="method-icon">🔑</div>
                  <div class="method-details">
                    <h3>Password Authentication</h3>
                    <p>Traditional password-based authentication</p>
                  </div>
                </div>
                <div class="method-status">
                  <span class="status enabled">Enabled</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Security Settings -->
          <div class="card security-settings">
            <div class="card-header">
              <h2>Security Settings</h2>
            </div>
            <div class="card-content">
              <div class="setting-item">
                <div class="setting-info">
                  <h3>Login Notifications</h3>
                  <p>Get notified of new login attempts</p>
                </div>
                <label class="toggle">
                  <input type="checkbox" v-model="securityData.loginNotifications">
                  <span class="toggle-slider"></span>
                </label>
              </div>

              <div class="setting-item">
                <div class="setting-info">
                  <h3>Session Timeout</h3>
                  <p>Automatically log out after inactivity</p>
                </div>
                <select v-model="securityData.sessionTimeout" class="setting-select">
                  <option value="30">30 minutes</option>
                  <option value="60">1 hour</option>
                  <option value="240">4 hours</option>
                  <option value="480">8 hours</option>
                </select>
              </div>

              <div class="setting-item">
                <div class="setting-info">
                  <h3>API Access</h3>
                  <p>Manage API keys and permissions</p>
                </div>
                <button class="btn btn-sm btn-outline">Manage Keys</button>
              </div>
            </div>
          </div>

          <!-- Recent Security Activity -->
          <div class="card security-activity">
            <div class="card-header">
              <h2>Security Activity</h2>
            </div>
            <div class="card-content">
              <div class="activity-list">
                <div 
                  v-for="activity in securityData.recentActivity" 
                  :key="activity.id"
                  class="security-activity-item"
                >
                  <div class="activity-icon" :class="activity.type">
                    {{ activity.icon }}
                  </div>
                  <div class="activity-details">
                    <div class="activity-title">{{ activity.title }}</div>
                    <div class="activity-time">{{ activity.time }}</div>
                    <div class="activity-location">{{ activity.location }}</div>
                  </div>
                  <div class="activity-status" :class="activity.status">
                    {{ activity.status }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Settings Modal -->
    <div v-if="showSettings" class="modal-overlay" @click="showSettings = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>Settings</h2>
          <button @click="showSettings = false" class="modal-close">×</button>
        </div>
        <div class="modal-content">
          <div class="settings-section">
            <h3>Account</h3>
            <div class="setting-item">
              <span>Email: {{ user.email }}</span>
              <button class="btn btn-sm btn-outline">Change</button>
            </div>
          </div>
          <div class="settings-section">
            <h3>Preferences</h3>
            <div class="setting-item">
              <span>Theme</span>
              <select class="setting-select">
                <option>Light</option>
                <option>Dark</option>
                <option>Auto</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showSettings = false" class="btn btn-secondary">Close</button>
          <button class="btn btn-primary">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const { session, signOut, setupPasskey, setupTOTP } = useAuthCustom()

// Reactive state
const activeTab = ref('portfolio')
const showSettings = ref(false)

// Mock user data (replace with actual session data)
const user = computed(() => ({
  email: 'user@example.com',
  name: 'John Trader',
  authMethods: ['password', 'passkey']
}))

const userInitials = computed(() => {
  if (user.value.name) {
    return user.value.name.split(' ').map(n => n[0]).join('').toUpperCase()
  }
  return user.value.email[0].toUpperCase()
})

const authMethod = computed(() => {
  if (user.value.authMethods.includes('passkey')) {
    return 'Passkey + Password'
  }
  return 'Password'
})

const tabs = [
  { id: 'portfolio', label: 'Portfolio', icon: '💼' },
  { id: 'trading', label: 'Trading', icon: '📈' },
  { id: 'security', label: 'Security', icon: '🛡️' }
]

// Mock portfolio data
const portfolioData = reactive({
  totalValue: 125840.32,
  totalChange: 2.34,
  dailyPnl: 2984.15,
  dailyPnlPercent: 2.4,
  availableBalance: 12500.00,
  topHoldings: [
    { symbol: 'ETH', name: 'Ethereum', quantity: '25.5', value: 45678.90, change: 3.2 },
    { symbol: 'BTC', name: 'Bitcoin', quantity: '1.2', value: 52341.20, change: 1.8 },
    { symbol: 'SOL', name: 'Solana', quantity: '150', value: 18750.00, change: -0.5 },
    { symbol: 'AVAX', name: 'Avalanche', quantity: '200', value: 9070.22, change: 4.1 }
  ],
  recentActivity: [
    { id: 1, type: 'buy', icon: '📈', title: 'Bought 5.2 ETH', time: '2 hours ago', amount: '+$9,234' },
    { id: 2, type: 'sell', icon: '📉', title: 'Sold 0.1 BTC', time: '4 hours ago', amount: '-$4,321' },
    { id: 3, type: 'transfer', icon: '💸', title: 'Deposited USDC', time: '1 day ago', amount: '+$10,000' },
    { id: 4, type: 'buy', icon: '📈', title: 'Bought 50 SOL', time: '2 days ago', amount: '+$6,250' }
  ]
})

// Mock security data
const securityData = reactive({
  passkey: true,
  totp: false,
  loginNotifications: true,
  sessionTimeout: 60,
  recentActivity: [
    { id: 1, type: 'success', icon: '✅', title: 'Successful login', time: '2 hours ago', location: 'Denver, CO', status: 'success' },
    { id: 2, type: 'success', icon: '✅', title: 'Passkey authentication', time: '1 day ago', location: 'Denver, CO', status: 'success' },
    { id: 3, type: 'warning', icon: '⚠️', title: 'Failed login attempt', time: '3 days ago', location: 'Unknown', status: 'blocked' }
  ]
})

// Page meta
useHead({
  title: 'Dashboard - HyperTrader',
  meta: [
    { name: 'description', content: 'Your HyperTrader trading dashboard' }
  ]
})

// Methods
const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num)
}

const handleSignOut = async () => {
  try {
    await signOut()
    router.push('/')
  } catch (error) {
    console.error('Sign out failed:', error)
  }
}

const handleSetupPasskey = async () => {
  try {
    await setupPasskey(user.value.email.split('@')[0], user.value.email)
    securityData.passkey = true
  } catch (error) {
    console.error('Passkey setup failed:', error)
  }
}

const handleSetupTOTP = async () => {
  try {
    // Navigate to TOTP setup page
    router.push('/setup-totp')
  } catch (error) {
    console.error('TOTP setup failed:', error)
  }
}

// Check authentication on mount
onMounted(() => {
  const config = useRuntimeConfig()
  // In dev mode, allow access without session
  // In production, require proper authentication
  if (!config.public.devMode && !session.value) {
    router.push('/login')
  }
})
</script>
<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
}

/* Header */
.dashboard-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.live {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
}

.status-text {
  font-size: 0.875rem;
  color: #10b981;
  font-weight: 500;
}

.nav-menu {
  display: flex;
  gap: 0.5rem;
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  color: #6b7280;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-tab:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-tab.active {
  background: #eff6ff;
  color: #3b82f6;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(45deg, #3b82f6, #1d4ed8);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
}

.user-status {
  font-size: 0.75rem;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-icon {
  padding: 0.5rem;
  aspect-ratio: 1;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-outline {
  background: transparent;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-outline:hover {
  background: #f3f4f6;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

/* Main Dashboard */
.dashboard-main {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

.portfolio-summary {
  grid-column: 1 / -1;
}

.holdings {
  grid-row: 2;
}

.activity {
  grid-row: 2;
}

.quick-actions {
  grid-column: 1 / -1;
  grid-row: 3;
}

/* Cards */
.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.card-content {
  padding: 1.5rem;
}
</style>
/* Portfolio Summary */
.portfolio-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-change {
  font-size: 0.875rem;
  font-weight: 600;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.stat-change.neutral {
  color: #6b7280;
}

.portfolio-actions {
  display: flex;
  gap: 0.5rem;
}

/* Holdings */
.holdings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.holding-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.holding-info {
  display: flex;
  flex-direction: column;
}

.holding-symbol {
  font-weight: 600;
  color: #1f2937;
}

.holding-name {
  font-size: 0.875rem;
  color: #6b7280;
}

.holding-amount {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.holding-quantity {
  font-weight: 600;
  color: #1f2937;
}

.holding-value {
  font-size: 0.875rem;
  color: #6b7280;
}

.holding-change {
  font-weight: 600;
  font-size: 0.875rem;
}

/* Activity */
.activity-filters {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.375rem 0.75rem;
  border: none;
  background: transparent;
  color: #6b7280;
  font-size: 0.875rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: #f3f4f6;
}

.filter-btn.active {
  background: #eff6ff;
  color: #3b82f6;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
}

.activity-icon.buy {
  background: rgba(16, 185, 129, 0.1);
}

.activity-icon.sell {
  background: rgba(239, 68, 68, 0.1);
}

.activity-icon.transfer {
  background: rgba(59, 130, 246, 0.1);
}

.activity-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-title {
  font-weight: 500;
  color: #1f2937;
}

.activity-time {
  font-size: 0.875rem;
  color: #6b7280;
}

.activity-amount {
  font-weight: 600;
}

.activity-amount.buy {
  color: #10b981;
}

.activity-amount.sell {
  color: #ef4444;
}

.activity-amount.transfer {
  color: #3b82f6;
}


/* Quick Actions */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: #eff6ff;
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.action-icon {
  font-size: 1.5rem;
}

.action-label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

/* Trading Layout */
.trading-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.trading-placeholder {
  text-align: center;
  max-width: 500px;
}

.placeholder-content {
  padding: 3rem;
  background: white;
  border-radius: 12px;
  border: 2px dashed #e5e7eb;
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.placeholder-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.placeholder-content p {
  color: #6b7280;
  margin-bottom: 2rem;
}

.placeholder-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  text-align: left;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #374151;
  font-size: 0.875rem;
}

.feature-icon {
  font-size: 1rem;
}

/* Security Grid */
.security-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

.auth-methods {
  grid-column: 1 / -1;
}

/* Authentication Methods */
.security-badge {
  background: rgba(16, 185, 129, 0.1);
  color: #065f46;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.auth-method {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1rem;
  transition: all 0.2s ease;
}

.auth-method.enabled {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.auth-method:last-child {
  margin-bottom: 0;
}

.method-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.method-icon {
  font-size: 1.5rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border-radius: 8px;
}

.method-details h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.method-details p {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.method-status .status {
  background: #10b981;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Security Settings */
.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info h3 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.setting-info p {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
}

.setting-select {
  padding: 0.375rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
}

/* Toggle Switch */
.toggle {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #d1d5db;
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle input:checked + .toggle-slider {
  background-color: #3b82f6;
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

/* Security Activity */
.security-activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.security-activity-item:last-child {
  border-bottom: none;
}

.security-activity-item .activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
}

.security-activity-item .activity-icon.success {
  background: rgba(16, 185, 129, 0.1);
}

.security-activity-item .activity-icon.warning {
  background: rgba(245, 158, 11, 0.1);
}

.security-activity-item .activity-details {
  flex: 1;
}

.security-activity-item .activity-title {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.security-activity-item .activity-time {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.125rem;
}

.security-activity-item .activity-location {
  font-size: 0.75rem;
  color: #9ca3af;
}

.activity-status {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  text-transform: uppercase;
}

.activity-status.success {
  background: rgba(16, 185, 129, 0.1);
  color: #065f46;
}

.activity-status.blocked {
  background: rgba(239, 68, 68, 0.1);
  color: #991b1b;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease-out;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.modal-close:hover {
  background: #f3f4f6;
}

.modal-content {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.settings-section {
  margin-bottom: 2rem;
}

.settings-section:last-child {
  margin-bottom: 0;
}

.settings-section h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .portfolio-summary,
  .holdings,
  .activity,
  .quick-actions {
    grid-column: 1;
    grid-row: auto;
  }

  .security-grid {
    grid-template-columns: 1fr;
  }

  .header-content {
    padding: 1rem;
  }

  .nav-menu {
    order: 3;
    margin-top: 1rem;
    width: 100%;
  }

  .header-content {
    flex-wrap: wrap;
  }

  .user-info {
    order: 2;
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    padding: 1rem;
  }

  .portfolio-stats {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .placeholder-features {
    grid-template-columns: 1fr;
  }

  .user-info {
    display: none;
  }

  .nav-tab {
    flex: 1;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .holding-item {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .holding-item > div {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .modal {
    width: 95%;
    margin: 1rem;
  }
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
