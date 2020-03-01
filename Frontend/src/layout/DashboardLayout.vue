<template>
  <div class="wrapper">
    <side-bar>
      <mobile-menu slot="content"></mobile-menu>
      <sidebar-link to="/admin/overview">
        <img src="/img/icons/dashboard-icon.svg" height="28px" width="28px" 
        style="margin-right: 15px; color: white; text-align: center; vertical-align: middle; float: left;"/>
        <p>Dashboard</p>
      </sidebar-link>
      <sidebar-link to="/admin/network-management">
        <i class="nc-icon nc-vector"></i>
        <p>Network Management</p>
      </sidebar-link>
      <sidebar-link to="/admin/user-management">
        <img src="/img/icons/multiple-11.svg" height="30px" width="30px" 
        style="margin-right: 15px; color: white; text-align: center; vertical-align: middle; float: left;"/>
        <p>User Management</p>
      </sidebar-link>
      <sidebar-link to="/admin/settings">
        <i class="nc-icon nc-settings-gear-64"></i>
        <p>Settings</p>
      </sidebar-link>
      <sidebar-link to="/admin/help">
        <i class="nc-icon nc-support-17"></i>
        <p>Help</p>
      </sidebar-link>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click="toggleSidebar">

      </dashboard-content>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script>
  import TopNavbar from './TopNavbar.vue'
  import ContentFooter from './ContentFooter.vue'
  import DashboardContent from './Content.vue'
  import MobileMenu from './MobileMenu.vue'
  export default {
    components: {
      TopNavbar,
      ContentFooter,
      DashboardContent,
      MobileMenu
    },
    methods: {
      toggleSidebar () {
        if (this.$sidebar.showSidebar) {
          this.$sidebar.displaySidebar(false)
        }
      }
    }
  }

</script>
