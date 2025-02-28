# pptAgent

## 目录

- config.py 配置文件
- router.py 路由设置
- ppt_gen.py 生成ppt核心代码
- prompts.py 提示词存放位置
- test_data.py 存放测试数据
- ppt_llm.py 生成markdown以及json转换
- ppt_templates ppt模板存放位置
- runs 上传文档、生成PPT的目录
- ui 前端
- main.py 主函数

## 配置说明

### 1、修改config.py

- LOCAL表示是否使用本地模型，True表示使用本地的, 设置False需要APIKEY
- MODEL表示llm的模型,BASEURL设置代理商的链接；选择本地模型的话, BASEURL = "http://127.0.0.1:11434"

### 2. 执行 ```pip install -r requirements.txt```后，运行main.py
