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
                <v-row no-gutters style="padding-top: 10px; padding-bottom: 20px;">
                  <v-dialog v-model="organizations_dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark class="mb-2" v-on="on">
                        <v-icon>mdi-plus</v-icon>Create Organization
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">{{ formOrgTitle }}</span>
                      </v-card-title>

                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-text-field
                                label="Organization Name"
                                v-model="organization_item.name"
                                required
                              ></v-text-field>
                              <input v-model="organization_item.id" hidden />
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
                        <v-btn color="grey darken-1" text @click="closeOrgDialog()">Cancel</v-btn>
                        <v-btn color="primary" outlined @click="saveOrg()">{{ submitOrgBtn }}</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <!-- END OF ORGANIZATIONS MODAL -->

                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>

                  <v-text-field
                    style="clear: both;"
                    v-model="organizations_search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-row>

                <v-data-table
                  :headers="organizations_headers"
                  :items="organizations"
                  :search="organizations_search"
                  sort-by="Name"
                  class="elevation-1"
                >
                  <template v-slot:item.action="{ item }">
                    <v-icon class="mr-2" @click="editOrgItem(item)" title="Edit Network">edit</v-icon>
                    <v-icon @click="deleteOrgItem(item)" title="Delete Network">delete</v-icon>
                  </template>
                </v-data-table>
              </v-tab-item>

              <!-- SERVER GROUPS TAB -->
              <v-tab-item style="margin-top: 1rem;">
                <v-row no-gutters style="padding-top: 10px; padding-bottom: 20px;">
                  <!-- SERVER GROUP MODAL -->
                  <v-dialog v-model="server_groups_dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark class="mb-2" v-on="on">
                        <v-icon>mdi-plus</v-icon>Create Server Group
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">{{ formServerGroupTitle }}</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-text-field label="Name" v-model="server_group_item.name" required></v-text-field>
                              <input v-model="server_group_item.id" hidden />
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
                        <v-btn color="grey darken-1" text @click="closeServerGroupDialog()">Cancel</v-btn>
                        <v-btn color="primary" outlined @click="saveServerGroup()">{{ submitServerGroupBtn }}</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <!-- END OF SERVER GROUP MODAL -->

                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>

                  <v-text-field
                    style="clear: both;"
                    v-model="server_group_search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-row>

                <v-data-table
                  :headers="server_group_headers"
                  :items="server_groups"
                  :search="server_group_search"
                  sort-by="Name"
                  class="elevation-1"
                >
                  <template v-slot:item.action="{ item }">
                    <v-icon class="mr-2" @click="editServerGroupItem(item)" title="Edit Server Group">edit</v-icon>
                    <v-icon @click="deleteServerGroupItem(item)" title="Delete Server Group">delete</v-icon>
                  </template>
                </v-data-table>
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
import { v4 as uuidv4 } from "uuid";
export default {
  components: {},
  data: () => ({
    // Organization data
    editedOrgIndex: -1,
    defaultOrgItem: {},
    organizations_dialog: false,
    organization_item: {},
    organizations: [],
    organizations_search: "",
    organizations_headers: [
      { text: "Organization Name", value: "name" },
      { text: "Description", value: "description" },
      { text: "Actions", value: "action", sortable: false }
    ],

    // Server group data
    editedServerGroupIndex: -1,
    defaultServerGroupItem: {},
    server_groups_dialog: false,
    server_group_item: {},
    server_groups: [],
    server_group_search: "",
    server_group_headers: [
      { text: "Name", value: "name" },
      { text: "Organization", value: "organization" },
      { text: "Lower IP Range", value: "lower_ip_range" },
      { text: "Upper IP Range", value: "upper_ip_range" },
      { text: "Description", value: "description" },
      { text: "Actions", value: "action", sortable: false }
    ]
  }),

  created() {
    this.getServerGroups();
    this.getOrganizations();
  },
  computed: {
    network_name() {
      return this.$route.query.name;
    },

    formOrgTitle() {
      return this.editedOrgIndex === -1
        ? "Add New Organization"
        : "Edit Organization";
    },
    submitOrgBtn() {
      return this.editedOrgIndex === -1 ? "Add" : "Update";
    },

    formServerGroupTitle() {
      return this.editedServerGroupIndex === -1
        ? "Create Server Group"
        : "Edit Server Group";
    },
    submitServerGroupBtn() {
      return this.editedServerGroupIndex === -1 ? "Create" : "Update";
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

    editOrgItem(item) {
      this.editedOrgIndex = this.organizations.indexOf(item);
      this.organization_item = Object.assign({}, item);
      this.organizations_dialog = true;
    },

    deleteOrgItem(item) {
      const index = this.organizations.indexOf(item); // gets index of user in table

      confirm("Are you sure you want to delete this organization?") &&
        this.$http
          .delete("http://127.0.0.1:5000/organization/delete/" + item.id)
          .then(({ data }) => {
            this.organizations.splice(index, 1); // remove user from table
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Organization has been successfully deleted!",
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
    },

    closeOrgDialog() {
      this.organizations_dialog = false;
      setTimeout(() => {
        this.organization_item = Object.assign({}, this.defaultOrgItem);
        this.editedOrgIndex = -1;
      }, 300);
    },

    saveOrg() {
      if (this.editedOrgIndex > -1) {
        // update org and save to db
        this.$http
          .put(
            "http://127.0.0.1:5000/organization/update/" +
              this.organization_item.id,
            {
              name: this.organization_item.name,
              description: this.organization_item.description
            }
          )
          .then(({ data }) => {
            Object.assign(
              this.organizations[this.editedOrgIndex],
              this.organization_item
            ); // update table info (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Organization has been successfully updated!",
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
      } else {
        var uuid = uuidv4();
        this.$http
          .post("http://127.0.0.1:5000/organization/create", {
            id: uuid,
            name: this.organization_item.name,
            description: this.organization_item.description,
            network_id: this.$route.query.id
          })
          .then(({ data }) => {
            (this.organization_item.id = uuid),
              this.organizations.push(this.organization_item); // add organization to table (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Organization has been successfully created!",
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
      this.closeOrgDialog();
    },

    getServerGroups() {
      this.$http
        .get("http://127.0.0.1:5000/server-group/all/" + this.$route.query.id)
        .then(({ data }) => {
          // Adds the server groups from the database to the table
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

    editServerGroupItem(item) {
      this.editedServerGroupIndex = this.server_groups.indexOf(item);
      this.server_group_item = Object.assign({}, item);
      this.server_groups_dialog = true;
    },

    deleteServerGroupItem(item) {
      const index = this.server_groups.indexOf(item); // gets index of server group in table

      confirm("Are you sure you want to delete this server group?") &&
        this.$http
          .delete("http://127.0.0.1:5000/server-group/delete/" + item.id)
          .then(({ data }) => {
            this.server_groups.splice(index, 1); // remove server group from table
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Server group has been successfully deleted!",
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
    },

    closeServerGroupDialog() {
      this.server_groups_dialog = false;
      setTimeout(() => {
        this.server_group_item = Object.assign({}, this.defaultServerGroupItem);
        this.editedServerGroupIndex = -1;
      }, 300);
    },

    saveServerGroup() {
      if (this.editedServerGroupIndex > -1) {
        // update server group and save to db
        this.$http
          .put(
            "http://127.0.0.1:5000/server-group/update/" +
              this.server_group_item.id,
            {
              name: this.server_group_item.name,
              organization: this.server_group_item.organization,
              lower_ip_range: this.server_group_item.lower_ip_range,
              upper_ip_range: this.server_group_item.upper_ip_range,
              description: this.server_group_item.description
            }
          )
          .then(({ data }) => {
            Object.assign(
              this.server_groups[this.editedServerGroupIndex],
              this.server_group_item
            ); // update table info (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Server group has been successfully updated!",
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
      } else {
        var uuid = uuidv4();
        this.$http
          .post("http://127.0.0.1:5000/server-group/create", {
            id: uuid,
            name: this.server_group_item.name,
            organization: this.server_group_item.organization,
            lower_ip_range: this.server_group_item.lower_ip_range,
            upper_ip_range: this.server_group_item.upper_ip_range,
            description: this.server_group_item.description,
            network_id: this.$route.query.id
          })
          .then(({ data }) => {
            (this.server_group_item.id = uuid),
              this.server_groups.push(this.server_group_item); // add organization to table (frontend)
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
      this.closeServerGroupDialog();
    }
  }
};
</script>
<style>
</style>
