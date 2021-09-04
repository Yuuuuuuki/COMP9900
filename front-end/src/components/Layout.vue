<template>
  <a-layout class="container">
    <a-layout-header class="header">
      <div class="logo" @click="() => $router.push({ name: $rootStore.mode === 'diner' ? 'home' : $rootStore.mode === 'eatery' ? ($rootStore.userInf ? 'history' : 'home' ) : 'home'})">ValueEats</div>
      <div class="right">
        <a-dropdown v-if="$rootStore.userInf">
          <a-avatar shape="square" :size="48" icon="user" :src="$rootStore.userInf.avatar"/>
          <a-menu slot="overlay" @click="handleMenuClick">
            <template v-if="$rootStore.mode !== 'admin'">
              <a-menu-item key="account">Account</a-menu-item>
              <a-menu-item key="profle">Profle</a-menu-item>
              <a-menu-item v-if="$rootStore.mode === 'diner'" key="history">History</a-menu-item>
            </template>
            <a-menu-item key="logout">Log out</a-menu-item>
          </a-menu>
        </a-dropdown>
        <template v-else>
<!--          <router-link :to="{ name: 'login' }"><a-button>Sign in</a-button></router-link>-->
          <router-link v-if="$rootStore.mode !== 'admin'" :to="{ name: 'login' }"><a-button>Sign in</a-button></router-link>
          <router-link v-if="$rootStore.mode !== 'admin'" :to="{ name: 'register' }"><a-button>Sign up</a-button></router-link>
          <a v-if="$rootStore.mode === 'diner'" href="/eatery"><a-button>For Eateries</a-button></a>
          <a v-if="$rootStore.mode === 'eatery'" href="/"><a-button>For Diners</a-button></a>
        </template>
      </div>
    </a-layout-header>
    <a-layout-content class="content">
      <div style="height: 100%;">
        <slot />
      </div>
    </a-layout-content>
  </a-layout>
</template>
<script>
import { CommonApi } from '@/apis/commonApi';

export default {
  created() {
    this.$rootStore.getUserInf();
  },
  methods: {
    handleMenuClick({ key }) {
      switch(key) {
        case 'account':
          this.$router.push({ name: 'account' });
          break;
        case 'profle':
          this.$router.push({ name: 'profile' });
          break;
        case 'history':
          this.$router.push({ name: 'history' });
          break;
        case 'logout':
          CommonApi.logout().then(() => {
            this.$rootStore.getUserInf();
            if (this.$rootStore.mode === 'admin') {
              window.location.href = '/admin';
            } else {
              this.$router.push({ name: 'home' });
            }
          });
          break;
        default:
          break;
      }
    }
  }
}
</script>
<style lang="less" scoped>
.container {
  padding: 0;
  width: 100%;
  min-height: 100vh;
  height: 100%;
  background: white;
}
.header {
  background: #fff;
  box-shadow: 0 2px 8px #f0f1f2;
  position: relative;
  z-index: 10;
  max-width: 100%;
}
.content {
  width: 100%;
  margin: 24px auto 0;
  height: 100%;
}
.logo {
  display: inline-block;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  color: #1890ff;
}
.right button {
  margin-left: 12px;
}
</style>
