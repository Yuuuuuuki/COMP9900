<template>
  <div class="page page-small">
    <a-carousel :autoplay="true">
      <div><img src="../../assets/1.png" /></div>
      <div><img src="../../assets/2.png" /></div>
      <div><img src="../../assets/3.png" /></div>
    </a-carousel>
    <a-tabs>
      <a-tab-pane key="1" tab="Valid">
        <valid-tab />
      </a-tab-pane>
      <a-tab-pane key="2" tab="History">
        <history-tab />
      </a-tab-pane>
      <a-tab-pane key="3" tab="Comments">
        <comments-tab />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>
<script>
import ValidTab from './ValidTab.vue';
import HistoryTab from './HistoryTab.vue';
import CommentsTab from './CommentsTab.vue';

export default {
  components: {
    ValidTab,
    HistoryTab,
    CommentsTab,
  },
};
</script>
<style lang="less" scoped>

</style>
