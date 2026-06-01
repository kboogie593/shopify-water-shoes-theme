#!/usr/bin/env python3
"""Verify the live FurQuiet Shopify storefront after GitHub theme sync."""

from __future__ import annotations

import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


STORE = "https://wxat5u-e3.myshopify.com"
PRODUCT_PATH = "/products/furquiet-grooming-vacuum-kit"
TIMEOUT_SECONDS = 20


@dataclass
class Check:
    name: str
    passed: bool
    evidence: str


def fetch(path: str) -> tuple[int, str, str]:
    url = f"{STORE}{path}"
    separator = "&" if "?" in url else "?"
    cache_busted_url = f"{url}{separator}codex_verify={int(time.time())}"
    request = urllib.request.Request(
        cache_busted_url,
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "FurQuietStorefrontVerifier/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.status, response.geturl(), body
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return error.code, error.geturl(), body


def contains(body: str, needle: str) -> bool:
    return needle in body


def run_checks() -> list[Check]:
    home_status, home_url, home_body = fetch("/")
    product_status, product_url, product_body = fetch(PRODUCT_PATH)

    checks = [
        Check("homepage_http_200", home_status == 200, f"{home_status} {home_url}"),
        Check(
            "homepage_live_theme",
            contains(home_body, 'shopify-water-shoes-theme\\/main'),
            "Shopify.theme contains shopify-water-shoes-theme/main",
        ),
        Check(
            "homepage_first_batch_anchor",
            contains(home_body, 'id="first-batch"'),
            "homepage renders id=\"first-batch\"",
        ),
        Check(
            "homepage_first_batch_links",
            contains(home_body, 'href="/#first-batch"'),
            "homepage header/CTA links route to /#first-batch",
        ),
        Check("product_http_200", product_status == 200, f"{product_status} {product_url}"),
        Check(
            "product_add_to_cart",
            contains(product_body, "Add to cart"),
            "product page renders Add to cart",
        ),
        Check(
            "product_no_liquid_error",
            "Liquid error" not in product_body,
            "product HTML has no Liquid error",
        ),
        Check(
            "product_share_media_fallback",
            "pinterest.com/pin/create/button/" in product_body
            and "furquiet-product-hero-ai.jpg" in product_body
            and "media=Liquid%20error" not in product_body
            and "media=Liquid error" not in product_body,
            "Pinterest media uses FurQuiet fallback image when product media is blank",
        ),
        Check(
            "product_meta_image_fallback",
            '"image": "https:' in product_body and "furquiet-product-hero-ai.jpg" in product_body,
            "data-product-meta image is a URL fallback",
        ),
    ]
    return checks


def main() -> int:
    checks = run_checks()
    failed = [check for check in checks if not check.passed]
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"{status} {check.name}: {check.evidence}")
    if failed:
        print(f"\n{len(failed)} storefront check(s) failed.", file=sys.stderr)
        return 1
    print("\nAll storefront checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
