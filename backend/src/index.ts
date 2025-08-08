import { Hono } from 'hono'
import { cors } from 'hono/cors'
import postgres from 'postgres'
import authRoutes from './routes/auth'

const app = new Hono()
const sql = postgres(process.env.DATABASE_URL!)

// CORS middleware
app.use('*', cors({
  origin: ['http://localhost:3001'],
  credentials: true,
}))

app.get('/', (c) => {
  return c.text('Hello Hono!')
})

app.get('/health', async (c) => {
  try {
    const result = await sql`SELECT NOW() as timestamp`
    return c.json({ 
      status: 'healthy', 
      database: 'connected',
      timestamp: result[0].timestamp 
    })
  } catch (error) {
    // Fix the error type issue
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    return c.json({ status: 'error', error: errorMessage }, 500)
  }
})

// Mount auth routes
app.route('/auth', authRoutes)

export default app