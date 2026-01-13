const API_BASE_URL = 'http://localhost:8000';

export interface VideoInfo {
  id: string;
  filename: string;
  original_name: string;
  size: number;
  content_type: string;
  path: string;
}

export interface VideosResponse {
  videos: VideoInfo[];
  count: number;
}

export const api = {
  // 获取所有视频列表
  async getVideos(): Promise<VideoInfo[]> {
    const response = await fetch(`${API_BASE_URL}/api/videos`);
    if (!response.ok) {
      throw new Error('获取视频列表失败');
    }
    const data: VideosResponse = await response.json();
    return data.videos;
  },

  // 获取单个视频信息
  async getVideoInfo(videoId: string): Promise<VideoInfo> {
    const response = await fetch(`${API_BASE_URL}/api/videos/${videoId}`);
    if (!response.ok) {
      throw new Error('获取视频信息失败');
    }
    return await response.json();
  },

  // 获取视频流URL
  getVideoStreamUrl(videoId: string): string {
    return `${API_BASE_URL}/api/videos/${videoId}/stream`;
  },
};
