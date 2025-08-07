export default defineNuxtConfig({
  modules: [
    '@sidebase/nuxt-auth',
    '@pinia/nuxt'
  ],
  
  auth: {
    // @sidebase/nuxt-auth specific configuration
    baseURL: process.env.AUTH_ORIGIN || 'http://localhost:3001',
    provider: {
      type: 'authjs'
    },
    sessionRefresh: {
      enablePeriodically: true,
      enableOnWindowFocus: true,
    },
    globalAppMiddleware: {
      isEnabled: true
    }
  },
  
  runtimeConfig: {
    authSecret: process.env.NUXT_AUTH_SECRET,
    // Server-side only
    jwtSecret: process.env.JWT_SECRET || 'dev-jwt-secret-change-in-production',
    
    public: {
      authBaseURL: process.env.NUXT_PUBLIC_AUTH_BASE_URL || 'http://localhost:3001/api/auth',
      devMode: process.env.NUXT_PUBLIC_DEV_MODE === 'true',
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:3000',
      rpName: process.env.NUXT_PUBLIC_RP_NAME || 'HyperTrader',
      rpId: process.env.NUXT_PUBLIC_RP_ID || 'localhost',
      origin: process.env.NUXT_PUBLIC_ORIGIN || 'http://localhost:3001',
    }
  }
})