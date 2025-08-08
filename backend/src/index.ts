import { Hono } from "hono";
import postgres from "postgres";

const app = new Hono();
const sql = postgres(process.env.DATABASE_URL!);

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

app.get("/health", async (c) => {
  try {
    const result = await sql`SELECT NOW() as timestamp`;
    return c.json({
      status: "healthy",
      database: "connected",
      timestamp: result[0].timestamp,
    });
  } catch (error) {
    return c.json({ status: "error", error: error.message }, 500);
  }
});

export default app;
