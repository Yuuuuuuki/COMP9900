<template>
  <div style="padding: 12px;">
    <a-row :gutter="48">
      <a-col :span="8">
        <a-date-picker v-model="filter.date" @change="getList" />
      </a-col>
    </a-row>
    <a-table
      :columns="columns"
      :data-source="dataSource"
      rowKey="id"
      style="margin-top: 12px;"
    />
    <a-modal v-model="visible" title="Comments" @ok="handleSubmit">
      <a-form-model
        ref="form"
        :model="form"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 13 }"
      >
        <a-form-model-item label="rating" prop="rate" required>
          <a-rate v-model="form.rate" allow-half :tooltips="desc" />
          <span class="ant-rate-text">{{ desc[form.rate - 1] }}</span>
        </a-form-model-item>
        <a-form-model-item prop="comment" :wrapper-col="{ span: 14, offset: 5 }">
          <a-textarea v-model="form.comment" :rows="5" placeholder="add comments"/>
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>
<script>
import moment from 'moment';
import { DinerApi } from '@/apis/dinerApi';

export default {
  data() {
    return {
      dataSource: [],
      filter: {
        date: undefined,
        type: 'used',
      },
      visible: false,
      form: {},
      desc: ['terrible', 'bad', 'normal', 'good', 'wonderful'],
    };
  },
  computed: {
    columns() {
      return [
        {
          title: 'Eatery',
          dataIndex: 'eateryName',
        },
        {
          title: 'Date',
          dataIndex: 'date',
        },
        {
          title: 'Time',
          dataIndex: 'time',
          customRender: (text, record) =>record.startTime + ' - ' + record.endTime,
        },
        {
          title: 'Rate',
          dataIndex: 'rate',
        },
        {
          title: 'Comment',
          dataIndex: 'comment',
          customRender: (text, record) => record.rate
            ? text
            : this.$createElement('a-button', { props: { type: 'primary' }, on: { click: () => this.handleAddClick(record.id) } }, 'add'),
        },
      ];
    },
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      const { filter } = this;
      DinerApi.getUsed({ ...filter, date: filter.date ? filter.date.valueOf() : undefined })
        .then(res => {
          this.dataSource = res;
        });
    },
    handleAddClick(id) {
      this.form = {
        rate: undefined,
        comment: '',
        voucher_id: id,
        diner_id: sessionStorage.getItem('id')
      };
      this.visible = true;
    },
    handleSubmit() {
      const { form } = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        DinerApi.comment(form)
          .then((res) => {
            if (res) {
              this.$message.success('Successful!');
              this.visible = false;
              this.getList();
            }
          });
      });
    },
  },
}
</script>
