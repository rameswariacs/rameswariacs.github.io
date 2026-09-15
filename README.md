# Academic website — deployment guide

Single self-contained file. No build step, no dependencies, no framework. `index.html` is the entire site.

## Publish on GitHub Pages (about 5 minutes)

1. Create a new **public** repository named exactly:

   ```
   rameswariacs.github.io
   ```

   The name must match your username exactly — that's what makes it a user site rather than a project site.

2. Upload `index.html` to the root of that repository (drag and drop works: **Add file → Upload files**).

3. Go to **Settings → Pages**. Under "Build and deployment", set Source to **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.

4. Wait 1–2 minutes. Your site is live at `https://rameswariacs.github.io`.

To update later, edit `index.html` in the repo and commit — the site rebuilds automatically.

## Before you publish — two things to fix

1. **CV PDF.** The "Curriculum Vitae" button points at `CV_Rameswar_Bhattacharjee.pdf`. Export your CV to PDF under exactly that filename and upload it alongside `index.html`. Until you do, that link 404s.

2. **Citation metrics.** The header shows 1,170+ citations and h-index 19, carried over from your CV draft. Confirm against your Google Scholar profile and edit the `.metrics` block if they've moved.

## Optional additions

- **Photo.** There's a commented-out `<img>` tag at the top of `<header>`. Uncomment it, upload `photo.jpg`, done.
- **Custom domain.** Buy a domain, add a file named `CNAME` containing just the domain, and point a CNAME DNS record at `rameswariacs.github.io`.
- **Research figures.** The Research section is text-only. One good figure per theme — a band structure, a pancake-bonding orbital, a parity plot from the ML paper — would make the page substantially more compelling. Upload images and add `<img src="..." style="width:100%;border-radius:6px;margin:12px 0">` inside the relevant `<article class="theme">`.

## Regenerating

`build_site.py` generates `index.html` from `pubs.json`, so publication citations stay consistent with your CV. Run:

```bash
python3 build_site.py
```

If you'd rather just hand-edit `index.html` from here on, that's fine too — nothing depends on the generator.

## A note on maintenance

The most common failure mode for academic sites is going stale. A site last updated three years ago is worse than no site. Set a reminder to add new papers when they're accepted — it takes two minutes.
