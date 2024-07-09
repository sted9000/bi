<template>
  <div class="min-h-screen p-4 bg-white">
    <h1 class="text-3xl font-bold text-blue-600 mb-2">Sign In</h1>
    <div class="inline-block mb-4">
      <input v-model="email" placeholder="Email" class="border mr-2 px-4 py-2 text-md" />
      <input v-model="password" type="password" placeholder="Password" class="border px-4 py-2 text-md mr-2" />
    </div>
    <button @click="login" class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition-colors duration-300">Sign In</button>
  </div>
</template>

<script>
import { signIn } from '../auth';

export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        await signIn(this.email, this.password);
        this.$router.push('/');
      } catch (error) {
        alert(error.message);
      }
    }
  }
};
</script>
