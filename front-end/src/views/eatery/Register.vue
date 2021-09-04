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
        <a-form-model-item label="Eatery Name" prop="eateryName" required>
          <a-input v-model="form.eateryName"/>
        </a-form-model-item>
        <a-form-model-item label="Region" prop="region" required>
          <a-select v-model="form.region" style="width: 90%;">
            <a-select-option v-for="item in regionList" :key="item.id">{{ item.name }}</a-select-option>
          </a-select>
          <a-tooltip>
            <a-icon type="question-circle" style="color: rgba(0,0,0,.45); cursor: pointer; margin-left: 6px;"/>
            <div slot="title">
              <div>If your location is not in this list, you can contact us by email. Our email is
                excellenteatery@outlook.com.
              </div>
            </div>
          </a-tooltip>
        </a-form-model-item>
        <a-form-model-item label="Street" prop="street">
          <a-input v-model="form.street"/>
        </a-form-model-item>
        <a-form-model-item label="Cuisine" prop="cuisine" required>
          <a-select v-model="form.cuisine">
            <a-select-option v-for="item in cuisineList" :key="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="Menu" prop="menu">
          <file-upload v-model="form.menu">
            <a-button>
              <a-icon type="upload"/>
              Click to Upload
            </a-button>
          </file-upload>
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
        eateryName: '',
        region: undefined,
        street: '',
        cuisine: undefined,
        menu: '',
      },
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
  },
  methods: {
    handleMenuChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        this.$message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        this.$message.error(`${info.file.name} file upload failed.`);
      }
    },
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
        CommonApi.registerEatery(form)
          .then(async (res) => {
            if (res) {
              await this.$rootStore.getUserInf();
              this.$router.push({name: 'history'});
            } else {
              this.$message.error('email repeat');
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
