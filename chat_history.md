
## 2026-06-28 启动项目

- 用户：启动项目，之前已经setup了
- 助手：查看项目结构和启动脚本，准备按根目录主开发脚本启动项目。


## 2026-06-28 启动进展

- 发现：just 未安装，un run dev 进入 Tauri 启动后报缺少 motion/react。
- 处理：将 pp/src/components/ShinyText.tsx 的导入改为已有依赖 ramer-motion。
- 注意：Tauri/Cargo 继续启动会联网更新 Rust 依赖索引，已停止避免继续下载。


## 2026-06-28 启动结果

- 已启动：后端 http://127.0.0.1:17493，Web 前端 http://localhost:5173/。
- 验证：后端 /health 返回 200，app TypeScript 检查通过。
- 未执行：桌面 Tauri 版继续启动，因为会触发 Cargo 联网更新 Rust 依赖索引。


## 2026-06-28 浏览器报错排查

- 用户：报错，自己看浏览器
- 助手：准备检查浏览器页面、控制台和网络错误。


## 2026-06-28 用户确认安装依赖

- 用户：你来执行
- 助手：执行 un install --frozen-lockfile 补齐前端依赖，随后重启并验证浏览器。


## 2026-06-28 确认清理依赖临时目录

- 用户：允许删除临时目录并继续安装
- 助手：删除 npm 临时残留目录，继续补齐依赖并重启验证。


## 2026-06-28 依赖修复与浏览器验证结果

- 已清理 npm 临时残留目录。
- 已补齐前端运行缺失依赖。
- 已恢复 web/vite.config.ts 的 React 插件配置。
- 验证：TypeScript 检查通过，前端 http://localhost:5173/ 正常渲染，后端 /health 正常。


## 2026-06-28 提交并新增下载源切换功能

- 用户：先commit，然后加一个功能，切换模型下载源：HF、MS
- 助手：先检查当前变更并提交，再实现 HF/ModelScope 下载源切换。


## 2026-06-28 模型下载源切换功能完成

- 已实现：模型页新增下载源切换，支持 HF 和 ModelScope。
- 后端：新增下载源设置字段、迁移、进程级 HuggingFace endpoint 应用逻辑。
- 验证：新增后端单测通过，前端 TypeScript 检查通过，接口读写通过，浏览器可见切换控件。


## 2026-06-28 默认源、启动脚本和中文 README

- 默认模型下载源改为 ModelScope。
- 新增 start-web.ps1，用于启动后端 API 和 Web 前端。
- 新增 README.zh-CN.md 中文说明。
- 验证：模型下载源单测、前端 TypeScript、PowerShell 脚本语法均通过。


## 2026-06-28 更新日志和 About 页面

- 版本号更新为 0.5.1。
- CHANGELOG 顶部新增中文 0.5.1 更新内容。
- About 页面新增增强者 patdelphi，并把项目 GitHub 链接指向 patdelphi/pat-voicebox。

