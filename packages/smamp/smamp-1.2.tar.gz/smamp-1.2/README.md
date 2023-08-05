# Tools for automated charge optimization

### Goal
SMAMP (synthetic mimics of antimicrobial peptides) can be used for antimicrobial coating in medical applications.
To understand a class of SMAMP, we simulate them via Molecular Dynamics (MD).
An MD models atom as point-charges, so these charges are an essential component of MD simulations.
These charges are not available for the SMAMP molecules of interest, so we have to determine them ourselves.

Multiple methods to determine point charges exists, e.g., Bader Charge Analysis, HORTON-style cost-function fitting and more.
Also, subvariants of these methods are of interest: diverse constraints, different algorithms and convergence parameters.

### Overview
* This package provides tools to make the charge optimization process easier.
* The documentation is available on [GitHub Pages](https://lukaselflein.github.io/smamp/).
* The smamp package is used in a [workflow management project](https://github.com/lukaselflein/charge_optimization_folderstructure).

### Content
* `smamp`: Code snippets for the charge optimization workflow
* `setup.py`: Configuration file to create a python package
* `README.md`: The document you are reading right now
* `Makefile`: Automatically build and upload the package and git via `make`
* `.update_version.py`: Increment version number by 0.01 in `setup.py`
* `.test.py`: check if package import works
