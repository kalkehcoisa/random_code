import Vue from 'vue'
import VueResource from 'vue-resource'
import Datatable from 'vue2-datatable-component'
import App from './App.vue'

import { apiPath } from './config.js'

Vue.use(VueResource);
Vue.use(Datatable);
Vue.http.options.emulateJSON = true

Vue.http.options.root = apiPath;

new Vue({
  el: '#app',
  render: h => h(App)
})
