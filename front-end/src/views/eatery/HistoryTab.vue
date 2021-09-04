<template>
  <div style="padding: 12px;">
    <a-date-picker v-model="filter.date" @change="getList"/>
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
import {EateryApi} from '@/apis/eateryApi';

export default {
  data() {
    return {
      dataSource: [],
      filter: {date: undefined},
    };
  },
  computed: {
    columns() {
      return [
        {
          title: 'Date',
          dataIndex: 'date',
        },
        {
          title: 'Time',
          dataIndex: 'time',
          customRender: (text, record) => record.startTime + ' - ' + record.endTime,
        },
        {
          title: 'Total',
          dataIndex: 'total',
        },
        {
          title: 'Booked',
          dataIndex: 'booked',
        },
        {
          title: 'Checked',
          dataIndex: 'checked',
        },
      ];
    },
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      const {filter} = this;
      EateryApi.getHistoryList({...filter, date: filter.date ? filter.date.valueOf() : undefined})
        .then(res => {
          this.dataSource = res;
        });
    },
  },
}
</script>
