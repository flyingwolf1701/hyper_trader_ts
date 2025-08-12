# GitHub OAuth Setup Guide

## Quick Setup Instructions

### 1. Create a GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the details:
   - **Application name**: `HyperTrader Local Development`
   - **Homepage URL**: `http://localhost:3001`
   - **Authorization callback URL**: `http://localhost:3001/api/auth/callback/github`
   - **Application description**: `Local development for HyperTrader`

4. Click "Register application"
5. Copy the **Client ID** and **Client Secret**

### 2. Update Environment Variables

1. Open `frontend/.env`
2. Replace the placeholder values:
   ```env
   GITHUB_CLIENT_ID=your_actual_client_id_here
   GITHUB_CLIENT_SECRET=your_actual_client_secret_here
   ```

### 3. Test the Authentication

1. Make sure the development server is running:
   ```bash
   cd frontend
   npm run dev
   ```

2. Go to `http://localhost:3001/login`

3. Try both authentication methods:
   - **Dev Mode**: Click "Skip Auth (Dev Only)" - should work immediately
   - **GitHub OAuth**: Click "Continue with GitHub" - will redirect to GitHub for authorization

### 4. Verify It's Working

- After authentication, you should be redirected to `/dashboard`
- You should see your user information in the header
- The sign-out button should work properly

## Current Status

✅ **Dev Mode Authentication** - Working (bypasses OAuth for testing)  
⚠️ **GitHub OAuth** - Ready (requires GitHub app setup)  
❌ **Google OAuth** - Not implemented yet  
❌ **Discord OAuth** - Not implemented yet  

## Development Notes

- The system is configured for localhost development
- Dev mode bypass is only available when `NUXT_PUBLIC_DEV_MODE=true`
- Session data is stored as JWT tokens
- User information is displayed in the dashboard header

## Next Steps

Once GitHub OAuth is working, you can:
1. Add Google OAuth provider
2. Add Discord OAuth provider  
3. Implement proper user persistence
4. Add role-based access control
5. Connect to your trading backend APIs