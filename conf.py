import pathlib

import GooseBib as bib
import pybtex.plugin
import texplain
import subprocess
import pathlib
import os
from pybtex.style.formatting import toplevel
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import field
from pybtex.style.template import href
from pybtex.style.template import join
from pybtex.style.template import optional_field
from pybtex.style.template import sentence
from pybtex.style.template import words
from contextlib import contextmanager


def myformat():
    root = pathlib.Path(__file__).parent
    bibfile = (root / "library.bib").read_text()

    data = {
        "library_invited.bib": [
            "conference_deGeus2022_7_invited",
            "conference_deGeus2022_4_invited",
            "conference_deGeus2021_1_invited",
            "conference_deGeus2019_4_invited",
            "conference_deGeus2019_3_invited",
            "conference_deGeus2018_1_invited",
            "conference_deGeus2017_3_invited",
            "conference_deGeus2017_2_invited",
            "conference_deGeus2015_5_invited",
            "conference_deGeus2015_4_invited",
        ],
        "library_conferences.bib": [
            "conference_deGeus2023_2",
            "conference_deGeus2023_1",
            "conference_deGeus2022_6",
            "conference_deGeus2022_5",
            "conference_deGeus2022_3",
            "conference_deGeus2022_2",
            "conference_deGeus2022_1",
            "conference_deGeus2021_2",
            "conference_deGeus2019_2",
            "conference_deGeus2019_1",
            "conference_deGeus2017_1",
            "conference_deGeus2016_5",
            "conference_deGeus2016_4",
            "conference_deGeus2016_3",
            "conference_deGeus2016_2",
            "conference_deGeus2016_1",
            "conference_deGeus2015_3",
            "conference_deGeus2015_2",
            "conference_deGeus2014_3",
            "conference_deGeus2014_2",
            "conference_deGeus2014_1",
            "conference_deGeus2013_3",
            "conference_deGeus2013_2",
            "conference_deGeus2013_1",
            "conference_deGeus2012_1",
        ],
        "library_posters.bib": [
            "poster_deGeus2022_2",
            "poster_deGeus2022_1",
            "poster_deGeus2018_2",
            "poster_deGeus2018_1",
            "poster_deGeus2017_1",
            "poster_deGeus2016_2",
            "poster_deGeus2016_1",
            "poster_deGeus2015_3",
            "poster_deGeus2015_2",
            "poster_deGeus2015_1",
            "poster_deGeus2014_2",
            "poster_deGeus2014_1",
            "poster_deGeus2013_2",
            "poster_deGeus2013_1",
            "poster_deGeus2012_1",
        ],
        "library_seminars.bib": [
            "seminar_deGeus2022_8",
            "seminar_deGeus2022_7",
            "seminar_deGeus2022_6",
            "seminar_deGeus2022_5",
            "seminar_deGeus2022_4",
            "seminar_deGeus2022_3",
            "seminar_deGeus2022_2",
            "seminar_deGeus2022_1",
            "seminar_deGeus2021_1",
            "seminar_deGeus2019_1",
            "seminar_deGeus2018_1",
            "seminar_deGeus2017_1",
            "seminar_deGeus2016_2",
            "seminar_deGeus2016_1",
        ],
        "library_publications.bib": [
            "ElSergany2023",
            "Poincloux2023",
            "deGeus2023",
            "deGeus2022",
            "Ji2022",
            "Popovic2021a",
            "Popovic2021b",
            "Vondrejc2020",
            "Ji2020",
            "Volmer2019",
            "deGeus2019",
            "Ji2019",
            "Popovic2018",
            "deGeus2017",
            "Zeman2017",
            "deGeus2017a",
            "deGeus2016",
            "deGeus2016c",
            "deGeus2016a",
            "deGeus2016b",
            "VanBeeck2016",
            "deGeus2016d",
            "deGeus2015a",
            "deGeus2015",
            "deGeus2014",
            "deGeus2013",
        ],
        # "library_friction.bib": [
        #     "ElSergany2023",
        #     "Poincloux2023",
        #     "deGeus2022",
        #     "deGeus2019",
        # ],
        # "library_amorphous.bib": [
        #     "Popovic2021a",
        #     "Popovic2021b",
        #     "Popovic2018",
        # ],
    }

    for fname, keys in data.items():
        fpath = root / fname
        fpath.write_text(texplain.bib_select(bibfile, keys, reorder=True))
        bib.bibtex.GbibClean(
            [
                "--in-place",
                "--arxiv",
                "arXiv preprint: {}",
                "--rename-field",
                "arxivid",
                "eprint",
                "--add-field",
                "book:date",
                "--add-field",
                "book:number",
                "--add-field",
                "book:address",
                fpath,
            ]
        )

    return [fname for fname in data]

libraries = myformat()

@contextmanager
def cwd(dirname: pathlib.Path):
    """
    Set the cwd to a specified directory::

        with cwd("foo"):
            # Do something in foo

    :param dirname: The directory to change to.
    """
    origin = pathlib.Path().absolute()
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(origin)


root = pathlib.Path(__file__).parent
projects = ["stick-slip", "shear-band", "fracture_dp"]

for project in projects:
    with cwd(root / "research" / project):
        subprocess.run(["latexmk", "-pdf", "main.tex"])


class MyConf(UnsrtStyle):
    def get_book_template(self, e):
        name = join(sep=", ")[field("publisher"), optional_field("number")]
        template = toplevel[
            # self.format_author_or_editor(e),
            words[field("date") if "date" in e.fields else field("year")],
            self.format_btitle(e, "title"),
            href(field("url", raw=True))[name] if "url" in e.fields else name,
            sentence[
                optional_field("address"),
                words[field("date") if "date" in e.fields else field("year")],
            ],
        ]
        return template


class MyPoster(UnsrtStyle):
    def get_book_template(self, e):
        name = join(sep=", ")[field("publisher"), optional_field("number")]
        template = toplevel[
            self.format_author_or_editor(e),
            # self.format_btitle(e, 'title'),
            href(field("url", raw=True))[name] if "url" in e.fields else name,
            sentence[
                optional_field("address"),
                words[field("date") if "date" in e.fields else field("year")],
            ],
        ]
        return template


class MySeminar(UnsrtStyle):
    def get_book_template(self, e):
        template = toplevel[
            sentence[
                field("publisher"),
                optional_field("number"),
                optional_field("address"),
                words[field("date") if "date" in e.fields else field("year")],
            ],
            self.format_web_refs(e),
        ]
        return template


pybtex.plugin.register_plugin("pybtex.style.formatting", "myconf", MyConf)
pybtex.plugin.register_plugin("pybtex.style.formatting", "myposter", MyPoster)
pybtex.plugin.register_plugin("pybtex.style.formatting", "myseminar", MySeminar)

project = "Tom de Geus"
copyright = "Tom de Geus"
author = "Tom de Geus"
html_theme = "furo"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_title = "Tom de Geus"
extensions = ["sphinxcontrib.bibtex", "sphinx_design"]
bibtex_bibfiles = libraries
