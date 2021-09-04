import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/diner/Home.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/diner/Register.vue';
import Profile from '@/views/diner/Profile.vue';
import Account from '@/views/Account.vue';
import History from '@/views/diner/History.vue';
import EateryDetail from '@/views/diner/EateryDetail.vue';
import { rootStore } from '../stores/rootStore';

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
    path: '/detail/:id',
    name: 'eateryDetail',
    component: EateryDetail,
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
  },
  {
    path: '/account',
    name: 'account',
    component: Account,
  },
  {
    path: '/history',
    name: 'history',
    component: History,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

const whiteList = ['login', 'register', 'home'];

router.beforeEach(async (to, home, next) => {
  if (whiteList.includes(to.name)) {
    next();
  } else {
    if (!rootStore.getInfPromise) {
      rootStore.getUserInf();
    }
    await rootStore.getInfPromise;
    if (rootStore.userInf) {
      next();
    } else {
      next({ name: 'login' });
    }
  }
});

export default router;
