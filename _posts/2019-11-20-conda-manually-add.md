---
layout: post
title:  "Conda tip: manually add library to Conda environment"
categories: [Conda]
---

Conda is a great tool as a package manager and virtual environment together. Many (up-to-date) packages are available through [conda-forge](https://conda-forge.org). However, ever to often you might want to install from a local source (for example to test the current master branch).

To do so, start by activating the relevant Conda environment (e.g. "myenv"):

```bash
conda activate myenv
```

(see [Conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) on how to manage environments).

Then, go to the library:

```bash
cd /path/to/library
```

and build using CMake, making sure to install to the currently activated Conda environment

```bash
cmake . -DCMAKE_INSTALL_PREFIX:PATH="${CONDA_PREFIX}"
```

>   It is recommended that you use a temporary "build" directory. In that case:
>   
>   ```bash
>   cd /path/to/library
>   mkdir build
>   cd build
>   cmake .. -DCMAKE_INSTALL_PREFIX:PATH="${CONDA_PREFIX}"
>   ```
