<template>
  <div style="padding: 12px;">
    <a-input-search placeholder="Enter" @search="onCheckCode" style="width: 400px;">
      <a-button slot="enterButton" type="primary">Check</a-button>
    </a-input-search>
    <a-button class="right" type="primary" @click="() => visible = true">Add</a-button>
    <a-table :columns="columns" :data-source="dataSource" rowKey="id" style="margin-top: 12px;"/>
    <a-modal v-model="visible" title="Add new voucher" @ok="handleCreateVoucher">
      <a-form-model ref="form" :model="form" :label-col="{ span: 9 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item label="Amount" prop="amount" required>
          <a-input-number v-model="form.amount" :min="0"/>
        </a-form-model-item>
        <a-form-model-item label="Discount" prop="discount" required>
          <a-input-number v-model="form.discount" :min="0" :max="100" :formatter="value => `${value}%`"
                          :parser="value => value.replace('%', '')"/>
        </a-form-model-item>
        <a-form-model-item label="Date" prop="date" required>
          <a-date-picker v-model="form.date"/>
        </a-form-model-item>
        <a-form-model-item label="Start Time" prop="startTime" required>
          <a-time-picker format="HH:mm" v-model="form.startTime"/>
        </a-form-model-item>
        <a-form-model-item label="End Time" prop="endTime" required>
          <a-time-picker format="HH:mm" v-model="form.endTime"/>
        </a-form-model-item>
        <a-form-model-item label="Release Everyweek" prop="everyWeekFlag" required>
          <a-radio-group v-model="form.everyWeekFlag">
            <a-radio :value="0">No</a-radio>
            <a-radio :value="1">Yes</a-radio>
          </a-radio-group>
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>
<script>
import moment from 'moment';
import {EateryApi} from '@/apis/eateryApi';

export default {
  data() {
    return {
      visible: false,
      dataSource: [],
      form: {},
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
          title: 'Checked',
          dataIndex: 'checked',
        },
        {
          title: 'Periodic',
          dataIndex: 'periodic',
          customRender: (text, record) => this.$createElement('a-button', {
            props: { type: 'primary' , disabled: !text },
            on: {click: () => this.doCancel(sessionStorage.getItem('id') + '_' + record.date + '_' + record.startTime + '-' + record.endTime)}
          }, 'cancel'),
        }

      ];
    },
  },
  created() {
    this.getList();
    this.resetForm();
  },
  methods: {
    getList() {
      EateryApi.getValidList()
        .then(res => {
          this.dataSource = res;
        });
    },
    onCheckCode(text) {
      EateryApi.checkCode(text)
        .then(res => {
          if (res === 0) {
            this.$message.success('The code is Valid!');
          } else if (res === 2) {
            this.$message.error('This code is invalid!/nPlease check the expiration date.');
          } else if (res === 3) {
            this.$message.error('This code is invalid!/nPlease check the voucher owner.');
          }
          this.getList()
        });
    },
    doCancel(id) {
      console.log('id1' + id)
      EateryApi.cancelPeriodic(id)
        .then((res) => {
          if (res) {
            this.getList()
          }
        })
    },

    resetForm() {
      this.form = {
        id: sessionStorage.getItem('id'),
        amount: 0,
        discount: 0,
        date: undefined,
        startTime: undefined,
        endTime: undefined,
        everyWeekFlag: 0,
      };
    },
    handleCreateVoucher() {
      const {form} = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        if (form.startTime && form.startTime.isAfter(form.endTime)) {
          this.$message.info('End time must after start time.')
          return;
        }
        EateryApi.addVoucher({
          ...form,
          date: form.date && form.date.valueOf(),
          startTime: form.startTime && form.startTime.valueOf(),
          endTime: form.endTime && form.endTime.valueOf(),
        })
          .then((res) => {
            if (res) {
              this.$message.success('Successful!');
              this.resetForm();
              this.getList();
              this.visible = false;
            }
          });
      });
    },
  },
}
</script>
