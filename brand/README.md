# Brand source files

Originals, kept for re-exporting. **Nothing in here is referenced by the site**,
so nothing in here should ever be linked from a page.

| File | What it is |
|---|---|
| `logo-brand-original.png` | Full-resolution supplied logo. `assets/img/logo-brand.png` is derived from it. |

It used to sit in `assets/img/src/`, which was misleading: `assets/` is the
public asset tree, so a 750 KB file nobody requests was being published
alongside the ones every page loads. It costs no page weight either way, since
no page links it, but it does not belong in the tree that gets cached forever
by the `/assets/*` rule in `_headers`.

If you host the repository root directly, this directory is still reachable over
HTTP. That is fine for a logo. Do not put anything private here.
