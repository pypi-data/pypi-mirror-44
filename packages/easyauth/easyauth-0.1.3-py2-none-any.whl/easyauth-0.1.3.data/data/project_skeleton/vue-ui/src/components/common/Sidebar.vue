<template>
    <div class="sidebar">
        <el-menu class="sidebar-el-menu" :collapse="collapse" :background-color="menu_background_color"
        :text-color="menu_text_color" :active-text-color="menu_active_text_color" unique-opened router>
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-submenu :index="item.index" :key="item.index">
                        <template slot="title">
                            <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu v-if="subItem.subs" :index="subItem.index" :key="subItem.index">
                                <template slot="title">{{ subItem.title }}</template>
                                <el-menu-item v-for="(threeItem,i) in subItem.subs" :key="i" :index="threeItem.index">
                                    {{ threeItem.title }}
                                </el-menu-item>
                            </el-submenu>
                            <el-menu-item v-else :index="subItem.index" :key="subItem.index">
                                {{ subItem.title }}
                            </el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index">
                        <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script>
    import menu from '../menu.js';
    import theme from '../../themes'
    import store from '../../store'
    import permission from './permission'

    const __getDisplayMenuFromMenu = function(currentMenu, level=1, parentPermissionMeta=null) {
            var menuItems = []
            if (level <= 0 || level > 3) {
                return menuItems
            }
            currentMenu.forEach((item, i) => {
                if (!item.hidden) {
                    var subPermissionMeta = item.meta && (item.meta.permissionCheck || item.meta.requiredRoles || item.meta.requiredPermissions)?item.meta:parentPermissionMeta
                    var menuItem = {index: item.name};
                    if (item.icon) {
                        menuItem.icon = item.icon
                    }
                    if (item.meta) {
                        menuItem.title = item.meta.getTitle()
                    }
                    if (subPermissionMeta) {
                        if (subPermissionMeta.permissionCheck) {
                            menuItem.permissionCheck = subPermissionMeta.permissionCheck
                        }
                        if (subPermissionMeta.requiredRoles) {
                            menuItem.requiredRoles = subPermissionMeta.requiredRoles
                        }
                        if (subPermissionMeta.requiredPermissions) {
                            menuItem.requiredPermissions = subPermissionMeta.requiredPermissions
                        }
                    }
                    if (item.subs) {
                        if (level < 3) {
                            var subMemuItems = __getDisplayMenuFromMenu(item.subs, level + 1, subPermissionMeta)
                            menuItem.subs = subMemuItems
                        }
                    } else {
                        if (item.path) {
                            menuItem.route = item.path
                            menuItem.index = item.path.substring(1, item.path.length)
                        }
                    }
                    menuItems.push(menuItem)
                }
            })
            return menuItems
    }

    const __filterMenuItems = function(menuItems, level=1) {
        var filterItems = []
        if (level <= 0 || level > 3) {
            return filterItems
        }
        menuItems.forEach((item, i) => {
                // 权限判断
                var hasPermission = false
                if (store.state.loginUser) {  // 是否已经登陆
                    if (permission.isSuperUser(store.state.loginUser)) {
                        hasPermission = true
                    } else if (item.permissionCheck &&  typeof(eval(item.permissionCheck)) == "function") {
                        hasPermission = item.permissionCheck(store.state.loginUser)
                    } else if (item.requiredRoles) {
                        hasPermission = permission.hasRole(store.state.loginUser, item.requiredRoles)
                    } else if (item.requiredPermissions) {
                        hasPermission = permission.hasPermission(store.state.loginUser, item.requiredPermissions)
                    } else {
                        hasPermission = true
                    }
                }
                if (hasPermission) {
                    var add = true
                    if (item.subs) {
                        item.subs = __filterMenuItems(item.subs, level + 1)
                        if (!item.subs || item.subs.length == 0) {
                            add = false
                        }
                    } 
                    if (add) {
                        filterItems.push(item)
                    }

                }
        })
        return filterItems
    }

    export default {
        data() {
            return {
                collapse: false,
                menu_background_color: theme.sidebarCss.menu_background_color,
                menu_text_color: theme.sidebarCss.menu_text_color,
                menu_active_text_color: theme.sidebarCss.menu_active_text_color,
                filterItems: []
            }
        },
        computed:{
            allItems() {
                return __getDisplayMenuFromMenu(menu)
            },
            items: {
                get: function() {
                    this.filterItems = __filterMenuItems(this.allItems)
                    return this.filterItems
                },
                set: function(newValue) {
                    this.filterItems = newValue
                },
            },
        },
        created(){
            // 通过 Event Bus 进行组件间通信，来折叠侧边栏
            this.$bus.$on('collapse', msg => {
                this.collapse = msg;
            })
            this.$bus.$on('updateSidebar', () => {
                this.items = __filterMenuItems(this.allItems)
            })
        }
    }
</script>

<style scoped>
    .sidebar{
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom:0;
        overflow-y: scroll;
    }
    .sidebar::-webkit-scrollbar{
        width: 0;
    }
    .sidebar-el-menu:not(.el-menu--collapse){
        width: 250px;
    }
    .sidebar > ul {
        height:100%;
    }
</style>
