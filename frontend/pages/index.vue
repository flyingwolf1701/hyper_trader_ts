<template>
  <div class="welcome-container">
    <h1>HyperTrader</h1>
    <p>Welcome to your trading application</p>
    <div class="nav-links">
      <NuxtLink to="/login" class="btn">Go to Login</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: #f9fafb;
}

h1 {
  color: #1f2937;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

p {
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

.btn {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}
</style>