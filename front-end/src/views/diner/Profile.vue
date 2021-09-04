<template>
  <div class="page page-small">
<!--    <a-page-header title="Home" @back="() => this.$router.push( {name:'home'} )" style="border-bottom: 1px solid rgb(235, 237, 240);"/>-->
    <a-form-model
      ref="form"
      :model="form"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 10 }"
      @submit="handleSubmit"
      @submit.native.prevent
    >
      <div class="center">
        <file-upload v-model="form.avatar">
          <a-avatar shape="square" :size="120" icon="user" :src="form.avatar"/>
        </file-upload>
      </div>
      <a-form-model-item label="User Name" prop="userName" required>
        <a-input v-model="form.userName" />
      </a-form-model-item>
      <a-form-model-item label="First Name" prop="firstName">
        <a-input v-model="form.firstName" />
      </a-form-model-item>
      <a-form-model-item label="Family Name" prop="familyName">
        <a-input v-model="form.familyName" />
      </a-form-model-item>
      <a-form-model-item label="Cuisine Preference" prop="preference" required>
        <a-select v-model="form.preference">
          <a-select-option v-for="item in cuisineList" :key="item.id">{{ item.name }}</a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item :wrapper-col="{ span: 10, offset: 8 }">
        <a-button
          type="primary"
          html-type="submit"
        >
          Update
        </a-button>
      </a-form-model-item>
    </a-form-model>
  </div>
</template>
<script>
import _ from 'lodash';
import { DinerApi } from '@/apis/dinerApi';
import {CommonApi} from "@/apis/commonApi";

export default {
  data() {
    return {
      form: {},
      cuisineList: [],
    };
  },
  created() {
    CommonApi.getCuisineList()
      .then(res => {
        this.cuisineList = res;
      });
    DinerApi.getDinerInf()
      .then((res) => {
        this.form = res;
      })
  },
  methods: {
    handleSubmit() {
      const { form } = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        DinerApi.modifyDinerInf(form)
          .then((res) => {
            if (res) {
              this.$message.success('Update Successful');
              this.$rootStore.getUserInf();
            } else {
              this.$message.error('Update failed');
            }
          });
      });
    },
  },
};
</script>
<style lang="less" scoped>
  .ant-avatar {
    position: relative;
    margin: 36px auto 48px;
    cursor: pointer;
    &:hover:after {
      content: 'Upload';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, .7);
      color: white;
      font-size: 20px;
    }
  }
  .ant-form {
    padding-bottom: 36px;
  }
</style>
