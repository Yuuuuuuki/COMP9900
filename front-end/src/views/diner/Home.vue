<template>
  <div class="page page-small">
    <a-carousel :autoplay="true">
      <div><img src="../../assets/4.png"/></div>
      <div><img src="../../assets/5.png"/></div>
      <div><img src="../../assets/6.png"/></div>
    </a-carousel>
    <a-input-search placeholder="Search for eateries" size="large" style="margin-top: 12px;" enter-button
                    @search="onSearch"/>
    <a-row :gutter="48">
      <a-col :span="8">
        <a-select v-model="region" placeholder="Region" @change="getList" allowClear>
          <a-select-option v-for="item in regionList" :key="item.id">{{ item.name }}</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="8">
        <a-date-picker v-model="date" :allowClear="true" @change="getList"/>
      </a-col>
      <a-col :span="8">
        <a-select v-model="sort" @change="getList">
          <a-select-option key="default">Default</a-select-option>
          <a-select-option key="top">Top Rated</a-select-option>
        </a-select>
      </a-col>
    </a-row>
    <a-back-top/>
    <div class="flex-half">
      <div class="flex-half-left">
        <a-list item-layout="horizontal" :data-source="dataList" rowKey="id">
          <a-list-item slot="renderItem" slot-scope="item">
            <a-list-item-meta>
              <router-link slot="title" :to="{ name: 'eateryDetail', params: { id: item.id } }">
                {{ item.name }}
              </router-link>
              <div slot="description">
                <a-rate :default-value=item.rate disabled/>
                <span style="margin-left: 15px" >{{ (item.rate - 1) > -1 ? desc[parseInt(item.rate - 1)] : "" }}</span>
              </div>
              <a-avatar slot="avatar" shape="square" :src="item.logo" :size="100" style="margin-right: 15px"/>
              <div slot="description">{{ item.content }}</div>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </div>
      <div class="flex-half-right">
        <h4>Cuisine</h4>
        <a-checkbox-group v-model="cuisine" @change="getList">
          <div v-for="item in cuisineList" class="checkbox-line" :key="item.id">
            <a-checkbox :value="item.id">{{ item.name }}</a-checkbox>
          </div>
        </a-checkbox-group>
      </div>
    </div>
  </div>
</template>
<script>
import {CommonApi} from '@/apis/commonApi';

export default {
  data() {
    return {
      eatery: '',
      region: undefined,
      date: undefined,
      sort: 'default',
      cuisine: [],
      dataList: [],
      regionList: [],
      cuisineList: [],
      desc: ['Terrible', 'Bad', 'Normal', 'Good', 'Wonderful'],
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
    this.getList();
  },
  watch: {
    id: function () {
      this.getList();
    }
  },
  methods: {
    getList() {
      const {eatery, region, date, sort, cuisine} = this;
      CommonApi.getEateryList({
        eatery,
        region,
        date: date && date.valueOf(),
        sort,
        cuisine,
      }).then((res) => {
        this.dataList = res;
      });
    },
    onSearch(text) {
      this.eatery = text;
      this.getList();
    },
  },
};
</script>
<style lang="less" scoped>
.page {
  padding: 16px;
}

.ant-input-search {
  margin-bottom: 16px;
}

.ant-col > * {
  width: 100%;
}

.flex-half {
  display: flex;
  margin: 24px 0 0;
}

.flex-half-left {
  flex-grow: 1;
  padding-right: 24px;
}

.flex-half-right {
  min-width: 180px;
  height: 600px;
  padding: 12px 16px;
  overflow-y: auto;
  border: 1px solid rgb(235, 237, 240);

  h4 {
    font-size: 18px;
    margin-bottom: 6px;
  }

  .checkbox-line {
    margin: 4px 0;
  }
}
</style>
