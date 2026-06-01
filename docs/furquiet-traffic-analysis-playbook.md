# FurQuiet Traffic Analysis Playbook

Updated: 2026-06-01

## Purpose

The $10K/month target needs a weekly operating model, not just more content. This playbook links organic social, GEO pages, email capture, add-to-cart behavior, and revenue so the next content batch can be prioritized by evidence.

## Funnel Model

Run the base case:

```bash
python3 scripts/analyze_furquiet_funnel.py
```

Run low or high cases:

```bash
python3 scripts/analyze_furquiet_funnel.py --mode low
python3 scripts/analyze_furquiet_funnel.py --mode high
```

The model reads `data/furquiet-channel-funnel-model.csv` and estimates:

- monthly sessions
- email captures
- add to carts
- orders
- revenue
- gap to the $10K/month target
- channel priorities by revenue per content unit and readiness

## Weekly Inputs

Update `data/furquiet-organic-channel-scoreboard.csv` every week from:

- Shopify analytics: sessions, add to carts, orders, revenue.
- Shopify customer/contact exports: email captures and attribution tags.
- TikTok, Instagram, Facebook, YouTube, X, and Pinterest analytics: content published, clicks, saves, comments, shares.
- Google Search Console: guide page impressions, clicks, queries, and indexed pages.
- AI-search referral/referrer evidence: ChatGPT, Perplexity, Claude, Gemini, Copilot, and other answer engines.

## Decision Rules

- If a channel creates sessions but no email capture, send that traffic to a more specific guide or first-batch CTA.
- If a guide captures email but produces no add-to-cart behavior, add product proof, kit contents, sample QA, or buying checklist links.
- If a channel has high saves/comments but low clicks, create a direct reply video and pin the matching guide URL.
- If a query appears in Search Console more than twice and has a clear objection, update the relevant GEO page and add one short-video script.
- If a channel has low readiness because sample footage is missing, do not scale output volume there until the sample arrives.

## Current Base-Case Reading

The starting model intentionally does not assume paid ads, fake reviews, or viral outliers. It treats TikTok, Instagram, YouTube Shorts, Facebook, X, Pinterest, GEO pages, and email as separate organic surfaces.

Base case from `2026-06-01`:

- Sessions: 13,960/month.
- Email captures: 1,161/month.
- Orders: 98.7/month.
- Revenue: $8,783/month.
- Gap to target: $1,217/month.

The current model says the fastest gap-closing paths are not more generic posts. They are:

- Build the email list so first-batch campaigns can convert.
- Produce Instagram/Reels-ready original media rather than repost-only clips.
- Create live Shopify page handles for the GEO cluster and submit the sitemap.
- Pair YouTube Shorts titles with the exact guide URLs for kit contents, noise, breed pages, and buying checklist queries.

Re-run the model after the first real seven days of traffic and replace assumptions with observed sessions, email captures, add-to-cart rate, and order conversion rate.
