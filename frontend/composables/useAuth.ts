export const useAuth = () => {
  const { data: session, status, signIn, signOut } = useAuth()
  const config = useRuntimeConfig()
  
  const devLogin = async () => {
    if (!config.public.devMode) {
      throw new Error('Dev mode not enabled')
    }
    
    try {
      const result = await signIn('dev-bypass', { 
        redirect: false 
      })
      
      if (result?.error) {
        throw new Error(result.error)
      }
      
      return result
    } catch (error) {
      console.error('Dev login failed:', error)
      throw error
    }
  }
  
  const loginWithPasskey = async (username: string) => {
    try {
      // Get authentication options from backend
      const authOptions = await $fetch('/auth/passkey/authenticate/start', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { username }
      })
      
      // Use WebAuthn browser API
      const { startAuthentication } = await import('@simplewebauthn/browser')
      const response = await startAuthentication(authOptions.options)
      
      // Sign in with the response
      const result = await signIn('passkey', {
        response: JSON.stringify(response),
        username,
        redirect: false
      })
      
      if (result?.error) {
        throw new Error(result.error)
      }
      
      return result
    } catch (error) {
      console.error('Passkey login failed:', error)
      throw error
    }
  }
  
  const loginWithFull = async (username: string, totpCode: string) => {
    try {
      // Get passkey challenge
      const authOptions = await $fetch('/auth/passkey/authenticate/start', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { username }
      })
      
      // Complete passkey authentication
      const { startAuthentication } = await import('@simplewebauthn/browser')
      const passkeyResponse = await startAuthentication(authOptions.options)
      
      // Sign in with both passkey and TOTP
      const result = await signIn('totp', {
        username,
        totpCode,
        passkeyResponse: JSON.stringify(passkeyResponse),
        redirect: false
      })
      
      if (result?.error) {
        throw new Error(result.error)
      }
      
      return result
    } catch (error) {
      console.error('Full auth login failed:', error)
      throw error
    }
  }
  
  // ... rest of your existing methods
  
  return {
    session,
    status,
    signIn,
    signOut,
    devLogin,
    loginWithPasskey,
    loginWithFull,
    setupPasskey,
    setupTOTP,
    isDevMode: config.public.devMode
  }
}