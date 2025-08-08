export default defineNuxtConfig({
  modules: [
    '@sidebase/nuxt-auth',
    '@pinia/nuxt'
  ],

  // Add these two lines to fix the port conflict and warning
  devServer: {
    port: 3001
  },
  
  auth: {
    // @sidebase/nuxt-auth specific configuration
    baseURL: process.env.AUTH_ORIGIN ,
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