import pathlib
import texplain

def myformat():

    root = pathlib.Path(__file__).parent
    categories = [{
        "title": "Stick-slip friction",
        "collaborators": ["Matthieu Wyart", "Marko Popović", "Alberto Rosso", "Wencheng Ji"],
        "students": ["Elisa El Sergany"],
        "cite": ["deGeus2019"],
        "bib": "library_friction.bib",
        "rst": "publications_friction.rst",
    }]

    bibfile = (root / "library.bib").read_text()

    for entry in categories:
        (root / entry["bib"]).write_text(texplain.bib_select(bibfile, entry["cite"]))
        txt = []
        txt += [entry["title"], "="*len(entry["title"]), ""]
        txt += [":cite:empty:`{}`".format(c) for c in entry["cite"]]
        txt += ["", ".. bibliography:: {}".format(entry["bib"]), "   :style: unsrt", ""]
        (root / entry["rst"]).write_text("\n".join(txt))

    return [entry["bib"] for entry in categories]


project = 'Tom de Geus'
copyright = 'Tom de Geus'
author = 'Tom de Geus'
html_theme = "furo"
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_title = "Tom de Geus"
extensions = ['sphinxcontrib.bibtex', 'sphinx_design']
bibtex_bibfiles = myformat()
