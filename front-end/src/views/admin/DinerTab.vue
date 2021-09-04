<template>
  <div style="padding: 12px;">
    <a-input-search v-model="filter.email" placeholder="Please enter email" style="width: 200px" @search="getList" />
    <a-table
      :columns="columns"
      :data-source="dataSource"
      rowKey="id"
      style="margin-top: 12px;"
    />
    <a-modal v-model="visible" title="Update" @ok="handleSubmit">
      <a-form-model
        ref="form"
        :model="form"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 13 }"
      >
        <a-form-model-item label="Email address" prop="email" required>
          <a-input v-model="form.email" />
        </a-form-model-item>
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
      </a-form-model>
    </a-modal>
  </div>
</template>
<script>
import moment from 'moment';
import { CommonApi } from '@/apis/commonApi';
import { AdminApi } from '@/apis/adminApi';

export default {
  data() {
    return {
      dataSource: [],
      filter: {
        email: '',
      },
      cuisineList: [],
      visible: false,
      form: {},
    };
  },
  computed: {
    columns() {
      return [
        {
          title: 'Email',
          dataIndex: 'email',
        },
        {
          title: 'User Name',
          dataIndex: 'userName',
        },
        {
          title: 'First Name',
          dataIndex: 'firstName',
        },
        {
          title: 'Family Name',
          dataIndex: 'familyName',
        },
        {
          title: 'Cuisine Preference',
          dataIndex: 'preference',
          customRender: (text) => this.cuisineList.find(t => t.id === text)?.name,
        },
        {
          title: 'Operate',
          key: 'action',
          customRender: (record) => [
            this.$createElement('a', { on: { click: () => this.handleUpdateClick(record)} }, 'update'),
            this.$createElement('a-divider', { props: { type: 'vertical' } }),
            this.$createElement('a', { on: { click: () => this.deleteRecord(record.id) } }, 'delete'),
          ],
        },
      ];
    },
  },
  created() {
    this.getList();
    CommonApi.getCuisineList()
      .then(res => {
        this.cuisineList = res;
      });
  },
  methods: {
    getList() {
      const { filter } = this;
      AdminApi.getDinerList(filter)
        .then(res => {
          this.dataSource = res;
        });
    },
    handleUpdateClick(record) {
      this.form = { ...record };
      this.visible = true;
    },
    handleSubmit() {
      const { form } = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        AdminApi.updateDiner(form)
          .then((res) => {
            if (res) {
              this.$message.success('Successful!');
              this.visible = false;
              this.getList();
            }
          });
      });
    },
    deleteRecord(id) {
      this.$confirm({
        title: 'Are you sure delete this record?',
        onOk: () => {
          AdminApi.deleteDiner(id)
            .then(res => {
              if (res) {
                this.$message.success('Successful!');
                this.getList();
              }
            });
        },
      });
    },
  },
}
</script>
