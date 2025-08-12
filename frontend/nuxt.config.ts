export default defineNuxtConfig({
  compatibilityDate: '2025-08-08',
  modules: [
    '@pinia/nuxt'
  ],

  devServer: {
    port: 3001
  },
  
  runtimeConfig: {
    // Server-side only
    jwtSecret: process.env.JWT_SECRET,
    
    public: {
      devMode: process.env.NUXT_PUBLIC_DEV_MODE === 'true',
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:3000',
    }
  },
})      