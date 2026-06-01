#!/usr/bin/env python3
"""Generate placeholder FurQuiet short-form videos from approved cover art."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

VIDEOS = [
    {
        "source": "assets/furquiet-social-quiet-start-story.jpg",
        "output": "assets/furquiet-video-quiet-start.mp4",
        "duration": 6,
    },
    {
        "source": "assets/furquiet-social-fur-cup-story.jpg",
        "output": "assets/furquiet-video-fur-cup-proof.mp4",
        "duration": 6,
    },
    {
        "source": "assets/furquiet-social-apartment-story.jpg",
        "output": "assets/furquiet-video-apartment-pet-hair.mp4",
        "duration": 6,
    },
]


def run_ffmpeg(source: Path, output: Path, duration: int) -> None:
    frames = duration * 24
    filtergraph = (
        "scale=900:-1,"
        "zoompan="
        "z='min(zoom+0.0009,1.055)':"
        f"d={frames}:"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':"
        "s=720x1280:"
        "fps=24,"
        "format=yuv420p"
    )
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-loop",
        "1",
        "-i",
        str(source),
        "-t",
        str(duration),
        "-vf",
        filtergraph,
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "23",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    for video in VIDEOS:
        source = ROOT / video["source"]
        output = ROOT / video["output"]
        if not source.exists():
            raise FileNotFoundError(source)
        run_ffmpeg(source, output, int(video["duration"]))
        print(f"generated {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
