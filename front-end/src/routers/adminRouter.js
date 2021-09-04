import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '@/views/Login.vue';
import Home from '@/views/admin/Home.vue';
import { rootStore } from '@/stores/rootStore';

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL + 'admin/',
  routes,
});

const whiteList = ['login', 'register'];

router.beforeEach(async (to, home, next) => {
  if (whiteList.includes(to.name)) {
    next();
  } else {
    await rootStore.getInfPromise;
    if (rootStore.userInf) {
      next();
    } else {
      next({ name: 'login' });
    }
  }
});


export default router;
