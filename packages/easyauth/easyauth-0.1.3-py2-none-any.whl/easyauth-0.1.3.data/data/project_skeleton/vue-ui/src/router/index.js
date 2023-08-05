import Vue from 'vue'
import Router from 'vue-router'
import i18n from '../i18n/i18n'
import menu from '../components/menu'
import Page_403 from '@/components/common/403'
import Page_404 from '@/components/common/404'
import Login from '@/components/common/Login'
import Home from '@/components/common/Home'

Vue.use(Router)

var __homePage = "/dashboard"
var __homePage_Set = false
const __getChildRoutersFromMenu = function(currentMenu, level=1, parentPermissionMeta=null) {
  var childRouters = []
  if (level <= 0 || level > 3) {
     return childRouters
  }
  currentMenu.forEach((item, i) => {
      var subPermissionMeta = item.meta && (item.meta.permissionCheck || item.meta.requiredRoles || item.meta.requiredPermissions)?item.meta:parentPermissionMeta
      if (item.subs) {
        if (level < 3) {
          childRouters = childRouters.concat(__getChildRoutersFromMenu(item.subs, level + 1, subPermissionMeta))
        }
      } else {
          if (item.path && item.component) {
            if (item.path != '/403' && item.path != '/404' && item.path != '/') {
              var route = {name: item.name, path: item.path, component: item.component};
              if (item.meta) {
                  route.meta = item.meta
              }
              if (parentPermissionMeta) {
                  if (!item.meta) {
                      item.meta = {}
                  }
                  if (!item.meta.permissionCheck && !item.meta.requiredRoles && !item.meta.requiredPermissions) {
                      if (parentPermissionMeta.permissionCheck) {
                         item.meta.permissionCheck = parentPermissionMeta.permissionCheck
                      } else if (parentPermissionMeta.requiredRoles) {
                        item.meta.requiredRoles = parentPermissionMeta.requiredRoles
                      } else if (parentPermissionMeta.requiredPermissions) {
                        item.meta.requiredPermissions = parentPermissionMeta.requiredPermissions
                      } 
                  }
              }
              if (item.default && !__homePage_Set) {
                __homePage = item.path
                __homePage_Set = true
              }
              childRouters.push(route)
            }
          }
      }
  })
  return childRouters
}

const children = __getChildRoutersFromMenu(menu)

var routes = [
  {
    path: '/',
    redirect: __homePage
  },
  {
    path: '/',
    name: '__Home',
    component: Home,
    meta: { 
      getTitle: function() {
        return i18n.t("page.homeTitle") 
      }
    },
    children:[
      {
        path: '/403',
        name: '__Page_403',
        component: Page_403,
        meta: {
          getTitle: function() {
            return i18n.t("page.permissionDenyTitle")
          }
        }      
      },
      {
        path: '/404',
        name: '__Page_404',
        component: Page_404,
        meta: {
          getTitle: function() {
           return i18n.t("page.notFoundTitle")
          }
        }
      },
    ].concat(children)
  },
  {
    path: '/login',
    name: '__Login',
    component: Login,
    meta: {
      // 添加该字段，表示进入这个路由是不需要登录的
       notRequireAuth: true, 
       getTitle: function() {
          title: i18n.t("page.loginTitle")
       }
    },  
    // component:  resolve => require(['../components/common/Login.vue'], resolve)
  },
  {
    path: '*',
    redirect: '/404'
  }
]


export default new Router({
  routes: routes
})
