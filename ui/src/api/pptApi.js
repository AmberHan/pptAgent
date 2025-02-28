import service from "./request";

// 获取文稿内容
export const getContent = (name, count) => {
  return service.get("/ppt/api/get_content", {
    params: { name: name || "1", count },
  });
};

// 上传文件
export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return service.post("/ppt/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

// 生成 PPT 图片
export const generatePPTImages = (content) => {
  return service.post("/ppt/api/convert_ppt_to_images", { content });
};

// PPT模板图片
export const generatePPTFirstImages = (content) => {
  return service.post("/ppt/api/ppt_first_template", { content });
};

// 生成最终 PPT 内容
export const backToFinalContent = (file, content) => {
  return service.post("/ppt/api/ppt_final_content", { file, content });
};
