#!/usr/bin/env python3
"""Generate a single-file academic website from the verified publication list."""
import json, html, re, pathlib

# ---------------------------------------------------------------
# EDIT ME: put your GitHub username here and re-run this script.
GITHUB_USER = "rameswariacs"
# Set True once the profile has at least one real repository. An empty GitHub
# behind a prominent link reads worse than no link at all.
SHOW_GITHUB = False

# ---------------------------------------------------------------
# EDIT THESE FOUR LINES when you refresh your publication metrics,
# then re-run:  python3 build_site.py
CITATIONS     = "1,200"
H_INDEX       = "19"
FIRST_AUTHOR  = "17"
CORRESPONDING_AUTHOR = "7"
# ---------------------------------------------------------------
# ---------------------------------------------------------------

pubs = json.load(open('pubs.json'))

# --- normalize name rendering (same rule as the CV) ---
def norm(t):
    t = re.sub(r'Bhattacharjee,\s*R\.?\s*(\*?)', lambda m: 'Bhattacharjee, R.' + m.group(1), t)
    t = re.sub(r';\s+‡', ';‡', t)
    return re.sub(r'\s{2,}', ' ', t).strip()

pubs = [norm(p) for p in pubs]

DOI_RE = re.compile(r'DOI:\s*(10\.\S+?)\s*$')
NAME_RE = re.compile(r'(Bhattacharjee, R\.\*?)')

def render_pub(text):
    """escape -> bold name -> linkify DOI"""
    doi = None
    m = DOI_RE.search(text)
    if m:
        doi = m.group(1).rstrip('.')
        text = text[:m.start()].strip()
    esc = html.escape(text)
    esc = NAME_RE.sub(r'<span class="me">\1</span>', esc)
    # italicize the journal-ish trailing segment is unreliable; leave as-is
    out = f'<div class="pub-text">{esc}</div>'
    if doi:
        out += f'<a class="doi" href="https://doi.org/{html.escape(doi)}" target="_blank" rel="noopener">{html.escape(doi)}</a>'
    return out

PUB_THUMBS = {
    '10.1021/jacs.4c10064': 'images/featured/jacs-topological.jpg',
    '10.1021/jacs.3c14065': 'images/featured/jacs-perylene.jpg',
    '10.1039/d5sc00639b': 'images/featured/quinonoid-radial.jpeg',
    '10.1021/acsmaterialsau.4c00153': 'images/featured/acene-dimers.jpg',
    '10.1039/d4sc03774j': 'images/featured/triphenylene.png',
    '10.1021/acs.chemmater.3c02547': 'images/featured/chemmat-topological.jpg',
}

year_rows = {}
for i, pub in enumerate(pubs):
    num = len(pubs) - i
    year_match = re.search(r'\b(?:19|20)\d{2}\b', pub)
    year = year_match.group() if year_match else 'Earlier work'
    doi_match = DOI_RE.search(pub)
    doi = doi_match.group(1).rstrip('.').lower() if doi_match else ''
    thumb = PUB_THUMBS.get(doi)
    visual = (
        f'<img src="{thumb}" alt="" loading="lazy" decoding="async">'
        if thumb else f'<span aria-hidden="true">#{num}</span>'
    )
    row = (
        '<li class="pub pub-row">'
        f'<div class="pub-thumbnail">{visual}</div>'
        f'<div class="pub-details"><span class="pubnum">#{num}</span>{render_pub(pub)}</div>'
        '</li>'
    )
    year_rows.setdefault(year, []).append(row)

pub_items = '\n'.join(
    '<div class="pub-year-group">'
    f'<h3 class="pub-year"><span>{year}</span></h3>'
    '<ol class="pubs">' + '\n'.join(rows) + '</ol>'
    '</div>'
    for year, rows in year_rows.items()
)

THEMES = [
    ("Topological electronic structure in π-conjugated materials",
     "Mechanical strain, quinonoid–aromatic competition, and electronic topology act as tunable design parameters "
     "for band structure in conjugated polymers. This work established strain as a continuous control knob for bandgap "
     "and identified topological transitions in ethynyl-linked acene polymers.",
     ["J. Am. Chem. Soc. 2024 — Strain-induced topological transition",
      "Chem. Sci. 2025 — Quinonoid radial π-conjugation",
      "Chem. Mater. 2024 — Continuous bandgap tuning"]),
    ("Radical π-stacking and non-classical pancake bonding",
     "Open-shell π-systems stack through SOMO–SOMO overlap rather than dispersion alone. I quantify how charge "
     "distribution, orbital symmetry, and spin delocalization govern this stabilization — predictions repeatedly "
     "validated by crystallographic collaborators.",
     ["J. Am. Chem. Soc. 2024 — Charge effects in π-stacked perylenes",
      "Chem. Sci. 2024 — Trimeric triphenylene radical cation",
      "ACS Mater. Au 2025 — Pancake bonding in acene dimers"]),
    ("Machine learning for structure–property prediction",
     "A chemistry-guided descriptor framework linking molecular packing to electronic structure across 2,582 π-radical "
     "dimer geometries. Nineteen interpretable geometric descriptors reproduce DFT-level properties at a fraction of the "
     "cost, with validation designed to separate genuine geometric information from family-level correlation.",
     ["2,582 dimer geometries across five PAH radical systems",
      "Test-set R² = 0.94–0.98; 0.82–0.92 on held-out geometry clusters",
      "500-fold Y-randomization and system-mean baseline controls",
      "Data and code released openly on Zenodo",
      "ChemRxiv preprint; under revision at J. Chem. Inf. Model., 2026"]),
    ("Mapping π–σ bonding landscapes in radical dimers",
     "Pancake-bonded π-dimers can compete with σ-bonded alternatives, but the structural pathways connecting them are "
     "poorly characterized. Combining conformational sampling, supervised classification, and intrinsic reaction "
     "coordinate calculations resolves the interconversion pathway in an experimentally characterized julolidine "
     "radical dimer, and explains why the condensed phase favours the π-dimer.",
     ["Machine-learning classification used to locate candidate transition structures",
      "DFT and IRC calculations give a ~16 kcal mol⁻¹ interconversion barrier",
      "Periodic stacking calculations rationalize the observed solid-state preference",
      "Manuscript in final preparation, 2026"]),
    ("Computational catalysis and reaction mechanisms",
     "Mechanistic studies of homogeneous and heterogeneous reaction landscapes, spanning metal-free CO₂ reduction, "
     "gold-catalyzed cross-coupling, and biomass valorization to lubricant base oils.",
     ["Green Chem. 2020 — Biomass-derived lubricant base oils",
      "Chem. Sci. 2019 / Angew. Chem. 2016 — Metal-free CO₂ reduction",
      "Chem. Eur. J. 2017 — Autocatalytic reductive elimination"]),
]

theme_html = '\n'.join(
    '      <article class="theme">\n'
    f'        <h3>{html.escape(t)}</h3>\n'
    f'        <p>{d}</p>\n'
    '        <ul>' + ''.join(f'<li>{html.escape(b)}</li>' for b in bullets) + '</ul>\n'
    '      </article>'
    for t, d, bullets in THEMES
)

github_link = (
    f'<a href="https://github.com/{GITHUB_USER}" target="_blank" rel="noopener">GitHub</a>'
    if SHOW_GITHUB else
    f'<!-- Restore once you have pushed a repository: '
    f'<a href="https://github.com/{GITHUB_USER}" target="_blank" rel="noopener">GitHub</a> -->'
)

JOURNAL_COVERS = [
    ('Journal of the American Chemical Society', 'jacs.jpg'),
    ('Angewandte Chemie', 'angewandte-chemie.jpg'),
    ('Chemical Science', 'chemical-science.jpg'),
    ('Chemistry of Materials', 'chemistry-of-materials.jpg'),
    ('ACS Materials Au', 'acs-materials-au.jpg'),
    ('ACS Physical Chemistry Au', 'acs-physical-chemistry-au.jpg'),
]
FEATURED_COVERS = [
    ('Organic & Biomolecular Chemistry', 'organic-biomolecular-chemistry.jpg'),
    ('Journal of Computational Chemistry', 'journal-of-computational-chemistry.jpg'),
    ('Precision Chemistry', 'precision-chemistry.jpg'),
]
MORE_COVERS = [
    ('Green Chemistry', 'green-chemistry.jpg'),
    ('Inorganic Chemistry', 'inorganic-chemistry.jpg'),
    ('The Journal of Physical Chemistry C', 'journal-of-physical-chemistry-c.jpg'),
    ('Chemistry – A European Journal', 'chemistry-a-european-journal.jpg'),
]
cover_dir = pathlib.Path('images/journals')
def available(covers):
    return [(name, filename) for name, filename in covers if (cover_dir / filename).is_file()]

featured_covers = available(FEATURED_COVERS)
main_covers = available(JOURNAL_COVERS)
more_covers = available(MORE_COVERS)

def cover_card(name, filename, featured=False):
    note = '<span class="cover-feature-note">My article featured on the cover</span>' if featured else ''
    return (
        '<figure class="journal-cover-card">'
        f'<img src="images/journals/{filename}" alt="{html.escape(name)} issue cover" loading="lazy" decoding="async">'
        f'<figcaption>{html.escape(name)}{note}</figcaption>'
        '</figure>'
    )

gallery_html = ''
gallery_nav = ''
if featured_covers or main_covers or more_covers:
    gallery_nav = '<a href="#journal-gallery">Gallery</a>'
    featured_html = (
        '<h3 class="gallery-subtitle">My work on journal covers</h3>'
        '<p class="gallery-caption">These covers feature papers I coauthored.</p>'
        '<div class="journal-cover-grid featured-cover-grid">'
        + '\n'.join(cover_card(name, filename, True) for name, filename in featured_covers)
        + '</div>'
    ) if featured_covers else ''
    main_html = (
        '<h3 class="gallery-subtitle">Journals where I have published</h3>'
        '<div class="journal-cover-grid">'
        + '\n'.join(cover_card(name, filename) for name, filename in main_covers)
        + '</div>'
    ) if main_covers else ''
    more_html = (
        '<details class="more-journals">'
        f'<summary>More journals ({len(more_covers)})</summary>'
        '<div class="journal-cover-grid">'
        + '\n'.join(cover_card(name, filename) for name, filename in more_covers)
        + '</div></details>'
    ) if more_covers else ''
    gallery_html = (
        '<section id="journal-gallery"><div class="wrap">'
        '<h2>Journal gallery</h2>'
        '<p class="gallery-intro">Selected issue covers from journals in which my work has appeared.</p>'
        f'{featured_html}{main_html}{more_html}'
        '</div></section>'
    )

secondary_preview_html = (
    '<section id="explore-more"><div class="wrap">'
    '<h2>Explore more</h2>'
    '<div class="page-preview-grid">'
    '<article class="card page-preview">'
    '<h3>Code &amp; Data</h3>'
    '<p>Open datasets, computational methods, and tools behind my research.</p>'
    '<a class="preview-link" href="code-data.html">Explore code and data &rarr;</a>'
    '</article>'
    '<article class="card page-preview">'
    '<h3>Teaching &amp; Mentoring</h3>'
    '<p>Courses I support, my teaching approach, and student research mentoring.</p>'
    '<a class="preview-link" href="teaching.html">Explore teaching and mentoring &rarr;</a>'
    '</article>'
    '</div></div></section>'
)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rameswar Bhattacharjee — Computational Chemistry</title>
<meta name="description" content="Rameswar Bhattacharjee — computational chemist working on electronic structure theory, pi-conjugated and radical materials, and machine learning for chemical discovery.">
<link rel="canonical" href="https://rameswariacs.github.io/">
<meta name="robots" content="index, follow">
<meta name="author" content="Rameswar Bhattacharjee">
<meta name="keywords" content="Rameswar Bhattacharjee, computational chemistry, electronic structure theory, pancake bonding, nanohoops, machine learning chemistry, Georgetown University">
<meta property="og:title" content="Rameswar Bhattacharjee — Computational Chemistry">
<meta property="og:description" content="Electronic structure theory, pi-conjugated and radical materials, and machine learning for chemical discovery.">
<meta property="og:url" content="https://rameswariacs.github.io/">
<meta property="og:type" content="profile">
<meta name="google-site-verification" content="hAc3K22zb3C66vtNvdvHTpIAnJmgmK3iT44Jfl8gBTw" />
<style>
  :root {{
    --ink: #1a1a1a; --muted: #5a6270; --accent: #1F3864; --accent-soft: #eaeff8;
    --line: #e2e6ee; --bg: #fdfdfc;
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0; background: var(--bg); color: var(--ink);
    font: 16px/1.65 "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    -webkit-font-smoothing: antialiased;
  }}
  .wrap {{ max-width: 820px; margin: 0 auto; padding: 0 28px; }}

  nav {{
    position: sticky; top: 0; z-index: 20; background: rgba(253,253,252,.94);
    backdrop-filter: blur(8px); border-bottom: 1px solid var(--line);
  }}
  nav .wrap {{ display: flex; gap: 22px; padding-top: 13px; padding-bottom: 13px; flex-wrap: wrap; }}
  nav a {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 13px; letter-spacing: .04em; text-transform: uppercase;
    color: var(--muted); text-decoration: none;
  }}
  nav a:hover {{ color: var(--accent); }}

  header {{ padding: 62px 0 40px; border-bottom: 1px solid var(--line); }}
  .hero-row {{ display: grid; grid-template-columns: minmax(0, 1fr) 190px; gap: 38px; align-items: center; }}
  h1 {{ font-size: 40px; line-height: 1.12; margin: 0 0 10px; letter-spacing: -.015em; color: var(--accent); }}
  .tagline {{ font-size: 18px; color: var(--muted); font-style: italic; margin: 0 0 6px; }}
  .role {{ font-size: 16px; margin: 0 0 22px; }}
  .links {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .links a {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 13px;
    text-decoration: none; color: var(--accent); border: 1px solid var(--line);
    background: #fff; padding: 6px 13px; border-radius: 5px; transition: .15s;
  }}
  .links a:hover {{ background: var(--accent-soft); border-color: #c9d4e8; }}

  .metrics {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 0; margin: 34px 0 0;
    border: 1px solid var(--line); border-radius: 7px; overflow: hidden; background: #fff; }}
  .metric {{ padding: 15px 8px; text-align: center; border-right: 1px solid var(--line); }}
  .metric:last-child {{ border-right: 0; }}
  .metric b {{ display: block; font-size: 24px; color: var(--accent); line-height: 1.2; }}
  .metric span {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 11px;
    text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }}

  .asof {{ margin: 8px 0 0; font-size: 12.5px; color: var(--muted); text-align: right; font-style: italic; }}
  .asof a {{ color: var(--muted); }}
  section {{ padding: 46px 0; border-bottom: 1px solid var(--line); scroll-margin-top: 64px; }}
  h2 {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 13px; letter-spacing: .13em; text-transform: uppercase;
    color: var(--accent); margin: 0 0 26px; font-weight: 600;
  }}
  h3 {{ font-size: 20px; margin: 0 0 8px; color: var(--ink); line-height: 1.3; }}
  p {{ margin: 0 0 14px; }}
  .lede {{ font-size: 17.5px; }}

  .theme {{ margin-bottom: 34px; padding-left: 18px; border-left: 3px solid var(--accent-soft); }}
  .theme ul {{ margin: 10px 0 0; padding-left: 18px; color: var(--muted); font-size: 14.5px; }}
  .theme li {{ margin-bottom: 3px; }}

  ol.pubs {{ list-style: none; margin: 0; padding: 0; }}
  .pub {{ display: flex; gap: 13px; padding: 13px 0; border-bottom: 1px solid #f0f2f6; font-size: 14.5px; line-height: 1.55; }}
  .pub:last-child {{ border-bottom: 0; }}
  .pubnum {{ flex: 0 0 26px; color: #aeb6c4; font-size: 12.5px; padding-top: 3px; text-align: right; }}
  .me {{ font-weight: 700; color: var(--accent); }}
  .doi {{ display: inline-block; margin-top: 3px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11.5px; color: var(--muted); text-decoration: none; }}
  .doi:hover {{ color: var(--accent); text-decoration: underline; }}

  .featured-intro {{ max-width: 760px; color: var(--muted); font-size: 15px; margin-bottom: 20px; }}
  .featured-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; margin-bottom: 38px; }}
  .featured-paper {{
    display: flex; flex-direction: column; overflow: hidden; background: #fff;
    border: 1px solid var(--line); border-radius: 9px;
    box-shadow: 0 6px 18px rgba(20, 43, 75, .055);
  }}
  .featured-figure {{
    display: flex; align-items: center; justify-content: center; height: 230px;
    padding: 14px; background: #fff; border-bottom: 1px solid var(--line);
  }}
  .featured-figure img {{ width: 100%; height: 100%; object-fit: contain; }}
  .featured-body {{ display: flex; flex-direction: column; flex: 1; padding: 18px 19px 19px; }}
  .featured-journal {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: var(--accent); font-size: 11.5px; font-weight: 700; letter-spacing: .07em;
    text-transform: uppercase; margin-bottom: 8px;
  }}
  .featured-title {{ font-size: 16.5px; line-height: 1.38; margin-bottom: 9px; }}
  .featured-summary {{ color: var(--muted); font-size: 14px; line-height: 1.5; margin-bottom: 12px; }}
  .featured-doi {{ margin-top: auto; }}

  .latest-paper {{
    display: grid; grid-template-columns: 1fr;
    overflow: hidden; margin: 18px 0 38px; background: #fff;
    border: 1px solid var(--line); border-radius: 11px;
    box-shadow: 0 10px 28px rgba(20, 43, 75, .08);
  }}
  .latest-figure {{
    display: flex; align-items: center; justify-content: center;
    background: #fff; border-bottom: 1px solid var(--line);
  }}
  .latest-figure img {{ display: block; width: 100%; height: auto; }}
  .latest-body {{ display: flex; flex-direction: column; padding: 26px 28px 28px; }}
  .latest-kicker {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: var(--accent); font-size: 11.5px; font-weight: 700; letter-spacing: .09em;
    text-transform: uppercase; margin-bottom: 10px;
  }}
  .latest-title {{ font-size: 22px; line-height: 1.32; margin-bottom: 12px; }}
  .latest-authors {{ color: var(--muted); font-size: 13.5px; line-height: 1.5; margin-bottom: 14px; }}
  .latest-summary {{ color: var(--muted); font-size: 14.5px; line-height: 1.55; }}
  .latest-badge {{
    display: inline-block; align-self: flex-start; margin: 2px 0 14px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 11px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;
    color: var(--accent); background: var(--accent-soft); padding: 4px 9px; border-radius: 4px;
  }}
  .latest-actions {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 5px; }}
  .latest-actions a {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 12.5px; font-weight: 600; text-decoration: none;
    color: var(--accent); border: 1px solid #c9d4e8; background: var(--accent-soft);
    padding: 6px 11px; border-radius: 5px;
  }}
  .latest-actions a:hover {{ background: #dce5f3; }}

  .card {{ background: #fff; border: 1px solid var(--line); border-radius: 7px; padding: 20px 22px; margin-bottom: 16px; }}
  .card h3 {{ font-size: 17px; }}
  .card p {{ font-size: 14.5px; color: var(--muted); margin-bottom: 10px; }}
  .tag {{ display: inline-block; font-family: -apple-system, sans-serif; font-size: 11px;
    text-transform: uppercase; letter-spacing: .05em; background: var(--accent-soft);
    color: var(--accent); padding: 3px 9px; border-radius: 3px; margin-bottom: 9px; }}

  .stack {{ display: grid; grid-template-columns: 145px 1fr; gap: 8px 18px; font-size: 14.5px; }}
  .stack dt {{ font-weight: 700; color: var(--accent); }}
  .stack dd {{ margin: 0; color: var(--muted); }}

  .teaching-intro {{ font-size: 17px; margin-bottom: 22px; }}
  .course-list {{ display: grid; grid-template-columns: 1fr; gap: 14px; margin-bottom: 28px; }}
  .course {{ margin: 0; }}
  .course-meta {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 12.5px; color: var(--accent); font-weight: 600; letter-spacing: .02em; }}
  .teaching-note {{ font-size: 14.5px; color: var(--muted); }}

  footer {{ padding: 34px 0 60px; font-size: 13.5px; color: var(--muted); }}
  footer .wrap {{ display: flex; justify-content: space-between; align-items: center; gap: 18px; }}
  .back-top {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 13px; text-decoration: none; white-space: nowrap; }}
  .back-top:hover {{ text-decoration: underline; }}
  a {{ color: var(--accent); }}

  @media (max-width: 620px) {{
    h1 {{ font-size: 30px; }}
    .hero-row {{ grid-template-columns: 1fr; gap: 24px; }}
    .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .metric {{ border-right: 1px solid var(--line); border-bottom: 0; }}
    .metric:nth-child(2n) {{ border-right: 0; }}
    .metric:nth-child(n+3) {{ border-top: 1px solid var(--line); }}
    .metric:last-child {{ grid-column: 1 / -1; border-right: 0; }}
    .featured-grid {{ grid-template-columns: 1fr; }}
    .featured-figure {{ height: 210px; }}
    .latest-body {{ padding: 22px; }}
    .latest-title {{ font-size: 19px; }}
    .stack {{ grid-template-columns: 1fr; gap: 2px 0; }}
    .stack dd {{ margin-bottom: 10px; }}
    nav .wrap {{ gap: 14px; }}
  }}

  /* Immersive scientific hero, inspired by the reference site's composition. */
  :root {{
    --ink: #172235; --muted: #536075; --accent: #35264f;
    --accent-soft: #ede9f4; --line: #dbe2eb; --bg: #f7f9fc;
  }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.65; }}
  .wrap {{ max-width: 1100px; padding: 0 30px; }}
  .site-nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 40;
    background: rgba(8, 15, 28, .72); border-bottom: 1px solid rgba(255,255,255,.15);
    backdrop-filter: blur(16px);
  }}
  .nav-inner {{ max-width: 1320px; margin: auto; padding: 18px 30px; display: flex; align-items: center; justify-content: space-between; gap: 28px; }}
  .brand {{ color: #fff; font: 700 25px/1 Georgia, serif; letter-spacing: -.02em; text-decoration: none; white-space: nowrap; }}
  .brand span:last-child {{ display: inline-block; margin-left: 8px; font: 500 14px/1.2 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: .02em; }}
  .brand-dot {{ color: #ad9ace; }}
  .nav-links {{ display: flex; align-items: center; gap: 24px; }}
  .nav-links a {{ color: rgba(255,255,255,.88); font-size: 14px; font-weight: 600; letter-spacing: 0; text-transform: none; }}
  .nav-links a:hover, .nav-links a:focus-visible {{ color: #fff; text-decoration: underline; text-underline-offset: 5px; }}
  .menu-toggle {{ display: none; background: none; border: 0; padding: 8px; cursor: pointer; }}
  .menu-toggle span {{ display: block; width: 25px; height: 2px; margin: 5px 0; border-radius: 2px; background: white; }}
  .hero {{
    min-height: 100svh; padding: 120px 24px 48px; border: 0;
    background: linear-gradient(180deg, rgba(4,9,21,.5), rgba(4,9,21,.34) 48%, rgba(4,9,21,.76)),
                url("images/hero-molecular-orbitals.jpg") center center / cover no-repeat;
    color: #fff;
  }}
  .hero-inner {{ min-height: calc(100svh - 168px); max-width: 1100px; margin: auto; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
  .hero-panel {{
    width: min(100%, 770px); padding: 45px 55px 48px; text-align: center;
    background: rgba(17, 25, 42, .66); border: 1px solid rgba(255,255,255,.27);
    border-radius: 19px; box-shadow: 0 22px 60px rgba(0,0,0,.3); backdrop-filter: blur(18px);
  }}
  .hero-kicker {{ color: #d9d0e8; font-size: 14px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 18px; }}
  .hero h1 {{ color: #fff; font: 500 clamp(3.15rem, 5.8vw, 5.5rem)/1.03 Georgia, "Iowan Old Style", serif; letter-spacing: -.035em; margin-bottom: 24px; }}
  .hero-rule {{ display: block; width: 70px; height: 2px; margin: 0 auto 25px; background: rgba(255,255,255,.75); }}
  .hero .tagline {{ max-width: 620px; margin: auto; color: #f0edf6; font: 400 clamp(1.05rem, 1.8vw, 1.35rem)/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  .hero .role {{ color: #dad5e4; font-size: 15px; margin: 20px 0 27px; }}
  .hero-actions {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 13px; }}
  .hero-button {{ display: inline-flex; justify-content: center; min-width: 190px; padding: 11px 22px; border-radius: 999px; font-size: 14px; font-weight: 700; text-decoration: none; border: 1px solid rgba(255,255,255,.35); }}
  .hero-button-primary {{ color: #fff; background: #46345f; }}
  .hero-button-primary:hover {{ background: #5c457b; }}
  .hero-button-light {{ color: #263043; background: #fff; }}
  .hero-button-light:hover {{ background: #eae7f1; }}
  .scroll-cue {{ color: rgba(255,255,255,.86); text-decoration: none; text-align: center; font-size: 13px; margin-top: auto; padding-top: 34px; }}
  .scroll-cue span {{ display: block; font-size: 20px; line-height: 1.2; }}
  .page-banner {{
    min-height: 340px; display: flex; align-items: end; padding: 115px 0 52px; border: 0;
    color: #fff; background: linear-gradient(90deg, rgba(7,13,27,.9), rgba(17,25,46,.48)),
      url("images/hero-molecular-orbitals.jpg") center 47% / cover no-repeat;
  }}
  .page-banner .wrap {{ width: 100%; }}
  .page-kicker {{ color: #d9d0e8; font-size: 14px; letter-spacing: .1em; text-transform: uppercase; font-weight: 700; margin: 0 0 11px; }}
  .page-banner h1 {{ color: #fff; font: 500 clamp(2.8rem, 5vw, 4.5rem)/1.1 Georgia, serif; margin: 0 0 12px; }}
  .page-banner p:last-child {{ color: #ece9f3; font-size: 18px; max-width: 720px; margin: 0; }}
  .nav-links a[aria-current="page"] {{ color: #fff; text-decoration: underline; text-underline-offset: 6px; }}
  .profile-strip {{ background: #fff; border-bottom: 1px solid var(--line); }}
  .profile-grid {{ padding-top: 28px; padding-bottom: 28px; }}
  .profile-intro p {{ margin-bottom: 15px; max-width: 740px; }}
  .profile-eyebrow {{ color: var(--accent); font-size: 13px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; }}
  .profile-intro .links a {{ font-size: 14px; border-radius: 999px; padding: 5px 12px; }}
  .metrics-band {{ background: #fff; padding: 0 0 30px; border-bottom: 1px solid var(--line); }}
  .metrics {{ margin-top: 0; border-radius: 12px; box-shadow: 0 12px 28px rgba(21, 33, 57, .06); }}
  .metric {{ padding: 18px 8px; }}
  .metric b {{ color: var(--accent); font: 600 27px/1.15 Georgia, serif; }}
  .metric span {{ font-size: 12px; }}
  section {{ padding: 70px 0; scroll-margin-top: 80px; }}
  section:nth-of-type(odd) {{ background: #fff; }}
  h2 {{ font: 600 clamp(1.8rem, 3vw, 2.4rem)/1.2 Georgia, serif; color: var(--ink); text-transform: none; letter-spacing: -.02em; margin-bottom: 28px; }}
  h3 {{ font-family: Georgia, "Iowan Old Style", serif; }}
  .lede {{ font: 400 21px/1.55 Georgia, serif; max-width: 900px; }}
  #about p {{ max-width: 880px; }}
  .about-layout {{ display: grid; grid-template-columns: minmax(0,1fr) 140px; gap: 26px; align-items: start; }}
  .about-copy {{ grid-column: 1; grid-row: 1; }}
  .about-portrait {{ grid-column: 2; grid-row: 1; display: block; width: 140px; height: 170px; object-fit: cover; object-position: 48% 35%; border-radius: 10px; box-shadow: 0 8px 20px rgba(20,34,55,.12); }}
  #research .wrap {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 18px; }}
  #research h2 {{ grid-column: 1 / -1; }}
  .theme {{ margin: 0; padding: 24px; border: 1px solid var(--line); border-left: 3px solid #735c9b; border-radius: 9px; background: #fff; box-shadow: 0 6px 20px rgba(20,34,55,.04); }}
  .theme h3 {{ font-size: 22px; }}
  .theme ul {{ font-size: 14px; }}
  #code .wrap {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 18px; }}
  #code h2 {{ grid-column: 1 / -1; }}
  .card, .featured-paper {{ border-radius: 11px; box-shadow: 0 6px 18px rgba(20,34,55,.04); }}
  #code .card {{ margin: 0; }}
  .featured-grid {{ grid-template-columns: repeat(3, minmax(0,1fr)); }}
  .featured-figure {{ height: 190px; }}
  .latest-paper {{ grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); margin-top: 0; }}
  .latest-figure {{ min-height: 500px; padding: 20px; border-bottom: 0; border-right: 1px solid var(--line); background: #e9edf3; }}
  .latest-figure img {{ width: auto; max-width: 100%; height: 460px; object-fit: contain; background: #fff; box-shadow: 0 12px 28px rgba(20,32,55,.17); }}
  .latest-body {{ justify-content: center; }}
  .latest-kicker, .featured-journal {{ font-size: 13px; }}
  .latest-title {{ font-size: 24px; }}
  .latest-badge {{ font-size: 12px; }}
  .latest-actions a {{ font-size: 14px; border-radius: 999px; padding: 8px 14px; }}
  .course-list {{ grid-template-columns: repeat(3, minmax(0,1fr)); }}
  .course-list .card {{ padding: 23px; }}
  .course-meta {{ font-size: 14px; }}
  .teaching-intro {{ max-width: 900px; }}
  .gallery-intro {{ color: var(--muted); font-size: 16px; margin-top: -12px; margin-bottom: 24px; }}
  .gallery-subtitle {{ margin: 34px 0 8px; color: var(--ink); font: 600 22px/1.25 Georgia, serif; }}
  .gallery-caption {{ margin: 0 0 20px; color: var(--muted); font-size: 15px; }}
  .journal-cover-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 22px; }}
  .journal-cover-card {{ margin: 0; padding: 18px 18px 15px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 6px 18px rgba(20,34,55,.06); text-align: center; }}
  .journal-cover-card img {{ display: block; width: 100%; height: 350px; object-fit: contain; background: #fff; }}
  .journal-cover-card figcaption {{ padding-top: 13px; color: var(--ink); font-size: 14px; font-weight: 700; }}
  .featured-cover-grid .journal-cover-card {{ border-color: #c7b3db; background: #fbf9fd; }}
  .cover-feature-note {{ display: block; margin-top: 8px; color: #684985; font-size: 12px; font-weight: 600; }}
  .more-journals {{ margin-top: 30px; }}
  .more-journals summary {{ display: table; margin: 0 auto 22px; padding: 10px 18px; border: 1px solid #c9b7da; border-radius: 999px; background: #f5f0fa; color: #593d72; font-weight: 700; cursor: pointer; }}
  .more-journals[open] {{ padding-bottom: 8px; }}
  .page-preview-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 22px; }}
  .page-preview {{ padding: 28px; }}
  .page-preview h3 {{ margin: 0 0 8px; }}
  .page-preview p {{ color: var(--muted); }}
  .preview-link {{ display: inline-block; color: #684985; font-weight: 700; text-decoration: none; }}
  .preview-link:hover {{ text-decoration: underline; text-underline-offset: 4px; }}
  a:focus-visible, button:focus-visible {{ outline: 3px solid #b69ad8; outline-offset: 3px; }}

  /* Year-grouped publication rows inside a translucent scientific panel. */
  .page-publications {{
    color: #f4f1f8;
    background: linear-gradient(rgba(6,11,24,.78), rgba(6,11,24,.85)),
      url("images/hero-molecular-orbitals.jpg") center center / cover fixed;
  }}
  .page-publications .page-banner {{ min-height: 290px; padding-bottom: 35px; background: transparent; }}
  .publication-shell {{
    width: min(calc(100% - 48px), 1120px); margin: 0 auto 70px;
    background: rgba(24, 31, 49, .7); border: 1px solid rgba(255,255,255,.22);
    border-radius: 18px; box-shadow: 0 20px 70px rgba(0,0,0,.24);
    backdrop-filter: blur(19px);
  }}
  .page-publications .publication-shell section {{ background: transparent; border-color: rgba(255,255,255,.17); padding: 50px 0; }}
  .page-publications .publication-shell .wrap {{ max-width: 1040px; }}
  .page-publications .publication-shell h2,
  .page-publications .publication-shell > section h3:not(.latest-title):not(.featured-title) {{ color: #fff; }}
  .page-publications .publication-shell > section > .wrap > p {{ color: #d6d8e2 !important; }}
  .page-publications .latest-paper, .page-publications .featured-paper {{ color: var(--ink); }}
  .page-publications .latest-title, .page-publications .featured-title {{ color: var(--ink); }}
  .page-publications .latest-summary, .page-publications .featured-summary,
  .page-publications .latest-authors {{ color: var(--muted); }}
  .page-publications .featured-paper {{ box-shadow: 0 10px 26px rgba(0,0,0,.18); }}
  .pub-year-group {{ margin-top: 38px; }}
  .pub-year {{ text-align: center; margin: 0 0 24px; font: 600 22px/1.2 Georgia, serif; }}
  .pub-year span {{ display: inline-block; border-bottom: 2px solid #b6aacd; padding: 0 0 8px; }}
  .pub-row {{ display: grid; grid-template-columns: 102px minmax(0,1fr); gap: 22px; align-items: center; padding: 14px 16px; margin-bottom: 7px; border: 1px solid rgba(255,255,255,.13); border-radius: 9px; background: rgba(255,255,255,.045); }}
  .pub-row:last-child {{ border-bottom: 1px solid rgba(255,255,255,.13); }}
  .pub-thumbnail {{ width: 102px; height: 80px; display: flex; align-items: center; justify-content: center; overflow: hidden; border-radius: 7px; background: rgba(255,255,255,.11); }}
  .pub-thumbnail img {{ width: 100%; height: 100%; object-fit: cover; background: #fff; }}
  .pub-thumbnail span {{ color: #d9d1e8; font: 600 26px Georgia, serif; }}
  .pub-row .pubnum {{ display: block; padding: 0; margin: 0 0 4px; text-align: left; color: #c8bce0; font-size: 13px; font-weight: 700; }}
  .pub-row .pub-text {{ color: #f4f1f8; font-size: 15px; line-height: 1.5; }}
  .pub-row .me {{ color: #dfd1f5; }}
  .pub-row .doi {{ display: inline-flex; margin-top: 9px; padding: 5px 9px; color: #ece7f7; border: 1px solid rgba(255,255,255,.19); border-radius: 5px; background: rgba(255,255,255,.07); font: 500 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  .page-publications footer {{ color: #d8d5df; }}
  .page-publications footer a {{ color: #f0e8ff; }}

  /* A restrained hover response for links, cards, and imagery. */
  .nav-links a, .hero-button, .links a, .latest-actions a, .doi, .preview-link,
  .theme, .card, .featured-paper, .pub-row, .featured-figure img,
  .latest-figure img, .journal-cover-card, .more-journals summary {{
    transition: transform .24s ease, box-shadow .24s ease,
      background-color .24s ease, border-color .24s ease, color .24s ease;
  }}
  @media (hover: hover) {{
    .nav-links a:hover, .hero-button:hover, .links a:hover,
    .latest-actions a:hover, .doi:hover, .preview-link:hover, .more-journals summary:hover {{ transform: translateY(-2px); }}
    .theme:hover, .card:hover, .featured-paper:hover,
    .journal-cover-card:hover {{ transform: translateY(-4px); box-shadow: 0 14px 32px rgba(20,30,54,.15); }}
    .pub-row:hover {{ transform: translateX(4px); background: rgba(255,255,255,.09); }}
    .featured-figure:hover img, .latest-figure:hover img {{ transform: scale(1.025); }}
  }}
  @media (max-width: 900px) {{
    .brand span:last-child {{ display: none; }}
    .nav-links {{ gap: 13px; }}
    .featured-grid, .course-list {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
    .latest-paper {{ grid-template-columns: 1fr; }}
    .latest-figure {{ border-right: 0; border-bottom: 1px solid var(--line); }}
    .journal-cover-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
    .page-preview-grid {{ grid-template-columns: 1fr; }}
  }}
  @media (max-width: 680px) {{
    .wrap {{ padding: 0 20px; }}
    .nav-inner {{ padding: 14px 20px; }}
    .menu-toggle {{ display: block; }}
    .nav-links {{ display: none; position: absolute; top: 100%; left: 0; right: 0; padding: 14px 20px 20px; flex-direction: column; align-items: stretch; gap: 0; background: rgba(10,17,31,.98); border-bottom: 1px solid rgba(255,255,255,.2); }}
    .nav-links.is-open {{ display: flex; }}
    .nav-links a {{ padding: 10px 0; }}
    .hero {{ min-height: 100svh; padding: 80px 16px 22px; background-position: 49% center; }}
    .hero-inner {{ min-height: calc(100svh - 102px); }}
    .hero-panel {{ padding: 29px 23px 32px; border-radius: 15px; }}
    .hero-kicker {{ font-size: 12px; letter-spacing: .08em; }}
    .hero h1 {{ font-size: clamp(2.75rem, 10vw, 4.3rem); }}
    .hero .tagline {{ font-size: 17px; }}
    .hero-actions {{ flex-direction: column; }}
    .hero-button {{ width: 100%; }}
    .metrics {{ grid-template-columns: repeat(2,minmax(0,1fr)); }}
    .about-layout {{ grid-template-columns: 1fr; gap: 18px; }}
    .about-portrait {{ grid-column: 1; grid-row: 1; width: 128px; height: 156px; justify-self: center; }}
    .about-copy {{ grid-column: 1; grid-row: 2; }}
    #research .wrap, #code .wrap {{ grid-template-columns: 1fr; }}
    .featured-grid, .course-list {{ grid-template-columns: 1fr; }}
    .latest-body {{ padding: 23px; }}
    .latest-title {{ font-size: 22px; }}
    section {{ padding: 53px 0; }}
    .page-banner {{ min-height: 280px; padding: 100px 0 42px; }}
    .publication-shell {{ width: calc(100% - 22px); border-radius: 12px; }}
    .page-publications .publication-shell section {{ padding: 38px 0; }}
    .pub-row {{ grid-template-columns: 64px minmax(0,1fr); gap: 13px; padding: 11px; }}
    .pub-thumbnail {{ width: 64px; height: 64px; }}
    .pub-thumbnail span {{ font-size: 18px; }}
    .pub-row .pub-text {{ font-size: 14px; }}
    .journal-cover-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; }}
    .journal-cover-card {{ padding: 10px 10px 12px; }}
    .journal-cover-card img {{ height: 230px; }}
    .journal-cover-card figcaption {{ font-size: 12px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    html {{ scroll-behavior: auto; }}
    .nav-links a, .hero-button, .links a, .latest-actions a, .doi, .preview-link,
    .theme, .card, .featured-paper, .pub-row, .featured-figure img,
    .latest-figure img, .journal-cover-card, .more-journals summary {{ transition: none; }}
  }}
</style>
</head>
<body id="top">

<nav class="site-nav" aria-label="Main navigation"><div class="nav-inner">
  <a class="brand" href="index.html">RB<span class="brand-dot">.</span> <span>Computational Chemistry</span></a>
  <button class="menu-toggle" type="button" aria-label="Toggle navigation" aria-controls="site-links" aria-expanded="false"><span></span><span></span><span></span></button>
  <div class="nav-links" id="site-links">
    <a href="#about">About</a>
    <a href="research.html">Research</a>
    <a href="code-data.html">Code &amp; Data</a>
    <a href="publications.html">Publications</a>
    {gallery_nav}
    <a href="teaching.html">Teaching</a>
    <a href="#contact">Contact</a>
  </div>
</div></nav>

<header class="hero"><div class="hero-inner">
  <div class="hero-panel">
    <p class="hero-kicker">Georgetown University · Department of Chemistry</p>
    <h1>Rameswar<br>Bhattacharjee</h1>
    <span class="hero-rule" aria-hidden="true"></span>
    <p class="tagline">Electronic structure theory · π-conjugated and radical materials · machine learning for chemical discovery</p>
    <p class="role">Research Assistant Professor</p>
    <div class="hero-actions">
      <a class="hero-button hero-button-primary" href="publications.html#latest-work">Explore latest work</a>
      <a class="hero-button hero-button-light" href="research.html">Explore research</a>
    </div>
  </div>
  <a class="scroll-cue" href="#latest-work">Scroll to explore <span aria-hidden="true">↓</span></a>
</div></header>

<div class="profile-strip"><div class="wrap profile-grid">
  <div class="profile-intro">
    <p class="profile-eyebrow">Computational chemist · Georgetown University</p>
    <p>I study how molecular structure, electronic topology, and π-stacking shape the properties of radical and conjugated materials.</p>
    <div class="links">
      <a href="mailto:rb1820@georgetown.edu">Email</a>
      <a href="https://scholar.google.com/citations?user=E4XO67YAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
      <a href="https://orcid.org/0000-0002-6631-5991" target="_blank" rel="noopener">ORCID</a>
      <a href="https://www.linkedin.com/in/rameswar-bhattacharjee-057249204/" target="_blank" rel="noopener">LinkedIn</a>
      {github_link}
      <a href="CV_Rameswar_Bhattacharjee.pdf">Curriculum Vitae</a>
    </div>
  </div>
</div></div>

<div class="metrics-band"><div class="wrap">
  <div class="metrics">
    <div class="metric"><b>{len(pubs)}</b><span>Publications</span></div>
    <div class="metric"><b>{CITATIONS}</b><span>Citations</span></div>
    <div class="metric"><b>{H_INDEX}</b><span>h-index</span></div>
    <div class="metric"><b>{FIRST_AUTHOR}</b><span>First author</span></div>
    <div class="metric"><b>{CORRESPONDING_AUTHOR}</b><span>Corresponding author</span></div>
  </div>
  <p class="asof">Citation metrics from <a href="https://scholar.google.com/citations?user=E4XO67YAAAAJ" target="_blank" rel="noopener">Google Scholar</a>.</p>
</div></div>

<section id="latest-work"><div class="wrap">
  <h2>Latest work</h2>
  <article class="latest-paper" id="latest-publication">
    <a class="latest-figure" href="https://doi.org/10.26434/chemrxiv.15006941/v1" target="_blank" rel="noopener">
      <img src="images/latest/chemrxiv-preprint-first-page.jpg" alt="First page of the ChemRxiv preprint, showing the title, authors, abstract, and preprint notice" decoding="async">
    </a>
    <div class="latest-body">
      <div class="latest-kicker">ChemRxiv preprint &middot; 2026 &middot; Under revision at JCIM</div>
      <h3 class="latest-title">How Molecular Packing Controls Electronic Structure in &pi;-Stacked Radical Dimers: A DFT and Descriptor-Based Machine-Learning Study</h3>
      <p class="latest-authors"><span class="me">Rameswar Bhattacharjee*</span>; Hans Lischka; Miklos Kertesz*</p>
      <span class="latest-badge">First &amp; corresponding author</span>
      <p class="latest-summary">Interpretable Extra Trees and neural-network models connect molecular packing to four electronic properties across 2,582 configurations of five radical-dimer families, achieving test-set R&sup2; values of 0.94&ndash;0.98 with rigorous geometry-clustered and Y-randomization validation.</p>
      <div class="latest-actions">
        <a href="https://doi.org/10.26434/chemrxiv.15006941/v1" target="_blank" rel="noopener">Read the preprint</a>
        <a href="https://doi.org/10.5281/zenodo.21712041" target="_blank" rel="noopener">Data &amp; code</a>
      </div>
    </div>
  </article>
</div></section>

<section id="about"><div class="wrap">
  <h2>About</h2>
  <div class="about-layout">
  <img class="about-portrait" src="images/profile.png" alt="Portrait of Rameswar Bhattacharjee" width="140" height="170" loading="lazy" decoding="async">
  <div class="about-copy">
  <p class="lede">I am a computational chemist working on the electronic structure of molecular and polymeric
  materials, with a focus on systems where conventional closed-shell intuition breaks down &mdash; open-shell
  radical aggregates, topologically non-trivial conjugated polymers, and strongly correlated &pi;-stacks.</p>
  <p>My work combines high-level electronic structure theory with data-driven methods. Recent projects establish
  design principles for topological conjugated polymers, quantify non-classical &ldquo;pancake&rdquo; bonding in
  radical &pi;-stacks, and introduce interpretable machine-learning frameworks that predict DFT-level electronic
  properties across thousands of molecular packing arrangements. Much of this work is done in close collaboration
  with experimental crystallography and synthesis groups, so that computational predictions are tested rather
  than merely reported.</p>
  <p>I hold a Ph.D. from the Indian Association for the Cultivation of Science and have held postdoctoral
  positions at the University of Delaware, the University of South Dakota, and Georgetown University. I am a
  named participant on active NSF and DOE research awards.</p>
  </div>
  </div>
</div></section>

{secondary_preview_html}

{gallery_html}

<section id="research"><div class="wrap">
  <h2>Research</h2>
{theme_html}
</div></section>

<section id="code"><div class="wrap">
  <h2>Code &amp; Data</h2>
  <div class="card">
    <span class="tag">Dataset + Code</span>
    <h3>&pi;-Stacked radical dimer descriptor dataset</h3>
    <p>Optimized geometries for 2,582 &pi;-stacked radical dimers spanning phenalenyl, olympicenyl, fluorenyl,
    and cyclopenta-fused bis(phenalenyl) systems, together with the Python pipeline for descriptor generation,
    model training, validation, and feature-importance analysis.</p>
    <a class="doi" href="https://doi.org/10.5281/zenodo.21712041" target="_blank" rel="noopener">10.5281/zenodo.21712041</a>
  </div>
  <div class="card">
    <span class="tag">Methods</span>
    <h3>Computational toolkit</h3>
    <dl class="stack">
      <dt>Molecular</dt><dd>Gaussian, ORCA, Q-Chem &mdash; DFT, TDDFT, broken-symmetry DFT, fragment-orbital DFT</dd>
      <dt>Periodic</dt><dd>VASP, CP2K, Quantum ESPRESSO &mdash; band structure, DOS, strain-dependent electronic structure</dd>
      <dt>Multireference</dt><dd>COLUMBUS, OpenMolcas, Molpro &mdash; biradical and polyradical character</dd>
      <dt>Sampling</dt><dd>GOAT conformer search, GFN2-xTB, automated high-throughput dataset curation</dd>
      <dt>Machine learning</dt><dd>Python, scikit-learn, PyTorch &mdash; ensemble trees, MLP regression, descriptor design, validation architecture</dd>
    </dl>
  </div>
</div></section>

<section id="publications"><div class="wrap">
  <h2>Publications</h2>
  <p style="font-size:14.5px;color:var(--muted)">{len(pubs)} peer-reviewed publications. Name in <span class="me">bold</span>;
  asterisk (*) indicates corresponding author. See <a href="https://scholar.google.com/citations?user=E4XO67YAAAAJ" target="_blank" rel="noopener">Google Scholar</a> for citation metrics.</p>



  <h3 style="font-size:18px;margin:30px 0 8px">Featured publications</h3>
  <p class="featured-intro">Six representative papers spanning topological &pi;-conjugated materials and non-classical pancake bonding. Each image is drawn from the article's graphical or supporting artwork.</p>
  <div class="featured-grid">
    <article class="featured-paper">
      <a class="featured-figure" href="https://doi.org/10.1021/jacs.4c10064" target="_blank" rel="noopener"><img src="images/featured/jacs-topological.jpg" alt="Orbital transition in a strained pi-conjugated polymer" loading="lazy" decoding="async"></a>
      <div class="featured-body">
        <div class="featured-journal">J. Am. Chem. Soc. &middot; 2024</div>
        <h3 class="featured-title">Topological Transition in Aromatic and Quinonoid &pi;-Conjugated Polymers Induced by Static Strain</h3>
        <p class="featured-summary">Static strain drives an electronic topological transition in conjugated polymers.</p>
        <a class="doi featured-doi" href="https://doi.org/10.1021/jacs.4c10064" target="_blank" rel="noopener">10.1021/jacs.4c10064</a>
      </div>
    </article>
    <article class="featured-paper">
      <a class="featured-figure" href="https://doi.org/10.1021/jacs.3c14065" target="_blank" rel="noopener"><img src="images/featured/jacs-perylene.jpg" alt="Energy landscape connecting pi-stacked perylene dimer geometries" loading="lazy" decoding="async"></a>
      <div class="featured-body">
        <div class="featured-journal">J. Am. Chem. Soc. &middot; 2024</div>
        <h3 class="featured-title">Structure and Bonding in &pi;-Stacked Perylenes: The Impact of Charge on Pancake Bonding</h3>
        <p class="featured-summary">Charge distribution and orbital overlap explain stabilization across &pi;-stacked perylene dimers.</p>
        <a class="doi featured-doi" href="https://doi.org/10.1021/jacs.3c14065" target="_blank" rel="noopener">10.1021/jacs.3c14065</a>
      </div>
    </article>
    <article class="featured-paper">
      <a class="featured-figure" href="https://doi.org/10.1039/D5SC00639B" target="_blank" rel="noopener"><img src="images/featured/quinonoid-radial.jpeg" alt="Energy-level crossings and molecular orbitals in quinonoid nanohoops" loading="lazy" decoding="async"></a>
      <div class="featured-body">
        <div class="featured-journal">Chemical Science &middot; 2025</div>
        <h3 class="featured-title">Quinonoid Radial &pi;-Conjugation</h3>
        <p class="featured-summary">Mixed aromatic and quinonoid nanohoops reveal frontier-orbital crossings and topological change.</p>
        <a class="doi featured-doi" href="https://doi.org/10.1039/D5SC00639B" target="_blank" rel="noopener">10.1039/D5SC00639B</a>
      </div>
    </article>
    <article class="featured-paper">
      <a class="featured-figure" href="https://doi.org/10.1021/acsmaterialsau.4c00153" target="_blank" rel="noopener"><img src="images/featured/acene-dimers.jpg" alt="Molecular stacks illustrating pancake bonding in cationic acene dimers" loading="lazy" decoding="async"></a>
      <div class="featured-body">
        <div class="featured-journal">ACS Materials Au &middot; 2025</div>
        <h3 class="featured-title">Pancake Bonding in the Stabilization of Cationic Acene Dimers</h3>
        <p class="featured-summary">A comparative study of how charge stabilizes cationic acene dimers through pancake bonding.</p>
        <a class="doi featured-doi" href="https://doi.org/10.1021/acsmaterialsau.4c00153" target="_blank" rel="noopener">10.1021/acsmaterialsau.4c00153</a>
      </div>
    </article>
    <article class="featured-paper">
      <a class="featured-figure" href="https://doi.org/10.1039/d4sc03774j" target="_blank" rel="noopener"><img src="images/featured/triphenylene.png" alt="Triphenylene radical-cation trimer with charge and spectroscopic features" loading="lazy" decoding="async"></a>
      <div class="featured-body">
        <div class="featured-journal">Chemical Science &middot; 2024</div>
        <h3 class="featured-title">A Unique Trimeric Triphenylene Radical Cation: Stacking Aggregation, Bonding, and Stability</h3>
        <p class="featured-summary">Crystallography and computation explain a shared-electron radical-cation trimer.</p>
        <a class="doi featured-doi" href="https://doi.org/10.1039/d4sc03774j" target="_blank" rel="noopener">10.1039/d4sc03774j</a>
      </div>
    </article>
    <article class="featured-paper">
      <a class="featured-figure" href="https://doi.org/10.1021/acs.chemmater.3c02547" target="_blank" rel="noopener"><img src="images/featured/chemmat-topological.jpg" alt="Frontier orbitals switching under strain in an acene pi-conjugated polymer" loading="lazy" decoding="async"></a>
      <div class="featured-body">
        <div class="featured-journal">Chemistry of Materials &middot; 2024</div>
        <h3 class="featured-title">Continuous Topological Transition and Bandgap Tuning in Ethynyl-Linked Acene &pi;-Conjugated Polymers through Mechanical Strain</h3>
        <p class="featured-summary">Mechanical strain provides continuous control of electronic topology and band gaps.</p>
        <a class="doi featured-doi" href="https://doi.org/10.1021/acs.chemmater.3c02547" target="_blank" rel="noopener">10.1021/acs.chemmater.3c02547</a>
      </div>
    </article>
  </div>

  <h3 style="font-size:16px;margin:26px 0 6px">Under review &amp; in preparation</h3>
  <ol class="pubs">
  <li class="pub"><span class="pubnum">&mdash;</span><div>
    <div class="pub-text"><span class="me">Bhattacharjee, R.*</span>; Lischka, H.; Kertesz, M.* How Molecular Packing
    Controls Electronic Structure in &pi;-Stacked Radical Dimers: A DFT and Descriptor-Based Machine-Learning Study.
    <em>Under revision at the Journal of Chemical Information and Modeling</em>, 2026.</div>
    <a class="doi" href="https://doi.org/10.26434/chemrxiv.15006941/v1" target="_blank" rel="noopener">Preprint: 10.26434/chemrxiv.15006941/v1</a><br>
    <a class="doi" href="https://doi.org/10.5281/zenodo.21712041" target="_blank" rel="noopener">Data &amp; code: 10.5281/zenodo.21712041</a>
  </div></li>
  <li class="pub"><span class="pubnum">&mdash;</span><div>
    <div class="pub-text"><span class="me">Bhattacharjee, R.*</span>; Lischka, H.; Kertesz, M.* Mapping the &pi;&ndash;&sigma;
    Bonding Landscape in a Pancake-Bonded Radical Dimer via Data-Driven and Chemistry-Guided Analysis.
    <em>Manuscript in final preparation</em>, 2026.</div>
  </div></li>
  </ol>

  <h3 style="font-size:16px;margin:30px 0 6px">Peer-reviewed</h3>
{pub_items}
</div></section>

<section id="teaching"><div class="wrap">
  <h2>Teaching</h2>
  <p class="teaching-intro">At Georgetown University, I currently teach General Chemistry Laboratory
  (CHEM 1105) as a teaching assistant. I lead a weekly recitation and laboratory session and hold office
  hours for the same group of 24 students.</p>

  <div class="course-list">
    <article class="card course">
      <span class="tag">Current course</span>
      <h3>CHEM 1105 &middot; General Chemistry Laboratory</h3>
      <p class="course-meta">Teaching Assistant &middot; Fall 2026</p>
      <p>One hour of recitation, two hours of laboratory, and one hour of office hours each week. I connect
      experimental observations with molecular explanations, quantitative reasoning, and safe laboratory practice.</p>
    </article>
    <article class="card course">
      <span class="tag">Previous course support</span>
      <h3>Physical Chemistry I</h3>
      <p class="course-meta">Teaching Assistant &middot; Fall 2023 and Fall 2024<br>
      Faculty Assistant &middot; Fall 2025</p>
      <p>I supported the course across three cohorts through problem solving and assessment, helping students
      connect thermodynamic and quantum-mechanical models with equations and chemical meaning.</p>
    </article>
    <article class="card course">
      <span class="tag">Previous course support</span>
      <h3>Computational Chemistry Methods</h3>
      <p class="course-meta">Teaching Assistant &middot; Spring 2025</p>
      <p>I helped students treat computation as a scientific argument: choose and justify a method, benchmark
      calculations, document the workflow, and communicate the limits of a result.</p>
    </article>
  </div>

  <h3>Teaching approach</h3>
  <p class="teaching-note">My teaching begins with a chemical question and a qualitative prediction, then moves
  among molecular pictures, equations, and data before returning to the chemical meaning of the result.</p>
  <p class="teaching-note">I am prepared to teach general, physical, quantum, and computational chemistry and to
  develop a project-based course in electronic structure and data-driven chemistry.</p>
</div></section>

<section id="mentoring"><div class="wrap">
  <h2>Mentoring</h2>
  <p class="teaching-note">I have mentored four undergraduate researchers. One Georgetown undergraduate became
  a co-author on two papers, and two NSF REU students each completed a self-contained project during a ten-week
  summer program.</p>
</div></section>

<section id="contact"><div class="wrap">
  <h2>Contact</h2>
  <p>Department of Chemistry, Georgetown University<br>
  37th and O Streets NW, Washington, DC 20057</p>
  <p><a href="mailto:rb1820@georgetown.edu">rb1820@georgetown.edu</a></p>
</div></section>

<footer><div class="wrap">
  <span>&copy; <span id="yr"></span> Rameswar Bhattacharjee.</span>
  <a class="back-top" href="#top">Back to top &uarr;</a>
</div></footer>

<script>
  document.getElementById('yr').textContent = new Date().getFullYear();
  const menuButton = document.querySelector('.menu-toggle');
  const siteLinks = document.querySelector('.nav-links');
  menuButton.addEventListener('click', () => {{
    const open = siteLinks.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(open));
  }});
  siteLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {{
    siteLinks.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
  }}));
</script>
</body>
</html>
"""

def section_markup(source, section_id):
    start = source.index(f'<section id="{section_id}">')
    end = source.index('</section>', start) + len('</section>')
    return source[start:end]

def page_metadata(source, page, title, description):
    result = source.replace(
        '<title>Rameswar Bhattacharjee — Computational Chemistry</title>',
        f'<title>{html.escape(title)} — Rameswar Bhattacharjee</title>', 1
    )
    result = re.sub(
        r'<meta name="description" content="[^"]+">',
        f'<meta name="description" content="{html.escape(description, quote=True)}">',
        result, count=1
    )
    result = result.replace(
        'href="https://rameswariacs.github.io/"',
        f'href="https://rameswariacs.github.io/{page}"', 1
    )
    result = result.replace(
        'content="https://rameswariacs.github.io/"',
        f'content="https://rameswariacs.github.io/{page}"', 1
    )
    result = result.replace(
        '<meta property="og:title" content="Rameswar Bhattacharjee — Computational Chemistry">',
        f'<meta property="og:title" content="{html.escape(title, quote=True)} — Rameswar Bhattacharjee">', 1
    )
    result = re.sub(
        r'<meta property="og:description" content="[^"]+">',
        f'<meta property="og:description" content="{html.escape(description, quote=True)}">',
        result, count=1
    )
    return result

head = HTML[:HTML.index('<body id="top">')]
nav_start = HTML.index('<nav class="site-nav"')
nav_end = HTML.index('</nav>', nav_start) + len('</nav>')
nav_markup = HTML[nav_start:nav_end]
footer_markup = HTML[HTML.index('<footer>'):]

def interior_nav(current):
    links = nav_markup.replace('href="#about"', 'href="index.html#about"')
    links = links.replace('href="#journal-gallery"', 'href="index.html#journal-gallery"')
    links = links.replace('href="#contact"', 'href="index.html#contact"')
    active = f'{current}.html'
    return links.replace(f'<a href="{active}">', f'<a href="{active}" aria-current="page">', 1)

def interior_page(filename, title, subtitle, content):
    page_head = page_metadata(head, filename, title, subtitle)
    banner = (
        '<header class="page-banner"><div class="wrap">'
        '<p class="page-kicker">Rameswar Bhattacharjee · Computational Chemistry</p>'
        f'<h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p>'
        '</div></header>'
    )
    current = filename.removesuffix('.html')
    if current == 'publications':
        content = '<main class="publication-shell">' + content + '</main>'
    return (
        page_head + f'<body id="top" class="page-{current}">\n'
        + interior_nav(current) + '\n' + banner + '\n' + content + '\n' + footer_markup
    )

research_page = interior_page(
    'research.html', 'Research',
    'Electronic structure, radical π-stacking, conjugated materials, and machine learning.',
    section_markup(HTML, 'research')
)
code_page = interior_page(
    'code-data.html', 'Code & Data',
    'Open datasets and the computational methods behind my research.',
    section_markup(HTML, 'code')
)
publications_page = interior_page(
    'publications.html', 'Publications',
    f'Latest work, selected articles, and the complete list of {len(pubs)} peer-reviewed publications.',
    section_markup(HTML, 'latest-work') + '\n' + section_markup(HTML, 'publications')
)
teaching_page = interior_page(
    'teaching.html', 'Teaching & Mentoring',
    'Course support, teaching approach, and undergraduate research mentoring.',
    section_markup(HTML, 'teaching') + '\n' + section_markup(HTML, 'mentoring')
)

home = HTML
for section_id in ('research', 'code', 'publications', 'teaching', 'mentoring'):
    home = home.replace(section_markup(HTML, section_id), '', 1)

for name, content in (
    ('index.html', home),
    ('research.html', research_page),
    ('code-data.html', code_page),
    ('publications.html', publications_page),
    ('teaching.html', teaching_page),
):
    pathlib.Path(name).write_text(content, encoding='utf-8')
print(f'wrote five pages — {len(pubs)} publications')
