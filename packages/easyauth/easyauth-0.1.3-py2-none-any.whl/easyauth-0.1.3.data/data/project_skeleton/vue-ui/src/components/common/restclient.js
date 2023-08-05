/**axios封装
 * 请求拦截、相应拦截、错误统一处理
 */
import axios from 'axios';
import QS from 'qs';
import router from '../../router'
import { Loading, Message } from 'element-ui'
import easyauth from './easyauth'
import utils from './utils'
import i18n from '../../i18n/i18n'
import store from '../../store'
import projConfig from '../config'
import bus from './bus'

axios.defaults.baseURL = projConfig.backendBaseURL;

// 请求超时时间
axios.defaults.timeout = projConfig.requestTimeout;

// post请求头
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8';
axios.defaults.headers.put['Content-Type'] = 'application/json;charset=UTF-8';
axios.defaults.headers.patch['Content-Type'] = 'application/json;charset=UTF-8';

if (process.env.NODE_ENV == 'development') {
    axios.defaults.withCredentials = true; //意思是携带cookie信息,保持session的一致性
}

var loadinginstace;

const __isSameUrl = function(checkUrl, expectUrl) {
    if (checkUrl != expectUrl
        && !checkUrl.startsWith(expectUrl + "?")
        && !checkUrl.startsWith(expectUrl + "#") ) {
            return false
    }
    return true
}

// 请求拦截器
axios.interceptors.request.use(
    config => {
        // 每次发送请求之前判断是否存在token，如果存在，则统一在http请求的header都加上token，不用每次请求都手动添加了
        // 即使本地存在token，也有可能token是过期的，所以在响应拦截器中要对返回状态进行判断
        // const token = store.state.token;
        // token && (config.headers.Authorization = token);

        var lang_code = store.state.langCode
        if (lang_code && lang_code.toLowerCase() != projConfig.defaultLangCode.toLowerCase()) {
            // for backend i18n
            config.url = utils.url.appendParameterInUrl(config.url, easyauth.config.lang_param, lang_code)
        }

        loadinginstace = Loading.service({ fullscreen: true })
        return config;
    },
    error => {
        if (loadinginstace) {
            loadinginstace.close()
        }
        Message.error({
            message: i18n.t("message.loadFailed")
        })
        return Promise.error(error);
    })

// 响应拦截器
axios.interceptors.response.use(
    response => {
        if (loadinginstace) {
            loadinginstace.close()
        }
        if (response.status === 401 || response.status === 403 || response.status === 404) {
            return Promise.reject(response);
        } else {
            if (__isSameUrl(response.config.url, easyauth.authentication.getLoginUserUrl)) {
                store.commit("saveLoginUser", response.data)
                bus.$emit("updateSidebar")
            }
            return Promise.resolve(response);
        }
    },
    // 服务器状态码不是200的情况
    error => {
        if (loadinginstace) {
            loadinginstace.close()
        }
        if (error.response && error.response.status) {
            switch (error.response.status) {
                // 401: 未登录
                // 未登录则跳转登录页面，并携带当前页面的路径
                // 在登录成功后返回当前页面，这一步需要在登录页操作。
                case 401:
                    if (!__isSameUrl(error.response.config.url, easyauth.authentication.changePasswordUrl)) {
                        // 清除token
                        var loginedBefore = false
                        if (store.state.loginUser) {
                            loginedBefore = true
                        }
                        store.commit("clearLoginUser")
                        if (__isSameUrl(error.response.config.url, easyauth.authentication.getLoginUserUrl)) {
                            if (router.currentRoute.meta && router.currentRoute.meta.notRequireAuth && utils.url.getParameterInUrl(error.response.config.url, "checkme")) {
                                return;
                            }
                        }
                        var loginFailedMessage
                        // 跳转
                        if ( !__isSameUrl(router.currentRoute.fullPath, '/login') ) {
                            router.replace({
                                path: '/login',
                                query: { redirect: router.currentRoute.fullPath }
                            });
                            if (loginedBefore) {
                                loginFailedMessage = i18n.t("message.reLogin")
                            } else {
                                loginFailedMessage = i18n.t("message.doLogin")
                            }
                        } else {
                            loginFailedMessage = [i18n.t("message.loginFailed"), ': ', error.response.data.detail].join("")
                        }
                        Message.error({
                            message: loginFailedMessage
                        })
                    }
                    break;
                // 403 没有权限
                case 403:
                    if ( !__isSameUrl(router.currentRoute.fullPath, '/403') ) {
                        router.replace({
                            path: '/403',
                            query: { redirect: router.currentRoute.fullPath }
                        });
                    }
                    break;
                // 404请求不存在
                case 404:
                    if ( !__isSameUrl(router.currentRoute.fullPath, '/404') ) {
                        router.replace({
                            path: '/404',
                            query: { redirect: router.currentRoute.fullPath }
                        });
                     }
                    break;
                // 其他错误
                default:
                    if (error.response.status == 500) {
                        Message.error({
                            message: [i18n.t("message.serverInternalError"), ': ', error.response.data.detail].join("")
                        })
                    }
            }
            return Promise.reject(error.response);
        } else {
            Message.error({
                message: i18n.t("message.networkIssue")
            })
            return Promise.reject(error.message);
        }
    }
);

/**
 * get方法，对应get请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
const get =(url, params)=>{
    return new Promise((resolve, reject) =>{
        axios.get(url, {
            params: params
        })
        .then(res => {
            resolve(res.data);
        })
        .catch(err => {
            reject(err.data)
        })
    });
}
/**
 * post方法，对应post请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
const post = (url,... params) =>{
    return new Promise((resolve, reject) => {
        axios.post(url, QS.stringify(... params))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}
/**
 * put方法，对应put请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
const put = (url,... params) =>{
    return new Promise((resolve, reject) => {
        axios.put(url, QS.stringify(...params))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}
/**
 * patch方法，对应patch请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
const patch = (url,... params) =>{
    return new Promise((resolve, reject) => {
        axios.patch(url, QS.stringify(...params))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}
/**
 * del方法，对应delete请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
const del = (url,... params) =>{
    return new Promise((resolve, reject) => {
        axios.delete(url, QS.stringify(...params))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}
/**
 * postJson方法，对应带json body的post请求
 * @param {String} url [请求的url地址]
 * @param {Object} jsonReq [请求时携带的参数]
 */
const postJson = (url, jsonReq) =>{
    return new Promise((resolve, reject) => {
        axios.post(url, JSON.stringify(jsonReq))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}
/**
 * putJson方法，对应带json body的put请求
 * @param {String} url [请求的url地址]
 * @param {Object} jsonReq [请求时携带的参数]
 */
const putJson = (url, jsonReq) =>{
    return new Promise((resolve, reject) => {
        axios.put(url, JSON.stringify(jsonReq))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}
/**
 * patchJson方法，对应带json body的patch请求
 * @param {String} url [请求的url地址]
 * @param {Object} jsonReq [请求时携带的参数]
 */
const patchJson = (url, jsonReq) =>{
    return new Promise((resolve, reject) => {
        axios.patch(url, JSON.stringify(jsonReq))
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            reject(err)
        })
    });
}

var restclient = {
    get, post, put, patch, del, postJson, putJson, patchJson
}

export { axios, restclient }
