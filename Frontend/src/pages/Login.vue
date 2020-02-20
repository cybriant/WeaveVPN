<template>
  <div class="login-form">
    <form class="login" @submit.prevent="login">
      <div class="avatar">
        <i class="material-icons">&#xE7FF;</i>
      </div>
      <h4 class="modal-title">Login to Your Account</h4>
      <div class="form-group">
        <input
          v-model="email"
          id="email"
          type="email"
          name="email"
          class="form-control"
          placeholder="Email"
          required
        />
      </div>
      <div class="form-group">
        <input
          v-model="password"
          id="password"
          type="password"
          name="password"
          class="form-control"
          placeholder="Password"
          required
        />
      </div>
      <div class="form-group small clearfix">
        <label class="checkbox-inline">
          <input type="checkbox" /> Remember me
        </label>
        <a href="forgotPassword.php" class="forgot-link">Forgot Password?</a>
      </div>
      <button type="submit" class="btn btn-primary btn-block btn-lg">
        <b-spinner style="height: 20px; width: 20px;" v-if="loading"></b-spinner>
        Login
      </button>
    </form>
    <div class="text-center small">
      Don't have an account?
      <router-link to="/register">Sign up</router-link>
    </div>
    <p style="color: red;">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
      loading: false
    };
  },
  methods: {
    login: function() {
      this.loading = true
      let email = this.email;
      let password = this.password;
      this.$store
        .dispatch("login", {
          email,
          password
        })
        .then(() => this.$router.push({ name: "Dashboard" }))
        .catch(err => {
          this.error = err.response.data.error;
        });
    }
  }
};
</script>

<style scoped>
body {
  color: #999;
  background: #f5f5f5;
  font-family: "Varela Round", sans-serif;
}

.form-control {
  box-shadow: none;
  border-color: #ddd;
}

.form-control:focus {
  border-color: #4f7bcc;
}

.login-form {
  width: 350px;
  margin: 0 auto;
  padding: 30px 0;
}

.login-form form {
  color: #434343;
  border-radius: 1px;
  margin-bottom: 15px;
  background: #fff;
  border: 1px solid #f3f3f3;
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  padding: 30px;
}

.login-form h4 {
  text-align: center;
  font-size: 22px;
  margin-bottom: 20px;
}

.login-form .avatar {
  color: #fff;
  margin: 0 auto 30px;
  text-align: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  z-index: 9;
  background: #3f72af;
  padding: 15px;
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.1);
}

.login-form .avatar i {
  font-size: 62px;
}

.login-form .form-group {
  margin-bottom: 20px;
}

.login-form .form-control,
.login-form .btn {
  min-height: 40px;
  border-radius: 2px;
  transition: all 0.5s;
}

.login-form .close {
  position: absolute;
  top: 15px;
  right: 15px;
}

.login-form .btn {
  background: #3f72af;
  border: none;
  line-height: normal;
}

.login-form .btn:hover,
.login-form .btn:focus {
  background: rgb(65, 145, 199);
}

.login-form .checkbox-inline {
  float: left;
}

.login-form input[type="checkbox"] {
  margin-top: 2px;
}

.login-form .forgot-link {
  float: right;
}

.login-form .small {
  font-size: 13px;
}

.login-form a {
  color: #3f72af;
}

.login-form .btn-primary {
  color: white;
}

label {
  font-weight: normal !important;
}
</style>