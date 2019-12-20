---
layout: post
title:  "Conda tip: manually add library to Conda environment"
categories: [Conda]
---

Conda is a great tool as a package manager and virtual environment together. Many (up-to-date) packages are available through [conda-forge](https://conda-forge.org). However, ever to often you might want to install from a local source (for example to test the current master branch).

Start by activating the relevant Conda environment (e.g. "myenv"):

```bash
conda activate myenv
```

(see [Conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) on how to manage environments).

Then, go to the library:

```bash
cd /path/to/library
```

*   **Python**

    Make sure that you have *Python* installed, e.g. using 

    ```
    conda install -c conda-forge python
    ```

    Then, with the *Python* executable that is loaded (from `myenv`)

    ```
    python -m pip install .
    ```

*   **CMake (for libraries in C, C++, etc.)**

    Make sure that you have *CMake* installed, e.g. using 

    ```
    conda install -c conda-forge cmake
    ```

    Then, with the *CMake* executable that is loaded (from `myenv`)

    ```bash
    cmake . -DCMAKE_INSTALL_PREFIX:PATH="${CONDA_PREFIX}"
    ```
