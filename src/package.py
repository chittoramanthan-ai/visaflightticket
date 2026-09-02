# -*- coding: utf-8 -*-
"""
Build deploy.zip: exactly what belongs in public_html, and nothing else.

    python src/package.py

Upload the zip through Hostinger's File Manager and extract it there. That
route matters more than it sounds: .htaccess is a dotfile, and most FTP
clients hide dotfiles by default, so uploading file-by-file is the usual way
people lose their security headers and redirects without noticing. A zip
carries it through untouched.

Excluded on purpose: src/ (the generator), supabase/ (Edge Function source),
brand/ (logo originals), _dev/ (the payment preview, which stubs the backend),
.git/, and the Netlify/Cloudflare header files that Apache ignores.
"""

import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deploy.zip")

# Directories never served to the public.
SKIP_DIRS = {".git", "src", "supabase", "brand", "_dev", "__pycache__", ".vscode"}

# Files that belong to the repo rather than the website.
SKIP_FILES = {
    "deploy.zip",
    "README.md",
    "_headers",      # Cloudflare Pages / Netlify. Apache reads .htaccess.
    "_redirects",    # same
    ".gitignore",
}

# Extensions that are source, not site.
SKIP_EXT = {".py", ".pyc", ".md", ".bak", ".log"}


def include(rel):
    parts = rel.split("/")
    if any(p in SKIP_DIRS for p in parts):
        return False
    name = parts[-1]
    if name in SKIP_FILES:
        return False
    if os.path.splitext(name)[1].lower() in SKIP_EXT:
        return False
    # .htaccess is the one dotfile that must ship.
    if name.startswith(".") and name != ".htaccess":
        return False
    return True


def main():
    if os.path.exists(OUT):
        os.remove(OUT)

    added, total = [], 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                if not include(rel):
                    continue
                z.write(full, rel)
                total += os.path.getsize(full)
                added.append(rel)

    pages = sum(1 for r in added if r.endswith(".html"))
    print("deploy.zip written")
    print("  %d files, %.1f MB uncompressed, %.1f MB zipped"
          % (len(added), total / 1048576.0, os.path.getsize(OUT) / 1048576.0))
    print("  %d HTML pages" % pages)

    must_have = [".htaccess", "index.html", "404.html", "robots.txt",
                 "sitemap.xml", "site.webmanifest"]
    print()
    for m in must_have:
        print("  %-18s %s" % (m, "yes" if m in added else "MISSING"))

    leaked = [r for r in added
              if r.startswith(("src/", "supabase/", "brand/", "_dev/"))]
    print()
    print("  source files leaked: %s" % (leaked if leaked else "none"))


if __name__ == "__main__":
    main()
