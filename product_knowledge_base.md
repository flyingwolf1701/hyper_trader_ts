# HyperTrader Project Knowledge Base

## Project Overview
**HyperTrader** - Personal trading application with advanced authentication (passkeys + TOTP) and eventual HyperLiquid API integration.

## Current Tech Stack

### Frontend (Nuxt 4)
- **Framework**: Nuxt 4.0.3 with Vue 3 Composition API
- **State Management**: Pinia
- **Styling**: CSS + SCSS
- **Authentication**: @sidebase/nuxt-auth with custom providers
- **Package Manager**: Bun
- **Port**: 3001

### Backend (Hono API)
- **Framework**: Hono with Bun runtime
- **Language**: TypeScript
- **Database**: Neon PostgreSQL (free tier) using `postgres` npm package
- **Port**: 3000

### Authentication Libraries
- **Frontend**: @simplewebauthn/browser, otplib, qrcode
- **Backend**: @simplewebauthn/server, otplib, qrcode

## Project Structure
```
hyper_trader_ts/
├── frontend/     # Nuxt 4 app (runs on :3001)
│   └── app/      # Modern Nuxt 4 app directory structure
│       ├── pages/
│       │   ├── index.vue       # Welcome page with "Go to Login" button
│       │   └── login.vue       # Auth page with dev bypass + debug info
│       ├── composables/
│       │   └── useAuth.ts      # useAuthCustom() with passkey/TOTP methods
│       ├── server/api/auth/
│       │   └── [...].ts        # NuxtAuthHandler with dev-bypass provider
│       └── app.vue             # Root app component with global styles
├── backend/      # Hono API (runs on :3000)
│   ├── src/
│   │   ├── index.ts        # Main Hono app with /health endpoint
│   │   └── routes/
│   │       └── auth.ts     # Full passkey + TOTP endpoints
│   └── package.json        # All auth dependencies installed
├── docs/
├── README.md
├── product_knowledge_base.md
└── .gitignore
```

## What's Implemented ✅

### Backend Authentication API
- **Dev bypass**: `GET /auth/dev-login` - Working
- **Passkey registration**: `POST /auth/passkey/register/start` & `/finish` - Complete
- **Passkey authentication**: `POST /auth/passkey/authenticate/start` & `/finish` - Complete  
- **TOTP setup**: `POST /auth/totp/setup` - QR code generation working
- **TOTP verification**: `POST /auth/totp/verify-setup` & `/verify` - Complete
- **User info**: `GET /auth/user/:userId` - Complete
- **In-memory storage**: Users, credentials, challenges, TOTP secrets

### Frontend Core
- **Working pages**: Home page, login page with debug info
- **Authentication flow**: Dev bypass working perfectly
- **Auth composable**: `useAuthCustom()` with all methods typed
- **app.vue**: Custom app wrapper with global styles and meta tags
- **Zero TypeScript errors**: All type issues resolved
- **Modern structure**: Using Nuxt 4 app/ directory pattern

### Infrastructure
- **Database**: Neon PostgreSQL connected successfully
- **CORS**: Properly configured between frontend/backend
- **Environment**: All .env files set up correctly
- **Error-free startup**: Both servers start cleanly

## What's NOT Implemented Yet ❌

### Frontend UI Components
- [ ] User registration page (signup flow)
- [ ] TOTP setup page with QR code display
- [ ] Enhanced login with multiple auth methods
- [ ] User dashboard/profile page
- [ ] Authentication middleware (disabled temporarily)

### Advanced Features
- [ ] HyperLiquid API integration
- [ ] Trading interface
- [ ] Portfolio tracking
- [ ] Database schemas (using in-memory storage currently)
- [ ] Session persistence
- [ ] Production deployment config

### Security Enhancements
- [ ] Real challenge storage (currently in-memory)
- [ ] Rate limiting
- [ ] CSRF protection
- [ ] Backup codes for TOTP

## Important Notes

### Authentication Flow
1. **Dev Mode**: Currently enabled for easy testing
2. **Auth Handler**: Minimal working version at `app/server/api/auth/[...].ts`
3. **Providers**: Only `dev-bypass` provider configured
4. **Session Strategy**: JWT-based

### Database
- Connected to Neon PostgreSQL but only using basic health checks
- All auth data stored in-memory Maps (not persistent)
- Ready for database schema implementation

### File Naming & Structure
- **Auth handler**: Must be `[...].ts` (with literal square brackets)
- **PowerShell tip**: Use `Get-Content -LiteralPath '[...].ts'` to read the file
- **Modern Nuxt 4**: Using app/ directory structure (best practice)

### Known Working Endpoints
- `http://localhost:3000/health` - Database health check
- `http://localhost:3000/auth/dev-login` - Dev authentication
- `http://localhost:3001/` - Frontend welcome page
- `http://localhost:3001/login` - Login page with working dev bypass

## Current State Summary
- ✅ **Infrastructure**: Solid foundation with clean startup
- ✅ **Modern Structure**: Following Nuxt 4 best practices with app/ directory
- ✅ **Basic Auth**: Dev bypass working end-to-end  
- ✅ **API**: Full passkey + TOTP backend ready
- ❌ **UI**: Need enhanced frontend components
- ❌ **Production**: Still in development mode

The project is at the perfect point to build enhanced frontend authentication components that utilize the robust backend API we've created.
