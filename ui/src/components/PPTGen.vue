<template>
  <div style="display: flex;  flex-wrap: wrap;">
    <loading :active.sync="isLoading" :can-cancel="false" :on-cancel="onCancel" color="#40a9ff"
      :is-full-page="fullPage">
    </loading>
    <a-card title="PPT生成选项" class="cardUse">
      <div style="display: flex; flex-wrap: wrap; padding-top: 10px; width: 600px;">
        <!-- 第一行 -->
        <div style="display: flex; width: 100%; align-items: center; margin-bottom: 10px;">
          <a-button type="primary" style="background: green; margin-right: 20px;" v-if="false">上传pdf</a-button>
          <a-upload-dragger name="file" :multiple="false" :action="baseUrl"
            :accept="`.docx,.pdf`" style="width:150px" @change="handleChange_upload">
            <p class="ant-upload-drag-icon">
              <a-icon type="inbox" />
            </p>
            <p class="ant-upload-text">
              点击或者拖拽上传
            </p>
            <p class="ant-upload-hint">
              word 或者 pdf上传
            </p>
          </a-upload-dragger>
          <span style="margin-left: 20px;font-size: large;color: white;">或</span>
          <a-button type="primary" v-if="false">上传ppt</a-button>
          <a-input placeholder="请输入主题:" style="width: 300px; margin-left: 20px;" v-model="name" />


        </div>

        <div style="margin-top:20px">
          <!-- <div style="display: flex; align-items: center; width: 100%; margin-top: 20px;" v-if="percent == 100"> -->
          <span style="font-size: 19px; color: white;">请选择ppt模板:</span>
        </div>
        <div style="display: flex; width: 100%; align-items: center; margin-bottom: 10px;">
          <div id="ppt-container">
            <div class="image-card" v-for="(image, index) in pptImagesTemplate" :key="index">
              <!-- <img v-for="(image, index) in pptImages" :key="index" :src="image" :class="{ 'active': index === currentIndex }" /> -->
              <img :src="image" :key="index" @click="getPPTTempTemplateClick(image)" />
            </div>
          </div>
          <img :src="this.imageChoose" :key="index" style="width: 40%;" />
        </div>
        <!-- </div> -->
        <!-- 第二行，将请输入页数放到右侧 -->
        <div
          style="display: flex; align-items: center; width: 80%; margin-top: 20px; margin-left: 15px; justify-content: end;">
          <div style="display: flex; align-items: center;" v-if="false">
            <span style="font-size: 19px; color: white;">请输入页数：</span>
            <a-select :size="size" default-value="1" style="width: 120px; margin-right: 1px;" @change="handleChange">
              <a-select-option v-for="i in 25" :key="i">
                {{ i }}
              </a-select-option>
            </a-select>
          </div>
          <a-button type="primary" style="margin-left:20px;" @click="generateContent">生成文稿</a-button>
          <a-button type="primary" style="background-color: #35495e;margin-left:20px"
            @click="generatePPT">点击生成ppt</a-button>
        </div>
      </div>
    </a-card>

    <a-card title="文稿内容" class="cardUse2">


      <mavon-editor :toolbars="{ 'fullscreen': true }" v-model="contentUse" />
      <a-progress :stroke-color="{
        from: 'yellow',
        to: 'green',
      }" :percent="percent" status="active" style="width: 70%;margin-top:60px;margin-bottom: 60px;"
        v-if="percent != 0" />

    </a-card>
    <a-modal title="PPT预览" :visible="visible" :confirm-loading="confirmLoading" @ok="handleOk" @cancel="handleCancel"
      :maskClosable="false" :destroyOnClose="true" ok-text="下载PPT" cancel-text="取消" style="z-index: 100;"
      @after-close="handleCancel">
      <div id="ppt-container2" v-if="percent == 100">
        <div class="image-card" v-for="(image, index) in pptImages" :key="index">
          <!-- <img v-for="(image, index) in pptImages" :key="index" :src="image" :class="{ 'active': index === currentIndex }" /> -->
          <img :src="image" :key="index" @click="getPPTTemp(index)" />
        </div>
      </div>
    </a-modal>


  </div>

</template>
<!-- generatePPTImages -->
<script>
import { getContent, generatePPTFirstImages, backToFinalContent } from '@/api/pptApi'; // 引入 API 方法
import { mavonEditor } from 'mavon-editor';
import 'mavon-editor/dist/css/index.css';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
export default {
  components: {
    mavonEditor,
    Loading
  },

  created() {
    this.generatePPTTemplate()
    this.baseUrl = process.env.VUE_APP_API_BASE_URL + `/ppt/upload`
  },
  data() {
    return {
      pptImages: [], size: 'default', name: "", count: "1", loading: false, percent: 0, contentUse: "", isLoading: false, markdownContent: `
# 标题
这是 **加粗** 的文字，这是 *斜体* 的文字。

- 列表项 1
- 列表项 2

[百度](https://www.baidu.com)
      `,
      ModalText: 'Content of the modal',
      visible: false,
      confirmLoading: false,
      defaultFileList: [],
      fileUploadSuccess: false,
      pptImagesTemplate: [],
      imageChoose: "",
      deep: 0,
      baseUrl:""
      // mode: 'default', // or 'simple'
    };
  },
  methods: {
    handleChange(value) {
      this.count = value

    },
    showModal() {
      this.visible = true;
    },
    handleOk() {
      window.open(process.env.VUE_APP_API_BASE_URL + "/static/final.pptx");  // 你的后端下载地址

    },
    getPPTTempTemplateClick(image) {
      // alert(image)
      this.imageChoose = image
    },
    handleCancel(e) {
      console.log(e);
      this.visible = false;
      this.pptImages = [];    // 清空PPT图片列表
      this.percent = 0;       // 进度重置
    },
    async generateContent() {
      if (!this.fileUploadSuccess && this.name === "") {
        this.$message.warning('文件上传和主题内容均为空，无法进行操作！');
        return;
      }
      this.isLoading = true;
      try {
        const response = await getContent(this.name, this.count);
        this.contentUse = response.content;
      } catch (error) {
        console.error('Error fetching content:', error);
      } finally {
        this.isLoading = false;
      }
    },
    handleChange_upload({ file, fileList }) {
      if (fileList.length > 1) {
        fileList.splice(0, 1); // 移除多余的文件
      }
      this.name = ""
      if (file.status !== 'uploading') {
        console.log(file, fileList);
      }
      if (fileList.length != 0) {
        this.fileUploadSuccess = true
      } else {
        this.fileUploadSuccess = false
      }
    },
    getPPTTemp(val) {
      alert(val)
    },
    async generatePPT() {
      this.pptImages = []
      this.isLoading = true
      if (this.contentUse == "") {
        this.isLoading = false
        return;
      }
      try {
        const response = await backToFinalContent(this.imageChoose.replace("first_pages", "模板2").replace("png", "pptx"), this.contentUse);
        this.pptImages = response.images;
        this.percent = 100;
        this.visible = true;
        this.isLoading = false;
      } catch (error) {
        this.isLoading = false;
      }
    },
    async generatePPTTemplate() {
      try {
        const response = await generatePPTFirstImages();
        this.pptImagesTemplate = response.images;
        this.imageChoose = this.pptImagesTemplate[0]

      } catch (error) {
        console.error('Error generating PPT images:', error);
      }
    }
  },
  beforeDestroy() {
  },
};
</script>
<style>
#ppt-container {
  margin-top: 20px;
  background-color: aliceblue;
  /* margin: 20px auto; */
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  /* 2列布局 */
  gap: 10px;
  /* 图片之间的间距 */
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  max-width: 30%;
  max-height: 350px;
  /* 限制最大宽度 */
  margin-left: 10px;
  margin-right: 60px;
  /* 让整个容器居中 */
  overflow: auto;
}

#ppt-container2 {
  background-color: aliceblue;
  margin: 20px auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  /* 2列布局 */
  gap: 10px;
  /* 图片之间的间距 */
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  max-width: 100%;
  max-height: 400px;
  /* 限制最大宽度 */
  margin-left: 10px;
  /* 让整个容器居中 */
  overflow: auto;
}

.ant-card-bordered.cardUse {
  background: linear-gradient(135deg, rgba(200, 120, 200, 0.6), rgba(230, 170, 210, 0.4));
  border-radius: 10px;
  /* 圆角 */
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* 添加阴影 */
  transition: background 0.5s ease-in-out;
  /* 平滑过渡效果 */
  /* margin: auto; */
  top: 20px;
  left: 20px;
  width: 40%;
  min-height: 400px;
}

.ant-card-bordered.cardUse2 {
  background: linear-gradient(135deg, rgba(200, 120, 200, 0.6), rgba(230, 170, 210, 0.4));
  border-radius: 10px;
  /* 圆角 */
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* 添加阴影 */
  transition: background 0.5s ease-in-out;
  /* 平滑过渡效果 */
  /* margin: auto; */
  top: 20px;
  margin-left: 40px;
  width: 55%;
  min-height: 400px;
}

/* 图片外层卡片 */
.image-card {
  width: 100%;
  /* aspect-ratio: 1 / 1; */
  /* 强制卡片为正方形 */
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* padding: 10px; */
  /* text-align: center; */
  transition: transform 0.3s ease-in-out;
  /* display: flex; */
  /* align-items: center; */
  /* justify-content: center; */
}

/* 悬停放大效果 */
.image-card:hover {
  transform: scale(1.05);
  /* 鼠标悬停时略微放大 */
}

/* 图片样式 */
.image-card img {
  width: 100%;
  /* 图片填充格子 */
  /* max-width: 300px; */
  /* 最大宽度 */
  border-radius: 5px;
  /* 圆角 */
  display: block;
  /* 避免额外间距 */
  margin: 0;
  /* 居中 */
}

.ant-card-head-title {
  color: white;
  flex: none;
}

.v-note-wrapper.shadow {
  z-index: 100;
}

.ant-modal {
  width: 1000px !important;
}
</style>
