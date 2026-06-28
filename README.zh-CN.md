# Voicebox 中文说明

Voicebox 是一个本地优先的 AI 语音工作室。它可以克隆声音、生成语音、录音转写，也可以通过 MCP 让支持工具调用的智能体用指定声音说话。

项目包含三个主要部分：

- `backend`：FastAPI 后端，负责模型加载、语音生成、转写、任务队列和本地数据管理。
- `app`：Tauri 桌面端共用的 React 前端源码。
- `web`：用于浏览器调试和开发的 Web 前端入口。

## 开发环境

建议在 Windows 上准备以下环境：

- Python 3.12
- Bun 1.x
- Node.js 22 或更高版本
- NVIDIA CUDA 环境，或可用的 CPU 推理环境

后端依赖安装在 `backend\venv` 中。前端依赖安装在项目根目录和工作区包中。

## 启动 Web 开发版

可以直接运行根目录的 PowerShell 脚本：

```powershell
powershell -ExecutionPolicy Bypass -File .\start-web.ps1
```

脚本会打开两个新的 PowerShell 窗口：

- 后端 API：`http://127.0.0.1:17493`
- Web 前端：`http://localhost:5173`

如果希望启动后自动打开浏览器：

```powershell
powershell -ExecutionPolicy Bypass -File .\start-web.ps1 -OpenBrowser
```

## 手动启动

也可以分别启动后端和 Web 前端。

后端：

```powershell
.\backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 17493
```

Web 前端：

```powershell
bun run dev:web
```

## 模型下载源

模型页提供“下载源”切换，支持：

- `HuggingFace`
- `ModelScope`

默认下载源是 `ModelScope`。切换后，后端会把当前选择应用到 HuggingFace Hub 使用的 `HF_ENDPOINT`，后续模型下载会优先连接对应来源。

## 常用检查

前端类型检查：

```powershell
.\node_modules\.bin\tsc.cmd -p .\app\tsconfig.json --noEmit
```

模型下载源单元测试：

```powershell
.\backend\venv\Scripts\python.exe -m pytest .\backend\tests\test_model_source.py
```

查看当前 Git 状态：

```powershell
git status --short
```

## 数据位置

运行数据默认保存在 `data` 目录中，包括 SQLite 数据库、缓存和本地生成记录。模型缓存位置由 HuggingFace Hub、ModelScope 下载源和应用设置共同决定。

## 注意事项

- Web 开发版用于浏览器调试，不等同于 Tauri 桌面版。
- 如果依赖安装被 npm 临时目录卡住，可以先清理 `node_modules` 里的 `.包名-随机串` 临时目录，再重新安装。
- 切换下载源只影响新的下载请求，不会自动迁移已经下载到本地的模型文件。
