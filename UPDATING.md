# How to update your website

Two things go stale: **citation metrics** and **publications**. Both are quick.

For a metrics-only change, you can edit the live homepage on GitHub. For
research, publication, teaching, or design changes, edit `build_site.py` and
regenerate the three pages so navigation and shared layout stay in sync.

---

## A. Updating citation metrics (every ~6 months)

### The fast way — edit directly on GitHub

1. Open your Google Scholar profile and note **Citations** and **h-index**. Update the authorship counts when a new paper is published.
2. Go to `github.com/rameswariacs/rameswariacs.github.io`
3. Click `index.html`, then the **pencil icon** (Edit this file)
4. Press **Ctrl+F** / **Cmd+F** and search for `class="metrics"`
5. You'll see five blocks that look like this:

   ```html
   <div class="metric"><b>37</b><span>Publications</span></div>
   <div class="metric"><b>1,196</b><span>Citations</span></div>
   <div class="metric"><b>19</b><span>h-index</span></div>
   <div class="metric"><b>17</b><span>First author</span></div>
   <div class="metric"><b>7</b><span>Corresponding author</span></div>
   ```

   Change only the numbers between `<b>` and `</b>`.

6. Just below, update the date in this line:

   ```html
   <p class="asof">Citation metrics from <a href="...">Google Scholar</a>, August 2026.</p>
   ```

7. Scroll to the bottom, click **Commit changes**

Done. The site rebuilds in about a minute.

### The tidy way — regenerate from the script

Open `build_site.py`, edit the block near the top:

```python
CITATIONS     = "1,196"
H_INDEX       = "19"
FIRST_AUTHOR  = "17"
CORRESPONDING_AUTHOR = "7"
METRICS_AS_OF = "August 2026"
```

Then run `python3 build_site.py` and upload the new `index.html`.
The generator also refreshes `research.html` and `publications.html`; upload
them whenever their content changes.

---

## B. Adding a new publication

Publications on the site are generated from `pubs.json`, the same file that
feeds your CV — so updating it keeps both in sync.

1. Open `pubs.json`
2. Add your new paper as the **first** entry in the list (newest first), matching
   the existing format exactly:

   ```
   "Bhattacharjee, R.*; Coauthor, A.; Kertesz, M.* Title of the paper. Journal Name 2027, 12, 3456-3467. DOI: 10.1021/xxxxx",
   ```

   Keep the trailing comma. Your own name must read `Bhattacharjee, R.` (with an
   asterisk if you are corresponding) — the scripts bold it automatically.

3. Run both generators:

   ```bash
   python3 build_site.py      # rebuilds all three web pages
   node build_cv.js           # rebuilds the R1 CV
   node build_cv_pui.js       # rebuilds the PUI CV
   ```

4. Update the publication count in the metrics (see section A)
5. Upload the new `index.html` and `publications.html`

If a paper moves from "submitted" to "published", also delete it from the
**Under review & in preparation** section — search `build_site.py` for
`Under review` to find it.

---

## C. Updating teaching courses

Teaching experience appears in the `Teaching & Mentoring` section of
`build_site.py`. Search for `<section id="teaching">` and update the course
cards there.

For each course, keep the following information current:

- official course number and title, when known
- role, such as Teaching Assistant or Faculty Assistant
- semester and year
- a brief description of the work you performed

The current entry for General Chemistry Laboratory is **CHEM 1105, Fall 2026**.
When the semester or assignment changes, update the `Current course` card and
then run `python3 build_site.py` before uploading the regenerated `index.html`.

## D. Changing your profile photo

The homepage photo is stored as `images/profile.png`. To replace it later:

1. Rename the new photograph to `profile.png`.
2. Replace the existing file inside the `images` folder on GitHub.
3. Keep the filename unchanged; no HTML editing is required.

A square or nearly square photograph works best. The page crops it automatically
on desktop and mobile screens.

## E. Updating the latest work and featured publications

The large **Latest work** card is maintained separately from the six
**Featured publications** cards. In `build_site.py`, search for
`id="latest-publication"` to update it when a newer paper appears.

Update the status and year, title, authors, short description, links, and image
path together. The current image is the first page of the ChemRxiv PDF at
`images/latest/chemrxiv-preprint-first-page.jpg`. When replacing it, regenerate
and upload both `index.html` and `publications.html` along with the new image.
This card is intentionally reserved
for the newest work that best represents your independent computational or
machine-learning research; it may be a preprint while under review. Featured
papers can remain selected examples of your strongest published work.

The six visual cards at the top of the Publications section are maintained in
`build_site.py`. Search for `featured-grid` to find them.

For each featured paper, update these four items together:

- the DOI link
- journal and year
- paper title and one-sentence description
- image path and descriptive `alt` text

Place the image file in `images/featured/` and use a short, web-safe filename.
Whenever possible, use the paper's official TOC graphic or an original figure
that you are permitted to display. Then run `python3 build_site.py` and upload
the regenerated `publications.html` and the new image file or folder.

The machine-learning paper is currently a **ChemRxiv preprint under revision**,
not a peer-reviewed publication. When its status changes, update the Latest work
card, the research-theme bullet, and the `Under review & in preparation` entry
in `build_site.py`.

## Journal gallery

The home gallery uses issue covers from journals in which your work has
appeared. Add the images to `images/journals/` using the filenames listed in
`README.md`, then run `python3 build_site.py`. Available covers appear in the
gallery; missing covers are skipped. The covers are journal examples rather than claims
that your articles were selected as cover features.

## F. Restoring the GitHub link

Once you have pushed at least one real repository:

- **In the script:** set `SHOW_GITHUB = True` near the top of `build_site.py`, re-run
- **Or in `index.html` directly:** find the line beginning
  `<!-- Restore once you have pushed a repository:` and remove the `<!--` and `-->`

---

## G. Things not to delete

- The line containing `google-site-verification` — removing it un-verifies you in
  Google Search Console
- `sitemap.xml` and `robots.txt`
- The `<link rel="canonical">` tag

---

## A sensible rhythm

- **When a paper is accepted** — add it to `pubs.json`, regenerate, upload. Five minutes.
- **Every six months** — refresh citations and the h-index, update the date.
- **Once a year** — reread the research themes and check they still describe what
  you actually work on.

A site that is a year out of date is worse than no site. Put a recurring
reminder in your calendar; it is the only thing that reliably prevents drift.
