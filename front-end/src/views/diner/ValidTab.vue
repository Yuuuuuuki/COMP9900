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
        type: 'valid',
      },
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
          title: 'Valid Code',
          dataIndex: 'validCode',
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
      DinerApi.getValid({ ...filter, date: filter.date ? filter.date.valueOf() : undefined })
        .then(res => {
          this.dataSource = res;
        });
    },
  },
}
</script>
