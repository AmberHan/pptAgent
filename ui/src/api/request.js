import axios from "axios";
import Vue from "vue";

// 创建 axios 实例
const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  timeout: 100000,
});

// 请求拦截器（可选：如果需要 token，可以在这里加）
service.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器（统一处理错误）
service.interceptors.response.use(
  (response) => {
    return response.data; 
  },
  (error) => {
    console.error("请求失败:", error);

    let errorMsg = "请求失败，请稍后重试";
    
    if (error.response) {
      errorMsg = error.response.data?.message || `服务器错误 (${error.response.status})`;
    } else if (error.request) {
      errorMsg = "服务器无响应，请检查网络";
    } else {
      errorMsg = `请求失败: ${error.message}`;
    }

    Vue.prototype.$message.error(errorMsg);

    return Promise.reject({ success: false, message: errorMsg });
  }
);

export default service;
