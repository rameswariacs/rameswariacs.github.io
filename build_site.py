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
# EDIT THESE FIVE LINES when you refresh your publication metrics,
# then re-run:  python3 build_site.py
CITATIONS     = "1,196"
H_INDEX       = "19"
FIRST_AUTHOR  = "17"
CORRESPONDING_AUTHOR = "7"
METRICS_AS_OF = "August 2026"
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

pub_items = '\n'.join(
    f'      <li class="pub"><span class="pubnum">{len(pubs)-i}</span><div>{render_pub(p)}</div></li>'
    for i, p in enumerate(pubs)
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
  .profile-photo {{
    display: block; width: 190px; height: 210px; object-fit: cover; object-position: center 34%;
    border-radius: 12px; border: 1px solid var(--line); background: #fff;
    box-shadow: 0 10px 28px rgba(20, 43, 75, .13);
  }}
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
    .profile-photo {{ grid-row: 1; width: 160px; height: 176px; }}
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
</style>
</head>
<body id="top">

<nav><div class="wrap">
  <a href="#about">About</a>
  <a href="#research">Research</a>
  <a href="#code">Code &amp; Data</a>
  <a href="#publications">Publications</a>
  <a href="#teaching">Teaching</a>
  <a href="#contact">Contact</a>
</div></nav>

<header><div class="wrap">
  <div class="hero-row">
    <div>
      <h1>Rameswar Bhattacharjee</h1>
      <p class="tagline">Electronic structure theory &middot; &pi;-conjugated and radical materials &middot; machine learning for chemical discovery</p>
      <p class="role">Research Assistant Professor, Department of Chemistry, Georgetown University</p>
      <div class="links">
        <a href="mailto:rb1820@georgetown.edu">Email</a>
        <a href="https://scholar.google.com/citations?user=E4XO67YAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
        <a href="https://orcid.org/0000-0002-6631-5991" target="_blank" rel="noopener">ORCID</a>
        <a href="https://www.linkedin.com/in/rameswar-bhattacharjee-057249204/" target="_blank" rel="noopener">LinkedIn</a>
        {github_link}
        <a href="CV_Rameswar_Bhattacharjee.pdf">Curriculum Vitae</a>
      </div>
    </div>
    <img class="profile-photo" src="images/profile.png" alt="Portrait of Rameswar Bhattacharjee">
  </div>
  <div class="metrics">
    <div class="metric"><b>{len(pubs)}</b><span>Publications</span></div>
    <div class="metric"><b>{CITATIONS}</b><span>Citations</span></div>
    <div class="metric"><b>{H_INDEX}</b><span>h-index</span></div>
    <div class="metric"><b>{FIRST_AUTHOR}</b><span>First author</span></div>
    <div class="metric"><b>{CORRESPONDING_AUTHOR}</b><span>Corresponding author</span></div>
  </div>
  <p class="asof">Citation metrics from <a href="https://scholar.google.com/citations?user=E4XO67YAAAAJ" target="_blank" rel="noopener">Google Scholar</a>, {METRICS_AS_OF}.</p>
</div></header>

<section id="about"><div class="wrap">
  <h2>About</h2>
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
</div></section>

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

  <h3 style="font-size:18px;margin:30px 0 8px">Latest work</h3>
  <article class="latest-paper" id="latest-publication">
    <a class="latest-figure" href="https://doi.org/10.26434/chemrxiv.15006941/v1" target="_blank" rel="noopener">
      <img src="images/latest/ml-radical-dimers-toc.png" alt="Machine-learning workflow mapping pi-stacked radical-dimer coordinates and structural descriptors to predicted electronic properties" decoding="async">
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
  <ol class="pubs">
{pub_items}
  </ol>
</div></section>

<section id="teaching"><div class="wrap">
  <h2>Teaching &amp; Mentoring</h2>
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

  <h3>Teaching approach and mentoring</h3>
  <p class="teaching-note">My teaching begins with a chemical question and a qualitative prediction, then moves
  among molecular pictures, equations, and data before returning to the chemical meaning of the result. I have
  mentored four undergraduate researchers. One Georgetown undergraduate became a co-author on two papers, and
  two NSF REU students each completed a self-contained project during a ten-week summer program.</p>
  <p class="teaching-note">I am prepared to teach general, physical, quantum, and computational chemistry and to
  develop a project-based course in electronic structure and data-driven chemistry.</p>
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

<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

out = pathlib.Path('site')
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(HTML, encoding='utf-8')
print(f'wrote site/index.html — {len(pubs)} publications, {len(HTML)} bytes')
