export default defineNuxtConfig({
  compatibilityDate: '2025-08-08',
  modules: [
    '@sidebase/nuxt-auth',
    '@pinia/nuxt'
  ],

  devServer: {
    port: 3001
  },
  
  auth: {
    baseURL: process.env.AUTH_ORIGIN || 'http://localhost:3001',
    provider: {
      type: 'authjs'
    },
    sessionRefresh: {
      enablePeriodically: false,
      enableOnWindowFocus: false,
    },
    globalAppMiddleware: {
      isEnabled: false  // Disable temporarily
    }
  },
  
  runtimeConfig: {
    authSecret: process.env.NUXT_AUTH_SECRET,
    // Server-side only
    jwtSecret: process.env.JWT_SECRET,
    
    public: {
      authBaseURL: process.env.NUXT_PUBLIC_AUTH_BASE_URL,
      devMode: process.env.NUXT_PUBLIC_DEV_MODE === 'true',
      apiBase: process.env.NUXT_PUBLIC_API_BASE,
      rpName: process.env.NUXT_PUBLIC_RP_NAME,
      rpId: process.env.NUXT_PUBLIC_RP_ID,
      origin: process.env.NUXT_PUBLIC_ORIGIN,
    }
  },
})