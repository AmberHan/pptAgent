import json

from .llm import Chain


def exec_start(content: str, page: int):
    chain = Chain([])
    output = chain.run(content, page)
    return output
    # return create_virtualization_ppt(output)
