"""Sphinx configuration for page2401/sphinx (Sphinx 9.1 + MyST-Parser 5.2 + Furo)."""

from __future__ import annotations

from sphinxcontrib.mermaid import mermaid as mermaid_node

# -- Project information -----------------------------------------------------
project = "Sphinx 9.1 + MyST 基准实测子站"
copyright = "2026, page2401"
author = "page2401"
language = "zh_CN"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.mathjax",
    "sphinxcontrib.mermaid",
]

source_suffix = {
    ".md": "markdown",
}
master_doc = "index"

exclude_patterns = [
    "_build",
    ".venv",
    ".github",
    "Thumbs.db",
    ".DS_Store",
    "README.md",
]

# -- MyST-Parser scientific Markdown configuration ---------------------------
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
    "deflist",
    "tasklist",
    "attrs_inline",
    "alert",
]
myst_heading_anchors = 3
myst_dmath_allow_labels = True
myst_fence_as_directive = ["mermaid"]

# -- Zero-CDN local MathJax 3 (tex-svg-full) configuration -------------------
mathjax_path = "vendor/tex-svg.js"
mathjax3_config = {
    "tex": {
        "inlineMath": [["\\(", "\\)"]],
        "displayMath": [["\\[", "\\]"]],
    },
    "options": {
        "enableMenu": False,
    },
}

# -- Zero-CDN local Mermaid 12.3 configuration -------------------------------
mermaid_output_format = "raw"
mermaid_use_local = "vendor/mermaid-esm.mjs"
mermaid_include_elk = False
mermaid_include_zenuml = False
mermaid_d3_zoom = False

# -- HTML output (Furo theme + dirhtml clean URLs) ---------------------------
html_theme = "furo"
html_title = "Sphinx 9.1 + MyST 5.2 基准实测子站"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_copy_source = False
html_show_sourcelink = False


def _inject_local_mermaid_umd(app, pagename, templatename, context, doctree):
    """Load local UMD mermaid.min.js before sphinxcontrib-mermaid's ES module script."""
    if doctree and doctree.next_node(mermaid_node):
        app.builder.add_js_file("vendor/mermaid.min.js", priority=100)


def setup(app):
    app.connect("html-page-context", _inject_local_mermaid_umd)
