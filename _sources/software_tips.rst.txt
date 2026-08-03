:bdg-link-primary:`Google Scholar <https://scholar.google.ch/citations?user=e5yVf8AAAAAJ&hl=en>`
:bdg-link-primary:`ORCiD <https://orcid.org/0000-0002-1694-3375>`
:bdg-link-primary:`GitHub <https://github.com/tdegeus>`

****
Tips
****

.. |br| raw:: html

   <br />

git
===

.. dropdown:: Update fork

    .. code-block:: bash

        git remote add upstream {url_to_remote}
        git fetch upstream
        git rebase upstream/main

.. dropdown:: Remove local and remote branch

    Note that a common usage of a fork is to open a pull-request, in particular from a branch on the fork:

    .. code-block:: bash

        git checkout -b patch
        ... # commits here

    Once merged, you can delete the branch:

    .. code-block:: bash

        git checkout main
        git branch -D patch
        git push --delete origin patch

.. dropdown:: Update remote branch

    When a remote branch is deleted from a repository,
    it can still show up in the local branch list.

    Often
    .. code-block:: bash

        git fetch

    should suffice. However, sometimes you'll have to do

    .. code-block:: bash

        git fetch --prune

    See `this StackOverflow discussion <https://stackoverflow.com/questions/32651627/how-do-i-update-the-remote-branches-list-in-git-from-the-server>`_.

.. dropdown:: Generate patch

    In case a new release cannot be made (because you don't have access to a repository), but you still want to update a `conda-forge <https://conda-forge.org>`_ recipe, you can add 'patches' to the recipe.

    To this end, clone the repository

    .. code-block:: bash

        git clone https://github.com/someuser/somerepo

    Move to the repository

    .. code-block:: bash

        cd somerepo

    and determine the number of commits since the last release (e.g. 3). Then have git create the patches, using:

    .. code-block:: bash

        git format-patch -3

    This will create a number of ``*.patch`` files (3 in this case). These patches can be added to the recipe. See for example the `cling-feedstock <https://github.com/conda-forge/cling-feedstock/blob/master/recipe/meta.yaml>`_.

.. dropdown:: Partial clone

    Recently I came across a few repositories with a very rich history
    (corresponding to a huge disk-space, requiring also a significant downloading time).
    If one is not particularly interested in the histories, on can
    partially (shallow) clone a repository:

    .. code-block:: bash

        git clone --depth=5 ...

conda
=====

.. dropdown:: Add library to Conda environment

    Conda is a great tool as a package manager and virtual environment together. Many (up-to-date) packages are available through `conda-forge <https://conda-forge.org>`_. However, ever to often you might want to install from a local source (for example to test the current master branch).

    Start by activating the relevant Conda environment (e.g. "myenv"):

    .. code-block:: bash

        conda activate myenv

    (see `Conda documentation <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ on how to manage environments).

    Then, go to the library:

    .. code-block:: bash

        cd /path/to/library

    .. dropdown:: Python

        Make sure that you have *Python* installed, e.g. using

        .. code-block:: bash

            conda install -c conda-forge python

        Then, with the *Python* executable that is loaded (from ``myenv``)

        .. code-block:: bash

            python -m pip install .

    .. dropdown:: CMake

        Make sure that you have *CMake* installed, e.g. using

        .. code-block:: bash

            conda install -c conda-forge cmake

        Then, with the *CMake* executable that is loaded (from ``myenv``)

        .. code-block:: bash

            cmake . -DCMAKE_INSTALL_PREFIX:PATH="${CONDA_PREFIX}"

Python
======

.. dropdown:: Create movie with 'ffmpeg-python'

    `ffmpeg-python <https://github.com/kkroening/ffmpeg-python>`_ is a great wrapper around *ffmpeg* to create your movie from Python.

    Let us begin by setting up an environment that contains what we need:

    .. code-block:: bash

        conda activate myenv
        conda install -c conda-forge ffmpeg-python
        conda install -c conda-forge matplotlib

    (see `Conda documentation <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ on how to manage environments).

    Then, we will create an animation as a batch of images:

    .. code-block:: python

        import matplotlib.pyplot as plt

        filenames = []

        for i in range(20):

            filename = 'image_{0:02d}.png'.format(i)
            filenames += [filename]

            fig, ax = plt.subplots()
            ax.plot([0, 1], [0, i])
            ax.set_ylim([0, 20])
            plt.savefig(filename)

    To convert this to a movie, we will use *ffmpeg-python*:

    .. code-block:: python

        import ffmpeg

        (
            ffmpeg
            .input('image_%02d.png', framerate=2)
            .output('movie.mp4')
            .run()
        )

.. dropdown:: pybind11 examples

    `pybind11 examples <https://github.com/tdegeus/pybind11_examples>`_.
    Some basic examples on how to start using pybind11. Pybind11 is a C++ library that allows to expose a C++ library to Python easily.

ParaView
========

.. dropdown:: ParaView examples

    `ParaView examples <https://github.com/tdegeus/paraview_examples>`_.
    Some basic examples on how to make data available in ParaView.
