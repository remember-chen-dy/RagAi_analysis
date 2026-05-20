import re
from typing import Any, List
from llama_index.core.schema import TransformComponent, BaseNode, Document

def clean_single_text(text: str) -> str:
    """清洗单个文本"""
    text = re.sub(r'\s+', ' ', text)
    # 去除特殊字符（保留中英文、数字、常用标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s.,;:!?()[\\]{}"''—-]', '', text)
    # 去除重复标点
    text = re.sub(r'([.,;:!?])\1+', r'\1', text)
    # 去除首尾空白
    text = text.strip()
    return text


class CleanTextTransform:
    """文本清理转换器"""
    def __call__(self, nodes: list[Document], **kwargs: Any) -> list[BaseNode]:
        """清理文本"""
        for node in nodes:
            cleaned_text = clean_single_text(node.text)
            node.set_content(cleaned_text)
            node.metadata['cleaned_text'] = True
        
        return nodes
    

class CleanTextTransformComponent(TransformComponent):
    """文本清理转换组件"""

    def create_pipeline(self,documents: list[Document]) -> list[TransformComponent]:
        """创建转换管道"""

