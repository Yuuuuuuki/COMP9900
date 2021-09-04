import Vue from 'vue';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import { rootStore } from '@/stores/rootStore';
import FileUpload from '@/components/FileUpload.vue';
import '@/styles/index.less';

Vue.use(Antd);
Vue.component('file-upload', FileUpload);

Vue.prototype.$rootStore = rootStore;

Vue.config.productionTip = false;
