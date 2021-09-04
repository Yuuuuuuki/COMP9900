<template>
  <div style="padding: 12px;">
    <div class="half-card">
      <a-button type="primary" @click="() => showAdd('cuisine')">Add</a-button>
      <a-table 
        :columns="cuisineColumns"
        :data-source="cuisineList"
        rowKey="id"
        style="margin-top: 12px;"
      />
    </div>
    <div class="half-card">
      <a-button type="primary" @click="() => showAdd('region')">Add</a-button>
      <a-table 
        :columns="regionColumns"
        :data-source="regionList"
        rowKey="id"
        style="margin-top: 12px;"
      />
    </div>
    <a-modal v-model="visible" :title="form.id ? 'Add' : 'Update'" @ok="handleSubmit">
      <a-form-model 
        ref="form"
        :model="form" 
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 13 }"
      >
        <a-form-model-item :label="type" prop="name" required>
          <a-input v-model="form.name" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>
<script>
import { CommonApi } from '@/apis/commonApi';
import { AdminApi } from '@/apis/adminApi';

export default {
  data() {
    return {
      cuisineList: [],
      regionList: [],
      visible: false,
      form: {},
      type: '',
    };
  },
  computed: {
    cuisineColumns() {
      return [
        {
          title: 'Cuisine',
          dataIndex: 'name',
        },
        {
          title: 'Operate',
          key: 'action',
          customRender: (record) => [
            this.$createElement('a', { on: { click: () => this.handleUpdateClick(record, 'cuisine')} }, 'update'),
            this.$createElement('a-divider', { props: { type: 'vertical' } }),
            this.$createElement('a', { on: { click: () => this.deleteRecord(record.id, 'cuisine') } }, 'delete'),
          ],
        },
      ];
    },
    regionColumns() {
      return [
        {
          title: 'Region',
          dataIndex: 'name',
        },
        {
          title: 'Operate',
          key: 'action',
          customRender: (record) => [
            this.$createElement('a', { on: { click: () => this.handleUpdateClick(record, 'region')} }, 'update'),
            this.$createElement('a-divider', { props: { type: 'vertical' } }),
            this.$createElement('a', { on: { click: () => this.deleteRecord(record.id, 'region') } }, 'delete'),
          ],
        },
      ];
    },
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
    showAdd(type) {
      this.form = {
        name: '',
      };
      this.type = type;
      this.visible = true;
    },
    handleUpdateClick(record, type) {
      this.type = type;
      this.form = { ...record };
      this.visible = true;
    },
    handleSubmit() {
      const { form } = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        AdminApi[form.id ? (this.type === 'cuisine' ? 'updateCuisine' : 'updateRegion') : (this.type === 'cuisine' ? 'addCuisine' : 'addRegion')](form)
          .then((res) => {
            if (res) {
              this.$message.success('Successful!');
              this.visible = false;
              if (this.type === 'cuisine') {
                  CommonApi.getCuisineList()
                    .then(res => {
                      this.cuisineList = res;
                    });
                } else {
                  CommonApi.getRegionList()
                    .then(res => {
                      this.regionList = res;
                    });
                }
            } 
          });
      });
    },
    deleteRecord(id, type) {
      this.$confirm({
        title: 'Are you sure delete this record?',
        onOk: () => {
          AdminApi[type === 'cuisine' ? 'deleteCuisine' : 'deleteRegion'](id)
            .then(res => {
              if (res) {
                this.$message.success('Successful!');
                if (type === 'cuisine') {
                  CommonApi.getCuisineList()
                    .then(res => {
                      this.cuisineList = res;
                    });
                } else {
                  CommonApi.getRegionList()
                    .then(res => {
                      this.regionList = res;
                    });
                }
              }
            });
        },
      });
    },
  },
}
</script>
<style lang="less" scoped>
.half-card {
  width: 45%;
  margin-right: 5%;
  float: left;
}
</style>