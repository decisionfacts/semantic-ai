# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Semantic AI'
copyright = '2023, DecisionFacts'
author = 'DecisionFacts Inc'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']

# Adding a custom css file in order to add custom css file and can change the necessary elements.
html_favicon = "_static/images/df.png"
html_css_files = ["base.css"]
# html_js_files = ["js/githubStargazers.js", "js/sidebarScrollPosition.js"]

html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "images/df.png",
    "dark_logo": "images/df.png",
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
        "font-stack": "Verdana, sans-serif",
        "font-stack--monospace": "Courier, monospace",
        "color-sidebar-background": "#FFFFFF",
        "color-sidebar-background-border": "#e9eaed",
        "color-sidebar-caption-text": "#484848",
        "color-sidebar-link-text": "#484848",
        "color-sidebar-link-text--top-level": "#484848",
        "color-sidebar-item-background--current": "transparent",
        "color-sidebar-item-background--hover": "transparent",
        "color-sidebar-item-expander-background": "transparent",
        "color-sidebar-item-expander-background--hover": "transparent",
        "color-sidebar-search-text": "#484848",
        "color-sidebar-search-background": "#FFFFFF",
        "color-sidebar-search-background--focus": "#FFFFFF",
        "color-sidebar-search-border": "#b9b9b9",
        "color-sidebar-search-border-focus": "#484848",
        "color-sidebar-current-text": "#ff675f",
        "color-content-foreground": "#484848",
        "color-toc-title": "#212529",
        "color-toc-item-text--hover": "#484848",
        "color-toc-item-text--active": "#484848",
        "color-table-header": "#FDDACA",
        "color-table-bg": "#FFE5D9",
        "color-table-row": "#FEEDE6",
        "color-link": "#ff675f",
        "color-link--hover": "#ff675f",
        "content-padding": "5em",
        "content-padding--small": "2em",
        "color-search-icon": "#484848",
        "color-search-placeholder": "#484848",
        "color-literal": "#FF675F",
        "toc-spacing-vertical": "3em",
        "color-page-info": "#646776",
        "toc-item-spacing-vertical": "1em",
        "color-img-background": "#ffffff",
        "sidebar-tree-space-above": "0",
        "sidebar-caption-space-above": "0",
    },
    "dark_css_variables": {
        "font-stack": "Verdana, sans-serif",
        "font-stack--monospace": "Courier, monospace",
        "color-sidebar-background": "#131416",
        "color-sidebar-background-border": "#303335",
        "color-sidebar-caption-text": "#FFFFFF",
        "color-sidebar-link-text": "#FFFFFF",
        "color-sidebar-link-text--top-level": "#FFFFFF",
        "color-sidebar-item-background--current": "none",
        "color-sidebar-item-background--hover": "none",
        "color-sidebar-item-expander-background": "transparent",
        "color-sidebar-item-expander-background--hover": "transparent",
        "color-sidebar-search-text": "#FFFFFF",
        "color-sidebar-search-background": "#131416",
        "color-sidebar-search-background--focus": "transparent",
        "color-sidebar-search-border": "#FFFFFF",
        "color-sidebar-search-border-focus": "#FFFFFF",
        "color-sidebar-search-foreground": "#FFFFFF",
        "color-sidebar-current-text": "#FFC2BF",
        "color-content-foreground": "#FFFFFF",
        "color-toc-title": "#FFFFFF",
        "color-toc-item-text--hover": "#FFFFFF",
        "color-toc-item-text--active": "#FFFFFF",
        "color-table-header": "#131416",
        "color-table-bg": "#232427",
        "color-table-row": "#444444",
        "color-link": "#FFC2BF",
        "color-link--hover": "#FFC2BF",
        "color-search-icon": "#FFFFFF",
        "color-search-placeholder": "#FFFFFF",
        "color-literal": "#F8C0A7",
        "color-page-info": "#FFFFFF",
        "color-img-background": "#131416",
        "sidebar-tree-space-above": "0",
        "sidebar-caption-space-above": "0",
    },
}
