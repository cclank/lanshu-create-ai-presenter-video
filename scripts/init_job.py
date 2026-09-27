#!/usr/bin/env python3
"""Create a non-overwriting presenter-video job from minimal inputs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "job.template.json"
JOB_DIRECTORIES = (
    "docs",
    "assets/source",
    "assets/audio/reference",
    "assets/audio/raw",
    "assets/audio/final",
    "assets/video/candidates",
    "assets/video/selected",
    "assets/video/render",
    "assets/captions",
    "qa/requests",
    "qa/asr",
    "qa/contacts",
    "qa/reports",
    "renders",
    "outputs",
)
ASPECT_DEFAULTS = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
}


def existing_file(path_text: str, label: str) -> Path:
    path = Path(path_text).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"{label} does not exist or is not a file: {path}")
    return path


def copy_into_job(source: Path, job_dir: Path, relative_dir: str) -> str:
    """Copy an input into the job and return its job-relative path."""
    destination_dir = job_dir / relative_dir
    destination = destination_dir / source.name
    counter = 2
    while destination.exists():
        destination = destination_dir / f"{source.stem}-{counter}{source.suffix}"
        counter += 1
    shutil.copy2(source, destination)
    return destination.relative_to(job_dir).as_posix()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "presenter-video"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-dir", required=True)
    parser.add_argument("--presenter-image", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--topic")
    source.add_argument("--script", help="Existing local script file")
    parser.add_argument("--voice-sample")
    parser.add_argument("--supporting-media", action="append", default=[])
    parser.add_argument("--language", default="auto")
    parser.add_argument("--audience", default="general")
    parser.add_argument("--duration", type=float, default=60.0)
    parser.add_argument("--aspect", choices=sorted(ASPECT_DEFAULTS), default="9:16")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--fps", type=int, choices=(24, 25, 30, 50, 60), default=30)
    parser.add_argument("--style", default="credible contemporary presenter")
    parser.add_argument("--watermark", default="")
    parser.add_argument("--cta", default="")
    parser.add_argument("--rights-confirmed", action="store_true")
    parser.add_argument("--adult-presenter-confirmed", action="store_true")
    parser.add_argument("--remote-upload-approved", action="store_true")
    parser.add_argument("--voice-clone-approved", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 5 <= args.duration <= 1800:
        raise ValueError("--duration must be between 5 and 1800 seconds")
    if (args.width is None) != (args.height is None):
        raise ValueError("--width and --height must be supplied together")

    width, height = ASPECT_DEFAULTS[args.aspect]
    if args.width is not None and args.height is not None:
        width, height = args.width, args.height
        if min(width, height) < 256 or max(width, height) > 7680:
            raise ValueError("custom dimensions must be between 256 and 7680 pixels")

    presenter_image = existing_file(args.presenter_image, "presenter image")
    script = existing_file(args.script, "script") if args.script else None
    voice_sample = (
        existing_file(args.voice_sample, "voice sample") if args.voice_sample else None
    )
    supporting_media = [
        existing_file(item, "supporting media") for item in args.supporting_media
    ]

    job_dir = Path(args.job_dir).expanduser().resolve()
    if job_dir.exists() and any(job_dir.iterdir()):
        raise ValueError(f"job directory must be absent or empty: {job_dir}")
    job_dir.mkdir(parents=True, exist_ok=True)
    for relative in JOB_DIRECTORIES:
        (job_dir / relative).mkdir(parents=True, exist_ok=True)

    # Copy inputs so the job stays self-contained and portable; originals stay untouched.
    manifest = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    manifest["job_id"] = slugify(job_dir.name)
    manifest["input"]["topic"] = (args.topic or "").strip()
    manifest["input"]["script_path"] = (
        copy_into_job(script, job_dir, "assets/source") if script else ""
    )
    manifest["input"]["presenter_image"] = copy_into_job(
        presenter_image, job_dir, "assets/source"
    )
    manifest["input"]["voice_sample"] = (
        copy_into_job(voice_sample, job_dir, "assets/audio/reference")
        if voice_sample
        else ""
    )
    manifest["input"]["supporting_media"] = [
        copy_into_job(item, job_dir, "assets/source") for item in supporting_media
    ]
    manifest["input"]["rights_confirmed"] = args.rights_confirmed
    manifest["input"]["adult_presenter_confirmed"] = args.adult_presenter_confirmed
    manifest["input"]["remote_upload_approved"] = args.remote_upload_approved
    manifest["input"]["voice_clone_approved"] = args.voice_clone_approved

    creative = manifest["creative"]
    creative.update(
        {
            "language": args.language,
            "audience": args.audience,
            "duration_target_s": args.duration,
            "aspect": args.aspect,
            "width": width,
            "height": height,
            "fps": args.fps,
            "style": args.style,
            "watermark": args.watermark,
            "cta": args.cta,
        }
    )

    job_path = job_dir / "job.json"
    job_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"job": str(job_path), "state": "intake"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
