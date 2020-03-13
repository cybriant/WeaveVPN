<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <card>
            <h4 style="margin-top: 0;">Network Management</h4>

            <v-dialog v-model="dialog" persistent max-width="600px">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" dark v-on="on">Create Server Group</v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">Create Server Group</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field label="Name" required></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field label="Organization"></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field
                          label="Category"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field label="Lower IP Range" hint="ex 192.168.0.1" required></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field label="Upper IP Range" hint="ex 192.168.10.100" required></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field label="Description"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog = false">Cancel</v-btn>
                  <v-btn color="blue darken-1" text @click="dialog = false">Create</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
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
  })
  // mounted () {
  // this.$http
  //   .get('http://127.0.0.1:5000/api/login')
  //   .then(response => (this.info = response.data.email))
  // }
};
</script>
<style>
</style>
