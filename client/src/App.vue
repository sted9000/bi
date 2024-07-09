<template>
  <div id="app" class="min-h-screen">
    <nav v-if="$route.path !== '/login'" class="p-4 bg-white">
      <div class="flex justify-between">
        <div>
          <h1 :class="headerClass">{{ name }}</h1>
        </div>
        <div class="flex justify-end gap-2">
          <router-link
              v-if="$route.path === '/'"
              to="/trends"
              class="bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded-md transition-colors duration-300"
          >
            Trends
          </router-link>
          <router-link
              v-if="$route.path === '/trends'"
              to="/"
              class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition-colors duration-300"
          >
            Daily Report
          </router-link>
          <router-link
              v-if="!user"
              to="/login"
              class="bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-md transition-colors duration-300"
          >
            Login
          </router-link>
          <button
              v-if="user"
              @click="signOut"
              class="bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-md transition-colors duration-300"
          >
            Sign Out
          </button>
        </div>
      </div>

    </nav>
    <router-view></router-view>
  </div>
</template>


<script>
import { signOut } from './auth';
import {supabase} from "./supabase";

export default {
  data() {
    return {
      user: null,
    };
  },
  computed: {
    name() {
      // get the name of the route
      return this.$route.name;
    },
    headerClass() {
      // change the header color based on the route
      // base class: text-3xl font-bold
      if (this.$route.path === '/trends') {
        return 'text-3xl font-bold text-purple-600';
      } else {
        return 'text-3xl font-bold text-blue-600';
      }
    },
  },
  methods: {
    async signOut() {
      try {
        await signOut();
        this.$router.push('/login');
      } catch (error) {
        console.error('Error signing out:', error);
      }
    },
  },
  async created() {
    // see if the user is already signed in
    this.user = (await supabase.auth.getSession()).data?.session?.user;

    supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN' || event === 'USER_UPDATED') {
        // handle sign in event or user updated event
        this.user = session.user;
      } else if (event === 'SIGNED_OUT') {
        // handle sign out event
        this.user = null;
      }
    })
  },
};

</script>
