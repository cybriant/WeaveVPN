<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <card>
            <h4 style="margin-top: 0;">{{ network_name }}</h4>

            <v-tabs>
              <v-tab>Organizations</v-tab>
              <v-tab>Server Groups</v-tab>
              <v-tab>Connections</v-tab>
              <v-tab>Firewall Rules</v-tab>

              <!-- ORGANIZATIONS TAB -->
              <v-tab-item style="margin-top: 1rem;">
                <!-- ORGANIZATIONS MODAL -->
                <v-dialog v-model="organizations_dialog" persistent max-width="600px">
                  <template v-slot:activator="{ on }">
                    <v-btn
                      color="primary"
                      dark
                      v-on="on"
                      style="margin-bottom: 20px;"
                    >Create Organization</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline">Create Organization</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12">
                            <v-text-field label="Organization Name" v-model="organization_item.name" required></v-text-field>
                            <input v-model="organization_item.id" hidden/>
                          </v-col>
                          <v-col cols="12">
                            <v-text-field
                              label="Description"
                              v-model="organization_item.description"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="grey darken-1" text @click="organizations_dialog = false">Cancel</v-btn>
                      <v-btn color="primary" outlined @click="addOrganization">Create</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- END OF ORGANIZATIONS MODAL -->

                <v-data-table
                  :headers="organizations_headers"
                  :items="organizations"
                  :search="search"
                  sort-by="Name"
                  class="elevation-1"
                ></v-data-table>
              </v-tab-item>

              <!-- SERVER GROUPS TAB -->
              <v-tab-item style="margin-top: 1rem;">
                <!-- SERVER GROUP MODAL -->
                <v-dialog v-model="server_groups_dialog" persistent max-width="600px">
                  <template v-slot:activator="{ on }">
                    <v-btn
                      color="primary"
                      dark
                      v-on="on"
                      style="margin-bottom: 20px;"
                    >Create Server Group</v-btn>
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
                            <input v-model="server_group_item.id" hidden/>
                          </v-col>
                          <v-col cols="12" sm="12">
                            <v-text-field
                              label="Organization"
                              v-model="server_group_item.organization"
                              required
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6">
                            <v-text-field
                              label="Lower IP Range"
                              hint="ex 172.24.0.1"
                              v-model="server_group_item.lower_ip_range"
                              required
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6">
                            <v-text-field
                              label="Upper IP Range"
                              hint="ex 172.24.0.254"
                              v-model="server_group_item.upper_ip_range"
                              required
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12">
                            <v-text-field
                              label="Description"
                              v-model="server_group_item.description"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="grey darken-1" text @click="server_groups_dialog = false">Cancel</v-btn>
                      <v-btn color="primary" outlined @click="addServerGroup">Create</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- END OF SERVER GROUP MODAL -->

                <v-data-table
                  :headers="server_group_headers"
                  :items="server_groups"
                  :search="search"
                  sort-by="Name"
                  class="elevation-1"
                ></v-data-table>
              </v-tab-item>

              <!-- CONNECTIONS TAB -->
              <v-tab-item style="margin-top: 1rem;">
                <p>conenction stuff goes here</p>
              </v-tab-item>

              <!-- FIREWALL RULES TAB -->
              <v-tab-item style="margin-top: 1rem;">
                <p>firewall rules stuff goes here</p>
              </v-tab-item>
            </v-tabs>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { v4 as uuidv4 } from 'uuid';
export default {
  components: {},
  data: () => ({
    organizations_dialog: false,
    organization_item: {},
    organizations: [],
    organizations_headers: [
      { text: "Organization Name", value: "name" },
      { text: "Description", value: "description" },
    ],
    server_groups_dialog: false,
    server_group_item: {},
    server_groups: [],
    search: "",
    server_group_headers: [
      { text: "Name", value: "name" },
      { text: "Organization", value: "organization" },
      { text: "Lower IP Range", value: "lower_ip_range" },
      { text: "Upper IP Range", value: "upper_ip_range" },
      { text: "Description", value: "description" }
    ]
  }),
  created() {
    this.getServerGroups();
    this.getOrganizations();
  },
  computed: {
    network_name() {
      return this.$route.query.name;
    }
  },
  methods: {

    getOrganizations() {
      this.$http
        .get("http://127.0.0.1:5000/organization/all/" + this.$route.query.id)
        .then(({ data }) => {
          // Adds the users from the database to the table
          this.organizations = data.organizations;
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
    addOrganization() {
      var uuid = uuidv4();
      this.$http
        .post("http://127.0.0.1:5000/organization/create", {
          id: uuid,
          name: this.organization_item.name,
          description: this.organization_item.description,
          network_id: this.$route.query.id,
        })
        .then(({ data }) => {
          this.organization_item.id = uuid,
          this.organizations.push(this.organization_item); // add server group to table (frontend)
          (this.organizations_dialog = false),
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

    getServerGroups() {
      this.$http
        .get("http://127.0.0.1:5000/server-group/all/" + this.$route.query.id)
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
      var uuid = uuidv4();
      this.$http
        .post("http://127.0.0.1:5000/server-group/create", {
          id: uuid,
          name: this.server_group_item.name,
          organization: this.server_group_item.organization,
          category: this.server_group_item.category,
          lower_ip_range: this.server_group_item.lower_ip_range,
          upper_ip_range: this.server_group_item.upper_ip_range,
          description: this.server_group_item.description,
          network_id: this.$route.query.id,
        })
        .then(({ data }) => {
          this.server_group_item.id = uuid,
          this.server_groups.push(this.server_group_item), // add server group to table (frontend)
          (this.server_groups_dialog = false),
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
    }
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