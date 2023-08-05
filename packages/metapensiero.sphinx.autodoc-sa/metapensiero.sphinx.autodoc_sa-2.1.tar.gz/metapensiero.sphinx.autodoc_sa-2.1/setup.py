# -*- coding: utf-8 -*-
# :Project:   metapensiero.sphinx.autodoc_sa -- Autodoc extension to pretty print canned SA queries
# :Created:   Sat 14 Jan 2017 10:34:19 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017, 2019 Lele Gaifax
#

from io import open
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name="metapensiero.sphinx.autodoc_sa",
    version=VERSION,
    url="https://bitbucket.org/lele/metapensiero.sphinx.autodoc_sa",

    description="Autodoc extension to pretty print canned SA queries",
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/x-rst',

    author="Lele Gaifax",
    author_email="lele@metapensiero.it",

    license="GPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Database",
        "Topic :: Utilities",
        "Framework :: Sphinx :: Extension",
        ],
    keywords="",

    packages=['metapensiero.sphinx.' + pkg
              for pkg in find_packages('src/metapensiero/sphinx')],
    package_dir={'': 'src'},
    namespace_packages=['metapensiero', 'metapensiero.sphinx'],

    install_requires=[
        'setuptools',
        'sphinx',
        'sqlalchemy',
    ],
    extras_require={
        'dev': [
            'metapensiero.tool.bump_version',
            'readme_renderer',
            'twine',
        ]
    },
)
