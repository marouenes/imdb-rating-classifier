#
# imdb-rating-classifier documentation master file, created by
# sphinx-quickstart on Sat Jan 21 15:49:28 2023.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# append the project root to the path
import pathlib
import sys

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
from imdb_rating_classifier import __version__  # noqa: E402

author = 'Marouane Skandaji'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# the suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    '_build',
    'naming20.rst',
    'test/*',
    'old_*',
    '*attic*',
    '*/attic*',
    'funcargs.rst',
    'setup.rst',
    'example/remoteinterp.rst',
]

# General information about the project.
project = 'imdb-rating-classifier'
copyright = '2023, Marouane Skandaji'


_repo = 'https://github.com/marouenes/imdb-rating-classifier'
extlinks = {
    'pypi': ('https://pypi.org/project/%s/', '%s'),
    'issue': (f'{_repo}/issues/%s', 'issue #%s'),
    'pull': (f'{_repo}/pull/%s', 'pull request #%s'),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {"index_logo": None}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = 'imdb-rating-classifier v%s' % release

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'imdb-rating-classifier-%s' % release

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'img/imdb-logo.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}
# html_sidebars = {'index': 'indexsidebar.html'}

html_sidebars = {
    'index': [
        'slim_searchbox.html',
        'sidebarintro.html',
        'globaltoc.html',
        'links.html',
        'sourcelink.html',
    ],
    '**': [
        'slim_searchbox.html',
        'globaltoc.html',
        'links.html',
        'sourcelink.html',
    ],
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}
# html_additional_pages = {'index': 'index.html'}


# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = False

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'imdb-rating-classifer-doc'


# -- Extension configuration -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#extension-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
]
