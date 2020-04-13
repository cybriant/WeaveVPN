<template>
  <card>
    <h4 slot="header" class="card-title">Edit Profile</h4>
    <form>
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
          <base-input
            type="text"
            label="Last Name"
            placeholder="Last Name"
            v-model="user.last_name"
          ></base-input>
        </div>
      </div>

      <div class="row">
        <div class="col-md-12">
          <base-input type="email" label="Email" placeholder="Email" v-model="user.email"></base-input>
        </div>
      </div>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="updateProfile">Update Profile</v-btn>
      </v-card-actions>
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
      this.$http
        .put("http://127.0.0.1:5000/update-profile/" + this.user.id, {
          first_name: this.user.first_name,
          last_name: this.user.last_name,
          email: this.user.email
        })
        .then(({ data }) => {
          this.$notify({
            group: "foo",
            title: "Success!",
            text: "Profile has been successfully updated!",
            type: "success"
          });
        })
        .catch(err => {
          this.$notify({
            group: "foo",
            title: "Error",
            text: err.response.data.msg,
            type: "error"
          });
        });
    }
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
<style>
</style>
