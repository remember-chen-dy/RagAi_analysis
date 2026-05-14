// 文件上传API客户端

import type {FileListResponse as FileListResponseType, UploadResponse} from '../types';
import { getAuthHeaders } from './auth'
import { API_BASE_URL } from '@/config'

interface FileUploadResponse {
  success: boolean
  message: string
  data?: any
}

export class UploadAPI {
  /**
   * 上传单个文件
   */
  static async uploadFile(
    file: File,
    onProgress?: (progress: number) => void,
    knowledgeBaseId?: string
  ): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (knowledgeBaseId) {
      formData.append('knowledge_base_id', knowledgeBaseId);
    }

    // 注意：对于FormData，不要设置Content-Type，让浏览器自动设置
    const authHeaders = getAuthHeaders()
    const headers: Record<string, string> = {}
    
    // 只添加Authorization头，不添加Content-Type
    if (authHeaders.Authorization) {
      headers.Authorization = authHeaders.Authorization
    }

    const response = await fetch(`${API_BASE_URL}/api/files/upload`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || '文件上传失败');
    }

    return await response.json();
  }

  /**
   * 获取可选择的知识库列表
   */
  static async getKnowledgeBases(): Promise<{ success: boolean; data: { knowledge_bases: any[]; total: number }; message: string }> {
    const response = await fetch(`${API_BASE_URL}/api/files/knowledge-bases`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取知识库列表失败');
    }

    return response.json();
  }

  /**
   * 获取文件列表
   */
      static async getFileList(prefix = '', limit = 50): Promise<FileListResponseType> {
    const params = new URLSearchParams({ prefix, limit: limit.toString() });

    const response = await fetch(`${API_BASE_URL}/api/files/list?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取文件列表失败');
    }

    return response.json();
  }

  /**
   * 删除文件
   */
  static async deleteFile(objectName: string): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${API_BASE_URL}/api/files/delete/${encodeURIComponent(objectName)}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '删除文件失败');
    }

    return response.json();
  }

  /**
   * 获取文件下载链接
   */
  static async getDownloadUrl(
    objectName: string,
    expires = 3600
  ): Promise<{ success: boolean; data: { download_url: string; expires_in: number }; message: string }> {
    const params = new URLSearchParams({ expires: expires.toString() });

    const response = await fetch(
      `${API_BASE_URL}/api/files/download/${encodeURIComponent(objectName)}?${params}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取下载链接失败');
    }

    return response.json();
  }

  /**
   * 获取文件信息
   */
  static async getFileInfo(objectName: string): Promise<{ success: boolean; data: any }> {
    const response = await fetch(`${API_BASE_URL}/api/files/info/${encodeURIComponent(objectName)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取文件信息失败');
    }

    return response.json();
  }

  /**
   * 获取文件预览URL（用于图片、PDF等）
   */
  static async getPreviewUrl(objectName: string): Promise<string> {
    try {
      // 直接使用预览接口
      return `${API_BASE_URL}/api/files/preview/${encodeURIComponent(objectName)}`;
    } catch (error) {
      // 如果API不可用，使用下载链接作为备选
      console.warn('预览接口不可用，尝试使用下载链接:', error);
      try {
        const response = await this.getDownloadUrl(objectName);
        if (response.success) {
          return response.data.download_url;
        }
      } catch (downloadError) {
        console.warn('下载链接也不可用:', downloadError);
      }
      
      // 最终备选方案
      return `${API_BASE_URL}/api/files/preview/${encodeURIComponent(objectName)}`;
    }
  }

  /**
   * 获取文本文件内容
   */
  static async getTextContent(objectName: string): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/files/content/${encodeURIComponent(objectName)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
      });
      
      if (!response.ok) {
        if (response.status === 400) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || '不支持的文件类型');
        }
        throw new Error('获取文件内容失败');
      }

      // 后端返回的是纯文本内容
      return await response.text();
    } catch (error) {
      console.warn('API获取文本内容失败，返回模拟内容:', error);
      // 返回模拟内
      return `这是 ${objectName} 的模拟文本内容。

在实际使用中，这里会显示文件的真实内容。

文件名: ${objectName}
当前时间: ${new Date().toLocaleString()}

请确保后端API正确实现了文件内容获取接口。

错误信息: ${error instanceof Error ? error.message : '未知错误'}`;
    }
  }

  /**
   * 检查文件是否支持预览
   */
  static isSupportedForPreview(fileName: string): boolean {
    const extension = fileName.split('.').pop()?.toLowerCase();
    const supportedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'txt', 'md'];
    return supportedExtensions.includes(extension || '');
  }
}

export default UploadAPI; 