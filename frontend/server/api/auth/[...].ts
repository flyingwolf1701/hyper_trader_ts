import { NuxtAuthHandler } from '#auth'
import type { AuthConfig } from '@auth/core/types'
import CredentialsProvider from '@auth/core/providers/credentials'

const runtimeConfig = useRuntimeConfig()

export default NuxtAuthHandler({
  secret: runtimeConfig.authSecret,
  
  providers: [
    CredentialsProvider({
      id: 'dev-bypass',
      name: 'Development Bypass',
      credentials: {},
      async authorize() {
        // Only allow in dev mode
        if (runtimeConfig.public.devMode) {
          return {
            id: 'dev-user-123',
            name: 'Developer',
            email: 'dev@localhost',
            role: 'developer'
          }
        }
        return null
      }
    }),
    
    CredentialsProvider({
      id: 'passkey',
      name: 'Passkey Authentication',
      credentials: {
        response: { label: 'WebAuthn Response', type: 'text' },
        username: { label: 'Username', type: 'text' }
      },
      async authorize(credentials) {
        try {
          // Call your backend to verify the passkey
          const response = await $fetch('/auth/passkey/verify', {
            baseURL: runtimeConfig.public.apiBase,
            method: 'POST',
            body: {
              response: credentials?.response,
              username: credentials?.username
            }
          })
          
          if (response.verified) {
            return {
              id: response.user.id,
              name: response.user.username,
              email: response.user.email,
              role: 'user'
            }
          }
          return null
        } catch (error) {
          console.error('Passkey verification failed:', error)
          return null
        }
      }
    }),
    
    CredentialsProvider({
      id: 'totp',
      name: 'TOTP + Passkey',
      credentials: {
        username: { label: 'Username', type: 'text' },
        totpCode: { label: 'TOTP Code', type: 'text' },
        passkeyResponse: { label: 'Passkey Response', type: 'text' }
      },
      async authorize(credentials) {
        try {
          // Verify both passkey and TOTP
          const response = await $fetch('/auth/verify-full', {
            baseURL: runtimeConfig.public.apiBase,
            method: 'POST',
            body: {
              username: credentials?.username,
              totpCode: credentials?.totpCode,
              passkeyResponse: credentials?.passkeyResponse
            }
          })
          
          if (response.verified) {
            return {
              id: response.user.id,
              name: response.user.username,
              email: response.user.email,
              role: 'user',
              authMethods: response.authMethods
            }
          }
          return null
        } catch (error) {
          console.error('Full auth verification failed:', error)
          return null
        }
      }
    })
  ],
  
  session: {
    strategy: 'jwt',
    maxAge: 24 * 60 * 60, // 24 hours
  },
  
  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.role = user.role
        token.authMethods = user.authMethods
      }
      return token
    },
    
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub
        session.user.role = token.role
        session.user.authMethods = token.authMethods
      }
      return session
    }
  },
  
  pages: {
    signIn: '/login',
    error: '/auth/error'
  }
} satisfies AuthConfig)