# lanshu-create-ai-presenter-video

[English](README.md) | **简体中文**

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-111827)](https://agentskills.io)
![Harness Neutral](https://img.shields.io/badge/Harness-Neutral-8B5CF6)
![Provider Neutral](https://img.shields.io/badge/Provider-Neutral-0EA5E9)
[![Validate Skill](https://github.com/cclank/lanshu-create-ai-presenter-video/actions/workflows/validate.yml/badge.svg)](https://github.com/cclank/lanshu-create-ai-presenter-video/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-F4C430.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-Required-007808?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![GitHub stars](https://img.shields.io/github/stars/cclank/lanshu-create-ai-presenter-video?style=flat)](https://github.com/cclank/lanshu-create-ai-presenter-video/stargazers)
[![Follow on X](https://img.shields.io/badge/Follow-@LufzzLiz-000000?logo=x&logoColor=white)](https://x.com/LufzzLiz)

> 一个主题或一份文案，加一张授权人物图，交给你正在用的 AI agent，产出一条经过验收、可直接发布的数字人讲解视频。

`lanshu-create-ai-presenter-video` 是一个 [Agent Skill](https://agentskills.io)（岚叔 · 通用数字人视频制作）。它带领 AI agent 走完数字人视频的全流程：文案、配音、人物生成、口型同步、字幕与关键词动效、剪辑、渲染和质量验收。每个阶段都以磁盘上的产物为准入证据，成片在通过完整解码和响度检查之前不会交付。

## 核心特性

- **不绑定 harness**：标准 `SKILL.md`，可在 Claude Code、Codex、Gemini CLI、Cursor、OpenCode、GitHub Copilot 等支持 Agent Skills 的工具中直接加载；任何能读文件、执行 shell 命令的 agent 也能照着执行。
- **不绑定服务商**：配音、数字人视频、口型同步和语音识别都按能力在运行时选型，每个任务记录实际使用的服务商、模型、参数和任务 ID。
- **配音锁定时间轴**：审定后的完整配音是人物动作、字幕、剪辑点和成片时长的统一时钟，保证口型与段落边界对齐。
- **证据驱动的阶段**：从 `intake` 到 `verified` 共八个阶段，状态由产物计算得出，而不是手工声明。
- **成本护栏**：先做低成本试片；首次付费调用前明确报价；设置重试上限；任务中断时凭任务 ID 恢复，避免重复扣费。
- **交付前验证**：母版与分享版先完成完整解码和响度检查，全部通过才发布。

## 需要提供什么

| 输入 | 必需 | 说明 |
|---|---|---|
| 主题或完整文案 | 是 | 主题会写成 45–75 秒的文案；自带文案保持自然时长。 |
| 人物图 | 是 | 包含一位清晰的成年人物，并已确认使用权。 |
| 声音样本 | 否 | 仅在明确授权克隆时使用，否则选用库存声音并记录。 |
| 辅助素材 | 否 | 屏幕录制、图片、B-roll 或品牌素材，只用在能证明或说明口播内容的地方。 |
| 交付偏好 | 否 | 目标平台、时长、画幅、风格、水印、音乐和结尾引导。 |

## 工作方式

```text
主题或文案 + 授权人物图
        │
        ▼
锁定文案与完整配音 ──► 配音成为全片时钟
        │
        ▼
低成本人物试片
        │
        ▼
生成数字人素材（服务商有时长上限时，按真实停顿分段）
        │
        ▼
按音频时间轴剪辑：字幕、关键词动效、封面、结尾
        │
        ▼
技术验收与画面验收
        │
        ▼
母版、分享版、九宫格与交付报告
```

任务必须具备相应证据才能进入下一阶段，由 `check_state.py` 根据产物计算：

| 阶段 | 所需证据 |
|---|---|
| `intake` | 任务已创建 |
| `content_locked` | 通过的预检报告、文案、节拍表 |
| `audio_locked` | 可解码的最终配音、ASR 报告 |
| `visual_plan_locked` | 时间轴、分镜、已审批的计划 |
| `presenter_generated` | 已记录的数字人能力、选定视频、画面审核 |
| `composition_checked` | 合成检查报告 |
| `rendered` | 同时含音视频、可解码的渲染文件 |
| `verified` | 母版、分享版，以及输出响度达标的交付报告 |

## 运行环境

- 支持 Agent Skills 的 harness，或任何能读文件、执行 shell 命令的 coding agent。
- Python 3.9+、FFmpeg 与 `ffprobe`、Bash、`jq`、`awk`、`sed`。
- 至少一种可调用的配音、数字人视频生成与口型同步能力，云服务 CLI、API 或本地模型均可。
- 可选：HyperFrames 等确定性时间轴合成器，用于字幕、动效和成片渲染。

## 安装

仓库目录本身就是 Skill。把它克隆到所用 harness 的 skills 目录，目录名保持 `lanshu-create-ai-presenter-video`（Agent Skills 规范要求与 Skill 的 `name` 一致）。

| Harness | Skills 目录 | 显式调用 |
|---|---|---|
| Claude Code | `~/.claude/skills/`，或项目内 `.claude/skills/` | `/lanshu-create-ai-presenter-video` |
| Codex | `~/.codex/skills/` | `$lanshu-create-ai-presenter-video` |
| 其他支持 Agent Skills 的工具 | 见该工具文档，[客户端列表](https://agentskills.io/clients)附有各家说明链接 | 按该工具的方式 |

以 Claude Code 为例：

```bash
git clone https://github.com/cclank/lanshu-create-ai-presenter-video.git \
  ~/.claude/skills/lanshu-create-ai-presenter-video
```

在安装目录执行 `git pull` 即可更新。同时使用多个 harness 时，每个 skills 目录各克隆一份。

**不支持 Agent Skills 的 agent**：把仓库克隆到任意位置，在对话开头告诉它：

```text
先阅读 /path/to/lanshu-create-ai-presenter-video/SKILL.md，并严格按其中的流程工作。
```

## 快速开始

多数 harness 会根据 Skill 的描述自动选中它，直接描述想要的视频即可：

```text
把这份文案和人物图做成一条 16:9、30 秒、有实时字幕的数字人讲解视频。
```

想确保命中时，使用上表中的显式调用方式。Skill 会沿用你提问所用的语言。

Agent 会自行调用内置脚本。如需手动建立任务，把 `SKILL_DIR` 指向安装目录：

```bash
SKILL_DIR=~/.claude/skills/lanshu-create-ai-presenter-video

python3 "$SKILL_DIR/scripts/init_job.py" \
  --job-dir ~/Videos/my-presenter-video \
  --presenter-image ~/Pictures/presenter.png \
  --topic "用一分钟讲清楚上下文工程" \
  --duration 60 \
  --aspect 9:16 \
  --rights-confirmed \
  --adult-presenter-confirmed
```

在 `job.json` 中补全人工检查与远程上传许可，然后运行预检：

```bash
python3 "$SKILL_DIR/scripts/preflight.py" ~/Videos/my-presenter-video/job.json
```

每完成一个阶段，在 `job.json` 中登记产物，由检查器计算任务状态：

```bash
python3 "$SKILL_DIR/scripts/check_state.py" ~/Videos/my-presenter-video/job.json --write
```

## 脚本

| 脚本 | 用途 |
|---|---|
| `init_job.py` | 创建自包含的任务目录，把全部输入复制进来，并只记录任务内相对路径。 |
| `preflight.py` | 校验素材、人工检查与授权，区分本地错误和远程生成前的阻塞项。 |
| `plan_segments.py` | 服务商限制单次请求或参考音频时长时，按锁定配音的 ASR 真实停顿规划分段。 |
| `check_state.py` | 根据证据计算任务所处阶段；声明的状态超出证据时返回非零。 |
| `finalize_delivery.sh` | 生成母版与分享版，验证完整解码、交付响度、黑帧与冻帧，全部通过后连同九宫格和报告一起发布。 |

## 参考文档

Agent 只在进入对应阶段时加载相应文档，减少上下文占用。

| 文档 | 内容 |
|---|---|
| [`generation.md`](references/generation.md) | 输入检查、文案与配音、能力选型、付费闸门、分段规划、人物提示词 |
| [`editing.md`](references/editing.md) | 时间轴约定、分段接缝、开场与结尾、字幕、关键词动效、预览与导出 |
| [`qa-recovery.md`](references/qa-recovery.md) | 验收标准，以及口型、人物一致性、接缝、响度和远程任务的故障修复 |

## 目录结构

```text
lanshu-create-ai-presenter-video/
├── SKILL.md                 # Skill 入口：元数据与工作流
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml          # Codex 界面显示信息，其他 harness 会忽略
├── assets/
│   └── job.template.json    # 任务清单模板
├── references/              # 按阶段加载的参考文档
├── scripts/                 # 任务初始化、闸门、分段规划与交付
└── tests/
    └── smoke.sh             # 基于合成素材的端到端测试
```

## 默认设置

| 设置 | 默认值 |
|---|---|
| 画幅 | 9:16、1080×1920、30 fps |
| 时长 | 主题生成 45–75 秒；自带文案保持自然时长 |
| 声音 | 无授权样本时使用库存声音 |
| 结构 | 开场钩子、2–4 个内容节拍、简洁结尾 |
| 音乐与结尾引导 | 默认不加，按需添加 |
| 响度 | −16 LUFS ±0.5 LU，真峰值 ≤ −1 dBTP；可用 `PROGRAM_LUFS` 覆盖 |

## 安全与成本控制

- 任何上传前，先确认图片使用权和人物已成年。
- 克隆声音需要明确授权，绝不根据图片推断声音。
- 首次付费调用前，agent 会说明上传内容、请求时长、已知价格、试片规模和重试上限。
- 服务商有时长上限时，按分段计划的总请求秒数报价。
- 远程任务中断后，先用已保存的任务 ID 查询，再考虑重新提交。
- 连续三个付费候选被否决后停止，并总结反复出现的问题和剩余选项。

## 隐私

- 仓库不包含 API 密钥、访问令牌、签名下载地址或用户素材。
- 服务商请求记录去除凭据与临时 URL 后再保存。
- 预检与交付报告只记录文件名或任务内相对路径，不写入本机绝对路径。

## 测试

冒烟测试用合成素材把一个任务从 `intake` 推进到 `verified`，不调用任何远程服务。需要 FFmpeg、`jq` 与 Python 3.9+：

```bash
bash tests/smoke.sh
```

每次推送和 Pull Request 都会在 CI 中运行元数据校验、可移植性检查和冒烟测试。

## 参与贡献

欢迎提交 Issue 和 Pull Request。特别欢迎反馈在不同 harness、不同服务商下的使用情况，以及对工作流、兼容性和质量检查的改进。

## 作者

由 **岚叔** 创建并维护。欢迎在 X 上关注，获取更新与更多 AI 视频工作流：**[@LufzzLiz](https://x.com/LufzzLiz)**。

## 许可证

基于 [MIT License](LICENSE) 发布。
