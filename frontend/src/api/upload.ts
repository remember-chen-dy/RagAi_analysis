import type {FileListResponse as FileListResponseType, UploadResponse} from '../types';
import { getAuthHeaders, removeAuthToken } from './auth'
import { API_BASE_URL } from '@/config'

function handleResponse(response: Response): void {
  if (response.status === 401) {
    removeAuthToken()
    window.location.href = '/login'
    throw new Error('登录已过期，请重新登录')
  }
}

interface FileUploadResponse {
  success: boolean
  message: string
  data?: any
}

export class UploadAPI {
  static async uploadFile(
    file: File,
    onProgress?: (progress: number) => void,
    knowledgeBaseId?: string
  ): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('files', file);
    if (knowledgeBaseId) {
      formData.append('knowledge_base_id', knowledgeBaseId);
    }

    const authHeaders = getAuthHeaders()
    const headers: Record<string, string> = {}

    if (authHeaders.Authorization) {
      headers.Authorization = authHeaders.Authorization
    }

    const response = await fetch(`${API_BASE_URL}/files/upload`, {
      method: 'POST',
      headers,
      body: formData,
    });

    handleResponse(response)
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || '文件上传失败');
    }

    return await response.json();
  }

  static async getKnowledgeBases(): Promise<{ success: boolean; data: any[]; message: string }> {
    const response = await fetch(`${API_BASE_URL}/knowledge/list`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    });

    handleResponse(response)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取知识库列表失败');
    }

    return response.json();
  }

  static async getFileList(prefix = '', limit = 50): Promise<FileListResponseType> {
    const params = new URLSearchParams({ prefix, limit: limit.toString() });

    const response = await fetch(`${API_BASE_URL}/files/filelist?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    });

    handleResponse(response)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取文件列表失败');
    }

    const result = await response.json();
    return {
      success: result.success,
      files: result.data?.files || [],
      total: result.data?.total || 0,
    };
  }

  static async deleteFile(objectName: string): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${API_BASE_URL}/files/filedelete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({ object_name: objectName }),
    });

    handleResponse(response)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '删除文件失败');
    }

    return response.json();
  }

  static async getDownloadUrl(
    objectName: string,
    expires = 3600
  ): Promise<{ success: boolean; data: { download_url: string; expires_in: number }; message: string }> {
    const response = await fetch(`${API_BASE_URL}/files/filepreview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({ object_name: objectName }),
    });

    handleResponse(response)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取下载链接失败');
    }

    const result = await response.json();
    return {
      success: result.success,
      data: {
        download_url: result.data?.preview_url || '',
        expires_in: expires,
      },
      message: result.message,
    };
  }

  static async getFileInfo(objectName: string): Promise<{ success: boolean; data: any }> {
    const response = await fetch(`${API_BASE_URL}/files/filepreview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({ object_name: objectName }),
    });

    handleResponse(response)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取文件信息失败');
    }

    return response.json();
  }

  static async getPreviewUrl(objectName: string): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/files/filepreview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({ object_name: objectName }),
    });

    handleResponse(response)
    if (!response.ok) {
      throw new Error('获取预览链接失败');
    }

    const result = await response.json();
    return result.data?.preview_url || '';
  }

  static async getTextContent(objectName: string): Promise<string> {
    const previewUrl = await this.getPreviewUrl(objectName);

    const response = await fetch(previewUrl);
    if (!response.ok) {
      throw new Error('获取文件内容失败');
    }

    return await response.text();
  }

  static isSupportedForPreview(fileName: string): boolean {
    const extension = fileName.split('.').pop()?.toLowerCase();
    const supportedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'txt', 'md'];
    return supportedExtensions.includes(extension || '');
  }
}

export default UploadAPI;
