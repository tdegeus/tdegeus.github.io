import os
import pathlib
import shutil
import subprocess
from contextlib import contextmanager

import GooseBib as bib
import pybtex.plugin
import texplain
from pybtex.style.formatting import toplevel
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.labels import BaseLabelStyle
from pybtex.style.template import field
from pybtex.style.template import href
from pybtex.style.template import join
from pybtex.style.template import optional_field
from pybtex.style.template import sentence
from pybtex.style.template import words


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
            "seminar_deGeus2024_1",
            "seminar_deGeus2022_10",
            "seminar_deGeus2022_9",
            "seminar_deGeus2022_8",
            "seminar_deGeus2022_7",
            "seminar_deGeus2022_6",
            "seminar_deGeus2022_5",
            "seminar_deGeus2022_4",
            "seminar_deGeus2022_3",
            "seminar_deGeus2022_2",
            "seminar_deGeus2022_1",
            "seminar_deGeus2021_2",
            "seminar_deGeus2021_1",
            "seminar_deGeus2020_1",
            "seminar_deGeus2019_2",
            "seminar_deGeus2019_1",
            "seminar_deGeus2018_1",
            "seminar_deGeus2017_1",
            "seminar_deGeus2016_2",
            "seminar_deGeus2016_1",
        ],
        "library_publications.bib": [
            "deGeus2024",
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
        "library_students.bib": [
            "thesis_Mortgat2023",
            "thesis_Pottie2023",
            "thesis_Fjellman2023",
            "thesis_Bugnard2023",
            "thesis_ElSergany2023",
            "thesis_Fjellman2022",
            "thesis_ElSergany2022",
            "thesis_Linder2022",
            "thesis_Li2022",
            "thesis_Ji2021",
            "thesis_Salomon2021",
            "thesis_Georgantas2019",
            "thesis_Chappuis2018",
            "thesis_Ma2018",
            "thesis_YllaArbos2017",
            "thesis_vanDuuren2016",
            "thesis_Dorussen2016",
            "thesis_Keulen2016",
            "thesis_Brekelmans2016",
            "thesis_Smeenk2015",
            "thesis_Tilmans2015",
            "thesis_Hubregtse2014",
            "thesis_Brands2014",
            "thesis_Ramp2014",
            "thesis_Mulder2014",
            "thesis_Lapasset2013",
            "thesis_Dronneau2013",
            "thesis_Ortun2013",
            "thesis_Maassen2013",
            "thesis_Hatzidimitris2013",
        ],
    }

    remove_fields = {
        "library_invited.bib": ["author"],
        "library_conferences.bib": ["author"],
        "library_seminars.bib": ["author"],
    }

    for fname, keys in data.items():
        fpath = root / fname
        fpath.write_text(texplain.bib_select(bibfile, keys, reorder=True))
        opts = [
            "--in-place",
            "--arxiv",
            "arXiv preprint: {}",
            "--add-field",
            "book:date",
            "--add-field",
            "book:number",
            "--add-field",
            "book:address",
            "--add-field",
            "phdthesis:type",
            "--add-field",
            "phdthesis:urldate",
        ]
        if fname in remove_fields:
            for key in remove_fields[fname]:
                opts += ["--remove-field", key]
        bib.bibtex.GbibClean(opts + [fpath])

    return [fname for fname in data]


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


libraries = myformat()
root = pathlib.Path(__file__).parent
bib.bibtex.GbibClean(
    [
        "--force",
        "--output",
        root / "research" / "library.bib",
        "--arxiv",
        "arXiv preprint: {}",
        root / "library.bib",
    ]
)

for project in [f for f in (root / "research").glob("*") if f.is_dir()]:
    with cwd(project):
        if not pathlib.Path("main.tex").exists():
            continue
        for fname in ["goose-article.cls", "unsrtnat.bst", "library.bib"]:
            shutil.copyfile(f"../{fname}", fname)
        if project.name == "cv":
            for lib in libraries:
                shutil.copyfile(f"../../{lib}", lib)
        result = subprocess.run(["latexmk", "-pdf", "main.tex"], capture_output=True)
        if result.returncode != 0:
            print(result.stdout.decode("utf-8"))
            raise RuntimeError(f"latexmk {project}/main.tex failed")

        if project.name in ["cv", "teaching", "ambizione"]:
            continue
        result = subprocess.run(
            [
                "gs",
                "-q",
                "-dNOSAFER",
                "-dNODISPLAY",
                "-c",
                '"(main.pdf) (r) file runpdfbegin pdfpagecount = quit"',
            ],
            capture_output=True,
        )
        if result.stdout.decode("utf-8").strip() != "1":
            raise RuntimeError(f"{project}/main.pdf not one page")


class MyPublicationsLabelStyle(BaseLabelStyle):
    def format_labels(self, sorted_entries):
        for i, entry in enumerate(sorted_entries):
            yield str(len(sorted_entries) - i)


class MyPublications(UnsrtStyle):
    default_label_style = MyPublicationsLabelStyle


class MyConf(UnsrtStyle):
    default_label_style = MyPublicationsLabelStyle

    def get_book_template(self, e):
        name = join(sep=", ")[field("publisher"), optional_field("number")]
        template = toplevel[
            # self.format_author_or_editor(e),
            words[field("date") if "date" in e.fields else field("year")],
            self.format_btitle(e, "title"),
            href(field("url", raw=True))[name] if "url" in e.fields else name,
            sentence[optional_field("address"),],
        ]
        return template


class MyPoster(UnsrtStyle):
    default_label_style = MyPublicationsLabelStyle

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
    default_label_style = MyPublicationsLabelStyle

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
pybtex.plugin.register_plugin("pybtex.style.formatting", "mypublications", MyPublications)

project = "Tom de Geus"
copyright = "Tom de Geus"
author = "Tom de Geus"
html_theme = "furo"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_title = "Tom de Geus"
extensions = [
    "sphinxcontrib.bibtex",
    "sphinx_design",
    "sphinx.ext.githubpages",
    "sphinx_reredirects",
]
bibtex_bibfiles = libraries
html_favicon = "favicon.ico"
redirects = {
    "phd": "education.html#doctor-of-philosophy",
}
