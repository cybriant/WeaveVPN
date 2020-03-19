<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <card>
            <h4 style="margin-top: 0;">Network Management</h4>


            <!-- CREATE SERVER GROUP MODAL -->

            <v-dialog v-model="dialog" persistent max-width="600px">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" dark v-on="on" style="margin-bottom: 20px;">Create Server Group</v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">Create Server Group</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field label="Name" v-model="server_group_item.name" required></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field label="Organization" v-model="server_group_item.organization" required></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field label="Category" v-model="server_group_item.category"></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field label="Lower IP Range" hint="ex 192.168.0.1" v-model="server_group_item.lower_ip_range" required></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field label="Upper IP Range" hint="ex 192.168.10.100" v-model="server_group_item.upper_ip_range" required></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field label="Description" v-model="server_group_item.description"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="grey darken-1" text @click="dialog = false">Cancel</v-btn>
                  <v-btn color="primary" outlined @click="addServerGroup">Create</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <!-- END OF SERVER GROUP MODAL --> 

            <v-data-table
              :headers="headers"
              :items="server_groups"
              :search="search"
              sort-by="Name"
              class="elevation-1"
            >
            </v-data-table>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  components: {},
  data: () => ({
    dialog: false,
    server_group_item: {},
    server_groups: [],
    search: "",
    headers: [
      { text: "Name", value: "name" },
      { text: "Organization", value: "organization" },
      { text: "Category", value: "category" },
      { text: "Lower IP Range", value: "lower_ip_range" },
      { text: "Upper IP Range", value: "upper_ip_range" },
      { text: "Description", value: "description" }
    ],

  }),
  created() {
    this.getServerGroups();
  },
  methods: {
    getServerGroups() {
      this.$http
        .get("http://127.0.0.1:5000/network/get-server-groups")
        .then(({ data }) => {
          // Adds the users from the database to the table
          this.server_groups = data.server_groups;
        })
        .catch(err => {
          console.log(err.response.data);
          this.$notify({
            group: "foo",
            title: "Error",
            text: err.response.data,
            type: "error"
          });
        });
    },
    addServerGroup() {
      this.$http
          .post("http://127.0.0.1:5000/network/add-server-group", {
            name: this.server_group_item.name,
            organization: this.server_group_item.organization,
            category: this.server_group_item.category,
            lower_ip_range: this.server_group_item.lower_ip_range,
            upper_ip_range: this.server_group_item.upper_ip_range,
            description: this.server_group_item.description
          })
          .then(({ data }) => {
            this.server_groups.push(this.server_group_item); // add server group to table (frontend)
            this.dialog = false,
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Server group has been successfully created!",
              type: "success"
            });
          })
          .catch(err => {
            this.error = err.response.data;
            this.$notify({
              group: "foo",
              title: "Error",
              text: err.response.data.msg,
              type: "error"
            });
          });
    },

  }
  // mounted () {
  // this.$http
  //   .get('http://127.0.0.1:5000/api/login')
  //   .then(response => (this.info = response.data.email))
  // }
};
</script>
<style>
</style>
