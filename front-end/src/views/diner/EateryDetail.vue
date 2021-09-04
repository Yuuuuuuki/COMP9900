<template>
  <div class="page page-small">
    <div v-if="detailData" style="display: flex;">
      <a-avatar shape="square" :size="120" icon="user" :src="detailData.avatar"/>
      <div class="inf-header">
        <h3>{{ detailData.eateryName }}</h3>
        <div>Email: {{ detailData.email }}</div>
        <div>Location:
          {{ detailData.street }},
          {{
            regionList.find(r => r.id === detailData.region) && regionList.find(r => r.id === detailData.region).name
          }}
        </div>
        <div>Cuisine:
          {{
            cuisineList.find(r => r.id === detailData.cuisine) && cuisineList.find(r => r.id === detailData.cuisine).name
          }}
        </div>
      </div>
    </div>
    <div v-if="detailData" style="margin-top: 24px; display: flex;">
      <div style="flex-grow: 1;">
        <a-date-picker v-model="date" @change="getValidList"/>
        <a-list item-layout="horizontal" :data-source="validList" rowKey="id" bordered style="margin-top: 12px;">
          <a-list-item slot="renderItem" slot-scope="item">
            <a-list-item-meta>
              <div slot="title" style="margin: 12px 0;">
                <a-icon type="carry-out" style="margin-right: 8px;"/>
                {{ item.startTime }} - {{ item.endTime }}
              </div>
            </a-list-item-meta>
            <a-button type="primary" slot="actions" @click="() => handleBookClick(item)"
                      :disabled="item.booked >= item.total">Book
            </a-button>
          </a-list-item>
        </a-list>
        <h4 style="margin: 24px 0 0;">Reviews</h4>
        <a-list item-layout="horizontal" :data-source="commendList" rowKey="id">
          <a-list-item slot="renderItem" slot-scope="item">
            <a-comment :author="item.userName">
              <p slot="content">
                <a-tag>{{ item.rate }}</a-tag>
                {{ item.comment }}
              </p>
              <a-tooltip slot="datetime" :title="item.date">
                <span>{{ item.date }}</span>
              </a-tooltip>
            </a-comment>
          </a-list-item>
        </a-list>
      </div>
      <div style="min-width: 300px; margin-left: 24px;">
        <h4>Menu</h4>
        <img :src="detailData.menu" style="width: 300px;margin-bottom: 30px"/>
        <h4>Recommendation</h4>
        <a-list item-layout="horizontal" :data-source="rl" rowKey="id" style="max-width: 300px">
          <a-list-item slot="renderItem" slot-scope="item" style="margin-bottom: 10px">
            <a-list-item-meta>
              <router-link slot="title" :to="{ name: 'eateryDetail', params: { id: item.id } }">{{ item.name }}
              </router-link>
              <div slot="description">
                <a-rate :default-value=item.rate disabled/>
                <span style="margin-left: 15px">{{ (item.rate - 1) > -1 ? desc[parseInt(item.rate - 1)] : "" }}</span>
              </div>
              <a-avatar slot="avatar" shape="square" :src="item.avatar" :size="50"/>
              <div slot="description">
                {{ item.content }}
              </div>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </div>
    </div>
  </div>
</template>
<script>
import {DinerApi} from '@/apis/dinerApi';
import {CommonApi} from '@/apis/commonApi';
import moment from 'moment';

export default {
  props: ['id'],
  data() {
    return {
      moment,
      detailData: null,
      regionList: [],
      cuisineList: [],
      date: moment(),
      validList: [],
      commendList: [],
      rl: [],
      visible: false,
      form: {},
      currentVaild: null,
      desc: ['Terrible', 'Bad', 'Normal', 'Good', 'Wonderful'],
    };
  },
  created() {
    this.getall();
  },
  watch: {
    id: function () {
      this.getall();
    }
  },
  methods: {
    getall() {
      CommonApi.getCuisineList()
        .then(res => {
          this.cuisineList = res;
        });
      CommonApi.getRegionList()
        .then(res => {
          this.regionList = res;
        });
      this.getData();
      this.getValidList();
      this.getCommentList();
      CommonApi.getRemendList(this.id)
        .then(res => {
          this.rl = res;
        });
    },
    getData() {
      DinerApi.getEateryInf(this.id)
        .then(res => {
          this.detailData = res;
        });
    },
    getValidList() {
      this.validList = [];
      DinerApi.getValidList(this.id, this.date.valueOf())
        .then(res => {
          this.validList = res;
        });
    },
    getCommentList() {
      DinerApi.getCommendList(this.id)
        .then(res => {
          this.commendList = res;
        });
    },
    handleBookClick(valid) {
      DinerApi.bookEatery({
        ...valid,
        id: this.id,
        date: this.date.format('DD-MM-yyyy'),

      }).then((res) => {
        if (res === 0) {
          this.$message.success('Successful!');
        } else if (res === 2) {
          this.$message.error('You have already booked in this time!');
        } else if (res === 3) {
          this.$message.error('Book failed!');
        }
      });
    },
    handleSubmit() {
      const {form} = this;
      this.$refs.form.validate(valid => {
        if (!valid) {
          return;
        }
        DinerApi.bookEatery({
          ...form,
          validId: this.currentVaild.id,
        }).then((res) => {
          if (res) {
            this.$message.success('Successful!');
            this.visible = false;
          }
        });
      });
    },
  },
};
</script>
<style lang="less" scoped>
.page {
  padding: 16px;
}

.inf-header {
  flex-grow: 1;
  margin-left: 24px;

  h3 {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 8px;
  }

  div {
    line-height: 28px;
  }
}

h4:not(.ant-list-item-meta-title) {
  font-size: 16px;
  margin-bottom: 8px;

  &::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 14px;
    background: #1890ff;
    margin-right: 8px;
  }
}

.ant-list-item {
  padding: 0;
}
</style>
