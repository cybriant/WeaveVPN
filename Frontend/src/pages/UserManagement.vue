<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <v-data-table
            :headers="headers"
            :items="users"
            :search="search"
            sort-by="Name"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat color="white" style="border-radius: 100px;">
                <h4>User Management</h4>
              </v-toolbar>

              <v-toolbar flat color="white">
                <!-- Start of dialog -->
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on }">
                    <v-btn color="primary" dark class="mb-2" v-on="on">
                      <v-icon style="padding-right: 5px;">mdi-account-plus</v-icon>Add User
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field v-model="editedItem.first_name" label="First Name" required></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field v-model="editedItem.last_name" label="Last Name" required></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field v-model="editedItem.email" label="Email" required></v-text-field>
                            <input v-model="editedItem.id" hidden />
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-select :items="roles" v-model="editedItem.role" label="Role" required></v-select>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
                      <v-btn color="primary" outlined @click="save">{{ submitBtn }}</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <!-- End of dialog -->
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
                <v-text-field
                  style="clear: both;"
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                ></v-text-field>
              </v-toolbar>
            </template>
            <template v-slot:item.action="{ item }">
              <v-icon class="mr-2" @click="editItem(item)" title="Edit User">edit</v-icon>
              <v-icon @click="deleteItem(item)" title="Delete User">delete</v-icon>
            </template>
            <template v-slot:no-data>
              <v-btn color="primary" @click="initialize">Reset</v-btn>
            </template>
          </v-data-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { v4 as uuidv4 } from 'uuid';
export default {
  data: () => ({
    roles: ["Administrator", "User"],
    search: "",
    dialog: false,
    headers: [
      { text: "First Name", align: "left", value: "first_name" },
      { text: "Last Name", value: "last_name" },
      { text: "Email", value: "email" },
      { text: "Role", value: "role" },
      { text: "Actions", value: "action", sortable: false }
    ],
    users: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {}
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Add New User" : "Edit User";
    },
    submitBtn() {
      return this.editedIndex === -1 ? "Add" : "Update";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.$http
        .get("http://127.0.0.1:5000/get-users")
        .then(({ data }) => {
          // Adds the users from the database to the table
          this.users = data.users;
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

    editItem(item) {
      this.editedIndex = this.users.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.editedItem.original_email = this.editedItem.email;
    },

    deleteItem(item) {
      const index = this.users.indexOf(item); // gets index of user in table

      confirm("Are you sure you want to delete this user?") &&
        this.$http
          .delete("http://127.0.0.1:5000/delete-user/" + item.id)
          .then(({ data }) => {
            this.users.splice(index, 1); // remove user from table
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "User has been successfully deleted!",
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

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    save() {
      if (this.editedIndex > -1) {
        // update user and save to db
        this.$http
          .put("http://127.0.0.1:5000/update-user/" + this.editedItem.id, {
            first_name: this.editedItem.first_name,
            last_name: this.editedItem.last_name,
            email: this.editedItem.email,
            role: this.editedItem.role
          })
          .then(({ data }) => {
            Object.assign(this.users[this.editedIndex], this.editedItem); // update table info (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "User has been successfully updated!",
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
        // create new user and save to db
        this.$http
          .post("http://127.0.0.1:5000/add-user", {
            id: uuid,
            first_name: this.editedItem.first_name,
            last_name: this.editedItem.last_name,
            email: this.editedItem.email,
            role: this.editedItem.role
          })
          .then(({ data }) => {
            this.editedItem.id = uuid,
            this.users.push(this.editedItem); // add user to table (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "User has been successfully created!",
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
      this.close();
    }
  }
};
</script>
<style>
.v-data-table {
  border-radius: 0.25rem;
  border: 1px solid rgba(0, 0, 0, 0.125);
}
.v-application .elevation-1 {
  -webkit-box-shadow: none !important;
  box-shadow: none !important;
}
</style>
