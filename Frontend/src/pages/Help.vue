<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <card>
            <h4 style="margin-top: 0;">Need help getting started?</h4>

            <ul>
              <li>Networks</li>
              <ul>
                <a href="#creating_networks">
                  <li>Creating networks</li>
                </a>
                <a href="#updating_networks">
                  <li>Updating networks</li>
                </a>
                <a href="#deleting_networks">
                  <li>Deleting networks</li>
                </a>
              </ul>
              <li>Organizations</li>
              <ul>
                <a href="#creating_organizations">
                  <li>Creating Organizations</li>
                </a>
                <a href="#updating_organizations">
                  <li>Updating Organizations</li>
                </a>
                <a href="#deleting_organizations">
                  <li>Deleting Organizations</li>
                </a>
              </ul>
              <li>Server Groups</li>
              <ul>
                <a href="#creating_server_groups"><li>Creating Server Groups</li></a>
                <a href="#updating_server_groups"><li>Updating Server Groups</li></a>
                <a href="#deleting_server_groups"><li>Deleting Server Groups</li></a>
              </ul>
              <li>Connection Rules</li>
              <ul>
                <a href="#creating_connection_rules"><li>Creating Connection Rules</li></a>
                <a href="#updating_connection_rules"><li>Updating Connection Rules</li></a>
                <a href="#deleting_connection_rules"><li>Deleting Connection Rules</li></a>
              </ul>
            </ul>

            <hr />

            <h3 style="margin-bottom: 0;">Networks</h3>

            <h4 id="creating_networks">Creating Networks</h4>
            <ol>
              <li>Click the "Network Management" tab from the sidebar</li>
              <li>Click the "Create Network" button</li>
              <li>Enter a network name - network names must be unique</li>
              <li>Enter a network description (Optional)</li>
              <li>Click the "Add" button to create the network</li>
            </ol>

            <h4 id="updating_networks">Updating Networks</h4>
            <ol>
              <li>Click the "Network Management" tab from the sidebar</li>
              <li>Click the pencil icon on the row of the network that you would like to edit</li>
              <li>Edit the network name - network names must be unique</li>
              <li>Edit the network description (Optional)</li>
              <li>Click the "Update" button to update the network</li>
            </ol>

            <h4 id="deleting_networks">Deleting Networks</h4>
            <ol>
              <li>Click the "Network Management" tab from the sidebar</li>
              <li>Click the trash icon on the row of the network that you would like to delete</li>
              <li>Confirm if you would like to delete the network</li>
            </ol>

            <hr />

            <h3 style="margin-bottom: 0;">Organizations</h3>

            <h4 id="creating_organizations">Creating Organizations</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Create Organization" button</li>
              <li>Enter an organization name - organization names must be unique within the network</li>
              <li>Enter an organization description (Optional)</li>
              <li>Click the "Add" button to create the organization</li>
            </ol>

            <h4 id="updating_organizations">Updating Organizations</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the pencil icon on the row of the organization that you would like to edit</li>
              <li>Edit the organization name - organization names must be unique within the network</li>
              <li>Edit the organization description (Optional)</li>
              <li>Click the "Update" button to update the organization</li>
            </ol>

            <h4 id="deleting_organizations">Deleting Organizations</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the trash icon on the row of the organization that you would like to delete</li>
              <li>Confirm if you would like to delete the organization</li>
            </ol>

            <hr />

            <h3 style="margin-bottom: 0;">Server Groups</h3>

            <h4 id="creating_server_groups">Creating Server Groups</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Server Groups" tab</li>
              <li>Click the "Create Server Group" button</li>
              <li>Enter a server group name - server group names must be unique within the network</li>
              <li>Select an organization for the server group</li>
              <li>Enter a description (Optional)</li>
              <li>Enter an IP subnet: lower IP range and upper IP range</li>
              <li>Click the "Create" button to create the server group</li>
            </ol>

            <h4 id="updating_server_groups">Updating Server Groups</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Server Groups" tab</li>
              <li>Click the pencil icon on the server group you would like to edit</li>
              <li>Enter a server group name - server group names must be unique within the network</li>
              <li>Select an organization for the server group</li>
              <li>Enter a description (Optional)</li>
              <li>Enter an IP subnet: lower IP range and upper IP range</li>
              <li>Click the "Update" button to update the server group</li>
            </ol>

            <h4 id="deleting_server_groups">Deleting Server Groups</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Server Groups" tab</li>
              <li>Click the trash icon on the server group you would like to delete</li>
              <li>Confirm if you would like to delete the server group</li>
            </ol>

            <hr>

            <h3 style="margin-bottom: 0;">Connection Rules</h3>

            <h4 id="creating_connection_rules">Creating Connection Rules</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Connection Rules" tab</li>
              <li>Click the "Create Connection Rule" button</li>
              <li>Select directionality for the connection: ex. A -> B, B -> A, or bi-directional</li>
              <li>Select an organization for organization A</li>
              <li>Select a server group from organization A</li>
              <li>Select an organization for organization B</li>
              <li>Select a server group from organization B</li>
              <li>Click the "Create" button to create the connection rule</li>
            </ol>

            <h4 id="updating_connection_rules">Updating Connection Rules</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Connection Rules" tab</li>
              <li>Click the pencil icon on the connection rule you would like to edit</li>
              <li>Select directionality for the connection: ex. A -> B, B -> A, or bi-directional</li>
              <li>Select an organization for organization A</li>
              <li>Select a server group from organization A</li>
              <li>Select an organization for organization B</li>
              <li>Select a server group from organization B</li>
              <li>Click the "Update" button to update the connection rule</li>
            </ol>

            <h4 id="deleting_connection_rules">Deleting Connection Rules</h4>
            <ol>
              <li>From the Network Management page, click on the appropriate network</li>
              <li>Click the "Connection Rules" tab</li>
              <li>Click the trash icon on the connection rule you would like to delete</li>
              <li>Confirm if you would like to delete the connection rule</li>
            </ol>



          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  components: {},
  data() {
    return {};
  }
};
</script>
<style>
</style>
