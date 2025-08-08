export default defineNuxtRouteMiddleware((to) => {
  const { status } = useAuth()
  const config = useRuntimeConfig()
  
  // Skip auth check in dev mode for certain routes
  if (config.public.devMode && to.path.startsWith('/dev')) {
    return
  }
  
  // Protected routes
  const protectedRoutes = ['/dashboard', '/trading', '/profile']
  
  if (protectedRoutes.some(route => to.path.startsWith(route))) {
    if (status.value === 'unauthenticated') {
      return navigateTo('/login')
    }
  }
  
  // Redirect authenticated users away from login
  if (to.path === '/login' && status.value === 'authenticated') {
    return navigateTo('/dashboard')
  }
})