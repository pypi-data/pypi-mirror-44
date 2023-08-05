import i18n from '../i18n/i18n'
import permission from './common/permission'
import Dashboard from '@/components/page/Dashboard'
import UserAdmin from '@/components/page/UserAdmin'
import RoleAdmin from '@/components/page/RoleAdmin'

var menu = [
        {
            name: 'Dashboard',
            path: '/dashboard',
            component: Dashboard,
            icon: 'el-icon-lx-home',
            meta: {
                getTitle: function() {
                    return i18n.t("page.homeTitle")
                },
            },
        },
        {
            name: 'UserAdmin',
            path: '/userAdmin',
            component: UserAdmin,
            icon: 'el-icon-lx-people',
            meta: {
                getTitle:  function() {
                    return i18n.t("page.userAdminTitle")
                },
                requiredPermissions: ['query_group', 'query_permission', 'add_user', 'change_user', 'delete_user',
                 'query_user'],
            },
        },
        {
            name: 'RoleAdmin',
            path: '/roleAdmin',
            component: RoleAdmin,
            icon: 'el-icon-lx-group',
            meta: {
                    getTitle: function() {
                        return i18n.t("page.roleAdminTitle")
                    },
                    permissionCheck: function(user) {
                        return permission.isSuperUser(user)
                    }
                },
        },
]

export default menu

