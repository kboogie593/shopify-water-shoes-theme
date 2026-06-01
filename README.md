# FurQuiet — Shopify Theme

A modern, performance-focused Shopify theme for **FurQuiet**, a quiet-start
pet grooming vacuum brand. Built to the Online Store 2.0 spec (JSON templates + section groups)
so it is fully editable from the Shopify Theme Editor.

![Theme color: sage #4F8F83](https://img.shields.io/badge/brand-FurQuiet-4F8F83)
![Online Store 2.0](https://img.shields.io/badge/Shopify-Online%20Store%202.0-95BF47)

## Highlights

- Online Store 2.0 JSON templates + section groups (`header-group`, `footer-group`)
- Editable sections: hero, **stats bar**, features, featured collection,
  image-with-text, testimonials, **FAQ**, newsletter — all merchandiser-friendly
- Liquid + vanilla CSS/JS only — no build step, drag-and-drop into Shopify
- Customer accounts, cart, search, blog, contact, 404, password, gift card

### Design
- Brand palette pre-tuned to FurQuiet sage (`#4F8F83` / `#234E48`) with
  warm clay accent (`#D97745`)
- Clean sticky header, visual product proof sections, and pet-care landing templates
- Refined product cards with quick-add hover state and lift animation
- Polished FAQ accordion, trust-badge bar on product pages, fade-in
  scroll reveal

### GEO (Generative Engine Optimization)
Built to be discoverable and citable by **ChatGPT, Perplexity, Google AI
Overviews, Bing Copilot, and Claude**:

- Comprehensive **JSON-LD schema.org** markup: `Organization`, `WebSite`,
  `Product` (with offers and brand until real reviews exist), `Article`,
  `CollectionPage`, `BreadcrumbList`, `FAQPage`
- `llms.txt` page template — drop-in factual brief for AI crawlers
- Enhanced `<meta>` tags: `max-snippet`, `max-image-preview`,
  product price/availability/brand, OG locale & image dimensions
- Visible on-page FAQ section paired with FAQ schema (the #1
  citation pattern AI engines pick up)
- E-E-A-T signals: author, organization contact, sameAs social profiles

### SEO
- OG and Twitter cards on every page, sitemap link, robots template
- Semantic HTML, accessible skip-link, alt text patterns
- Mobile-first responsive layout

## Installing into Shopify

1. **Zip the theme files** (do _not_ zip the parent folder — zip the
   contents). On macOS/Linux:

   ```bash
   cd shopify-water-shoes-theme
   zip -r ../furquiet-theme.zip . -x "*.git*" "README.md" "LICENSE"
   ```

2. In your Shopify admin, go to **Online Store → Themes → Add theme →
   Upload zip file**, then choose `furquiet-theme.zip`.

3. Once uploaded, click **Customize** to open the Theme Editor and tune
   sections, colors, logo, and menus.

## Directory layout

```
shopify-water-shoes-theme/
├── assets/        # CSS, JS, fonts, images
├── config/        # settings_schema.json, settings_data.json
├── layout/        # theme.liquid (main), password.liquid
├── locales/       # en.default.json
├── sections/      # All editable sections + header-group / footer-group
├── snippets/      # Reusable Liquid snippets (product-card, price, icons)
└── templates/     # JSON page templates + customer .liquid templates
```

## Brand setup

Open **Theme settings** in the editor to tune:

- **Logo** image and width
- **Colors** — primary, primary-dark, accent, foreground, background
- **Typography** — heading + body fonts (Shopify font picker)
- **Social links** — Instagram, Facebook, TikTok, YouTube, X

Recommended starting palette (already set as defaults):

| Token              | Hex       |
|--------------------|-----------|
| Primary            | `#4F8F83` |
| Primary dark       | `#234E48` |
| Accent             | `#D97745` |
| Background         | `#FFFFFF` |
| Foreground         | `#0F172A` |

## Required navigation menus

This theme references two menus by default. Create them in
**Online Store → Navigation**:

- `main-menu` — top header navigation
- `footer` — primary footer column

## Activating the llms.txt for AI crawlers

Shopify routes `/pages/<handle>` to `templates/page.<handle>.liquid` when a
page exists with that handle. To publish an AI-discoverable brief:

1. Go to **Online Store → Pages → Add page**
2. Title: `llms` (handle becomes `llms`)
3. **Theme template:** select `llms` (this loads `page.llms.liquid`)
4. Leave the content blank — the template overrides it
5. Save. The file is now live at `/pages/llms`

Then add `<link rel="alternate" type="text/plain" href="/pages/llms">` to
your homepage (already wired into `meta-tags.liquid` via the sitemap
discovery link, and the URL is referenced in the JSON-LD).

## FurQuiet execution docs

- `docs/furquiet-10k-roadmap.md` — $10K/month revenue math, traffic system, and current gaps
- `docs/furquiet-product-development-qa.md` — 1688 supplier screening, sample tests, and claim policy
- `docs/furquiet-1688-supplier-message-cn.md` — Chinese supplier outreach script for sample and QA details
- `docs/furquiet-shopify-launch-runbook.md` — Shopify page/media/theme launch checklist
- `data/furquiet-geo-content-backlog.csv` — GEO/SEO page and FAQ backlog
- `data/furquiet-supplier-scorecard.csv` — supplier reply and sample-readiness scoring table
- `data/furquiet-video-shot-list.csv` — short-video production shot list
- `data/furquiet-organic-channel-scoreboard.csv` — weekly organic traffic and revenue scoreboard
- `data/furquiet-comment-to-content-log.csv` — comment/query-to-content tracking log
- `data/furquiet-social-captions.csv` — first captions mapped to platform, page, and asset
- `data/furquiet-utm-naming.csv` — UTM naming convention for organic and GEO traffic
- `data/furquiet-routine-finder-content-map.csv` — routine finder routing, tags, and follow-up angles
- `data/furquiet-first-batch-email-flow.csv` — first-batch email sequence and proof gates
- `docs/furquiet-short-video-scripts.md` — first reusable short-video scripts
- `docs/furquiet-social-asset-guide.md` — generated social image asset usage
- `docs/furquiet-seo-blog-drafts.md` — first Shopify blog outlines for GEO support
- `docs/furquiet-attribution-and-utm.md` — how the theme captures first/last-touch source data
- `docs/furquiet-first-batch-email-flow.md` — waitlist capture, tags, and email sequence boundaries
- `scripts/generate_furquiet_social_videos.py` — regenerates the MP4 placeholder videos from cover images

Create `/pages/grooming-guides` first; it acts as the internal guide hub for
all FurQuiet long-tail pages and should be linked from navigation once the
theme is published.

## Sections you can add to any page

- `Hero`
- `Featured collection`
- `Features` (4-up cards with emoji icons)
- `Image with text`
- `Testimonials`
- `Newsletter`

Each is configurable via the Theme Editor sidebar.

## License

MIT — see `LICENSE`.

## Credits

Built with care for the FurQuiet launch. Theme architecture follows
[Shopify Dawn](https://github.com/Shopify/dawn) conventions.
