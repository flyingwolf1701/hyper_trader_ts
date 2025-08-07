import postgres from 'postgres'

const sql = postgres(process.env.DATABASE_URL!)

async function testConnection() {
  try {
    const result = await sql`SELECT version()`
    console.log('Database connected successfully!')
    console.log('PostgreSQL version:', result[0].version)
    await sql.end()
  } catch (error) {
    console.error('Database connection failed:', error)
  }
}

testConnection()