from llama_index.core import Document, SimpleDirectoryReader
from llama_index.readers.file import PDFReader, DocxReader, ImageReader, MarkdownReader
from loguru import logger
from llama_index.core.base.llms.types import MessageRole, ChatMessage
import dashscope
from typing import List, Optional, Dict
import base64
import os
from pathlib import Path
import fitz

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from loguru import logger
# from ai_platform.config.resource import get_vl_client
from llama_index.multi_modal_llms.dashscope import (
    DashScopeMultiModal,
    DashScopeMultiModalModels,
)
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls

class MyPDFReader(BaseReader):
    """自定义 PDF 文件加载器，支持文本提取和图片识别"""
    
    def __init__(
        self,
        enable_image_recognition: bool = True,
    ):
        self.enable_image_recognition = enable_image_recognition
        # self._vl_client = get_vl_client()
    
    def _resolve_image(self, image_bytes: bytes, page_num: int, img_index: int) -> str:

        try:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            # message = ChatMessage(
            #     role=MessageRole.USER,
            #     content=[
            #         {"image": f"data:image/png;base64,{base64_image}"},
            #         {"text": "请详细描述这张图片的内容"},
            #     ],
            # )
            # response = self.vl_client.chat([message])
            # image_urls = [
            #     "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
            # ]

            # image_documents = load_image_urls(image_urls)

            # dashscope_multi_modal_llm = DashScopeMultiModal(
            #     model_name=DashScopeMultiModalModels.QWEN_VL_MAX,
            #     api_key=os.getenv("DASHSCOPE_APIKEY"),
            # )
            # response = dashscope_multi_modal_llm.complete(
            # prompt="请详细描述这张图片的内容?",
            # image_documents=image_documents,
            # )
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            messages = [
            {
                "role": "user",
                "content": [
                {"image": f"data:image/png;base64,{base64_image}"},
                {"text": "请仅输出图像中的文本内容。"}]
            }]
            response = dashscope.MultiModalConversation.call(
                #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
                api_key = 'sk-59c734d97ba447dc9983c2987c32c83d',
                model = 'qwen3-vl-8b-instruct',
                messages = messages
            )
            
            logger.info(f'{img_index} 张图片成功 {response.output.choices[0].message.content[0]["text"]}')
            # result_text = ""
            # if hasattr(response, 'message') and hasattr(response.message, 'content'):
            #     content = response.message.content
            #     if isinstance(content, str):
            #         result_text = content
            #     elif isinstance(content, list):
            #         for block in content:
            #             if isinstance(block, dict) and 'text' in block:
            #                 result_text += block['text']
            
            # if result_text:
            #     logger.info(f"识别第 {page_num} 页第 {img_index} 张图片成功")
            #     return result_text
            return response.output.choices[0].message.content[0]["text"]
            
        except Exception as e:
            logger.error(f"识别第 {page_num} 页第 {img_index} 张图片失败: {e}")
            return ""
    
    def load_data(
        self,   
        file: str,
        extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """
        加载 PDF 文件
        
        Args:
            file: PDF 文件路径
            extra_info: 额外的元数据信息
            
        Returns:
            Document 对象列表
        """
        if not os.path.exists(file):
            raise FileNotFoundError(f"PDF 文件不存在: {file}")
        
        logger.info(f"开始加载 PDF 文件: {file}")
        
        documents = []
        doc = fitz.open(file)
        total_pages = len(doc)
        
        # 基础元数据
        base_metadata = {
            "file_type": "pdf",
            "file_name": os.path.basename(file),
            "total_pages": total_pages,
        }
        if extra_info:
            base_metadata.update(extra_info)
        
        try:
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                page_index = page_num + 1
                
                # 提取文本
                text = page.get_text("text")
                if text.strip():
                    documents.append(Document(
                        text=text.strip(),
                        metadata={
                            **base_metadata,
                            "page_number": page_index,
                            "content_type": "text",
                        }
                    ))
                
                # 提取并识别图片
                image_list = page.get_images(full=True)
                if image_list:
                    logger.info(f"  第 {page_index} 页发现 {len(image_list)} 张图片")
                    
                    for img_index, img in enumerate(image_list):
                        try:
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            # 识别图片内容
                            image_description = self._resolve_image(
                                image_bytes, page_index, img_index + 1
                            )
                            
                            if image_description:
                                documents.append(Document(
                                    text=image_description,
                                    metadata={
                                        **base_metadata,
                                        "page_number": page_index,
                                        "content_type": "image_description",
                                        "image_index": img_index + 1,
                                    }
                                ))
                                
                        except Exception as e:
                            logger.error(f"处理第 {page_index} 页图片 {img_index + 1} 失败: {e}")
                            continue
            
            doc.close()
            logger.info(f"PDF 加载完成，共生成 {len(documents)} 个文档")
            
        except Exception as e:
            doc.close()
            logger.error(f"加载 PDF 文件失败: {e}")
            raise
        
        return documents

class DataLoader:
    """数据加载器"""
    
    @staticmethod
    def load_file_dir(file_paths: List[str]) -> List[Document]:
        """加载文件"""
        # 为不同文件类型指定不同的加载器
        file_extractor = {
            ".pdf": MyPDFReader(),
            ".docx": DocxReader(),
            ".png": ImageReader(),
            ".jpg": ImageReader(),
            '.md': MarkdownReader(),
            # ".json": JSONReader(),
        }
        reader=SimpleDirectoryReader(   
            input_files=file_paths,
            recursive=True,
            file_extractor=file_extractor
        )
        documents = reader.load_data(
            num_workers=4,
            show_progress=True,
        )
        logger.info(f"成功加载 {len(documents)} 个文档")
        return documents

