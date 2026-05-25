from abc import ABC, abstractmethod
from ai_platform.config.resource import get_vector_store ,get_llm
from llama_index.core.memory import Memory, StaticMemoryBlock, FactExtractionMemoryBlock, VectorMemoryBlock


class RagEngine(ABC):
    """RAG查询引擎 - 检索增强生成"""
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    #创建引擎
    @abstractmethod
    def create_engine(self):
        """创建RAG引擎"""
        pass

    #查询
    def query(self, query: str):
        """查询RAG引擎"""
        


#向量检索
class VectorRagEngine(RagEngine):
    """RAG 向量检索引擎实现"""
    def create_engine(self):
        """创建RAG引擎"""
        pass

#混合检索
class HybridRagEngine(RagEngine):
    """RAG 混合检索引擎实现"""
    def create_engine(self):
        """创建RAG引擎"""
        pass

#图检索
class GraphRagEngine(RagEngine):
    """RAG 图检索检索引擎实现"""
    def create_engine(self):
        """创建RAG引擎"""
        pass