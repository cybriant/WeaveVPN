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
              <v-tab>Connection Rules</v-tab>

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

              <!-- END OF ORGANIZATIONS TAB -->

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
                              <v-text-field
                                label="Server Group Name"
                                v-model="server_group_item.name"
                                required
                              ></v-text-field>
                              <input v-model="server_group_item.id" hidden />
                            </v-col>
                          </v-row>

                          <v-row>
                            <v-col cols="12" sm="12">
                              <v-select
                                :items="organizations"
                                item-text="name"
                                item-value="name"
                                v-model="server_group_item.organization"
                                label="Organization"
                                required
                              ></v-select>
                            </v-col>
                          </v-row>

                          <v-row>
                            <v-col cols="12">
                              <v-text-field
                                label="Description"
                                v-model="server_group_item.description"
                              ></v-text-field>
                            </v-col>
                          </v-row>

                          <v-row style="padding-top: 10px;">
                            <v-col cols="12" sm="12" style="padding-bottom: 0;">
                              <label style="margin-bottom: 0;">IP Subnet:</label>
                            </v-col>

                            <v-col cols="12" sm="6" style="padding-top: 0;">
                              <v-text-field
                                label="Lower IP Range"
                                hint="ex 172.24.0.1"
                                v-model="server_group_item.lower_ip_range"
                                required
                              ></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" style="padding-top: 0;">
                              <v-text-field
                                label="Upper IP Range"
                                hint="ex 172.24.0.254"
                                v-model="server_group_item.upper_ip_range"
                                required
                              ></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="grey darken-1" text @click="closeServerGroupDialog()">Cancel</v-btn>
                        <v-btn
                          color="primary"
                          outlined
                          @click="saveServerGroup()"
                        >{{ submitServerGroupBtn }}</v-btn>
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
                    <v-icon
                      class="mr-2"
                      @click="editServerGroupItem(item)"
                      title="Edit Server Group"
                    >edit</v-icon>
                    <v-icon @click="deleteServerGroupItem(item)" title="Delete Server Group">delete</v-icon>
                  </template>
                </v-data-table>
              </v-tab-item>

              <!-- END OF SERVER GROUPS TAB -->

              <!-- CONNECTIONS TAB -->

              <v-tab-item style="margin-top: 1rem;">
                <v-row no-gutters style="padding-top: 10px; padding-bottom: 20px;">
                  <!-- CONNECTIONS MODAL -->

                  <v-dialog v-model="connections_dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark class="mb-2" v-on="on">
                        <v-icon>mdi-plus</v-icon>Create Connection Rule
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">{{ formConnectionTitle }}</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <input v-model="connection_item.id" hidden />
                            <v-col cols="12">
                              <v-select
                                :items="connection_directions"
                                item-text="text"
                                item-value="value"
                                v-model="connection_item.direction"
                                label="Connection Direction"
                                required
                              ></v-select>
                            </v-col>
                            <v-col cols="12" sm="6">
                              <v-select
                                :items="organizations"
                                item-text="name"
                                item-value="name"
                                v-model="connection_item.organization_A"
                                label="Organization A"
                                @change="organization_A_selected()"
                                return-object
                                required
                              ></v-select>
                            </v-col>
                            <v-col cols="12" sm="6">
                              <v-select
                                :items="server_groups_from_org_A"
                                item-text="name"
                                item-value="name"
                                v-model="connection_item.server_group_A"
                                label="Server Group A"
                                required
                              ></v-select>
                            </v-col>
                            <v-col cols="12" sm="6">
                              <v-select
                                :items="organizations"
                                item-text="name"
                                item-value="name"
                                v-model="connection_item.organization_B"
                                @change="organization_B_selected()"
                                label="Organization B"
                                return-object
                                required
                              ></v-select>
                            </v-col>
                            <v-col cols="12" sm="6">
                              <v-select
                                :items="server_groups_from_org_B"
                                item-text="name"
                                item-value="name"
                                v-model="connection_item.server_group_B"
                                label="Server Group B"
                                required
                              ></v-select>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="grey darken-1" text @click="closeConnectionDialog()">Cancel</v-btn>
                        <v-btn
                          color="primary"
                          outlined
                          @click="saveConnection()"
                        >{{ submitConnectionBtn }}</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                  <!-- END OF CONNECTIONS MODAL -->

                  <v-spacer></v-spacer>
                  <v-spacer></v-spacer>

                  <v-text-field
                    style="clear: both;"
                    v-model="connections_search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-row>

                <v-data-table
                  :headers="connections_headers"
                  :items="connections"
                  :search="connections_search"
                  sort-by="Organization A"
                  class="elevation-1"
                >
                  <template v-slot:item.action="{ item }">
                    <v-icon
                      class="mr-2"
                      @click="editConnectionItem(item)"
                      title="Edit Connection"
                    >edit</v-icon>
                    <v-icon @click="deleteConnectionItem(item)" title="Delete Connection">delete</v-icon>
                  </template>
                </v-data-table>
              </v-tab-item>

              <!-- END OF CONNECTIONS TAB -->
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
      { text: "Server Group Name", value: "name" },
      { text: "Organization", value: "organization" },
      { text: "Lower IP Range", value: "lower_ip_range" },
      { text: "Upper IP Range", value: "upper_ip_range" },
      { text: "Description", value: "description" },
      { text: "Actions", value: "action", sortable: false }
    ],

    // Connection data
    editedConnectionIndex: -1,
    defaultConnectionItem: {},
    connections_dialog: false,
    connection_item: {},
    connections: [],
    connection_directions: [
      {
        text: "Server Group A to Server Group B",
        value: "Server Group A to Server Group B"
      },
      {
        text: "Server Group B to Server Group A",
        value: "Server Group B to Server Group A"
      },
      { text: "Bi-directional", value: "Bi-directional" }
    ],
    server_groups_from_org_A: [],
    server_groups_from_org_B: [],
    connections_search: "",
    connections_headers: [
      { text: "Connection Direction", value: "direction" },
      { text: "Organization A", value: "organization_A" },
      { text: "Organization B", value: "organization_B" },
      { text: "Server Group A", value: "server_group_A" },
      { text: "Server Group B", value: "server_group_B" },
      { text: "Actions", value: "action", sortable: false }
    ]
  }),

  created() {
    this.getServerGroups();
    this.getOrganizations();
    this.getConnections();
  },
  computed: {
    network_name() {
      return this.$route.query.name;
    },

    // Organization methods
    formOrgTitle() {
      return this.editedOrgIndex === -1
        ? "New Organization"
        : "Edit Organization";
    },
    submitOrgBtn() {
      return this.editedOrgIndex === -1 ? "Add" : "Update";
    },

    // Server Group methods
    formServerGroupTitle() {
      return this.editedServerGroupIndex === -1
        ? "New Server Group"
        : "Edit Server Group";
    },
    submitServerGroupBtn() {
      return this.editedServerGroupIndex === -1 ? "Create" : "Update";
    },

    // Connection methods
    formConnectionTitle() {
      return this.editedConnectionIndex === -1
        ? "New Connection Rule"
        : "Edit Connection Rule";
    },
    submitConnectionBtn() {
      return this.editedConnectionIndex === -1 ? "Create" : "Update";
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
    },

    // Connection methods
    getConnections() {
      this.$http
        .get("http://127.0.0.1:5000/connection/all/" + this.$route.query.id)
        .then(({ data }) => {
          // Adds the connections from the database to the table
          this.connections = data.connections;
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

    editConnectionItem(item) {
      this.editedConnectionIndex = this.connections.indexOf(item);
      this.connection_item = Object.assign({}, item);
      // console.log(this.connection_item)
      this.connections_dialog = true;
    },

    deleteConnectionItem(item) {
      const index = this.connections.indexOf(item); // gets index of connection in table

      confirm("Are you sure you want to delete this network connection?") &&
        this.$http
          .delete("http://127.0.0.1:5000/connection/delete/" + item.id)
          .then(({ data }) => {
            this.connections.splice(index, 1); // remove user from table
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Connection has been successfully deleted!",
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

    closeConnectionDialog() {
      this.connections_dialog = false;
      (this.server_groups_from_org_A = []),
        (this.server_groups_from_org_B = []),
        setTimeout(() => {
          this.connection_item = Object.assign({}, this.defaultConnectionItem);
          this.editedConnectionIndex = -1;
        }, 300);
    },

    saveConnection() {
      if (this.editedConnectionIndex > -1) {
        // update connection and save to db
        this.$http
          .put(
            "http://127.0.0.1:5000/connection/update/" +
              this.connection_item.id,
            {
              id: this.connection_item.id,
              direction: this.connection_item.direction,
              organization_A: this.connection_item.organization_A.name,
              organization_B: this.connection_item.organization_B.name,
              server_group_A: this.connection_item.server_group_A,
              server_group_B: this.connection_item.server_group_B
            }
          )
          .then(({ data }) => {
            (this.connection_item.organization_A = this.connection_item.organization_A.name),
              (this.connection_item.organization_B = this.connection_item.organization_B.name),
              Object.assign(
                this.connections[this.editedConnectionIndex],
                this.connection_item
              );
            console.log(this.connections), // update table info (frontend)
              this.$notify({
                group: "foo",
                title: "Success!",
                text: "Connection has been successfully updated!",
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
          .post("http://127.0.0.1:5000/connection/create", {
            id: uuid,
            direction: this.connection_item.direction,
            organization_A: this.connection_item.organization_A.name,
            organization_B: this.connection_item.organization_B.name,
            server_group_A: this.connection_item.server_group_A,
            server_group_B: this.connection_item.server_group_B,
            network_id: this.$route.query.id
          })
          .then(({ data }) => {
            (this.connection_item.id = uuid),
              (this.connection_item.organization_A = this.connection_item.organization_A.name),
              (this.connection_item.organization_B = this.connection_item.organization_B.name),
              this.connections.push(this.connection_item); // add connection to table (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Connection has been successfully created!",
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
      this.closeConnectionDialog();
    },

    organization_A_selected() {
      this.$http
        .get(
          "http://127.0.0.1:5000/server-group/all/" +
            this.$route.query.id +
            "/" +
            this.connection_item.organization_A.id
        )
        .then(({ data }) => {
          // Adds the connections from the database to the table
          this.server_groups_from_org_A = data.server_groups;
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

    organization_B_selected() {
      this.$http
        .get(
          "http://127.0.0.1:5000/server-group/all/" +
            this.$route.query.id +
            "/" +
            this.connection_item.organization_B.id
        )
        .then(({ data }) => {
          // Adds the connections from the database to the table
          this.server_groups_from_org_B = data.server_groups;
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
    }
  }
};
</script>
<style>
</style>
