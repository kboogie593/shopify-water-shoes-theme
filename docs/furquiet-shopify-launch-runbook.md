# FurQuiet Shopify Launch Runbook

Updated: 2026-06-01

## Current Shopify State

- Store: `wxat5u-e3` / Shopify Admin test store.
- Product created: `FurQuiet Grooming Vacuum Kit`.
- Product admin URL: `https://admin.shopify.com/store/wxat5u-e3/products/8964334616745`
- GitHub repo pushed: `https://github.com/kboogie593/shopify-water-shoes-theme`
- Product image upload is blocked until the Codex Chrome Extension has file URL access enabled.

## Fix Product Media Upload

Enable Chrome extension file URL permission:

1. Open `chrome://extensions`.
2. Click **Details** under the Codex extension.
3. Enable **Allow access to file URLs**.
4. Return to the product page.
5. Upload these files:
   - `assets/furquiet-product-hero-ai.jpg`
   - `assets/furquiet-kit-flatlay-ai.jpg`
   - `assets/furquiet-grooming-lifestyle-ai.jpg`
   - `assets/furquiet-clean-home-ai.jpg`

Until this is fixed, the theme product template still has fallback gallery assets, but the Shopify product itself has no native product media.

## Create Required Pages

Create these Shopify pages and assign the matching theme template:

| Title | Handle | Template |
|---|---|---|
| First Batch | `first-batch` | `page.first-batch` |
| Sample QA Log | `sample-qa-log` | `page.sample-qa-log` |
| Grooming Guides | `grooming-guides` | `page.grooming-guides` |
| Routine Finder | `routine-finder` | `page.routine-finder` |
| Quiet Start Guide | `quiet-start-guide` | `page.quiet-start-guide` |
| Pet Grooming Vacuum for Shedding Dogs | `pet-grooming-vacuum-for-shedding-dogs` | `page.pet-grooming-vacuum-for-shedding-dogs` |
| Husky Grooming Vacuum Guide | `husky-grooming-vacuum` | `page.husky-grooming-vacuum` |
| Long-Hair Cat Grooming Vacuum Guide | `long-hair-cat-grooming-vacuum` | `page.long-hair-cat-grooming-vacuum` |
| Apartment Pet Hair Control | `apartment-pet-hair-control` | `page.apartment-pet-hair-control` |
| Pet Grooming Vacuum vs De-shedding Brush | `pet-grooming-vacuum-vs-deshedding-brush` | `page.pet-grooming-vacuum-vs-deshedding-brush` |
| llms | `llms` | `page.llms` |

Page body can stay short because the templates carry the content.

## Theme Publish Gate

Before publishing the theme:

1. Run `shopify theme check`.
2. Push to the target draft theme.
3. Preview homepage, product page, cart, search, about, contact, and all GEO pages.
4. Confirm no fake reviews, fake press, or unsupported claims are visible.
5. Confirm product media is present or fallback gallery renders correctly.
6. Confirm add-to-cart works on the FurQuiet product.
7. Publish only after product media and checkout policy are ready.

## Search Setup

After publishing:

1. Add sitemap in Google Search Console.
2. Inspect `/pages/llms`, product page, `/pages/first-batch`, `/pages/sample-qa-log`, `/pages/routine-finder`, and the six guide pages.
3. Submit page URLs for indexing.
4. Track query impressions weekly.
5. Add content only where impressions or social comments show demand.

## Organic Attribution Setup

Before posting organic content:

1. Use `data/furquiet-utm-naming.csv` to create links for each platform.
2. Test one newsletter form submission with a UTM link.
3. Confirm Shopify receives source tags such as `first_src_tiktok` and `last_med_organic_social`.
4. Test `/pages/first-batch` and confirm tags such as `first_batch` plus custom fields such as `first_batch_interest`.
5. Check whether custom fields such as `traffic_snapshot` are visible in the Shopify contact/customer record.
6. If Shopify does not retain custom fields for newsletter customers, rely on tags plus the weekly scoreboard until a dedicated email platform is connected.

## Weekly Admin Checklist

- Check orders, add-to-cart, and conversion.
- Export search terms and product page sessions.
- Add new FAQs from comments.
- Replace AI product images with real sample photos as soon as samples arrive.
- Update supplier QA notes before increasing order volume.
