# FurQuiet Attribution and UTM Plan

Updated: 2026-06-01

## Purpose

The $10K/month target needs channel-level evidence, not just content output. The theme now captures first-touch and last-touch attribution in the browser and attaches it to Shopify contact/newsletter submissions.

If a visitor has rejected the cookie banner, the theme clears this attribution store, removes attribution hidden fields, and does not inject attribution fields on future page loads.

Captured fields:

- `traffic_first_source`
- `traffic_first_medium`
- `traffic_first_landing`
- `traffic_last_source`
- `traffic_last_medium`
- `traffic_campaign`
- `traffic_referrer`
- `traffic_snapshot`

Newsletter forms with `contact[tags]` also receive tags such as:

- `first_src_tiktok`
- `last_src_instagram`
- `last_med_organic_social`
- `camp_quiet_start_week1`

## Source Classification

The script classifies:

- TikTok, Instagram, Facebook, YouTube, X, Pinterest as `organic_social`.
- Google, Bing, DuckDuckGo, Yahoo, Ecosia as `organic_search`.
- ChatGPT/OpenAI, Perplexity, Claude, Gemini, Copilot as `ai_search`.
- Other external domains as `referral`.
- No referrer and no UTM as `direct`.

## UTM Standard

Use lowercase values with hyphens or underscores.

Required fields for every organic content link:

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content`

Optional:

- `utm_term` for SEO/GEO experiments.

Example:

```text
/pages/quiet-start-guide?utm_source=tiktok&utm_medium=organic_social&utm_campaign=quiet_start_week1&utm_content=fur_cup_hook
```

## Weekly Review

Every week, combine Shopify form submissions and platform analytics into:

- `data/furquiet-organic-channel-scoreboard.csv`
- `data/furquiet-comment-to-content-log.csv`

Review questions:

1. Which platform created first-touch email capture?
2. Which guide page created the highest email capture rate?
3. Which post created add-to-cart traffic?
4. Which repeated comments should become guide updates?
5. Which sources produced no qualified action and should be deprioritized?

## Limits

- This is not a full analytics replacement.
- It does not prove revenue attribution until checkout/orders are live.
- It depends on Shopify accepting custom contact fields and tags in the relevant forms.
- It should be paired with Shopify analytics, Search Console, and platform analytics once the site is live.
