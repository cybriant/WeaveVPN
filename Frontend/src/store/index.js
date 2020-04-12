import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import jwtDecode from 'jwt-decode'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('access_token') || '',
    user: null
  },

  // MUTATIONS - Change the state of a vuex store
  mutations: {

    SET_USER_DATA(state, access_token) {
      var decoded_payload = jwtDecode(access_token)
      console.log(decoded_payload.user_claims)
      state.user = decoded_payload.user_claims // store user data in state
      localStorage.setItem('access_token', access_token) // store user data in local storage
      axios.defaults.headers.common['Authorization'] = `Bearer ${ access_token }` // add token to axios header
    },
    CLEAR_USER_DATA(state) {
      state.user = null // remove user data in store
      state.token = null
      localStorage.removeItem('access_token') // remove user data in local storage
      axios.defaults.headers.common['Authorization'] = null // remove token from axios header

      // or location.reload()
    }
  },

  

  // ACTIONS
  actions: {
    register({ commit }, credentials) {
      return axios
      .post('http://127.0.0.1:5000/register', credentials)
      .then(({ data }) => {
          commit('SET_USER_DATA', data.access_token)
        }
      )
    },
    login({ commit }, credentials) {
      return axios
      .post('http://127.0.0.1:5000/login', credentials)
      .then(({ data }) => {
          commit('SET_USER_DATA', data.access_token)
        }
      )
    },

    logout({commit}) {
      commit('CLEAR_USER_DATA')
    }
  },

  // Getters - Get the value of the vuex state
  getters: {
    isLoggedIn: state => !!state.token, // if user state is null it returns false, otherwise it returns true
    authStatus: state => state.status,
    role: state => state.user.role
  },
  modules: {

  }
})
