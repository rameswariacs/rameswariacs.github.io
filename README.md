# Academic website — GitHub Pages guide

The site now has three pages: `index.html` (home), `research.html`, and `publications.html`. All three use the same `images/` folder. Keep the `CV_Rameswar_Bhattacharjee.pdf`, `robots.txt`, and `sitemap.xml` files at the repository root.

## Update the published site

Upload or replace these files in `rameswariacs/rameswariacs.github.io`, preserving their paths:

- `index.html`, `research.html`, and `publications.html`
- `images/hero-molecular-orbitals.jpg`
- `images/latest/chemrxiv-preprint-first-page.jpg`
- `sitemap.xml`

Keep the existing profile and featured-publication images in `images/`. Commit the changes on the branch configured for GitHub Pages. The latest-work image is the actual first page of the version-1 ChemRxiv PDF, rendered as a web image; its card continues to label the study as a preprint under revision.

## Journal gallery covers

The homepage gallery displays the issue-cover images present in
`images/journals/`. Use these exact filenames for the original six journals:

- `jacs.jpg`
- `angewandte-chemie.jpg`
- `chemical-science.jpg`
- `chemistry-of-materials.jpg`
- `acs-materials-au.jpg`
- `acs-physical-chemistry-au.jpg`

Three covers featuring papers you coauthored use:

- `organic-biomolecular-chemistry.jpg`
- `journal-of-computational-chemistry.jpg`
- `precision-chemistry.jpg`

Four more journals in the expandable gallery use:

- `green-chemistry.jpg`
- `inorganic-chemistry.jpg`
- `journal-of-physical-chemistry-c.jpg`
- `chemistry-a-european-journal.jpg`

The gallery does not link covers to individual papers. Only the three verified
cover-feature examples carry a cover-feature label. After adding
or replacing covers, run the generator and upload `index.html` plus the
`images/journals/` folder.

## Regenerate after content or design changes

Edit `build_site.py` and `pubs.json`, then run:

```bash
python3 build_site.py
```

The generator writes the three root HTML files and matching copies in `site/`. Upload the changed root files and any new images. See `UPDATING.md` for metrics, publications, teaching, and Latest Work instructions.
