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

// Schemas for validation
const RegisterStartSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email()
})

const AuthenticateStartSchema = z.object({
  username: z.string().min(3).max(50)
})

const TotpSetupSchema = z.object({
  userId: z.string()
})

const TotpVerifySchema = z.object({
  userId: z.string(),
  token: z.string().length(6)
})

// In-memory storage for demo (replace with database in production)
const users = new Map()
const challenges = new Map()
const credentials = new Map()
const totpSecrets = new Map()

// Dev mode bypass
auth.get('/dev-login', async (c) => {
  if (process.env.DEV_MODE !== 'true') {
    return c.json({ error: 'Dev mode disabled' }, 403)
  }
  
  return c.json({
    success: true,
    user: {
      id: 'dev-user-123',
      username: 'developer',
      email: 'dev@localhost',
      isAuthenticated: true,
      authMethods: ['dev-bypass']
    }
  })
})

// Start passkey registration
auth.post('/passkey/register/start', async (c) => {
  try {
    const body = await c.req.json()
    const { username, email } = RegisterStartSchema.parse(body)
    
    // Check if user already exists
    const existingUser = Array.from(users.values()).find(u => u.username === username)
    if (existingUser) {
      return c.json({ error: 'Username already exists' }, 400)
    }
    
    const userId = `user-${Date.now()}-${Math.random().toString(36).substring(2)}`
    
    const options = await generateRegistrationOptions({
      rpName: 'HyperTrader',
      rpID: process.env.NODE_ENV === 'production' ? 'yourdomain.com' : 'localhost',
      userID: new TextEncoder().encode(userId),
      userName: username,
      userDisplayName: email,
      attestationType: 'none',
      authenticatorSelection: {
        residentKey: 'preferred',
        userVerification: 'preferred',
        authenticatorAttachment: 'platform',
      },
      supportedAlgorithmIDs: [-7, -257], // ES256, RS256
    })

    // Store user and challenge
    users.set(userId, { id: userId, username, email, verified: false })
    challenges.set(userId, options.challenge)
    
    return c.json({ 
      options, 
      userId,
      message: 'Registration started successfully' 
    })
  } catch (error) {
    console.error('Registration start error:', error)
    return c.json({ error: 'Registration failed' }, 400)
  }
})

// Finish passkey registration
auth.post('/passkey/register/finish', async (c) => {
  try {
    const body = await c.req.json()
    const { userId, credential } = body
    
    const user = users.get(userId)
    const expectedChallenge = challenges.get(userId)
    
    if (!user || !expectedChallenge) {
      return c.json({ error: 'Invalid registration session' }, 400)
    }
    
    const verification = await verifyRegistrationResponse({
      response: credential,
      expectedChallenge,
      expectedOrigin: 'http://localhost:3001',
      expectedRPID: 'localhost',
    })
    
    if (verification.verified && verification.registrationInfo) {
      // Store the credential - Fixed property names
      credentials.set(userId, {
        credentialID: verification.registrationInfo.credential.id,
        credentialPublicKey: verification.registrationInfo.credential.publicKey,
        counter: verification.registrationInfo.credential.counter,
      })
      
      // Mark user as verified
      user.verified = true
      users.set(userId, user)
      
      // Clean up challenge
      challenges.delete(userId)
      
      return c.json({ 
        success: true, 
        userId,
        message: 'Passkey registered successfully!' 
      })
    } else {
      return c.json({ error: 'Failed to verify passkey' }, 400)
    }
  } catch (error) {
    console.error('Registration finish error:', error)
    return c.json({ error: 'Registration verification failed' }, 400)
  }
})

// Start passkey authentication
auth.post('/passkey/authenticate/start', async (c) => {
  try {
    const body = await c.req.json()
    const { username } = AuthenticateStartSchema.parse(body)
    
    // Find user
    const user = Array.from(users.values()).find(u => u.username === username)
    if (!user || !user.verified) {
      return c.json({ error: 'User not found or not verified' }, 404)
    }
    
    const credential = credentials.get(user.id)
    if (!credential) {
      return c.json({ error: 'No passkey found for user' }, 404)
    }
    
    const options = await generateAuthenticationOptions({
      rpID: 'localhost',
      allowCredentials: [{
        id: credential.credentialID,
        // Remove 'type' property - it's not needed here
      }],
      userVerification: 'preferred',
    })
    
    // Store challenge for verification
    challenges.set(user.id, options.challenge)
    
    return c.json({ options, userId: user.id })
  } catch (error) {
    console.error('Authentication start error:', error)
    return c.json({ error: 'Authentication failed' }, 400)
  }
})

// Finish passkey authentication
auth.post('/passkey/authenticate/finish', async (c) => {
  try {
    const body = await c.req.json()
    const { userId, credential } = body
    
    const user = users.get(userId)
    const expectedChallenge = challenges.get(userId)
    const storedCredential = credentials.get(userId)
    
    if (!user || !expectedChallenge || !storedCredential) {
      return c.json({ error: 'Invalid authentication session' }, 400)
    }
    
    const verification = await verifyAuthenticationResponse({
      response: credential,
      expectedChallenge,
      expectedOrigin: 'http://localhost:3001',
      expectedRPID: 'localhost',
      // Fix: Use 'credential' instead of 'authenticator'
      credential: {
        id: storedCredential.credentialID,
        publicKey: storedCredential.credentialPublicKey,
        counter: storedCredential.counter,
      },
    })
    
    if (verification.verified) {
      // Update counter
      storedCredential.counter = verification.authenticationInfo.newCounter
      credentials.set(userId, storedCredential)
      
      // Clean up challenge
      challenges.delete(userId)
      
      return c.json({
        success: true,
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
          authMethods: ['passkey']
        }
      })
    } else {
      return c.json({ error: 'Failed to verify passkey' }, 400)
    }
  } catch (error) {
    console.error('Authentication finish error:', error)
    return c.json({ error: 'Authentication verification failed' }, 400)
  }
})

// Setup TOTP
auth.post('/totp/setup', async (c) => {
  try {
    const body = await c.req.json()
    const { userId } = TotpSetupSchema.parse(body)
    
    const user = users.get(userId)
    if (!user) {
      return c.json({ error: 'User not found' }, 404)
    }
    
    const secret = authenticator.generateSecret()
    const serviceName = 'HyperTrader'
    const accountName = user.username
    
    const otpauth = authenticator.keyuri(accountName, serviceName, secret)
    const qrCode = await QRCode.toDataURL(otpauth)
    
    // Store secret temporarily (user needs to verify before we save it)
    totpSecrets.set(`${userId}-pending`, secret)
    
    return c.json({
      secret,
      qrCode,
      serviceName,
      accountName,
      manualEntryKey: secret
    })
  } catch (error) {
    console.error('TOTP setup error:', error)
    return c.json({ error: 'TOTP setup failed' }, 400)
  }
})

// Verify and enable TOTP
auth.post('/totp/verify-setup', async (c) => {
  try {
    const body = await c.req.json()
    const { userId, token } = TotpVerifySchema.parse(body)
    
    const pendingSecret = totpSecrets.get(`${userId}-pending`)
    if (!pendingSecret) {
      return c.json({ error: 'No pending TOTP setup found' }, 404)
    }
    
    // Simple verification without extra options
    const isValid = authenticator.check(token, pendingSecret)
    
    if (isValid) {
      // Move from pending to active
      totpSecrets.set(userId, pendingSecret)
      totpSecrets.delete(`${userId}-pending`)
      
      return c.json({ 
        success: true, 
        message: 'TOTP enabled successfully!' 
      })
    } else {
      return c.json({ error: 'Invalid TOTP code' }, 400)
    }
  } catch (error) {
    console.error('TOTP verification error:', error)
    return c.json({ error: 'TOTP verification failed' }, 400)
  }
})

// Verify TOTP during login
auth.post('/totp/verify', async (c) => {
  try {
    const body = await c.req.json()
    const { userId, token } = TotpVerifySchema.parse(body)
    
    const secret = totpSecrets.get(userId)
    if (!secret) {
      return c.json({ error: 'TOTP not enabled for this user' }, 404)
    }
    
    // Simple verification without extra options
    const isValid = authenticator.check(token, secret)
    
    return c.json({ valid: isValid })
  } catch (error) {
    console.error('TOTP login verification error:', error)
    return c.json({ error: 'TOTP verification failed' }, 400)
  }
})

// Get user info
auth.get('/user/:userId', async (c) => {
  try {
    const userId = c.req.param('userId')
    const user = users.get(userId)
    
    if (!user) {
      return c.json({ error: 'User not found' }, 404)
    }
    
    const hasPasskey = credentials.has(userId)
    const hasTOTP = totpSecrets.has(userId)
    
    return c.json({
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        verified: user.verified,
        authMethods: {
          passkey: hasPasskey,
          totp: hasTOTP
        }
      }
    })
  } catch (error) {
    return c.json({ error: 'Failed to get user info' }, 400)
  }
})

export default auth