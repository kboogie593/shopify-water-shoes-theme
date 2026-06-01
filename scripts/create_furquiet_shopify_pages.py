#!/usr/bin/env python3
"""Create or update FurQuiet Shopify page objects through Admin GraphQL."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


DEFAULT_STORE = "wxat5u-e3.myshopify.com"
DEFAULT_API_VERSION = "2026-04"
DEFAULT_PAGES_FILE = Path("data/furquiet-shopify-pages.csv")
TIMEOUT_SECONDS = 30

LOOKUP_QUERY = """
query PageByHandle($query: String!) {
  pages(first: 1, query: $query) {
    nodes {
      id
      title
      handle
      templateSuffix
    }
  }
}
"""

CREATE_MUTATION = """
mutation CreateFurQuietPage($page: PageCreateInput!) {
  pageCreate(page: $page) {
    page {
      id
      title
      handle
      templateSuffix
    }
    userErrors {
      field
      message
    }
  }
}
"""

UPDATE_MUTATION = """
mutation UpdateFurQuietPage($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) {
    page {
      id
      title
      handle
      templateSuffix
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass
class PageSpec:
    title: str
    handle: str
    template_suffix: str
    body: str


def load_pages(path: Path) -> list[PageSpec]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    pages: list[PageSpec] = []
    for row in rows:
        pages.append(
            PageSpec(
                title=(row.get("title") or "").strip(),
                handle=(row.get("handle") or "").strip(),
                template_suffix=(row.get("template_suffix") or "").strip(),
                body=(row.get("body") or "").strip(),
            )
        )
    missing = [page for page in pages if not page.title or not page.handle or not page.template_suffix]
    if missing:
        raise ValueError("Every page row must include title, handle, and template_suffix.")
    return pages


def graphql(store: str, api_version: str, token: str, query: str, variables: dict) -> dict:
    endpoint = f"https://{store}/admin/api/{api_version}/graphql.json"
    request = urllib.request.Request(
        endpoint,
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
            "User-Agent": "FurQuietPageCreator/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify Admin API returned HTTP {error.code}: {body[:500]}") from error
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], ensure_ascii=False))
    return payload.get("data") or {}


def find_page(store: str, api_version: str, token: str, handle: str) -> dict | None:
    data = graphql(store, api_version, token, LOOKUP_QUERY, {"query": f"handle:{handle}"})
    nodes = (((data.get("pages") or {}).get("nodes")) or [])
    for node in nodes:
        if node.get("handle") == handle:
            return node
    return None


def page_input(page: PageSpec) -> dict:
    return {
        "title": page.title,
        "handle": page.handle,
        "body": page.body,
        "isPublished": True,
        "templateSuffix": page.template_suffix,
    }


def user_errors(payload: dict, key: str) -> list[str]:
    errors = ((payload.get(key) or {}).get("userErrors")) or []
    return [
        f"{'.'.join(map(str, error.get('field') or []))}: {error.get('message')}"
        if error.get("field")
        else str(error.get("message"))
        for error in errors
    ]


def upsert_page(store: str, api_version: str, token: str, page: PageSpec, dry_run: bool) -> tuple[str, str]:
    if dry_run:
        return "DRY", f"upsert /pages/{page.handle} template={page.template_suffix}"

    existing = find_page(store, api_version, token, page.handle)
    if existing:
        data = graphql(
            store,
            api_version,
            token,
            UPDATE_MUTATION,
            {"id": existing["id"], "page": page_input(page)},
        )
        errors = user_errors(data, "pageUpdate")
        if errors:
            return "FAIL", f"/pages/{page.handle}: {'; '.join(errors)}"
        saved = data["pageUpdate"]["page"]
        return "UPDATED", f"/pages/{saved['handle']} template={saved.get('templateSuffix') or 'default'}"

    data = graphql(store, api_version, token, CREATE_MUTATION, {"page": page_input(page)})
    errors = user_errors(data, "pageCreate")
    if errors:
        return "FAIL", f"/pages/{page.handle}: {'; '.join(errors)}"
    saved = data["pageCreate"]["page"]
    return "CREATED", f"/pages/{saved['handle']} template={saved.get('templateSuffix') or 'default'}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", default=os.getenv("SHOPIFY_STORE_DOMAIN", DEFAULT_STORE))
    parser.add_argument("--api-version", default=os.getenv("SHOPIFY_API_VERSION", DEFAULT_API_VERSION))
    parser.add_argument("--pages-file", type=Path, default=DEFAULT_PAGES_FILE)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN", "").strip()
    if not token and not args.dry_run:
        print(
            "Missing SHOPIFY_ADMIN_ACCESS_TOKEN with read_online_store_pages and write_online_store_pages access.",
            file=sys.stderr,
        )
        return 2

    pages = load_pages(args.pages_file)
    failed = 0
    for page in pages:
        try:
            status, message = upsert_page(args.store, args.api_version, token, page, args.dry_run)
        except Exception as error:  # noqa: BLE001 - CLI should report per-page failures cleanly.
            status, message = "FAIL", f"/pages/{page.handle}: {error}"
        if status == "FAIL":
            failed += 1
        print(f"{status} {message}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
