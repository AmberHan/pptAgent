from telnetlib import OUTMRK
from typing import Any

from anyio import sleep_forever
from langchain_community.chat_models import MoonshotChat
from langchain_community.output_parsers.ernie_functions import JsonOutputFunctionsParser, OutputFunctionsParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
import dotenv


class MarkdownToJsonConverter:
    def __init__(self, model_name="moonshot-v1-8k", debug=False):
        dotenv.load_dotenv()
        self.debug = debug  # 是否启用调试模式
        # self.prompt = ChatPromptTemplate.from_template("""
        # 你是一名专业的Markdown解析与JSON转换专家，任务是将给定的Markdown内容精准转换为特定的JSON格式。
        # ## **任务要求：**
        # 1. **层级映射**：
        #    - `#`（一级标题） → `title`
        #    - `##`（二级标题） → `sections.sectionTitle`
        #    - `###`（三级标题） → `sections.slides.title`
        #    - `####`（四级标题） → `sections.slides.contents.title`
        #    - `-`（列表项） → `sections.slides.contents.contents`
        # 2. **严格遵循JSON格式**：
        #    - 解析后的JSON结构必须与示例一致，字段名称、嵌套层级不得变动。
        #    - `contents` 字段始终是数组，存储子内容或文本。
        # 3. **输出要求**：
        #    - 仅返回转换后的JSON，不要额外的文本说明或解释。
        #    - JSON必须符合标准格式，确保结构清晰且无语法错误。
        #
        # **Markdown 内容：**
        # {query}
        # """)
        self.prompt = """
        你是一名专业的Markdown解析与JSON转换专家，任务是将给定的Markdown内容精准转换为特定的JSON格式。
        ## **任务要求：**
        1. **层级映射**：
           - `#`（一级标题） → `title`
           - `##`（二级标题） → `sections.sectionTitle`
           - `###`（三级标题） → `sections.slides.title`
           - `####`（四级标题） → `sections.slides.contents.title`
           - `-`（列表项） → `sections.slides.contents.contents`
        2. **严格遵循JSON格式**：
           - 解析后的JSON结构必须与示例一致，字段名称、嵌套层级不得变动。
           - `contents` 字段始终是数组，存储子内容或文本。
        3. **输出要求**：
           - 仅返回转换后的JSON，不要额外的文本说明或解释，不需要json样式符号。
           - JSON必须符合标准格式，确保结构清晰且无语法错误。

        3. **举例输出**：
        ```
        {
            "title": "大模型概述",
            "sections": [
                {
                    "sectionTitle": "大模型的定义与特点",
                    "slides": [
                        {
                            "title": "定义",
                            "contents": [
                                {
                                    "title": "参数量巨大",
                                    "contents": ["通常包含数亿甚至数十亿个参数"]
                                },
                                {
                                    "title": "需要训练",
                                    "contents": ["目的是通过大规模数据训练，提高模型的泛化能力和性能"]
                                }
                            ]
                        },
                        {
                            "title": "特点",
                            "contents": [
                                {
                                    "title": "参数量庞大",
                                    "contents": ["训练和推理需要强大的计算资源"]
                                },
                                {
                                    "title": "数据需求高",
                                    "contents": ["需要大量高质量的数据进行训练", "能够处理多样化的任务和场景"]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        ```
        """

        self.llm = MoonshotChat(model=model_name)
        self.parser = JsonOutputParser()  # 解析 LLM 输出为 JSON


    def convert(self, markdown_text: str) -> dict:
        """将Markdown转换为JSON"""
        # formatted_prompt = self.prompt.format(query=markdown_text)
        messages = [
            (
                "system",
                self.prompt,
            ),
            ("human", markdown_text),
        ]


        llm_response = self.llm.invoke(messages)
        json_result = self.parser.invoke(llm_response)

        if self.debug:
            print(llm_response)
        return json_result


    def generate_final_content(self, markdown_input):
        converter = MarkdownToJsonConverter(debug=True)  # 设为 True 启用调试信息
        output_json = converter.convert(markdown_input)
        return output_json
