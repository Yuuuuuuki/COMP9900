<template>
  <div class="container">
    <div class="login-box">
      <h3>LOGIN</h3>
      <a-form-model :model="form" @submit="handleSubmit" @submit.native.prevent>
        <a-form-model-item>
          <a-input v-model="form.user" placeholder="Email" size="large">
            <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)"/>
          </a-input>
        </a-form-model-item>
        <a-form-model-item>
          <a-input-password  v-model="form.password" placeholder="Password" size="large">
            <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25);"/>
          </a-input-password>
        </a-form-model-item>
        <a-form-model-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            block
            :disabled="form.user === '' || form.password === ''"
          >
            Login
          </a-button>
        </a-form-model-item>
      </a-form-model>
      <a @click="() => visible = true">Forget password?</a>
      <div style="margin-top: 8px;"></div>
      <router-link :to="{ name: 'register' }">Doesn't have an account for ValueEats?</router-link>
    </div>
    <a-modal v-model="visible" title="Forget password" :footer="null">
      <a-input-search placeholder="Email" @search="sendEmail">
        <a-button slot="enterButton">
          Send Email
        </a-button>
      </a-input-search>
    </a-modal>
  </div>
</template>
<script>
import {CommonApi} from '@/apis/commonApi';

export default {
  data() {
    return {
      form: {
        user: '',
        password: '',
      },
      visible: false,
    };
  },
  methods: {
    handleSubmit() {
      const {user, password} = this.form;
      CommonApi.login(user, password, this.$rootStore.mode)
        .then((res) => {
          if (res) {
            this.$rootStore.getUserInf();
            this.$router.push({name: this.$rootStore.mode === 'eatery' ? 'history' : 'home'});
          } else {
            this.$message.error('Email or password error');
          }
        });
    },
    sendEmail(text) {
      CommonApi.sendPasswordEmail(text)
        .then(res => {
          if (res) {
            this.$message.success('Send Successful!');
          }
        })
    },
  },
};
</script>
<style lang="less" scoped>
.container {
  height: 100%;
  padding: 100px;
  background-image: url('../assets/bg.jpg');
  background-size: 100% auto;
  background-repeat: no-repeat;
}

.login-box {
  width: 500px;
  margin: auto;
  padding: 48px 64px;
  background: rgba(255, 255, 255, .8);
}

h3 {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 24px;
}
</style>
