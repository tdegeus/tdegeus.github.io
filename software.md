---
layout: page
title: Software
---

# Contents

<!-- MarkdownTOC -->

- [Mechanics](#mechanics)
- [Statistical \(image\) analysis](#statistical-image-analysis)
- [C++](#c)
- [Python](#python)
- [Paraview](#paraview)
- [LaTeX tools](#latex-tools)
- [Command-line tools](#command-line-tools)
- [Computing cluster](#computing-cluster)

<!-- /MarkdownTOC -->

# Mechanics

*   [GooseFFT](http://goosefft.geus.me).

    Simple Python examples of the variational FFT-based solution technique of partial differential equations (in this case representing mechanical equilibrium, described by a vanishing divergence of stress).

*   [GooseFEM](http://goosefem.geus.me).

    A simple C++ header-only library to run Finite Element computations. This is really a quite simple library to do some specialized computations, not at all meant to come close to more professional libraries.

*   [GooseMaterial](https://github.com/tdegeus/GooseMaterial).

    A C++ implementation of several continuum mechanics constitutive model.

# Statistical (image) analysis

*   [GooseEYE](http://gooseeye.geus.me).

# C++

*   [cppmat](http://cppmat.geus.me)

    A header-only library to work with multi-dimensional arrays and tensors in C++. It works much like Eigen but for multi-dimensional arrays. It also features a wide scope of tensor algebra.

*   [HDF5pp](http://hdf5pp.geus.me)

    A header-only wrapper around the HDF5 C++ API. This wrapper makes use of templating and operator overloading, resulting in extremely easy use.

*   [pybind11 examples](https://github.com/tdegeus/pybind11_examples).

    Some basic examples on how to start using pybind11. Pybind11 is a C++ library that allows to expose a C++ library to Python easily.

# Python

*   [GooseMPL](http://goosempl.geus.me).

    The key thing is a style for Matplotlib. Additionally functions are provided that can simplify making professional plots. Finally, several examples to make customized plots are well documented.

# Paraview

*   [ParaView examples](https://github.com/tdegeus/paraview_examples).

    Some basic examples on how to make data available in ParaView.

# LaTeX tools

# Command-line tools

# Computing cluster

*   [GooseSLURM](https://github.com/tdegeus/GooseSLURM).

    Examples of job-scripts for slurm, and some wrappers around the default functions provided by slurm.
