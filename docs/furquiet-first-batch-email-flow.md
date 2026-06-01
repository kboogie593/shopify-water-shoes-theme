# FurQuiet First-Batch Email Flow

Updated: 2026-06-01

## Purpose

The first-batch list is the safest conversion path while sample QA, real media, shipping cost, and return policy details are still being verified. It lets FurQuiet collect qualified organic and GEO traffic without pretending the product has verified reviews or complete test proof.

## Lead Sources

Capture first-batch leads from:

- `/pages/first-batch`
- `/pages/routine-finder`
- Newsletter popup
- Footer newsletter
- GEO pages and guide hub
- TikTok, Instagram, Facebook, YouTube Shorts, X, Pinterest UTM links
- AI-search traffic from `/pages/llms` and answer pages

## Tags And Fields

The theme should tag leads with:

- `first_batch`
- `newsletter`
- `routine_*` when the routine finder is used
- `first_src_*`, `last_src_*`, and `last_med_*` from attribution tracking

Hidden fields used by the first-batch page:

- `contact[first_batch_interest]`
- `contact[first_batch_offer]`
- `contact[sample_gate_acknowledged]`

## Sequence

| Step | Timing | Goal | CTA |
|---:|---|---|---|
| 1 | Immediate | Confirm signup and explain the honest launch gate | `/pages/routine-finder` |
| 2 | Day 1 | Teach the quiet-start routine before pitching the product | `/pages/quiet-start-guide` |
| 3 | Day 3 | Explain what sample QA must prove | `/pages/faq` |
| 4 | After sample arrives | Share sample notes and real product media | `/products/furquiet-grooming-vacuum-kit` |
| 5 | Launch window | Move qualified leads to checkout | `/products/furquiet-grooming-vacuum-kit` |

## Claim Boundaries

Do not send:

- Exact decibel claims before repeated measurements.
- Review, rating, or customer-result claims before real reviews exist.
- "Stops shedding" claims.
- "Works for every pet" claims.
- Urgency that suggests inventory or launch timing is verified when it is not.

Use:

- "First-batch interest list."
- "Sample QA before scale."
- "Target price."
- "Launch window."
- "Real sample notes once available."
