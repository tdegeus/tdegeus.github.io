:bdg-link-primary:`Google Scholar <https://scholar.google.ch/citations?user=e5yVf8AAAAAJ&hl=en>`
:bdg-link-primary:`ORCiD <https://orcid.org/0000-0002-1694-3375>`
:bdg-link-primary:`GitHub <https://github.com/tdegeus>`

FFT homogenisation
==================

Computational micromechanics and homogenization require the solution of the mechanical equilibrium of a periodic cell that comprises a (generally complex) microstructure.
Techniques that apply the Fast Fourier Transform have attracted much attention as they outperform other methods in terms of speed and memory footprint.
Moreover, the Fast Fourier Transform is a natural companion of pixel-based digital images which often serve as input.
In its original form, one of the biggest challenges for the method is the treatment of (geometrically) non-linear problems, partially due to the need for a uniform linear reference problem.
In a geometrically linear setting, the problem has recently been treated in a variational form resulting in an unconditionally stable scheme that combines Newton iterations with an iterative linear solver, and therefore exhibits robust and quadratic convergence behavior :footcite:`Zeman2017`.
Through this approach, well-known key ingredients were recovered in terms of discretization, numerical quadrature, consistent linearization of the material model, and the iterative solution of the resulting linear system.
As a result, the extension to finite strains, using arbitrary constitutive models, is at hand.
Because of the application of the Fast Fourier Transform, the implementation is substantially easier than that of other (Finite Element) methods.
Both claims are demonstrated in this paper and substantiated with a `simple code in Python of just 59 lines (without comments) <https://github.com/tdegeus/GooseFFT>`_ :footcite:`deGeus2017a`.
The aim is to render the method transparent and accessible, whereby researchers that are new to this method should be able to implement it efficiently.
The potential of this method is demonstrated using two examples, each with a different material model.

**Selected publications**

.. footbibliography::
