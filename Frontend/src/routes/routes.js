import DashboardLayout from '../layout/DashboardLayout.vue'
// GeneralViews
import NotFound from '../pages/NotFoundPage.vue'
import RegisterUser from '../pages/Register.vue'
import LoginUser from '../pages/Login.vue'

// Admin pages
import Overview from 'src/pages/Overview.vue'
import UserProfile from 'src/pages/UserProfile.vue'
import TableList from 'src/pages/TableList.vue'
import Typography from 'src/pages/Typography.vue'
import Icons from 'src/pages/Icons.vue'
import Notifications from 'src/pages/Notifications.vue'

const routes = [
  {
    path: '/register',
    name: 'register',
    component: RegisterUser
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginUser
  },
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/admin/overview',
    name: 'Dashboard',
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/overview',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: Overview
      },
      {
        path: 'user',
        name: 'User',
        component: UserProfile
      },
      {
        path: 'user-management',
        name: 'User Management',
        component: UserProfile
      },
      {
        path: 'network-management',
        name: 'Network Management',
        component: UserProfile
      },
      {
        path: 'settings',
        name: 'Settings',
        component: UserProfile
      },
      {
        path: 'help',
        name: 'Help',
        component: UserProfile
      },

    ]
  },
  { path: '*', component: NotFound }
]

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes
