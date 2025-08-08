import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { z } from 'zod'
import { 
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse
} from '@simplewebauthn/server'
import { authenticator } from 'otplib'
import QRCode from 'qrcode'

const auth = new Hono()

// CORS for auth endpoints
auth.use('/*', cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3001'],
  credentials: true,
}))

// Passkey registration schemas
const RegisterStartSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email()
})

const RegisterFinishSchema = z.object({
  username: z.string(),
  credential: z.any()
})

// TOTP setup schema
const TotpSetupSchema = z.object({
  userId: z.string()
})

// Dev mode bypass
auth.get('/dev-login', async (c) => {
  if (process.env.DEV_MODE !== 'true') {
    return c.json({ error: 'Dev mode disabled' }, 403)
  }
  
  // Return a mock user session
  return c.json({
    user: {
      id: 'dev-user-123',
      username: 'developer',
      email: 'dev@localhost',
      isAuthenticated: true,
      authMethods: ['dev-bypass']
    },
    token: 'dev-token-' + Date.now()
  })
})

// Passkey registration start
auth.post('/passkey/register/start', async (c) => {
  try {
    const body = await c.req.json()
    const { username, email } = RegisterStartSchema.parse(body)
    
    const options = await generateRegistrationOptions({
      rpName: 'HyperTrader',
      rpID: process.env.NODE_ENV === 'production' ? 'yourdomain.com' : 'localhost',
      userID: new TextEncoder().encode(username),
      userName: username,
      userDisplayName: email,
      attestationType: 'none',
      authenticatorSelection: {
        residentKey: 'preferred',
        userVerification: 'preferred',
        authenticatorAttachment: 'platform',
      },
    })

    // Store challenge in session/cache (you'll need to implement this)
    // For now, we'll return it to be stored client-side (less secure but simpler for dev)
    
    return c.json({ options, challenge: options.challenge })
  } catch (error) {
    return c.json({ error: 'Registration failed' }, 400)
  }
})

// Passkey registration finish
auth.post('/passkey/register/finish', async (c) => {
  try {
    const body = await c.req.json()
    const { username, credential } = RegisterFinishSchema.parse(body)
    
    // Verify the registration response
    // You'll need to implement user storage and challenge verification
    
    return c.json({ success: true, userId: `user-${Date.now()}` })
  } catch (error) {
    return c.json({ error: 'Registration verification failed' }, 400)
  }
})

// TOTP setup
auth.post('/totp/setup', async (c) => {
  try {
    const body = await c.req.json()
    const { userId } = TotpSetupSchema.parse(body)
    
    const secret = authenticator.generateSecret()
    const serviceName = 'HyperTrader'
    const accountName = `user-${userId}`
    
    const otpauth = authenticator.keyuri(accountName, serviceName, secret)
    const qrCode = await QRCode.toDataURL(otpauth)
    
    // Store secret in database associated with user
    // TODO: Implement user secret storage
    
    return c.json({
      secret,
      qrCode,
      backupCodes: generateBackupCodes() // Implement this function
    })
  } catch (error) {
    return c.json({ error: 'TOTP setup failed' }, 400)
  }
})

// TOTP verification
auth.post('/totp/verify', async (c) => {
  try {
    const { userId, token } = await c.req.json()
    
    // Get user's TOTP secret from database
    const userSecret = 'TODO_GET_FROM_DB' // Implement this
    
    const isValid = authenticator.verify({
      token,
      secret: userSecret,
      window: 2 // Allow some time drift
    })
    
    return c.json({ valid: isValid })
  } catch (error) {
    return c.json({ error: 'TOTP verification failed' }, 400)
  }
})

function generateBackupCodes(): string[] {
  return Array.from({ length: 8 }, () => 
    Math.random().toString(36).substring(2, 10).toUpperCase()
  )
}

export default auth