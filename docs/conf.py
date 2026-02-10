from datetime import datetime

project = "adamacs documentation"
author = "Rose Lab"
copyright = f"{datetime.now():%Y}, Rose Lab"
release = "2026.02"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
]

source_suffix = {
    ".md": "markdown",
}

master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "substitution",
    "tasklist",
]

html_theme = "sphinx_rtd_theme"
html_title = "adamacs documentation"
html_static_path = ["assets"]
html_css_files = ["custom.css"]
html_show_sourcelink = False

# Make links to section headings predictable in markdown pages.
myst_heading_anchors = 3
