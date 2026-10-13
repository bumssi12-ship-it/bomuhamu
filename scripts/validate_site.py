#!/usr/bin/env python3
"""Offline quality gate for Bomuhamu's five public Meta policy pages.

Run from any working directory: python3 scripts/validate_site.py
Only the Python standard library is required. No API credentials are needed.
"""
from __future__ import annotations

import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

PREFIX = "/bomuhamu/"
BASE = "https://example.invalid" + PREFIX
PAGES = {
    "/": "index.html",
    "/privacy-policy/": "privacy-policy/index.html",
    "/data-deletion/": "data-deletion/index.html",
    "/terms/": "terms/index.html",
    "/review-guide/": "review-guide/index.html",
}
REQUIRED_LINKS = {
    "/": {"/privacy-policy/", "/data-deletion/", "/terms/", "/review-guide/"},
    "/privacy-policy/": {"/data-deletion/"},
    "/terms/": {"/privacy-policy/"},
    "/review-guide/": {"/privacy-policy/", "/data-deletion/", "/terms/"},
}
SENSITIVE_VALUES = (
    re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}"),
    re.compile(r"\bsk-proj-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)\b(?:THREADS_ACCESS_TOKEN|THREADS_APP_SECRET|META_APP_SECRET)\s*=\s*[^\s<]{8,}"),
)


class HTMLQuality(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.hrefs = []
        self.charset = False
        self.viewport = False
        self.h1 = False
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        elif tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
        elif tag == "meta":
            self.charset |= (attrs.get("charset") or "").lower() == "utf-8"
            self.viewport |= attrs.get("name") == "viewport" and bool(attrs.get("content"))
        elif tag == "h1":
            self.h1 = True
        elif tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.title += text


def validate(root):
    errors = []
    for route, source in PAGES.items():
        page = root / source
        if not page.is_file():
            errors.append(f"{source}: file missing")
            continue
        html = page.read_text(encoding="utf-8-sig")
        parser = HTMLQuality()
        parser.feed(html)
        if parser.lang != "en":
            errors.append(f"{source}: html lang=en missing")
        if not parser.charset or not parser.viewport:
            errors.append(f"{source}: UTF-8 or viewport metadata missing")
        if not parser.h1 or not parser.title.strip():
            errors.append(f"{source}: heading or title missing")
        if not re.search(r"Last updated:\s*20\d{2}-\d{2}-\d{2}", html, re.I):
            errors.append(f"{source}: Last updated date missing")
        if any(pattern.search(html) for pattern in SENSITIVE_VALUES):
            errors.append(f"{source}: potential embedded credential")
        linked = set()
        for href in parser.hrefs:
            link = urlsplit(href)
            if link.scheme:
                if link.scheme not in ("https", "mailto"):
                    errors.append(f"{source}: unsupported link scheme {link.scheme}")
                continue
            if href.startswith("//"):
                errors.append(f"{source}: protocol-relative link")
                continue
            target = urlsplit(urljoin(BASE + route.lstrip("/"), href))
            if target.netloc != "example.invalid" or not target.path.startswith(PREFIX):
                errors.append(f"{source}: local link escapes site: {href}")
                continue
            rel = target.path[len(PREFIX) - 1:]
            if rel not in PAGES:
                errors.append(f"{source}: unknown local link: {href}")
            else:
                linked.add(rel)
        for missing in sorted(REQUIRED_LINKS.get(route, set()) - linked):
            errors.append(f"{source}: required link missing: {missing}")
    return errors


if __name__ == "__main__":
    errors = validate(pathlib.Path(__file__).resolve().parent.parent)
    for message in errors:
        print("[FAIL]", message)
    if errors:
        print(f"[HOLD] Static site quality: {len(errors)} error(s)")
        sys.exit(1)
    print(f"[PASS] Static site quality: {len(PAGES)} pages, links, metadata, basic credential patterns")
