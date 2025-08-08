# Continue HyperTrader Development - Enhanced Authentication UI (v2)

I'm continuing development of my **HyperTrader** personal trading application. I have a working foundation with modern Nuxt 4 structure and need to build enhanced authentication UI components.

## Current Status ✅
- **Backend**: Hono API with full passkey + TOTP endpoints working (port 3000)
- **Frontend**: Nuxt 4 with modern app/ directory structure (port 3001) 
- **Authentication**: Dev bypass working perfectly, @sidebase/nuxt-auth configured
- **Infrastructure**: Clean startup, zero TypeScript errors, database connected
- **Structure**: Following Nuxt 4 best practices with app/ directory pattern

## Project Structure
```
hyper_trader_ts/
├── frontend/     # Nuxt 4 app (:3001)
│   └── app/      # Modern Nuxt 4 app directory structure
│       ├── pages/index.vue + login.vue (working)
│       ├── composables/useAuth.ts (useAuthCustom with all methods)
│       ├── server/api/auth/[...].ts (NuxtAuthHandler)
│       └── app.vue (custom app wrapper with global styles)
├── backend/      # Hono API (:3000) 
│   ├── src/index.ts + routes/auth.ts (full API)
│   └── All passkey/TOTP endpoints implemented
└── product_knowledge_base.md (complete project documentation)
```

## Tech Stack
- **Frontend**: Nuxt 4, Vue 3, Pinia, @sidebase/nuxt-auth, @simplewebauthn/browser
- **Backend**: Hono, Bun, TypeScript, Neon PostgreSQL, @simplewebauthn/server, otplib
- **Auth**: Passkeys (WebAuthn) + TOTP, currently using in-memory storage

## Available Backend API Endpoints
- `POST /auth/passkey/register/start` & `/finish` - Passkey registration
- `POST /auth/passkey/authenticate/start` & `/finish` - Passkey login  
- `POST /auth/totp/setup` - Generate QR code for TOTP
- `POST /auth/totp/verify-setup` - Verify TOTP during setup
- `POST /auth/totp/verify` - Verify TOTP during login
- `GET /auth/user/:userId` - Get user info and auth methods

## Frontend useAuthCustom() Methods Available
```typescript
const { 
  session, status, signIn, signOut,     // From @sidebase/nuxt-auth
  devLogin,                             // Working dev bypass
  loginWithPasskey,                     // Passkey-only login
  loginWithFull,                        // Passkey + TOTP login  
  setupPasskey,                         // Register new passkey
  setupTOTP,                           // Generate TOTP QR code
  verifyTOTP,                          // Verify TOTP setup
  isDevMode                            // Dev mode flag
} = useAuthCustom()
```

## What I Want to Build Next

I want to create **enhanced authentication UI components** using modern Nuxt 4 structure to utilize the robust backend API:

### Priority 1: User Registration Flow
- **Page**: `app/pages/register.vue` - New user signup with passkey setup
- **Flow**: Username/email → Passkey registration → Success redirect
- **UX**: Step-by-step progress, WebAuthn browser integration

### Priority 2: TOTP Setup Page  
- **Page**: `app/pages/setup-totp.vue` - Add TOTP to existing account
- **Features**: QR code display, manual entry key, verification
- **UX**: Camera-friendly QR code, clear instructions

### Priority 3: Enhanced Login Page
- **Upgrade current**: `app/pages/login.vue` - Multiple auth method selection
- **Options**: Passkey-only vs Passkey+TOTP
- **UX**: Progressive disclosure, clear auth status

### Priority 4: User Dashboard
- **Page**: `app/pages/dashboard.vue` - Post-authentication landing
- **Features**: Auth status, security settings, method management
- **Future**: Trading interface integration point

## Current Working State
- Both servers running error-free on modern Nuxt 4 structure
- Dev bypass authentication working end-to-end
- All API endpoints tested and functional
- Custom app.vue with global styles and proper meta tags
- Following Nuxt 4 best practices with app/ directory

## Request
Please help me build these enhanced authentication UI components, starting with the **user registration flow**. I want to create a polished, step-by-step signup experience that uses passkeys for modern, secure authentication.

Focus on:
1. **Clean, modern UI** with good UX following current design trends
2. **WebAuthn browser integration** using @simplewebauthn/browser
3. **Error handling** and loading states
4. **Progress indication** through the signup flow
5. **Responsive design** that works well on all devices
6. **Proper Nuxt 4 structure** using the app/ directory pattern

Let's start with the user registration page and flow!
