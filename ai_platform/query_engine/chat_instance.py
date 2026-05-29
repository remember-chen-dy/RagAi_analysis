import threading
from typing import Dict, AsyncGenerator

from ai_platform.query_engine.rag_engine import RagEngineFactory
from ai_platform.services.konwledge_service import knowledge_service
from ai_platform.config.resource import get_llm
from loguru import logger

class RAGEngineCache:
    """线程安全的RAGQueryEngine缓存类"""

    def __init__(self):
        self._cache: Dict[str, RagEngineFactory] = {}
        self._lock = threading.RLock()

    def get_engine(self, session_id: str) -> RagEngineFactory:
        """获取或创建RAGEngineFactory对象"""
        with self._lock:
            if session_id not in self._cache:
                self._cache[session_id] = RagEngineFactory(session_id=session_id)
            return self._cache[session_id]

    def remove_engine(self, session_id: str) -> bool:
        """移除指定session的RAGEngineFactory对象"""
        with self._lock:
            if session_id in self._cache:
                del self._cache[session_id]
                return True
            return False

    def clear_cache(self):
        """清空所有缓存的RAGEngineFactory对象"""
        with self._lock:
            self._cache.clear()

    def get_cache_size(self) -> int:
        """获取当前缓存的RAGEngineFactory对象数量"""
        with self._lock:
            return len(self._cache)


# 全局RAGEngineFactory缓存实例
rag_engine_cache = RAGEngineCache()


class ChatInstance:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.rag_engine_factory = rag_engine_cache.get_engine(session_id)
        self.llm = get_llm()

    async def query(self, query: str, knowledge_base_ids: list = None):
        """
        执行查询，返回查询结果
        """
        # 获取知识库的索引类型
        index_type = "vector"  # 默认类型
        if knowledge_base_ids and len(knowledge_base_ids) > 0:
        # 获取第一个知识库的索引类型（如果有多个知识库，使用第一个的设置）
            kb = await knowledge_service.get_knowledge_base_detail(knowledge_base_ids[0])
            if kb and kb.settings:
                index_type = kb.settings.get("index_type", "vector")

        response = await self.rag_engine_factory.query(
            query=query,          
            index_type=index_type, 
            knowledge_base_ids=knowledge_base_ids,
            similarity_top_k=5
        )
        logger.info(f"ChatInstance query: {query}, response: {response}")
        if response.get('response') == 'Empty Response':
            empty_prompt = (
                "根据用户的问题，知识库中没有检索到相关信息。"
                "请直接根据你的知识回答用户问题，并在回答开头明确说明【以下回答由AI大模型直接生成，未基于知识库内容，仅供参考】。"
                "用户的问题是：{query}"
            )
            prompt = empty_prompt.format(query=query)
            
            llm_response = self.llm.complete(prompt)
            
            # 构建和 query() 返回结构一致的字典
            response = {
                **response,
                "response": llm_response.text
            }

        return response
    
    async def stream_query(
        self, query: str, knowledge_base_ids: list = None
    ) -> AsyncGenerator[str, None]:
        index_type = "vector"
        if knowledge_base_ids and len(knowledge_base_ids) > 0:
            kb = await knowledge_service.get_knowledge_base_detail(knowledge_base_ids[0])
            if kb and kb.settings:
                index_type = kb.settings.get("index_type", "vector")

        async for chunk in self.rag_engine_factory.stream_query(
            query=query,
            index_type=index_type,
            knowledge_base_ids=knowledge_base_ids,
            similarity_top_k=5,
        ):
            yield chunk

    @classmethod
    def clear_session_cache(cls, session_id: str) -> bool:
        """清除指定session的RAGQueryEngine缓存"""
        return rag_engine_cache.remove_engine(session_id)

    @classmethod
    def clear_all_cache(cls):
        """清空所有RAGQueryEngine缓存"""
        rag_engine_cache.clear_cache()

    @classmethod
    def get_cache_info(cls) -> dict:
        """获取缓存信息"""
        return {
            "cached_sessions": rag_engine_cache.get_cache_size(),
            "cache_type": "thread_safe_dict",
            "cached_object": "RAGQueryEngine"
        }

    async def get_chat_history(self, limit: int, offset: int):
        return await self.query_engine.get_chat_history(limit, offset)
