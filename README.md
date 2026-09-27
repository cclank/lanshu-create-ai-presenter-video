# lanshu-create-ai-presenter-video

**English** | [简体中文](README.zh-CN.md)

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-111827)](https://agentskills.io)
![Harness Neutral](https://img.shields.io/badge/Harness-Neutral-8B5CF6)
![Provider Neutral](https://img.shields.io/badge/Provider-Neutral-0EA5E9)
[![Validate Skill](https://github.com/cclank/lanshu-create-ai-presenter-video/actions/workflows/validate.yml/badge.svg)](https://github.com/cclank/lanshu-create-ai-presenter-video/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-F4C430.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-Required-007808?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![GitHub stars](https://img.shields.io/github/stars/cclank/lanshu-create-ai-presenter-video?style=flat)](https://github.com/cclank/lanshu-create-ai-presenter-video/stargazers)
[![Follow on X](https://img.shields.io/badge/Follow-@LufzzLiz-000000?logo=x&logoColor=white)](https://x.com/LufzzLiz)

> Turn a topic or script and one authorized portrait into a verified, publish-ready AI presenter video, driven by the coding agent you already use.

`lanshu-create-ai-presenter-video` is an [Agent Skill](https://agentskills.io) that takes an AI agent through the full production of a talking-presenter video: script, narration, presenter generation, lip-sync, captions and keyword motion graphics, editing, rendering, and quality assurance. Every stage is gated by evidence on disk, and nothing is delivered until the output passes decode and loudness checks.

## Highlights

- **Harness-neutral.** A standard `SKILL.md` that loads in Claude Code, Codex, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and other Agent Skills clients. Any agent that can read files and run shell commands can follow it directly.
- **Provider-neutral.** Voice, presenter video, lip-sync, and speech recognition are selected by capability at run time. Each job records the provider, model, parameters, and task IDs it actually used.
- **Audio-locked timeline.** The approved narration is the master clock for presenter motion, captions, cuts, and final duration, which keeps lip-sync and scene boundaries aligned.
- **Evidence-gated workflow.** Eight production states, from `intake` to `verified`, computed from artifacts instead of declared by hand.
- **Cost guardrails.** Pilot-first generation, an explicit billing statement before the first paid call, retry ceilings, and task-ID recovery to avoid duplicate charges.
- **Verified delivery.** Master and share encodes are fully decoded and loudness-checked before any file is published.

## What you provide

| Input | Required | Notes |
|---|---|---|
| Topic or finished script | Yes | A topic becomes a 45–75 second script; a supplied script keeps its natural length. |
| Presenter image | Yes | One clear adult presenter, with confirmed rights to use the image. |
| Voice sample | No | Used only with explicit cloning authorization; otherwise a stock voice is selected and recorded. |
| Supporting media | No | Screen recordings, images, B-roll, or brand assets, used where they prove or clarify a spoken point. |
| Delivery preferences | No | Platform, duration, aspect ratio, style, watermark, music, and call to action. |

## How it works

```text
Topic or script + authorized portrait
        │
        ▼
Lock script and full narration ──► narration becomes the master clock
        │
        ▼
Low-cost presenter pilot
        │
        ▼
Presenter generation (split at real pauses when a provider caps duration)
        │
        ▼
Audio-driven edit: captions, keyword graphics, cover, close
        │
        ▼
Technical and visual QA
        │
        ▼
Master, share copy, contact sheet, and delivery report
```

Each state requires evidence before a job may advance. `check_state.py` computes the state from the job's artifacts:

| State | Evidence required |
|---|---|
| `intake` | Job created |
| `content_locked` | Passing preflight report, script, beat sheet |
| `audio_locked` | Decodable final narration, ASR report |
| `visual_plan_locked` | Timeline, storyboard, approved plan |
| `presenter_generated` | Recorded presenter capability, selected video, visual review |
| `composition_checked` | Composition report |
| `rendered` | Decodable render with video and audio |
| `verified` | Master, share copy, and a delivery report with passing output loudness |

## Requirements

- An Agent Skills harness, or any coding agent that can read files and run shell commands.
- Python 3.9+, FFmpeg with `ffprobe`, Bash, `jq`, `awk`, and `sed`.
- Access to at least one voice synthesis, presenter video generation, and lip-sync capability: a cloud CLI, an API, or a local model.
- Optional: a deterministic timeline compositor such as HyperFrames for captions, motion graphics, and final rendering.

## Installation

The repository directory is the skill. Clone it into your harness's skills directory and keep the folder name `lanshu-create-ai-presenter-video`, which the Agent Skills specification requires to match the skill `name`.

| Harness | Skills directory | Explicit invocation |
|---|---|---|
| Claude Code | `~/.claude/skills/` or project-level `.claude/skills/` | `/lanshu-create-ai-presenter-video` |
| Codex | `~/.codex/skills/` | `$lanshu-create-ai-presenter-video` |
| Other Agent Skills clients | See the client's documentation, linked from the [client list](https://agentskills.io/clients) | Client-specific |

For example, with Claude Code:

```bash
git clone https://github.com/cclank/lanshu-create-ai-presenter-video.git \
  ~/.claude/skills/lanshu-create-ai-presenter-video
```

Run `git pull` in the installed directory to update. If you use several harnesses, clone once into each skills directory.

**Agents without Agent Skills support.** Clone the repository anywhere, then start the session with:

```text
Read /path/to/lanshu-create-ai-presenter-video/SKILL.md and follow its workflow exactly.
```

## Quick start

Most harnesses select the skill automatically from its description, so you can describe the video you want:

```text
Turn this script and portrait into a 30-second 16:9 presenter video with live captions.
```

Use the explicit invocation from the table above to guarantee selection. The skill works in the language of your request.

The agent runs the bundled scripts itself. To set up a job manually, point `SKILL_DIR` at your installation:

```bash
SKILL_DIR=~/.claude/skills/lanshu-create-ai-presenter-video

python3 "$SKILL_DIR/scripts/init_job.py" \
  --job-dir ~/Videos/my-presenter-video \
  --presenter-image ~/Pictures/presenter.png \
  --topic "Context engineering in one minute" \
  --duration 60 \
  --aspect 9:16 \
  --rights-confirmed \
  --adult-presenter-confirmed
```

Complete the manual review and upload approvals in `job.json`, then run preflight:

```bash
python3 "$SKILL_DIR/scripts/preflight.py" ~/Videos/my-presenter-video/job.json
```

After each stage, record its artifacts in `job.json` and let the checker compute the state:

```bash
python3 "$SKILL_DIR/scripts/check_state.py" ~/Videos/my-presenter-video/job.json --write
```

## Scripts

| Script | Purpose |
|---|---|
| `init_job.py` | Creates a self-contained job directory, copies all inputs into it, and records job-relative paths. |
| `preflight.py` | Validates inputs, manual review, and approvals; separates local errors from remote-generation blockers. |
| `plan_segments.py` | Splits the locked narration at real ASR pauses when a provider caps request or reference-audio duration. |
| `check_state.py` | Computes the evidence-backed production state and exits non-zero when the recorded state overclaims. |
| `finalize_delivery.sh` | Builds master and share encodes, verifies full decode, delivered loudness, and black or frozen frames, then publishes them with a contact sheet and report. |

## Reference guides

The agent loads each guide only when it reaches the matching stage, which keeps context usage low.

| Guide | Covers |
|---|---|
| [`generation.md`](references/generation.md) | Intake, script and narration, capability selection, billing gates, segment planning, presenter prompts |
| [`editing.md`](references/editing.md) | Timeline contract, segment seams, openings and closes, captions, keyword graphics, preview and export |
| [`qa-recovery.md`](references/qa-recovery.md) | Acceptance gates and recovery playbooks for lip-sync, identity, seams, loudness, and remote tasks |

## Repository layout

```text
lanshu-create-ai-presenter-video/
├── SKILL.md                 # Skill entry point: metadata and workflow
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml          # Codex display metadata; other harnesses ignore it
├── assets/
│   └── job.template.json    # Job manifest template
├── references/              # Stage guides loaded on demand
├── scripts/                 # Job setup, gates, segment planning, delivery
└── tests/
    └── smoke.sh             # End-to-end test with synthetic media
```

## Defaults

| Setting | Default |
|---|---|
| Format | 9:16, 1080×1920, 30 fps |
| Duration | 45–75 seconds from a topic; natural length for a supplied script |
| Voice | Stock voice unless an authorized sample is provided |
| Structure | Hook, 2–4 content beats, concise close |
| Music and call to action | Off unless requested |
| Loudness | −16 LUFS ±0.5 LU, true peak ≤ −1 dBTP; override with `PROGRAM_LUFS` |

## Safety and cost controls

- Image rights and adult-presenter status are confirmed before any upload.
- Voice cloning requires explicit authorization, and a voice is never inferred from an image.
- Before the first paid call, the agent states the uploads, requested seconds, known price, pilot size, and retry ceiling.
- When a provider caps duration, the quote uses the total requested seconds from the segment plan.
- Interrupted remote tasks are polled by their saved task ID before any resubmission.
- Work stops after three rejected paid candidates, with a summary of the recurring failure and remaining options.

## Privacy

- The repository contains no API keys, access tokens, signed URLs, or user media.
- Provider request records are stored without credentials or expiring URLs.
- Preflight and delivery reports store file names or job-relative paths only, never absolute machine paths.

## Testing

The smoke test drives a synthetic job from `intake` to `verified` without calling any remote service. It requires FFmpeg, `jq`, and Python 3.9+:

```bash
bash tests/smoke.sh
```

CI runs metadata validation, a portability check, and the smoke test on every push and pull request.

## Contributing

Issues and pull requests are welcome. Reports from different harnesses and providers are especially valuable, as are improvements to the workflow, compatibility, and quality checks.

## Author

Created and maintained by **岚叔 (Lanshu)**. Follow on X for updates and new AI video workflows: **[@LufzzLiz](https://x.com/LufzzLiz)**.

## License

Released under the [MIT License](LICENSE).
