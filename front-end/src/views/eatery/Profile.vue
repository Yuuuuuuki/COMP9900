<template>
  <div class="page page-small">
<!--    <a-page-header title="Home" @back="() => this.$router.push( {name:'history'} )"-->
<!--                   style="border-bottom: 1px solid rgb(235, 237, 240);"/>-->
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
      <a-form-model-item label="Eatery Name" prop="eateryName" required>
        <a-input v-model="form.eateryName"/>
      </a-form-model-item>
      <a-form-model-item label="Region" prop="region" required>
        <a-select v-model="form.region">
          <a-select-option v-for="item in regionList" :key="item.id">{{ item.name }}</a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="Street" prop="street">
        <a-input v-model="form.street"/>
      </a-form-model-item>
      <a-form-model-item label="Cuisine" prop="cuisine" required>
        <a-select v-model="form.cuisine">
          <a-select-option v-for="item in cuisineList" :key="item.id">{{ item.name }}</a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="Introduction" prop="intro">
        <a-textarea v-model="form.intro"/>
      </a-form-model-item>
      <a-form-model-item label="Menu" prop="menu">
        <file-upload v-model="form.menu">
          <img :src="form.menu" style="width: 200px; height: 200px;"/>
        </file-upload>
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
import {EateryApi} from '@/apis/eateryApi';
import {CommonApi} from '@/apis/commonApi';

export default {
  data() {
    return {
      form: {},
      cuisineList: [],
      regionList: [],
    };
  },
  created() {
    CommonApi.getCuisineList()
      .then(res => {
        this.cuisineList = res;
      });
    CommonApi.getRegionList()
      .then(res => {
        this.regionList = res;
      });
    EateryApi.getEateryInf()
      .then((res) => {
        this.form = res;
      })
  },
  methods: {
    handleSubmit() {
      const {form} = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        EateryApi.modifyEateryInf(form)
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
