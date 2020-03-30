<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          

            <v-data-table
              :headers="headers"
              :items="networks"
              :search="search"
              sort-by="Name"
              class="elevation-1"
            >

              <template v-slot:top>
                <v-toolbar flat color="white" style="border-radius: 100px;">
                  <h4>Network Management</h4>
                </v-toolbar>
      
                <v-toolbar flat color="white">
                  <!-- Start of dialog -->
                  <v-dialog v-model="dialog" max-width="500px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark class="mb-2" v-on="on">
                        <v-icon style="padding-right: 5px;">mdi-plus</v-icon>Create Network
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">{{ formTitle }}</span>
                      </v-card-title>

                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12" sm="12" md="12">
                              <v-text-field v-model="editedItem.name" label="Name"></v-text-field>
                              <input v-model="editedItem.id" hidden />
                            </v-col>
                            <v-col cols="12" sm="12" md="12">
                              <v-text-field v-model="editedItem.description" label="Description"></v-text-field>
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

              <template v-slot:item.name="{ item }">
                <router-link :to="'/admin/network?name='+ item.name + '&id=' + item.id">{{ item.name }}</router-link>
              </template>

              <template v-slot:item.action="{ item }">
                <v-icon class="mr-2" @click="editItem(item)" title="Edit Network">edit</v-icon>
                <v-icon @click="deleteItem(item)" title="Delete Network">delete</v-icon>
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
    search: "",
    dialog: false,
    headers: [
      { text: "Name", value: "name" },
      { text: "Description", value: "description" },
      { text: "Actions", value: "action", sortable: false }
    ],
    networks: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {}
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Add New Network" : "Edit Network";
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
        .get("http://127.0.0.1:5000/network/all")
        .then(({ data }) => {
          // Adds the networks from the database to the table
          this.networks = data.networks;
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
      this.editedIndex = this.networks.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.networks.indexOf(item); // gets index of network in table

      confirm("Are you sure you want to delete this network?") &&
        this.$http
          .delete("http://127.0.0.1:5000/network/delete/" + item.id)
          .then(({ data }) => {
            this.networks.splice(index, 1); // remove network from table
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Network has been successfully deleted!",
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
        // update network and save to db
        this.$http
          .put(
            "http://127.0.0.1:5000/network/update/" +
              this.editedItem.id,
            {
              name: this.editedItem.name,
              description: this.editedItem.description
            }
          )
          .then(({ data }) => {
            Object.assign(this.networks[this.editedIndex], this.editedItem); // update table info (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Network has been successfully updated!",
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
        // create new network and save to db
        this.$http
          .post("http://127.0.0.1:5000/network/create", {
            id: uuid,
            name: this.editedItem.name,
            description: this.editedItem.description
          })
          .then(({ data }) => {
            this.editedItem.id = uuid,
            this.networks.push(this.editedItem); // add network to table (frontend)
            this.$notify({
              group: "foo",
              title: "Success!",
              text: "Network has been successfully created!",
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