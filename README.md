# HyperTrader TS

Personal trading application with advanced authentication (passkeys + TOTP) and planned HyperLiquid API integration.

## Tech Stack

### Frontend (Nuxt 4)
- **Framework**: Nuxt 4.0.3 with Vue 3 Composition API
- **State Management**: Pinia
- **Styling**: CSS + SCSS
- **Authentication**: @sidebase/nuxt-auth with WebAuthn + TOTP
- **Package Manager**: Bun

### Backend (Hono API)
- **Framework**: Hono with Bun runtime
- **Language**: TypeScript
- **Database**: Neon PostgreSQL (free tier)
- **Authentication**: Passkeys (WebAuthn) + TOTP support

### Authentication Features
- **Passkey Registration**: WebAuthn credential creation
- **Passkey Login**: Secure passwordless authentication
- **TOTP Setup**: QR code generation for authenticator apps
- **Dev Mode**: Development bypass for testing

## Project Structure
```
hyper_trader_ts/
├── frontend/     # Nuxt 4 app (port 3001)
│   └── app/      # Modern Nuxt 4 app directory structure
├── backend/      # Hono API (port 3000)
├── docs/
└── .gitignore
```

## Development

### Prerequisites
- Bun installed
- Neon PostgreSQL database set up

### Backend
```bash
cd backend
bun install
bun run dev  # http://localhost:3000
```

### Frontend
```bash
cd frontend
bun install
bun run dev  # http://localhost:3001
```

### Environment Setup
Create `.env` files in both frontend and backend directories:

**backend/.env:**
```env
DATABASE_URL=your-neon-postgres-url
DEV_MODE=true
ALLOWED_ORIGINS=http://localhost:3001
```

**frontend/.env:**
```env
NUXT_AUTH_SECRET=your-secret-key
NUXT_PUBLIC_DEV_MODE=true
NUXT_PUBLIC_API_BASE=http://localhost:3000
```

## Current Features ✅

### Authentication API (Backend)
- ✅ Dev bypass authentication
- ✅ Passkey registration flow
- ✅ Passkey authentication flow
- ✅ TOTP setup with QR codes
- ✅ TOTP verification
- ✅ User management

### Frontend Interface
- ✅ Welcome page
- ✅ Login page with dev bypass
- ✅ Authentication status display
- ✅ Error-free TypeScript setup
- ✅ Modern Nuxt 4 app/ directory structure

## Planned Features 🚧

### Enhanced Frontend
- [ ] User registration page
- [ ] TOTP setup interface
- [ ] User dashboard
- [ ] Enhanced login flow

### Trading Features
- [ ] HyperLiquid API integration
- [ ] Trading interface
- [ ] Portfolio tracking
- [ ] Real-time data

### Production Ready
- [ ] Database schemas
- [ ] Session persistence
- [ ] Rate limiting
- [ ] Deployment configuration

## API Endpoints

### Authentication
- `GET /auth/dev-login` - Development bypass
- `POST /auth/passkey/register/start` - Start passkey registration
- `POST /auth/passkey/register/finish` - Complete passkey registration
- `POST /auth/passkey/authenticate/start` - Start passkey login
- `POST /auth/passkey/authenticate/finish` - Complete passkey login
- `POST /auth/totp/setup` - Generate TOTP QR code
- `POST /auth/totp/verify-setup` - Verify TOTP setup
- `POST /auth/totp/verify` - Verify TOTP during login
- `GET /auth/user/:userId` - Get user information

### Health
- `GET /health` - Database connection status

## Security Features

- **Passkeys**: Modern WebAuthn-based authentication
- **TOTP**: Time-based one-time passwords (Google Authenticator compatible)
- **CORS**: Properly configured cross-origin requests
- **JWT**: Secure session management
- **Dev Mode**: Safe development authentication bypass

## License

Private project for personal use.
