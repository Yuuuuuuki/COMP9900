<template>
  <div class="page">
    <a-tabs>
      <a-tab-pane key="1" tab="Diner">
        <diner-tab />
      </a-tab-pane>
      <a-tab-pane key="2" tab="Eatery">
        <eatery-tab />
      </a-tab-pane>
      <a-tab-pane key="3" tab="Cuisine & Region">
        <cuisine-region-tab />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>
<script>
import DinerTab from './DinerTab.vue';
import EateryTab from './EateryTab.vue';
import CuisineRegionTab from './CuisineRegionTab.vue';

export default {
  components: {
    DinerTab,
    EateryTab,
    CuisineRegionTab,
  },
}
</script>