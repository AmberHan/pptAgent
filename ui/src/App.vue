<template>
  <div id="app">
    <PPTGen msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import PPTGen from './components/PPTGen.vue';

export default {
  name: 'App',
  components: {
    PPTGen
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;


  /* 设置背景图片 */
  background: url("./assets/绘制网页背景图.png") no-repeat center center fixed;

  /* 确保背景铺满整个屏幕 */
  background-size: cover;

  /* 让 #app 至少充满整个视口 */
  min-height: 100vh;
}
</style>
