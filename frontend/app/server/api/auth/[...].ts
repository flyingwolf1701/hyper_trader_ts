import { NuxtAuthHandler } from '#auth'

export default NuxtAuthHandler({
  secret: 'dev-secret-for-testing',
  
  providers: [
    {
      id: 'dev-bypass',
      name: 'Dev',
      type: 'credentials',
      credentials: {},
      authorize() {
        return {
          id: '1',
          name: 'Dev User',
          email: 'dev@test.com'
        }
      }
    }
  ],
  
  session: {
    strategy: 'jwt'
  }
})
