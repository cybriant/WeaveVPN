<template>
  <div :class="{'nav-open': $sidebar.showSidebar}">
    <notifications group="foo" position="bottom right"></notifications>
    <v-app>
      <router-view></router-view>
    </v-app>
  </div>
</template>

<script>
  export default {
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn
    }
  },
  methods: {
    logout: function() {
      this.$store.dispatch('logout')
      .then(() => {
        this.$router.push('/login')
      })
    }
  },
  created: function() {
    this.$http.interceptors.response.use(undefined, function(error) {
      return new Promise(function() {
        if(error.status === 401 && error.config && !error.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw error;
      });
    });
  }
}
</script>
