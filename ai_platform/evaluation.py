import os
import uuid
import asyncio
import warnings
from typing import List, Dict, Optional

from pydantic import BaseModel, Field
from loguru import logger

from llama_index.core import Document as LlamaIndexDocument
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from ragas import aevaluate, EvaluationDataset, SingleTurnSample
    from ragas.metrics import (
        Faithfulness,
        AnswerRelevancy,
        ContextPrecision,
        ContextRecall,
    )
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.testset import TestsetGenerator

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from ai_platform.query_engine.chat_instance import ChatInstance
from ai_platform.config.resource import get_vector_store, get_llm, get_embedding


class EvaluationRequest(BaseModel):
    knowledge_base_ids: List[str] = Field(description="知识库ID列表")
    index_type: str = Field(default="vector", description="索引类型: vector, hybrid")
    testset_size: int = Field(default=5, description="自动生成的测试集大小")
    similarity_top_k: int = Field(default=5, description="检索返回数量")
    metrics: List[str] = Field(
        default=["faithfulness", "answer_relevancy", "context_precision", "context_recall"],
        description="评估指标列表",
    )


class EvaluationResult(BaseModel):
    samples: List[dict] = Field(description="各样本详细结果")
    aggregate_scores: Dict[str, float] = Field(description="整体得分汇总")
    knowledge_base_ids: List[str] = Field(description="评测的知识库")
    index_type: str = Field(description="索引类型")
    sample_count: int = Field(description="样本数量")


class RagasEvaluator:

    def __init__(self):
        self._eval_llm = None
        self._eval_embeddings = None

    @property
    def eval_llm(self):
        if self._eval_llm is None:
            base_url = os.getenv(
                "DASHSCOPE_OPENAI_BASE_URL",
                "https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            api_key = os.getenv("DASHSCOPE_APIKEY")
            self._eval_llm = LangchainLLMWrapper(
                ChatOpenAI(
                    model="qwen-max",
                    openai_api_key=api_key,
                    openai_api_base=base_url,
                    temperature=0,
                )
            )
        return self._eval_llm

    @property
    def eval_embeddings(self):
        if self._eval_embeddings is None:
            api_key = os.getenv("DASHSCOPE_APIKEY")
            base_url = os.getenv(
                "DASHSCOPE_OPENAI_BASE_URL",
                "https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            self._eval_embeddings = LangchainEmbeddingsWrapper(
                OpenAIEmbeddings(
                    model="text-embedding-v2",
                    openai_api_key=api_key,
                    openai_api_base=base_url,
                )
            )
        return self._eval_embeddings

    def _get_metrics(self, metric_names: List[str]):
        available = {
            "faithfulness": Faithfulness(),
            "answer_relevancy": AnswerRelevancy(),
            "context_precision": ContextPrecision(),
            "context_recall": ContextRecall(),
        }
        return [available[n] for n in metric_names if n in available]

    async def _fetch_kb_documents(
        self, knowledge_base_ids: List[str]
    ) -> List[LlamaIndexDocument]:
        vector_store = get_vector_store()
        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key="knowledge_base_id",
                    value=knowledge_base_ids,
                    operator=FilterOperator.IN,
                )
            ]
        )
        all_nodes = await vector_store.aget_nodes(filters=filters)
        logger.info(f"从向量库获取到 {len(all_nodes)} 个节点")

        docs = []
        for node in all_nodes:
            text = node.get_content()
            if not text or not text.strip():
                continue
            metadata = dict(node.metadata) if node.metadata else {}
            docs.append(LlamaIndexDocument(text=text, metadata=metadata))

        logger.info(f"转换为 {len(docs)} 个 LlamaIndex Document")
        return docs

    async def _generate_testset(
        self, documents: List[LlamaIndexDocument], testset_size: int
    ) -> List[dict]:
        li_llm = get_llm()
        li_embedding = get_embedding()

        generator = TestsetGenerator.from_llama_index(
            llm=li_llm,
            embedding_model=li_embedding,
        )

        logger.info(f"开始生成测试集, 目标 {testset_size} 条, 文档数 {len(documents)}")

        testset = await asyncio.to_thread(
            generator.generate_with_llamaindex_docs,
            documents=documents,
            testset_size=testset_size,
        )

        eval_dataset = testset.to_evaluation_dataset()
        logger.info(f"测试集生成完成, 共 {len(eval_dataset.samples)} 条")

        samples = []
        for sample in eval_dataset.samples:
            samples.append({
                "question": sample.user_input,
                "ground_truth": sample.reference or "",
                "reference_contexts": sample.reference_contexts or [],
            })

        return samples

    async def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        logger.info(
            f"开始RAGAS评估: 知识库 {request.knowledge_base_ids}, "
            f"类型: {request.index_type}, 测试集大小: {request.testset_size}"
        )

        li_docs = await self._fetch_kb_documents(request.knowledge_base_ids)
        if not li_docs:
            raise ValueError("知识库中没有可用的文档数据，无法生成测试集")

        test_samples = await self._generate_testset(li_docs, request.testset_size)
        logger.info(f"测试集生成完成, 共 {len(test_samples)} 条样本")

        query_results = []
        async for i, sample in enumerate(test_samples):
            try:
                result = await self._query_sample(
                    question=sample["question"],
                    ground_truth=sample["ground_truth"],
                    knowledge_base_ids=request.knowledge_base_ids,
                    index_type=request.index_type,
                    similarity_top_k=request.similarity_top_k,
                )
                query_results.append(result)
                logger.info(f"样本 {i + 1}/{len(test_samples)} 查询完成")
            except Exception as e:
                logger.error(f"样本 {i + 1} 查询失败: {e}")
                query_results.append({
                    "question": sample["question"],
                    "ground_truth": sample["ground_truth"],
                    "answer": "",
                    "contexts": [],
                    "error": str(e),
                })

        aggregate_scores = await self._compute_aggregate_scores(
            query_results, request.metrics
        )

        return EvaluationResult(
            samples=query_results,
            aggregate_scores=aggregate_scores,
            knowledge_base_ids=request.knowledge_base_ids,
            index_type=request.index_type,
            sample_count=len(test_samples),
        )

    async def _query_sample(
        self,
        question: str,
        ground_truth: Optional[str],
        knowledge_base_ids: List[str],
        index_type: str,
        similarity_top_k: int,
    ) -> dict:
        session_id = str(uuid.uuid4())
        chat_instance = ChatInstance(session_id=session_id)

        result = await chat_instance.stream_query(
            query=question,
            knowledge_base_ids=knowledge_base_ids,
        )

        answer = result.get("response", "")
        contexts = []
        for src in result.get("source", []):
            content = src.get("content", "")
            if content:
                contexts.append(content)

        return {
            "question": question,
            "ground_truth": ground_truth,
            "answer": answer,
            "contexts": contexts,
        }

    async def _compute_aggregate_scores(
        self,
        query_results: List[dict],
        metric_names: List[str],
    ) -> Dict[str, float]:
        valid_results = [r for r in query_results if "error" not in r]
        if not valid_results:
            logger.warning("没有有效的查询结果，无法计算评估分数")
            return {}

        samples = []
        for r in valid_results:
            sample = SingleTurnSample(
                user_input=r["question"],
                response=r["answer"],
                retrieved_contexts=r["contexts"],
            )
            if r.get("ground_truth"):
                sample.reference = r["ground_truth"]
            samples.append(sample)

        dataset = EvaluationDataset(samples=samples)
        metrics = self._get_metrics(metric_names)

        if not metrics:
            logger.warning("没有有效的评估指标")
            return {}

        logger.info(f"开始RAGAS aevaluate, 共 {len(samples)} 个样本, {len(metrics)} 个指标")

        try:
            result = await aevaluate(
                dataset=dataset,
                metrics=metrics,
                llm=self.eval_llm,
                embeddings=self.eval_embeddings,
            )
        except Exception as e:
            logger.error(f"RAGAS aevaluate 失败: {e}")
            return {}

        scores: Dict[str, float] = {}
        try:
            df = result.to_pandas()
            metric_cols = [c for c in df.columns if c in metric_names]
            for col in metric_cols:
                vals = df[col].dropna()
                if len(vals) > 0:
                    scores[col] = round(float(vals.mean()), 4)
        except Exception as e:
            logger.error(f"计算聚合分数失败: {e}")

        logger.info(f"RAGAS评估完成: {scores}")
        return scores


ragas_evaluator = RagasEvaluator()
