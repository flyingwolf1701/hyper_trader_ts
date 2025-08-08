Tech Stack Setup: I'm building a personal trading application with this current tech stack:
* Frontend: Nuxt 4, Vue 3 Composition API, Pinia, CSS + SCSS
* Backend: Hono API framework with Bun runtime, TypeScript
* Database: Neon PostgreSQL (free tier), using postgres npm package
* Package Manager: Bun
* Trading API: hyperliquid (nomeida's TypeScript SDK) - not yet integrated
* Planned Auth: @sidebase/nuxt-auth with passkeys + TOTP support
Project Structure:

hyper_trader_ts/
├── frontend/     # Nuxt 4 app (runs on :3001)
├── backend/      # Hono API (runs on :3000) 
├── docs/
└── .gitignore
Current Status: 
✅ Basic setup complete - both frontend and backend running 
✅ Database connected (health endpoint working at :3000/health) 
✅ Git repo created and pushed to GitHub (public) 
✅ All basic infrastructure tested and working
Next Steps Discussion: I want to implement authentication with a dev flag (so I can skip auth during development but enable it for production). Specifically looking for @sidebase/nuxt-auth with passkeys and Google Authenticator TOTP support.
Context: This is a personal trading app, will start local-only for development, eventually deploy to managed hosting. Security is important since it handles financial data, but I want development flexibility.