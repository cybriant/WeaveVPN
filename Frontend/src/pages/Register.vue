<template>
  <div class="register-form">
    <form class="login" @submit.prevent="register">
      <h4 class="modal-title">Sign up to Create Account</h4>
      <div class="form-group">
        <label for="firstName">First Name:</label>
        <input v-model="first_name" type="text" name="first_name" class="form-control" id="firstName" value required/>
      </div>

      <div class="form-group">
        <label for="lastName">Last Name:</label>
        <input v-model="last_name" type="text" name="last_name" class="form-control" id="lastName" value required/>
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="email" type="email" class="form-control" name="email" value required/>
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" type="password" name="password" class="form-control" value required/>
      </div>

      <div class="form-group">
        <button type="submit" class="btn btn-primary btn-block btn-lg">Register</button>
      </div>
      <div class="form-group">
        <p>
          Already have an account?
          <router-link to="/login">Login</router-link>
        </p>
      </div>
    </form>

    <ul>
      <li v-for="(error, index) in error" :key="index" style="color: red;">{{ error }}</li>
    </ul>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid';
export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      error: ""
    };
  },
  methods: {
    register() {
      this.$store
        .dispatch("register", {
          id: uuidv4(),
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          password: this.password
        })
        .then(() => {
          this.$router.push({ name: "Dashboard" });
        })
        .catch(err => {
          console.log('error')
          this.error = err.response.data;
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

.register-form {
  width: 350px;
  margin: 0 auto;
  padding: 30px 0;
}

.register-form form {
  color: #434343;
  border-radius: 1px;
  margin-bottom: 15px;
  background: #fff;
  border: 1px solid #f3f3f3;
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  padding: 30px;
}

.register-form h4 {
  text-align: center;
  font-size: 22px;
  margin-bottom: 20px;
}

.register-form .form-group {
  margin-bottom: 20px;
}

.register-form .form-control,
.register-form .btn {
  min-height: 40px;
  border-radius: 2px;
  transition: all 0.5s;
}

.register-form .close {
  position: absolute;
  top: 15px;
  right: 15px;
}

.register-form .btn {
  background: #3f72af;
  border: none;
  line-height: normal;
}

.register-form .btn:hover,
.register-form .btn:focus {
  background: rgb(65, 145, 199);
}

.register-form .checkbox-inline {
  float: left;
}

.register-form input[type="checkbox"] {
  margin-top: 2px;
}

.register-form .forgot-link {
  float: right;
}

.register-form .small {
  font-size: 13px;
}

.register-form a {
  color: #3f72af;
}

.register-form .btn-primary {
  color: white;
}

label {
  font-weight: normal !important;
}
</style>