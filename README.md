# 视频播放器

一个使用 TypeScript 和 React.js 构建的现代化视频播放器。

## 功能特性

- 🎬 视频播放/暂停控制
- ⏯️ 进度条拖拽
- 🔊 音量控制
- 🔇 静音功能
- ⏩ 播放速度调节（0.5x - 2x）
- 🖥️ 全屏播放
- 📱 响应式设计
- 🎨 现代化 UI 设计

## 技术栈

- React 18
- TypeScript
- Vite
- CSS3

## 安装和运行

1. 安装依赖：
```bash
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

3. 构建生产版本：
```bash
npm run build
```

4. 预览生产版本：
```bash
npm run preview
```

## 使用说明

视频播放器组件支持以下属性：

- `src`: 视频源地址（字符串）
- `poster`: 视频封面图片（字符串，可选）
- `autoPlay`: 自动播放（布尔值，默认 false）
- `controls`: 显示控制栏（布尔值，默认 true）

示例：
```tsx
<VideoPlayer
  src="your-video-url.mp4"
  poster="your-poster-image.jpg"
  autoPlay={false}
  controls={true}
/>
```

## 浏览器支持

支持所有现代浏览器（Chrome, Firefox, Safari, Edge）。
