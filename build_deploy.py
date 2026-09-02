#!/usr/bin/env python3
"""
Assemble deploy/ — exactly what goes on the hosting, nothing else.

Run after build_pages.py and build_seo.py:

    python3 build_deploy.py

It works out the asset list from the pages themselves and then VERIFIES the result.
An earlier shell version read the list with `while read`, which silently drops the last
line of a file that has no trailing newline — it shipped a site missing one image, and
nothing complained. Hence the verification step: this exits non-zero if anything the
pages reference is not in deploy/.
"""
import re, shutil, sys, pathlib

SITE = "https://automatonpower.com.ua/"
PAGES = ["index.html", "21700.html", "high-density.html", "ev-packs.html"]
EXTRA = ["send-form.php", "config.example.php", "robots.txt", "sitemap.xml", "llms.txt"]
OUT = pathlib.Path("deploy")


def referenced():
    """Every local file the built pages point at — including absolute self-URLs in
    Open Graph tags and JSON-LD, which a naive src/href scan misses."""
    found = set()
    for page in PAGES:
        s = pathlib.Path(page).read_text(encoding="utf-8")
        for m in re.findall(r'(?:src|href)="([^"]+)"', s):
            if m.startswith(("#", "data:", "mailto:", "tel:")):
                continue
            if m.startswith(SITE):
                m = m[len(SITE):]
            elif m.startswith("http"):
                continue
            found.add(m.split("?")[0].split("#")[0])
        for m in re.findall(re.escape(SITE) + r'([A-Za-z0-9_\-./]+\.(?:jpg|jpeg|png|webp|svg|pdf))', s):
            found.add(m)
    return {f for f in found if f and not f.endswith(".html")}


def main():
    assets = referenced()

    absent = sorted(a for a in assets if not pathlib.Path(a).is_file())
    if absent:
        print("ERROR: pages reference files that do not exist:", file=sys.stderr)
        for a in absent:
            print("   ", a, file=sys.stderr)
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    for name in PAGES + EXTRA:
        src = pathlib.Path(name)
        if not src.is_file():
            print(f"ERROR: {name} is missing", file=sys.stderr)
            return 1
        shutil.copy2(src, OUT / name)

    for a in sorted(assets):
        dst = OUT / a
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(a, dst)

    # ---- verify: every referenced asset AND every page must be present ----
    missing = [a for a in sorted(assets) + PAGES + EXTRA if not (OUT / a).is_file()]
    if missing:
        print("ERROR: deploy/ is incomplete:", file=sys.stderr)
        for m in missing:
            print("   ", m, file=sys.stderr)
        return 1

    files = sum(1 for _ in OUT.rglob("*") if _.is_file())
    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"deploy/ assembled and verified")
    print(f"  pages:  {len(PAGES)}")
    print(f"  assets: {len(assets)}  (all referenced files present)")
    print(f"  files:  {files}")
    print(f"  size:   {size/1024/1024:.1f} MB")
    print("\nUpload the CONTENTS of deploy/ to the web root, then create config.php there.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
