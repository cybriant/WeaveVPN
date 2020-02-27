<template>
  <card>
    <h4 slot="header" class="card-title">Edit Profile</h4>
    <form>
      <div class="row">
        <div class="col-md-12">
          <base-input
            type="text"
            label="Company"
            :disabled="true"
            placeholder="Light dashboard"
            v-model="user.company"
          ></base-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <base-input
            type="text"
            label="First Name"
            placeholder="First Name"
            v-model="user.first_name"
          ></base-input>
        </div>
        <div class="col-md-6">
          <base-input type="text" label="Last Name" placeholder="Last Name" v-model="user.last_name"></base-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-12">
          <base-input type="email" label="Email" placeholder="Email" v-model="user.email"></base-input>
        </div>
      </div>

      <div class="text-center">
        <button
          type="submit"
          class="btn btn-info btn-fill float-right"
          @click.prevent="updateProfile"
        >Update Profile</button>
      </div>
      <div class="clearfix"></div>
    </form>
  </card>
</template>
<script>
import Card from "src/components/Cards/Card.vue";

export default {
  components: {
    Card
  },
  methods: {
    updateProfile() {
      alert("Your data: " + JSON.stringify(this.user));
    }
  },
  computed: {
      user () {
        return this.$store.state.user
      }
    }
};
</script>
<style>
</style>
