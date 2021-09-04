<template>
  <div class="container">
    <div class="register-box">
      <h3>REGISTER</h3>
      <a-form-model
        ref="form"
        :model="form"
        :label-col="{ span: 7 }"
        :wrapper-col="{ span: 16 }"
        @submit="handleSubmit"
        @submit.native.prevent
      >
        <a-form-model-item label="Email address" prop="email" :rules="[{ type: 'email' }]" required>
          <a-input v-model="form.email"/>
        </a-form-model-item>
        <a-form-model-item label="Password" prop="password" :rules="[{ min: 6 }]" required>
          <a-input v-model="form.password" type="password"/>
        </a-form-model-item>
        <a-form-model-item label="Confirm Password" prop="confirmPassword" :rules="[{ min: 6 }]" required>
          <a-input v-model="form.confirmPassword" type="password"/>
        </a-form-model-item>
        <a-form-model-item label="User Name" prop="userName" required>
          <a-input v-model="form.userName"/>
        </a-form-model-item>
        <a-form-model-item label="First Name" prop="firstName">
          <a-input v-model="form.firstName"/>
        </a-form-model-item>
        <a-form-model-item label="Family Name" prop="familyName">
          <a-input v-model="form.familyName"/>
        </a-form-model-item>
        <a-form-model-item label="Cuisine Preference" prop="preference" required>
          <a-select v-model="form.preference">
            <a-select-option v-for="item in cuisineList" :key="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item :wrapper-col="{ span: 17, offset: 7 }">
          <a-button
            type="primary"
            html-type="submit"
          >
            Create
          </a-button>
        </a-form-model-item>
      </a-form-model>
    </div>
  </div>
</template>
<script>
import {CommonApi} from '@/apis/commonApi';

export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
        confirmPassword: '',
        userName: '',
        firstName: '',
        familyName: '',
        preference: undefined,
      },
      cuisineList: [],
    };
  },
  created() {
    CommonApi.getCuisineList()
      .then(res => {
        this.cuisineList = res;
      });
  },
  methods: {
    handleSubmit() {
      const {form} = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        if (form.password !== form.confirmPassword) {
          this.$message.error('Two passwords are inconsistent');
          return;
        }
        CommonApi.registerDiner(form)
          .then((res) => {
            if (res) {
              this.$router.push({name: 'home'});
              this.$rootStore.getUserInf();
            } else {
              this.$message.error('Email repeat');
            }
          });
      });
    },
  },
};
</script>
<style lang="less" scoped>
.container {
  height: 100%;
  padding: 100px;
  background-image: url('../../assets/bg.jpg');
  background-size: 100% auto;
  background-repeat: no-repeat;
}

.register-box {
  width: 600px;
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
