from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, String, DateTime, Integer, Text, JSON, ForeignKey, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import UUID

Base = declarative_base()

#知识库表
class KnowledgeBase(Base):
    """知识库表"""
    __tablename__ = "knowledge_base"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,comment="知识库ID")
    name = mapped_column(String, index=True,comment="知识库名称")
    description = mapped_column(String,nullable=True,comment="知识库描述")
    status = mapped_column(String(20),default="active",nullable=False,comment="知识库状态 active, inactive, building")
    #知识库设置
    settings = mapped_column(JSON,nullable=True,default=lambda: {
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'text_split_strategy': 'fixed_chars', #fixed_chars, semantic
        'split_chars': ['\n\n', '\n', '。', '！', '？', '；'],
        'index_type': 'vector'  # vector, hybrid, graph
    },comment="知识库设置")
    create_time = mapped_column(DateTime, default=datetime.now,comment="创建时间")
    update_time = mapped_column(DateTime, onupdate=datetime.now,comment="更新时间")

    files=relationship("KnowledgeBaseFile",back_populates="knowledge_base")

    
#文件表
class KnowledgeBaseFile(Base):
    """知识库文件表"""
    __tablename__ = "knowledge_base_file"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,comment="文件ID")
    knowledge_base_id = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_base.id"), nullable=False,comment="知识库ID")
    filename = mapped_column(String(255), nullable=False,comment="文件名")
    original_filename = mapped_column(String(255), nullable=False,comment="原始文件名")
    file_path = mapped_column(String(512), nullable=False,comment="文件路径")
    file_size = mapped_column(BigInteger, nullable=False,comment="文件大小")
    file_type = mapped_column(String(100), nullable=False,comment="文件类型")
    mime_type = mapped_column(String(100), nullable=True,comment="文件MIME类型")
    #文件元数据
    file_metadata = mapped_column(JSON, nullable=True, default=dict,comment="文件元数据")
    #文件处理状态
    is_processed = mapped_column(Boolean, default=False, nullable=False,comment="文件是否处理完成")
    status = mapped_column(String(20), default='pending', nullable=False,comment="文件处理状态")  # pending, processing, completed, failed

    knowledge_base = relationship("KnowledgeBase", back_populates="files")