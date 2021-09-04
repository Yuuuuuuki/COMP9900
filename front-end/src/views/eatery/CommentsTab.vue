<template>
  <div style="padding: 12px;">
    <a-row :gutter="48">
      <a-col :span="6">
        <a-date-picker v-model="filter.date" @change="getList"/>
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
import { EateryApi } from '@/apis/eateryApi';

export default {
  data() {
    return {
      dataSource: [],
      filter: {
        userName: '',
        email: '',
        date: undefined,
      },
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
          title: 'Diner',
          dataIndex: 'userName',
        },
        {
          title: 'Email Address',
          dataIndex: 'email',
        },
        {
          title: 'Comment',
          dataIndex: 'comment',
        },
        {
          title: 'Rate',
          dataIndex: 'rate',
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
      EateryApi.getCommentList({ ...filter, date: filter.date ? filter.date.valueOf() : undefined })
        .then(res => {
          this.dataSource = res;
        });
    },
  },
}
</script>
