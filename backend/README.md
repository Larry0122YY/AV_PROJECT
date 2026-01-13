# 视频播放器后台 API

使用 FastAPI 构建的 Python 后台服务。

## 功能

- 📤 视频文件上传
- 📋 视频列表获取（自动扫描目录）
- 📹 视频流传输（支持范围请求）
- 🗑️ 视频删除
- 🔍 视频信息查询

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 配置视频目录

### 方法 1: 使用环境变量（推荐）

创建 `.env` 文件（复制 `.env.example` 并修改）：

```bash
# Windows
VIDEO_DIR=D:/download/FX

# Linux/Mac
VIDEO_DIR=/home/user/videos
```

### 方法 2: 直接修改代码

编辑 `main.py` 文件，修改第 26 行：

```python
VIDEO_DIR_STR = os.getenv("VIDEO_DIR", "你的视频文件夹路径")
```

### 方法 3: 设置系统环境变量

**Windows:**
```cmd
set VIDEO_DIR=D:\download\FX
```

**Linux/Mac:**
```bash
export VIDEO_DIR=/home/user/videos
```

## 运行服务器

```bash
python main.py
```

或者使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务器将在 `http://localhost:8000` 启动。

启动时会显示视频目录路径，确认是否正确。

## API 文档

启动服务器后，访问以下地址查看自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

- `GET /` - 根路径，检查服务状态
- `GET /api/videos` - 获取所有视频列表（自动扫描目录）
- `GET /api/videos/{video_id}` - 获取单个视频信息
- `POST /api/videos/upload` - 上传视频文件
- `GET /api/videos/{video_id}/stream` - 视频流传输
- `DELETE /api/videos/{video_id}` - 删除视频

## 视频存储

- 视频文件存储在配置的 `VIDEO_DIR` 目录下
- 支持自动扫描目录中的所有视频文件（.mp4, .avi, .mov, .mkv, .webm, .flv, .wmv）
- 视频信息存储在 `videos.json` 文件中
