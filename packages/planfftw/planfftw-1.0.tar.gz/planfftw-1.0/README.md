planfftw
========

planfftw provides Julia-inspired function planners for fft and a number of fft-
based operations. The initial objective was to provide a clean and highly
optimized interface to the excellent PyFFTW package. However, PyFFTW is not
a strict requirement and planfftw falls back on scipy.fftpack or numpy.fft, 
should it not be available.

Requirements
------------
Python 3.5 or higher
numpy 1.16.1 or higher

Earlier versions may very well work but are not tested.

Highly recommended
-----------
PyFFTW

Installation
------------
Install with::

    pip install planfftw

or::

    easy_install planfftw
