# Java Audio Courseware — Thinking in Java 4e

基于《Thinking in Java》第四版制作的双语（英文语音 + 中文注释）自动播放课件。

- **Java OOP Foundations**（基础课）：120 页幻灯片，覆盖第 1–9 章（对象、封装、继承、多态、接口、设计模式）
- **Java Advanced Topics**（进阶课）：139 页幻灯片，覆盖第 10–22 章（内部类、容器、异常、字符串、泛型、I/O、并发、GUI）

## 使用方法

无需 Web 服务器，直接用浏览器打开 `index.html`：

1. 在课程选择页面点击任意课程卡片
2. 点击 ▶ 开始播放：英文语音播报，幻灯片随音频自动翻页
3. 底部面板同步显示英文讲稿（上）与中文翻译（下，不播报）

### 播放器快捷键

| 按键 | 功能 |
|------|------|
| Space | 播放 / 暂停 |
| ← / → | 上一页 / 下一页 |
| G | 幻灯片缩略图总览 |
| N | 显示 / 隐藏讲稿文本 |
| F | 全屏 |

> 提示：如浏览器限制本地文件播放音频，可在项目目录运行 `python -m http.server 8080`，然后访问 `http://localhost:8080/index.html`。

## 目录结构

```
├── index.html                      # 课程选择菜单
├── courseware_player/              # 基础课（120 页）
│   ├── index.html                  # 播放器
│   ├── audio/*.mp3                 # 英文语音（本地 XTTS v2 生成）
│   └── img/*.png                   # 幻灯片图片（PowerPoint 导出）
├── courseware_advanced/            # 进阶课（139 页）
│   ├── index.html                  # 播放器
│   ├── audio/*.mp3
│   └── img/*.png
├── player_template.html            # 播放器 HTML 模板
├── build_all.py                    # 播放器构建脚本（读取双语讲稿，生成两个播放器）
├── build_course_menu.py            # 课程选择菜单构建脚本
├── narration/                      # 基础课双语讲稿（英文 + --- Chinese Annotation --- + 中文）
├── narration_advanced/             # 进阶课双语讲稿
├── gen_audio_local.py              # 本地 TTS 音频生成脚本（XTTS v2，GPU 加速）
├── extract_advanced.py             # 从 PPTX 提取讲稿
└── export_advanced.ps1             # 从 PPTX 导出幻灯片图片（PowerPoint COM）
```

## 技术说明

- **语音合成**：Coqui XTTS v2（本地推理，NVIDIA GPU 加速，说话人 "Claribel Dervla"），MP3 96kbps
- **双语讲稿格式**：每页一个 txt 文件，`--- Chinese Annotation ---` 之前是英文（用于 TTS），之后是中文翻译（仅显示）
- **播放器**：单文件 HTML + 原生 JS，音频结束自动翻页，预加载下一页音频

## 重新构建

```bash
# 修改 narration/ 或 narration_advanced/ 中的讲稿后：
python build_all.py
python build_course_menu.py
```
