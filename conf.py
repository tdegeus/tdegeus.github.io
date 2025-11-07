import datetime
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


def myformat() -> tuple[list[str], dict[int]]:
    """
    Create separate bibtex files for each citation category.

    :return: ``(files, counters)``, with
        ``files`` a list of created files, and
        ``counters`` a dictionary with the number of citations per file.
    """
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
            "deGeus2024_line",
            "deGeus2024",
            "Chen2024",
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
            "thesis_Mortgat2024",
            "thesis_Pottie2024",
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

    return [fname for fname in data], {k: len(v) for k, v in data.items()}


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


def myrun(cmd: list[str], error_message: str) -> str:
    """
    Run command.
    Print error if command fails.

    :param cmd: Command (as list, see ``subprocess.run``).
    :error_message: Error message to print if command fails.
    :return: Decoded stdout.
    """
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode == 0:
        return result.stdout.decode("utf-8").strip()

    print("stdout:")
    print(result.stdout.decode("utf-8"))
    print("stderr:")
    print(result.stderr.decode("utf-8"))
    raise RuntimeError(error_message)


libraries, counters = myformat()
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

# text / url / dates

standard_text = {
    "Citations": r"> 800 citations on Google Scholar",
}

sources = {
    "Mail": "mailto:tom@geus.me",
    "Site": "https://www.geus.me",
    "GitHub": "https://github.com/tdegeus",
    "StackOverflow": "https://stackoverflow.com/users/2646505/tom-de-geus",
    "LinkedIn": "https://www.linkedin.com/in/tdegeus/",
    "ORCID": "https://orcid.org/0000-0002-1694-3375",
    "GoogleScholar": "https://scholar.google.ch/citations?user=e5yVf8AAAAAJ&hl=en",
    "Grants": "https://www.geus.me/grants.html",
    "PhD": "https://www.geus.me/education.html#doctor-of-philosophy",
    "Publications": "https://www.geus.me/publications.html",
    "Students": "https://www.geus.me/students.html",
    "StickSlip": "https://www.geus.me/research_stick-slip.html",
    "Excitations": "https://www.geus.me/research_excitations.html",
    "ChampionSuisse": "https://www.geus.me/activities.html#swiss-champions-rowing",
    "TdL": "https://www.geus.me/activities.html#tour-du-leman",
    "RTS": "https://pages.rts.ch/la-1ere/programmes/forum/11247813-forum-du-22-04-2020.html",
    "Horizons": "https://www.horizons-mag.ch/2024/12/05/reminiscent-of-the-da-vinci-code/",
}

dates = {
    "IPI": [datetime.date(2024, 9, 1), None],
    "Ambizione": [datetime.date(2019, 10, 1), datetime.date(2024, 3, 1)],
    "Rubicon": [datetime.date(2016, 9, 1), datetime.date(2019, 10, 1)],
    "Valorization": [datetime.date(2016, 4, 1), datetime.date(2016, 7, 1)],
    "Harvard": [datetime.date(2010, 9, 1), datetime.date(2010, 11, 1)],
    "PhD": [datetime.date(2012, 4, 1), datetime.date(2016, 4, 1)],
    "EM": [datetime.date(2012, 4, 1), datetime.date(2015, 10, 1)],
    "MSc": [datetime.date(2009, 9, 1), datetime.date(2012, 8, 1)],
    "BSc": [datetime.date(2004, 9, 1), datetime.date(2009, 12, 1)],
    "HighSchool": [datetime.date(1997, 9, 1), datetime.date(2004, 6, 1)],
    "PrizeMartinus": datetime.date(2017, 6, 1),
    "PrizeTUe": datetime.date(2017, 5, 1),
    "PrizeEccomas": datetime.date(2017, 9, 1),
    "PrizePosterMB": datetime.date(2016, 12, 1),
    "PrizePosterMA": datetime.date(2013, 12, 1),
    "PrizeEntrepreneurship": datetime.date(2008, 2, 1),
    "DataChampion": [datetime.date(2021, 9, 1), None],
    "ClusterEPFL": [datetime.date(2017, 3, 1), None],
    "ClusterTUe": [datetime.date(2013, 9, 1), datetime.date(2016, 7, 1)],
    "InterviewRTS": datetime.date(2020, 4, 22),
    "InterviewHorizons": datetime.date(2024, 8, 28),
    "InterviewTerlouw": datetime.date(2017, 5, 1),
    "InterviewRradio": datetime.date(2016, 5, 1),
    "CAS": [datetime.date(2024, 2, 1), None],
    "LSArandonnee": [datetime.date(2019, 4, 1), None],
    "LSAencadrant": [datetime.date(2019, 4, 1), None],
    "HoraEst": [datetime.date(2014, 9, 1), datetime.date(2015, 9, 1)],
    "Buddy": [datetime.date(2008, 9, 1), datetime.date(2009, 9, 1)],
    "HockeyEquipment": [datetime.date(2003, 9, 1), datetime.date(2007, 9, 1)],
    "HockeyTrainer": [datetime.date(2005, 9, 1), datetime.date(2010, 9, 1)],
    "Hockey": [datetime.date(2003, 9, 1), datetime.date(2015, 9, 1)],
    "Tutor": [datetime.date(2004, 9, 1), datetime.date(2008, 9, 1)],
    "Boels": [datetime.date(2003, 9, 1), datetime.date(2007, 9, 1)],
    "PSV": [datetime.date(2001, 9, 1), datetime.date(2004, 9, 1)],
    "TdLA": datetime.date(2022, 9, 1),
    "TdLB": datetime.date(2023, 9, 1),
    "ChampionSuisseA": datetime.date(2021, 7, 1),
    "ChampionSuisseB": datetime.date(2023, 7, 1),
    "ChampionSuisseC": datetime.date(2024, 7, 1),
    "ChampionSuisseD": datetime.date(2024, 7, 6),
    "TeachingEPFLStatPhys": [datetime.date(2020, 2, 1), datetime.date(2020, 9, 1)],
    "TeachingEPFLContinuum": [datetime.date(2016, 9, 1), datetime.date(2017, 2, 1)],
    "TeachingTUeProgramming": [datetime.date(2011, 9, 1), datetime.date(2015, 9, 1)],
    "TeachingTUeFEM": [datetime.date(2010, 9, 1), datetime.date(2011, 9, 1)],
    "TeachingTUeMatlab": [datetime.date(2009, 9, 1), datetime.date(2010, 9, 1)],
    "TeachingTUeDBL": [datetime.date(2008, 9, 1), datetime.date(2009, 9, 1)],
}

formatted = {}
for project, date_range in dates.items():
    if isinstance(date_range, datetime.date):
        formatted[project] = date_range.strftime("%Y")
        continue

    first, last = date_range

    if project.startswith("Teaching"):
        if first.year == last.year:
            first = datetime.date(first.year - 1, 9, 1)

    if last is None:
        formatted[project] = f"{first.strftime('%Y')}--pres."
    elif first.year == last.year:
        formatted[project] = first.strftime("%Y")
    else:
        formatted[project] = f"{first.strftime('%Y')}--{last.strftime('%Y')}"

# register counters and dates for later use

today = datetime.datetime.now().strftime("%Y/%m/%d")

text = []
text.append(r"\NeedsTeXFormat{LaTeX2e}")
text.append(rf"\ProvidesPackage{{mycounters}}[{today} Counters of output]")
text.append("")
text.append(rf"\newcommand{{\mypublications}}{{{counters['library_publications.bib']}}}")
text.append(rf"\newcommand{{\mystudents}}{{{counters['library_students.bib']}}}")

text.append("")
for key, value in formatted.items():
    text.append(rf"\newcommand{{\MyDate{key}}}{{{value}}}")

text.append("")
for key, value in sources.items():
    value = value.replace("#", r"\#")
    if key == "Mail":
        text.append(rf"\newcommand{{\MySource{key}}}[1][tom@geus.me]{{\href{{{value}}}{{#1}}}}")
    elif key == "Site":
        text.append(rf"\newcommand{{\MySource{key}}}[1][www.geus.me]{{\href{{{value}}}{{#1}}}}")
    else:
        text.append(rf"\newcommand{{\MySource{key}}}[1]{{\href{{{value}}}{{#1}}}}")

text.append("")
for key, value in standard_text.items():
    text.append(rf"\newcommand{{\MyText{key}}}{{{value}}}")

pathlib.Path("mycounters.sty").write_text("\n".join(text))
shutil.copyfile("mycounters.sty", os.path.join("research", "cv_short_en", "mycounters.sty"))
shutil.copyfile("mycounters.sty", os.path.join("research", "cv_medium_en", "mycounters.sty"))
shutil.copyfile("mycounters.sty", os.path.join("research", "cv", "mycounters.sty"))
shutil.copyfile("mycounters.sty", os.path.join("research", "teaching", "mycounters.sty"))

# compile LaTeX projects

for project in [f for f in (root / "research").glob("*") if f.is_dir()]:
    with cwd(project):
        # nothing to compile
        if not pathlib.Path("main.tex").exists():
            assert len([i for i in pathlib.Path().glob("*.tex")]) == 0
            continue

        # copy style and library / extracted libraries
        for fname in ["goose-article.cls", "unsrtnat.bst", "library.bib"]:
            shutil.copyfile(f"../{fname}", fname)
        if project.name in ["cv", "publications"]:
            for lib in libraries:
                shutil.copyfile(f"../../{lib}", lib)

        # compile
        myrun(["latexmk", "-pdf", "main.tex"], error_message=f"latexmk {project}/main.tex failed")
        assert pathlib.Path("main.pdf").exists

        # flyers: check that they have only one page
        if project.name in ["cv", "cv_medium_en", "teaching", "ambizione", "publications"]:
            continue
        cmd = [
            "gs",
            "-q",
            "-dNOSAFER",
            "-dNODISPLAY",
            "-c",
            "(main.pdf) (r) file runpdfbegin pdfpagecount = quit",
        ]
        ret = myrun(cmd, error_message=f"Failed: {project} $ {' '.join(cmd)}")
        if ret != "1":
            raise RuntimeError(f"{project}/main.pdf has {ret} pages (instead of 1)")

static = pathlib.Path("_static")
static.mkdir(exist_ok=True)
research = pathlib.Path("research")
shutil.copy(research / "cv_medium_en" / "main.pdf", static / "cv.pdf")


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
html_static_path = ["_static"]
redirects = {
    "phd": "education.html#doctor-of-philosophy",
    "cv": "_static/cv.pdf",
}
