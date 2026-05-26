import re
from typing import Any, List
from llama_index.core.schema import TransformComponent, BaseNode, Document
from llama_index.core.node_parser import SemanticSplitterNodeParser, LangchainNodeParser
from ai_platform.config.setting import KnowledgeBaseSettings
from llama_index.core.ingestion import IngestionPipeline
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai_platform.config.resource import get_embedding
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


class CleanTextTransform(TransformComponent):
    """文本清理转换器"""
    def __call__(self, nodes: List[Document], **kwargs: Any) -> List[BaseNode]:
        """清理文本"""
        for node in nodes:
            cleaned_text = clean_single_text(node.text)
            node.set_content(cleaned_text)
            node.metadata['cleaned_text'] = True
        return nodes
    

class TransformerComponent:
    """文本清理转换组件"""
    def __init__(self, settings: KnowledgeBaseSettings):
        self.nodes = CleanTextTransform()
        self.settings = settings


    def create_pipeline(self,documents: List[Document]) -> IngestionPipeline:
        """创建转换管道"""
        tansformations:List[TransformComponent]=[self.nodes]

        if self.settings.text_split_strategy == 'semantic':
            tansformations.append(
                SemanticSplitterNodeParser(
                    buffer_size=7,
                    breakpoint_percentile_threshold=90,
                    embed_model=get_embedding(),
                )
            )
        if self.settings.text_split_strategy == 'fixed_chars':
            #使用Langchain的递归字符文本分割器进行分割文本
            tansformations.append(
                LangchainNodeParser(
                    RecursiveCharacterTextSplitter(
                        separators=self.settings.split_chars,
                        chunk_size=self.settings.chunk_size,
                        chunk_overlap=self.settings.chunk_overlap,
                    )
                )
            )
        
        pipeline = IngestionPipeline(
            documents=documents,
            transformations=tansformations
        )
        return pipeline

