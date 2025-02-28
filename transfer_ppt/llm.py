from typing import Any, List
from langchain_community.chat_models import MoonshotChat
# from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
import dotenv

class Chain:
    def __init__(self, steps: List[Any]):
        dotenv.load_dotenv()
        # """初始化链"""
        # self.prompt = ChatPromptTemplate.from_template("""
        # 请生成一个关于“{topic}”的PPT内容，总页数为{page}
        # 1、返回markdown格式, 内容不包括markdown字段
        # 2、直接从markdown格式部分开始，不要有多余的字影响格式
        # """)
        self.prompt = ChatPromptTemplate.from_template("""
            你是一名专业的PPT专家，精通创作PPT，任务是根据主题生成PPT的文案。

            以下是PPT的主题

            {topic},

            ## **任务要求：**
            1. **生成原则**：
                - 按照此主题，进行PPT内容扩展，生成PPT内容,PPT内容需要是中文的。
                - PPT控制在4-6个章节，每一章节至少需要2-3张内容页
                - 内容页的要点控制在2-4个，要点必须有要点明细，要点明细控制在1-3个，要点明细如果多条需要以1、2、区分，且要点明细不宜冗长。
                - 章节和要点不需要数字序号，不需要生成总目录。
                - 核心内容控制在14-16页。

            2. **生成原则**：
                - 输出：请确保仅输出Markdown代码，不包含任何额外解释或文字。

            2. **举例输出**：
                - ```
                # 黄山之美

                ## 黄山概览

                ### 黄山简介

                - 位于中国安徽省南部
                  - 距离省会合肥约300公里
                - 是中国十大名山之一
                  - 以奇松、怪石、云海、温泉四绝著称

                ### 地理位置与气候

                - 海拔1864米
                  - 最高峰为莲花峰
                - 气候特点
                  - 1、四季分明，温差较大
                  - 2、夏季凉爽，冬季寒冷
                ## 奇松

                ### 迎客松

                - 黄山的标志性景观
                  - 1、位于玉屏楼左侧
                  - 2、树龄超过800年
                - 象征意义
                  - 1、迎接四方宾客
                  - 2、体现黄山的热情好客

                ### 黑虎松

                - 位于北海景区
                  - 树形奇特，似黑虎蹲坐
                - 生长环境
                  - 1、高山岩石缝隙中
                  - 2、生存条件极为艰苦
                ```
            """)
        self.llm = MoonshotChat(model="moonshot-v1-8k")
        # self.llm = ChatOllama(model="deepseek-r1:14b")
        self.parser = StrOutputParser()
        self.steps = steps

    def invoke(self, input_data: Any) -> Any:
        """执行链中的每个步骤"""
        for i, step in enumerate(self.steps):
            input_data = step.invoke(input_data)
            print(f"步骤 {i+1}: {step}")
            print(f"输出: {input_data}")
            print("=" * 30)
        return input_data

    def run(self, query: str, page: int):
        """运行完整的链"""
        self.steps = [self.prompt, self.llm, self.parser]  # 确保 steps 正确初始化
        # result = self.invoke({"topic" : query, "page": page})
        result = self.invoke({"topic" : query})
        if "</think>" in result:
            result = result.split("</think>")[1].lstrip()
            print(result)
        if "```markdown" in result:
            result = result.replace("```markdown", "")
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        return result

#
# if __name__ == "__main__":
#     chain = Chain([])
#     output = chain.run("人工只能", 1)
#     print("\n最终输出:", output)
