import vue from 'vue'
import  vuex from 'vuex'
// import utils from '../components/common/utils'
import easyauth from '../components/common/easyauth'
import config from '../components/config'


vue.use(vuex)

const __getStoredObject = function(key) {
    var storedObj = localStorage.getItem("loginUser")
    if (storedObj) {
        return JSON.parse(storedObj)
    }
    return null
}

const state = {
    loginUser: __getStoredObject("loginUser"),
    // langCode: utils.cookie.get(easyauth.config.lang_param) || config.defaultLangCode,
    langCode: localStorage.getItem(easyauth.config.lang_param) || config.defaultLangCcode,
}

const mutations = {
    changeLangCode(state, langCode) {
        // utils.cookie.set(easyauth.config.lang_param, langCode)
        localStorage.setItem(easyauth.config.lang_param, langCode)
        state.langCode=langCode;
    },
    saveLoginUser(state, loginUser) {
        localStorage.setItem("loginUser", JSON.stringify(loginUser))
        state.loginUser = loginUser
    },
    clearLoginUser(state) {
        state.loginUser = null
        localStorage.removeItem("loginUser")
    },
}

const actions = {
    changeLangCode:({commit},langCode)=>commit('changeLangCode', langCode)
}

const store = new vuex.Store ({
    state: state,
    actions: actions,
    mutations: mutations
})

export default store