# FurQuiet Social Asset Guide

Updated: 2026-06-01

## Generated Assets

| Asset | Size | Use |
|---|---:|---|
| `assets/furquiet-social-quiet-start-story.jpg` | 1080x1920 | TikTok, Instagram Reels cover, YouTube Shorts thumbnail, Pinterest Idea Pin |
| `assets/furquiet-social-fur-cup-story.jpg` | 1080x1920 | Fur-cup proof hook, kit tour cover, product page retargeting creative |
| `assets/furquiet-social-apartment-story.jpg` | 1080x1920 | Apartment pet hair control hook, Reels cover, Facebook Reels cover |
| `assets/furquiet-guide-hub-og.jpg` | 1200x630 | Guide hub OG image, X link card, Facebook link preview, blog cover |
| `assets/furquiet-video-quiet-start.mp4` | 720x1280 | Placeholder vertical video for quiet-start posts |
| `assets/furquiet-video-fur-cup-proof.mp4` | 720x1280 | Placeholder vertical video for fur-cup proof posts |
| `assets/furquiet-video-apartment-pet-hair.mp4` | 720x1280 | Placeholder vertical video for apartment pet hair posts |

## Usage Rules

- Use these as launch placeholders until real sample footage is filmed.
- The MP4 files are motion placeholders generated from the approved cover art with a subtle zoom.
- Do not present AI-assisted product imagery as customer proof.
- Replace with real sample photos after supplier QA passes.
- Keep the same sage, cream, and clay palette across all short-form covers.
- Every cover should link to either the FurQuiet kit or one specific guide page.

## First Cover Mapping

| Content Angle | Cover Asset | Destination |
|---|---|---|
| Quiet-start routine | `furquiet-social-quiet-start-story.jpg` | `/pages/quiet-start-guide` |
| Fur cup proof | `furquiet-social-fur-cup-story.jpg` | `/products/furquiet-grooming-vacuum-kit` |
| Apartment pet hair | `furquiet-social-apartment-story.jpg` | `/pages/apartment-pet-hair-control` |
| Guide hub | `furquiet-guide-hub-og.jpg` | `/pages/grooming-guides` |

## Regeneration

Run:

```bash
python3 scripts/generate_furquiet_social_videos.py
```

The script requires `ffmpeg` and regenerates the three MP4 placeholder videos from the 1080x1920 cover images.

## Replacement Criteria

Replace each cover when the real sample provides:

- A clear tool-in-use frame.
- A visible fur cup result.
- A pet reaction frame that does not show stress.
- A clean room or sofa before-after frame.
- Product labels and accessories that match the Shopify product page.
