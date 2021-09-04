import Vue from 'vue';
import Layout from './components/Layout';
import router from './routers/adminRouter';
import { rootStore } from './stores/rootStore';
import './common/bootstrap';

rootStore.mode = 'admin';

new Vue({
  router,
  render: h => h(Layout, [h('router-view')]),
}).$mount('#app');