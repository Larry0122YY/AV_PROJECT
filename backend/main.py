from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil
from pathlib import Path
import json
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

app = FastAPI(title="视频播放器后台API")

# 配置 CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 视频存储目录
# 方式1: 从环境变量读取（推荐）
# 设置环境变量: VIDEO_DIR=D:/download/FX
# 或者在 .env 文件中设置: VIDEO_DIR=D:/download/FX
video_path = r"D:\download\FX"
video_path = r"F:\video"
video_path = r"F:\video\佳品\开端"
VIDEO_DIR_STR = os.getenv("VIDEO_DIR", video_path)  # 默认路径

# 方式2: 直接在这里修改路径（如果不想用环境变量）
# VIDEO_DIR_STR = "D:/download/FX"  # Windows 路径
# VIDEO_DIR_STR = "/home/user/videos"  # Linux/Mac 路径
# VIDEO_DIR_STR = "C:/Users/YourName/Videos"  # 其他路径

VIDEO_DIR = Path(VIDEO_DIR_STR)
VIDEO_DIR.mkdir(exist_ok=True)

print(f"视频目录设置为: {VIDEO_DIR.absolute()}")

# 视频信息存储文件（存储在项目目录下）
VIDEO_INFO_FILE = Path("videos.json")  # 存储在 backend 目录下

def load_videos_info():
    """加载视频信息"""
    if VIDEO_INFO_FILE.exists():
        with open(VIDEO_INFO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_videos_info(videos):
    """保存视频信息"""
    with open(VIDEO_INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

@app.get("/")
async def root():
    """根路径"""
    return {"message": "视频播放器后台API", "status": "running"}

@app.get("/api/videos")
async def get_videos():
    """获取所有视频列表（自动扫描目录中的视频文件）"""
    # 自动扫描目录中的视频文件
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
    scanned_videos = []
    
    if VIDEO_DIR.exists() and VIDEO_DIR.is_dir():
        for video_file in VIDEO_DIR.iterdir():
            if video_file.is_file() and video_file.suffix.lower() in video_extensions:
                video_id = video_file.stem
                # 检查是否已存在
                existing = next((v for v in scanned_videos if v["id"] == video_id), None)
                if not existing:
                    scanned_videos.append({
                        "id": video_id,
                        "filename": video_file.name,
                        "original_name": video_file.name,
                        "size": video_file.stat().st_size,
                        "content_type": "video/mp4",  # 默认类型
                        "path": f"/api/videos/{video_id}/stream"
                    })
    
    # 合并已上传的视频信息
    saved_videos = load_videos_info()
    # 合并列表，避免重复
    all_videos = saved_videos.copy()
    for scanned in scanned_videos:
        if not any(v["id"] == scanned["id"] for v in all_videos):
            all_videos.append(scanned)
    
    return {"videos": all_videos, "count": len(all_videos)}

@app.get("/api/videos/{video_id}")
async def get_video_info(video_id: str):
    """获取单个视频信息"""
    videos = load_videos_info()
    video = next((v for v in videos if v["id"] == video_id), None)
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    return video

@app.post("/api/videos/upload")
async def upload_video(file: UploadFile = File(...)):
    """上传视频文件"""
    # 检查文件类型
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="只能上传视频文件")
    
    # 生成唯一文件名
    file_ext = Path(file.filename).suffix
    video_id = f"{len(load_videos_info()) + 1}_{Path(file.filename).stem}"
    video_filename = f"{video_id}{file_ext}"
    video_path = VIDEO_DIR / video_filename
    
    # 保存文件
    try:
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    
    # 保存视频信息
    videos = load_videos_info()
    video_info = {
        "id": video_id,
        "filename": video_filename,
        "original_name": file.filename,
        "size": video_path.stat().st_size,
        "content_type": file.content_type,
        "path": f"/api/videos/{video_id}/stream"
    }
    videos.append(video_info)
    save_videos_info(videos)
    
    return {
        "message": "上传成功",
        "video": video_info
    }

@app.get("/api/videos/{video_id}/stream")
async def stream_video(video_id: str, request: Request):
    """视频流传输（支持范围请求，用于视频播放）"""
    # 先尝试从保存的列表中查找
    videos = load_videos_info()
    video = next((v for v in videos if v["id"] == video_id), None)
    
    # 如果没找到，尝试直接通过文件名查找
    if not video:
        # 尝试查找文件（支持多种扩展名）
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
        for ext in video_extensions:
            video_path = VIDEO_DIR / f"{video_id}{ext}"
            if video_path.exists():
                video = {
                    "id": video_id,
                    "filename": video_path.name,
                    "original_name": video_path.name,
                    "content_type": "video/mp4"
                }
                break
    
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    
    video_path = VIDEO_DIR / video["filename"]
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="视频文件不存在")
    
    # 检测 MIME 类型
    content_type = video.get("content_type", "video/mp4")
    if video_path.suffix.lower() == '.mp4':
        content_type = "video/mp4"
    elif video_path.suffix.lower() == '.webm':
        content_type = "video/webm"
    elif video_path.suffix.lower() == '.avi':
        content_type = "video/x-msvideo"
    
    # 获取文件大小
    file_size = video_path.stat().st_size
    
    # 支持范围请求（Range requests），这对视频播放很重要
    range_header = request.headers.get('range')
    
    if range_header:
        # 解析范围请求
        try:
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if len(range_match) > 1 and range_match[1] else file_size - 1
            
            # 确保范围有效
            if start < 0:
                start = 0
            if end >= file_size:
                end = file_size - 1
            if start > end:
                raise HTTPException(status_code=416, detail="Range Not Satisfiable")
            
            # 计算内容长度
            content_length = end - start + 1
            
            # 使用生成器函数进行流式传输，避免一次性读取大文件
            def generate_chunks():
                chunk_size = 8192  # 8KB 块大小
                with open(video_path, 'rb') as f:
                    f.seek(start)
                    remaining = content_length
                    while remaining > 0:
                        read_size = min(chunk_size, remaining)
                        chunk = f.read(read_size)
                        if not chunk:
                            break
                        yield chunk
                        remaining -= len(chunk)
            
            # 返回部分内容响应（流式传输）
            return StreamingResponse(
                generate_chunks(),
                status_code=206,  # Partial Content
                headers={
                    'Content-Range': f'bytes {start}-{end}/{file_size}',
                    'Accept-Ranges': 'bytes',
                    'Content-Length': str(content_length),
                    'Content-Type': content_type,
                },
                media_type=content_type
            )
        except (ValueError, IndexError) as e:
            # 如果范围请求格式错误，返回整个文件
            pass
    # 没有范围请求或解析失败，使用流式传输返回整个文件
    # 对于大文件，使用 StreamingResponse 避免一次性加载到内存
    def generate_file():
        chunk_size = 8192  # 8KB 块大小
        with open(video_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    return StreamingResponse(
        generate_file(),
        status_code=200,
        headers={
            'Accept-Ranges': 'bytes',
            'Content-Length': str(file_size),
            'Content-Type': content_type,
        },
        media_type=content_type
    )

@app.delete("/api/videos/{video_id}")
async def delete_video(video_id: str):
    """删除视频"""
    videos = load_videos_info()
    video = next((v for v in videos if v["id"] == video_id), None)
    
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    
    # 删除文件
    video_path = VIDEO_DIR / video["filename"]
    if video_path.exists():
        video_path.unlink()
    
    # 从列表中移除
    videos = [v for v in videos if v["id"] != video_id]
    save_videos_info(videos)
    
    return {"message": "删除成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
