<template>
  <div class="page page-small">
<!--    <a-page-header title="Home" @back="() => this.$router.push( {name:'home'} )" style="border-bottom: 1px solid rgb(235, 237, 240);"/>-->
    <a-tabs>
      <a-tab-pane key="1" tab="Valid">
        <valid-tab />
      </a-tab-pane>
      <a-tab-pane key="2" tab="Used">
        <used-tab />
      </a-tab-pane>
      <a-tab-pane key="3" tab="Overdue">
        <overdue-tab />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>
<script>
import ValidTab from './ValidTab.vue';
import UsedTab from './UsedTab.vue';
import OverdueTab from './OverdueTab.vue';

export default {
  components: {
    ValidTab,
    UsedTab,
    OverdueTab,
  },
};
</script>
