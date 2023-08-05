import Vue from 'vue'
import VueI18n from 'vue-i18n'
import messages from './langs'
import locale from 'element-ui/lib/locale'
import store from '../store'

Vue.use(VueI18n)
var lang_code = store.state.langCode
const i18n = new VueI18n({
  locale: lang_code.replace("-", "_"),
  messages
})

locale.i18n((key, value) => i18n.t(key, value)) //重点：为了实现element插件的多语言切换

export default i18n
