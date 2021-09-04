<template>
  <div class="container">
<!--    <a-page-header title="Home" @back="() => this.$router.push( {name:$rootStore.mode=='eatery'?'history':'home'} )" style="border-bottom: 1px solid rgb(235, 237, 240);"/>-->
    <div class="reset-box">
      <h3>Reset Password</h3>
      <div style="margin-top: 8px;"></div>
      <a-input style="float: left;width: 200px" :value="email" disabled></a-input>
      <a-button style="float: left;margin-left: 12px" @click="sendEmail">
        Send Email
      </a-button>
    </div>
  </div>
</template>
<script>
import {CommonApi} from '@/apis/commonApi';
import {DinerApi} from "@/apis/dinerApi";

export default {
  data() {
    return {
      email: '',
    }
  },
  created() {
    console.log(this.$rootStore.userInf)
    this.email = this.$rootStore.userInf.email;
  },
  methods: {
    sendEmail() {
      CommonApi.sendPasswordEmail(this.email)
        .then(res => {
          if (res) {
            this.$message.success('Send Successful!');
            sessionStorage.removeItem('id');
            sessionStorage.removeItem('role');
            this.$rootStore.getUserInf();
            this.$router.push({name: 'home'})
          }
        })
    },
  },
};
</script>
<style lang="less" scoped>
.container {
  height: 800px;
  padding: 100px;
  background: rgba(255, 255, 255, .8);
}

.reset-box {
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
