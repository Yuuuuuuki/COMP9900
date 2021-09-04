<template>
  <div class="page page-small">
    <a-carousel :autoplay="true">
      <div><img src="../../assets/1.png" /></div>
      <div><img src="../../assets/2.png" /></div>
      <div><img src="../../assets/3.png" /></div>
    </a-carousel>
    <p>If you like food,if you want to save money,please don't hesitate to join in our website. Our website provide most
      comprehensive discount voucher of all the eatery around the greater sydney. On our website, we provide real-time
      discount voucher of all provided eatery. You would show more store details and get more potential eateries through
      our advertising! You are free to view any restaurant's profile and reviwes on this website.<br/>
      So what are you waiting for?<br/>
      Join us!
    </p>
    <div style="text-align: center; margin: 48px;">
      <router-link :to="{ name: 'register' }">
        <a-button type="primary" size="large">Sign up now！</a-button>
      </router-link>
    </div>
  </div>
</template>
<script>
export default {}
</script>
<style lang="less" scoped>
.ant-carousel /deep/ .slick-slide {
  text-align: center;
  height: 320px;
  line-height: 320px;
  background: #364d79;
  overflow: hidden;
  cursor: pointer;
  text-align: center;
}

.ant-carousel /deep/ .slick-slide h3 {
  color: #fff;
}

img {
  height: 320px;
  width: auto;
}

p {
  text-align: center;
  font-size: 19px;
  letter-spacing: -0.3px;
  margin: 1em;
  padding: 12px;
  font-family: "Open Sans", sans-serif;
  color: rgb(39, 43, 46);
  line-height: 1.8;
}
</style>
