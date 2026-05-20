from llama_index.core import Document, SimpleDirectoryReader
from llama_index.readers.file import PDFReader, DocxReader, ImageReader
from loguru import logger


# class JSONReader(BaseReader):
#     """自定义 JSON 文件加载器"""
    
#     def load_data(self, file, extra_info: Optional[Dict] = None) -> List[Document]:
#         with open(file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
        
#         # 将 JSON 转为文本
#         text = json.dumps(data, ensure_ascii=False, indent=2)
        
#         metadata = {"file_type": "json"}
#         if extra_info:
#             metadata.update(extra_info)
        
#         return [Document(text=text, metadata=metadata)]


class DataLoader:
    """数据加载器"""

    @staticmethod
    def load_file_dir(file_paths: list[str]) -> Document:
        """加载文件"""
        # 为不同文件类型指定不同的加载器
        file_extractor = {
            ".pdf": PDFReader(),
            ".docx": DocxReader(),
            ".png": ImageReader(),
            ".jpg": ImageReader(),
            # ".json": JSONReader(),
        }
        reader=SimpleDirectoryReader(
            input_files=file_paths,
            recursive=True,
            file_extractor=file_extractor
        )
        documents=reader.load_data(
            num_workers=4,  # 并行加载，文件越多提速越明显  
            show_progress=True,   # 显示进度条，了解加载状态
        )
        logger.info(f"成功加载 {len(documents)} 个文档")
        return documents

