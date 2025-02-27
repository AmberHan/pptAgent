# pptAgent

## 目录

- config.py 配置文件
- router.py 路由设置
- ppt_gen.py ppt 生成ppt核心代码
- prompts.py ppt 提示词存放位置
- test_data.py ppt 存放部分测试数据
- ppt_llm.py 生成markdown文案以及json转换
- ppt_templates ppt模板存放位置
- runs 程序运行保存文件位置
- main.py 主函数

## 配置说明

1. 修改config.py

- LOCAL表示是否使用本地模型，True表示使用本地的, 设置False需要APIKEY
- 修改SERVER_PORT，改为server映射端口，（与nginx配置的代理端口需一致）。

2. 执行 ```pip install -r requirements.txt```后，运行main.py
