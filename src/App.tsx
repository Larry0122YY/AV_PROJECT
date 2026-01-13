import React, { useState, useEffect } from 'react';
import VideoPlayer from './components/VideoPlayer';
import { api, VideoInfo } from './services/api';
import './App.css';

const App: React.FC = () => {
  const [videos, setVideos] = useState<VideoInfo[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<VideoInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    try {
      setLoading(true);
      const videoList = await api.getVideos();
      setVideos(videoList);
      // 自动选择第一个视频
      if (videoList.length > 0) {
        setSelectedVideo(videoList[0]);
      }
      setError(null);
    } catch (err) {
      setError('无法连接到后台服务器，请确保后台服务正在运行 (http://localhost:8000)');
      console.error('加载视频失败:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>视频播放器</h1>
        <p>现代化的 React + TypeScript 视频播放器</p>
      </header>
      <main className="app-main">
        {loading && <div className="loading">加载中...</div>}
        {error && (
          <div className="error">
            <p>{error}</p>
            <button onClick={loadVideos}>重试</button>
          </div>
        )}
        {!loading && !error && videos.length === 0 && (
          <div className="no-videos">
            <p>没有找到视频文件</p>
            <p>请确保视频文件在: D:/download/FX/ 目录下</p>
          </div>
        )}
        {!loading && !error && selectedVideo && (
          <>
            <div className="video-selector">
              <label>选择视频: </label>
              <select
                value={selectedVideo.id}
                onChange={(e) => {
                  const video = videos.find(v => v.id === e.target.value);
                  if (video) setSelectedVideo(video);
                }}
              >
                {videos.map(video => (
                  <option key={video.id} value={video.id}>
                    {video.original_name} ({(video.size / 1024 / 1024).toFixed(2)} MB)
                  </option>
                ))}
              </select>
            </div>
            <VideoPlayer
              src={api.getVideoStreamUrl(selectedVideo.id)}
              poster={undefined}
            />
          </>
        )}
      </main>
    </div>
  );
};

export default App;
