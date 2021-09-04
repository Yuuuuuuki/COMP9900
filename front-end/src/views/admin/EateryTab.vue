<template>
  <div style="padding: 12px;">
    <a-input-search v-model="filter.eateryName" placeholder="search for eateries" style="width: 200px" @search="getList" />
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
        <a-form-model-item label="Eatery Name" prop="eateryName" required>
          <a-input v-model="form.eateryName" />
        </a-form-model-item>
        <a-form-model-item label="Region" prop="region" required>
          <a-select v-model="form.region">
            <a-select-option v-for="item in regionList" :key="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="Street" prop="street" required>
          <a-input v-model="form.street" />
        </a-form-model-item>
        <a-form-model-item label="Cuisine" prop="cuisine" required>
          <a-select v-model="form.cuisine">
            <a-select-option v-for="item in cuisineList" :key="item.id">{{ item.name }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="Menu" prop="menu">
          <file-upload v-model="form.menu">
            <a-button> <a-icon type="upload" /> Click to Upload </a-button>
          </file-upload>
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
        eateryName: '',
      },
      cuisineList: [],
      regionList: [],
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
          title: 'Eatery Name',
          dataIndex: 'eateryName',
        },
        {
          title: 'Region',
          dataIndex: 'region',
          customRender: (text) => this.regionList.find(t => t.id === text)?.name,
        },
        {
          title: 'Street',
          dataIndex: 'street',
        },
        {
          title: 'Cuisine',
          dataIndex: 'cuisine',
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
    CommonApi.getRegionList()
      .then(res => {
        this.regionList = res;
      });
  },
  methods: {
    getList() {
      const { filter } = this;
      AdminApi.getEateryList(filter)
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
        AdminApi.updateEatery(form)
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
          AdminApi.deleteEatery(id)
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
