/*!
 * Product Page: http://www.creative-tim.com/product/light-bootstrap-dashboard
 * Copyright 2019 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard/blob/master/LICENSE.md)
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 */

import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import Axios from 'axios'
import store from './store'
import vuetify from './plugins/vuetify';
import bootstrap from 'bootstrap-vue'
import jwtDecode from 'jwt-decode'

Vue.use(bootstrap)

// LightBootstrap plugin
import LightBootstrap from './light-bootstrap-main'

// router setup
import routes from './routes/routes'

import './registerServiceWorker'


Vue.prototype.$http = Axios;

const token = localStorage.getItem('access_token');

if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token;
}

// plugin setup
Vue.use(VueRouter)
Vue.use(LightBootstrap)

// configure router
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes, // short for routes: routes
  linkActiveClass: 'nav-item active',
  scrollBehavior: (to) => {
    if (to.hash) {
      return { selector: to.hash }
    } else {
      return { x: 0, y: 0 }
    }
  }
})

router.beforeEach((to, from, next) => { // prevents unauthorzied access to routes
  const loggedIn = localStorage.getItem('access_token')

  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login') // if user is not logged in then return to login route
  }
  next() // continue with route

})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  bootstrap,
  vuetify,

  created () {
    const access_token = localStorage.getItem('access_token')

    if (access_token) {
      this.$store.commit('SET_USER_DATA', access_token)
    }
    Axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response.status === 401) {
          this.$store.dispatch('logout')
        }
        return Promise.reject(error)
      }
    )
  }
})
