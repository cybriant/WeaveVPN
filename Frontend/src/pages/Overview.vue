<template>
  <div class="content">
    <div class="container-fluid">
      <h4>Welcome, {{ user.first_name }}!</h4>

      <div class="row">
        <div class="col-md-12">
          <card>
            <div class="row" style="text-align: center;">
              <!-- Grid column -->
              <div class="col-md-4">
                <i class="fas fa-network-wired fa-3x" style="color: #FF4A55;"></i>
                <h5 class="font-weight-bold my-4">Network Management</h5>
                <p class="grey-text">Setup and configure Software Defined Networks</p>
                <div class="text-center">
                  <router-link :to="'/admin/network-management'" style="color: white;">
                    <v-btn rounded color="primary" dark>
                      Manage Networks
                    </v-btn>
                  </router-link>
                </div>
              </div>
              <!-- Grid column -->

              <!-- Grid column -->
              <div class="col-md-4">
                <i class="fas fa-users fa-3x" style="color: #87CB16"></i>
                <h5 class="font-weight-bold my-4">User Management</h5>
                <p class="grey-text">Create, update, or delete users</p>
                <div class="text-center">
                  <router-link :to="'/admin/user-management'" style="color: white;">
                    <v-btn rounded color="primary" dark>
                      Manage Users
                    </v-btn>
                  </router-link>
                </div>
              </div>
              <!-- Grid column -->

              <!-- Grid column -->
              <div class="col-md-4">
                <i class="fas fa-book fa-3x" style="color: #1D62F0;"></i>
                <h5 class="font-weight-bold my-4">REST API Documentation</h5>
                <p class="grey-text">View and test API endpoints</p>
                <div class="text-center">
                  <a href="http://127.0.0.1:5000/" style="color: white;" target="_blank">
                    <v-btn rounded color="primary" dark>
                      View Documentation
                    </v-btn>
                  </a>
                </div>
              </div>
            </div>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import ChartCard from "src/components/Cards/ChartCard.vue";
import StatsCard from "src/components/Cards/StatsCard.vue";
import LTable from "src/components/Table.vue";

export default {
  components: {
    LTable,
    ChartCard,
    StatsCard
  },
  data() {
    return {
      user_list_size: "",
      network_list_size: "",
      info: null,
      editTooltip: "Edit Task",
      deleteTooltip: "Remove",
    };
  },
  mounted() {
    
  },

  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>