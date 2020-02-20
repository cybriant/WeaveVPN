import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: null
  },

  // MUTATIONS - Change the state of a vuex store
  mutations: {

    SET_USER_DATA(state, userData) {
      state.user = userData // store user data in state
      localStorage.setItem('user', JSON.stringify(userData)) // store user data in local storage
      axios.defaults.headers.common['Authorization'] = `Bearer ${ userData.token }` // add token to axios header
    },
    CLEAR_USER_DATA(state) {
      state.user = null // remove user data in store
      state.token = null
      localStorage.removeItem('user') // remove user data in local storage
      axios.defaults.headers.common['Authorization'] = null // remove token from axios header

      // or location.reload()
    }
  },

  // ACTIONS
  actions: {
    register({ commit }, credentials) {
      return axios
      .post('http://0.0.0.0:3000/register', credentials)
      .then(({ data }) => {
          commit('SET_USER_DATA', data)
        }
      )
    },
    login({ commit }, credentials) {
      return axios
      .post('http://127.0.0.1:5000/api/loginpost', credentials)
      .then(({ data }) => {
          commit('SET_USER_DATA', data)
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
  },
  modules: {

  }
})
