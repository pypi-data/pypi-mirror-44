==================================
 Documentation and style guideline
==================================

.. _example.py: example.py
.. |br| raw:: html

   <br />


Contents
========

.. contents:: Table of Contents
   :depth: 2
   :local:

For an accompanying example, see `example.py`_.


Overview
========

**We mostly follow the standard Python style conventions as described here:**

* `Style Guide for Python Code <http://python.org/dev/peps/pep-0008/>`_.
* `Docstring Conventions <http://python.org/dev/peps/pep-0257/>`_.
* `Numpy doc <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_

**You can use a code checker to format your code:**

* `pylint <http://www.logilab.org/857>`_.
* `pyflakes <https://pypi.python.org/pypi/pyflakes>`_.
* `pep8.py <http://svn.browsershots.org/trunk/devtools/pep8/pep8.py>`_.
* `flake8 <https://pypi.python.org/pypi/flake8>`_.
* Or use the auto-organizer of your editor.


Documentation standards
=======================
A documentation string (docstring) is a string that describes a module, function, class, or method definition. Please use three " (double quotation mark) to start and end a doc string, i.e.: ::

  """
  This is an example documentation

  It can be spread over several lines.
  """

* Every module should have a docstring at the very top of the file. The module's docstring may extend over multiple lines. If your docstring does extend over multiple lines, the closing three quotation marks must be on a line by itself, preferably preceeded by a blank line.
* Each class, method or function should be documentated, unless it is a private or hidden function.   
* We follow the `re-structured text (reST) <http://docutils.sourceforge.net/rst.html>`_ syntax and use `Sphinx <http://sphinx.pocoo.org/>`_ to render the documentation.
* The general line width should not exceed 79 characters.


Writing a module header
^^^^^^^^^^^^^^^^^^^^^^^

* Explain the method in detail
* Include figures where appropriate
* References: should include DOI, and link to publication with DOI if possible
* Author Contributions as section-title: one sentence per contribution
      

Sections of a docstring
^^^^^^^^^^^^^^^^^^^^^^^

* The documentation should start with a one line summary of the method.
* After a blank line, a more detailed description follows. Implementation details should be not mentioned here, instead refer to the *Notes* section. 
* Parameters describe the function arguments, keywords and respective types
    .. code-block:: python

        """
        Parameters
        ----------
        spiketrains: list of neo.SpikeTrain objects.
            The input is a list of neo.SpikeTrain objects.

        """
|br|

* For more sections please have a look at the `Numpy doc guidelines <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#sections>`_ and our `example.py`_.


Conventions on writing docstrings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Functions should have meaningful names.
* Variable, module, function, and class names should be written between single back-ticks (`numpy`), NOT *bold*.
* References should go into the field References.
* Code examples should go to the `Examples` section.
* Examples should be runnable (and complete), you can test them with `doctest <https://docs.python.org/3/library/doctest.html>`_
* Code references should go to the `Notes section`  or as a last short sentence in the main top documentation of the function.
* Do not reference hidden functions.
* If an argument has a `Default` value specify it as ``Default is ...`` at the end of the description.
* You do not need to cite the same references in the module twice or more.
  


Style conventions
=================

* Indentation: 4 spaces (no tabs!)
* Blank lines: 2 lines between classes and top level functions, otherwise 1 line.
* Line width: 79 characters.
* Prefer comments written above the code, not behind the code.
* Classes need 2 blank lines between any (text/code) structure.
* Classes use CamelCase notation, e.g. ``MyClass``, whereas function or methods use underscores ``my_function``. 


* Convention of array_like:

  * For functions that take arguments which can have not only a type ndarray, but  also types that can be converted to an `ndarray` (i.e. scalar types, sequence types), those arguments can be documented with type `array_like`.

    .. code-block:: python

        #==============================================================================
        # Large blocks of code may be indicated by block comments
        # For example, you might want to separate public from private functions in your
        # code or otherwise distinguish larger logically disjunct code segments in a
        # single file. Block comments can contain a single line, or several lines such
        # as this comment.
        #==============================================================================
|br|


Modules
^^^^^^^
* Module / Package naming convention: short, small letters, no underscores (reason: reduce typing effort) 
      
  * Good examples: elephant, analysis, core, sta, ue, worms, surrogate
    * Bad examples:  STA, StaAnalysis, UE_analysis, UEanalysis, UEAnalysis, mySuperAnalysis

  * Importing modules
      
    * Do not abbreviate scipy
    * Do not import using \*, e.g. ``from numpy import *``
    * Import strucure:

    .. code-block:: python

        import scipy
        import matplotlib.pyplot as plt
        import numpy as np
        from numpy.random import normal


Parameter
^^^^^^^^^
* Always try to find meaningful names.
* Names such as  `n_spiketrains` are alright if `n` is indicating a number. 
* List of neo.AnalogSignal or List of neo.AnalogSignal objects      
* How to declare particular properties of a parameter.

      * min_spikes: int (positive)
	
* How to state that a parameter has a certain value.

  * If n_subset is set to 0 (not if n_subset==0).



**Rules regarding ChannelIndex and AnalogSignal:**
* Use one AnalogSignal unless:
      
  * Function works with signals of different length
    * Function can’t be replaced with a for loop, e.g. ``[f(x) for x in list]``,
    * Or equivalent constructs,  ``sum([...])``
