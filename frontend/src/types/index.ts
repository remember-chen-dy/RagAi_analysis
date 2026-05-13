export interface UploadFile {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
  progress: number;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  data?: {
    file_id: string;
    original_filename: string;
    download_url: string;
    file_size: number;
    content_type: string;
    upload_time: string;
    bucket_name: string;
    object_name: string;
  };
}


export interface FileInfo {
  object_name: string;
  size: number;
  last_modified: string;
  content_type?: string;
  etag: string;
}

export interface FileListResponse {
  success: boolean;
  files: FileInfo[];
  total: number;
} 