*Example on writing a module header*
Explain method in detail
Include figures where appropriate
References: should include DOI, and link to publication with DOI if possible
Author Contributions as section-title: one sentence per contribution


*Rules regarding ChannelIndex and AnalogSignal:*
Use one AnalogSignal unless 
Function works with signals of different length
Function can’t be replaced with a for loop, e.g. [f(x) for x in list],
Or equivalent constructs,  sum([...]), … 


*Parameter naming conventions*
spiketrains or spiketrain, not sts or st
binsize
Write full names 
Do not use ‘x’, ‘v’ if the context is not clear, better would be signal or vector
Mat to matrix 
Width instead w 
T_start or just start ? 
Quantity scalar? 
Possible to leave out the names for parameter, e.g., Return int? (numpy doc says it is ok. AY: I do prefer always with names)
Use x_x notation for names not CamelCase or similar
Remove xrange patch in asset, instead use xrange function from the six package

*Documentation*
neo.AnalogSinal or neo.core.AnalogSinal,  numpy.ndarray, quantities.Quantity
List of neo.AnalogSignal or List of neo.AnalogSignal objects 
Do not reference hidden functions
‘Default’ as last in the documentation and in a new line
Default is or Default: … 
Examples should be runnable (complete) -> doctest
References should go into the field References
Need a standardized reference style
Check and update references (e.g. asset: not in press anymore)
Based on code … should go to Notes or as a last short sentence in the main top documentation of the function 
How to explain kwargs, still no good solution, see matplotlib
Examples should go into Examples field not in main documentation 
Functions should have meaningful names
Maybe indicating the main method? At least in the examples
Does not need to cite the same references in the module twice or more
Documentation should have a short introductory sentence 
Module should have introduction at the top
Authors contribution, should be on module top, example see current_source_density
Should describe who did what in a sentence 
Import order, from general (e.g. Python intern modules) to external dependencies to elephant, put from … import … on top 
Use full names when import … as (exclude standardized names e.g. pq, np) 
n_xxx is alright if n is the number of xxx 


*Conventions on writing docstrings*
How to declare particular properties of a parameter
min_spikes: int (positive)

How to state that a parameter has a certain value
If n_subset is set to 0 (not if n_subset==0).

Referring to other functions
within ]t-dither, t+dither[ (see also elephant.spike_train_surrogates.dither_spikes).

Multiple options, and multiple identical options:
stat_corr: str
    Statistical correction to be applied:
            '' : no statistical correction
            'f', 'fdr' : false discovery rate
            'b', 'bonf': Bonferroni correction


*Example*

"""
Code style template for the Elephant project (short (one line) description
only.)

In the following lines you may expand about the module in detail if desired.
Other optional sections include:
3. function listing
4. see also
5. notes
6. references
7. examples

Please use three " (double quotation mark) to start and end a doc string.

Every module should have a docstring at the very top of the file. The
module's docstring may extend over multiple lines. If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceeded by a blank line.

"""

# For more info, see:
# https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
# https://github.com/numpy/numpy/blob/master/doc/example.py

# Module / Package naming convention: short, small letters,
# no underscores (reason: reduce typing effort)
#
# Good examples:
#   * elephant, analysis, core, sta, ue, worms, surrogate
# Bad examples:
#   * STA, StaAnalysis, UE_analysis, UEanalysis, UEAnalysis, mySuperAnalysis

# Importing modules
# Use auto-organizer of editor!
# Do not abbreviate scipy
# Do NOT import using *, e.g. from numpy import *
import scipy

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Indentation: 4 spaces (no tabs!)

# Blank lines: 2 lines between classes and top level functions, otherwise 1
# line.

# Line width: 79 characters (PEP8 conformity)

# Prefer comments written above the code
pass  # ...not behind the code

# Convention of array_like:
# For functions that take arguments which can have not only a type ndarray, but
# also types that can be converted to an ndarray (i.e. scalar types, sequence
# types), those arguments can be documented with type array_like.


#==============================================================================
# Large blocks of code may be indicated by block comments
#
# For example, you might want to separate public from private functions in your
# code or otherwise distinguish larger logically disjunct code segments in a
# single file. Block comments can contain a single line, or several lines such
# as this comment.
#==============================================================================


# Classes need 2 blank lines between any (text/code) structure
class MyClass(object):  # Classes use CamelCase notation
    """
    One line description of class.

    Long description of class, may span several lines. Possible sections:

    Parameters
    ----------
    List the arguments of the constructor (__init__) here!

    param : int
        The number of cookies to buy.

    Raises
    ------
    ...

    See Also
    --------
    ...

    Notes
    -----
    ...

    References
    ----------
    ...

    Examples
    --------
    ...

    Attributes
    ----------
    x : float
        The X coordinate
    y : float
        The Y coordinate
    real     <-- If attributes are a properties with a docstring, only list!
    imag

    Methods
    -------
    Only list methods if the class is very complex
    """

    def __init__(self, param):
        """
        Constructor
        (actual documentation is in class documentation, see above!)
        """
        self.param = param

    def function_a(self, param, lst, is_true=True, c='C', var=None):
        """
        One-line short description of the function.

        Long description of the function. Details of what the function is doing
        and how it is doing it. Used to clarify functionality, not to discuss
        implementation detail or background theory, which should rather be
        explored in the notes section below. You may refer to the parameters
        and the function name, but parameter descriptions still belong in the
        parameters section.

        Variable, module, function, and class names should be written
        betweensingle back-ticks (`numpy`), NOT *bold*.

        Parameters
        ----------
        param : int or float
            Description of parameter `param`. Enclose variables in single
            backticks. The colon must be preceded by a space, or omitted if the
            type is absent.
        lst : list of strings
            A list to copy all strings in the world.
        is_true :
            True, if you are happy.
            False, if you have a bad day.
            Default is True.
        c : {'C', 'F', 'A'}
            If only certain values are allowed. Default is 'C'.
        var : int, optional
            If it is not necessary to specify a keyword argument, use
            `optional`.

        Returns
        -------
        signal : int
            Description of return value.
        list : list of numpy.array
            This is something I do sometimes, just to see directly the return
            type. Use the full module name for non-builtin return types.

        Raises
        ------
        ValueError :
            Condition when a ValueError can occur.

        See Also
        --------
        average : Weighted average
            Used to refer to related code. Should be used judiciously.
            Functions may be listed without descriptions, and this is
            preferable if the functionality is clear from the function name.
        scipy.random.norm : Random variates, PDFs, etc.

        Notes
        -----
        An optional section that provides additional information about the
        code, possibly including a discussion of the algorithm. This section
        may include mathematical equations, written in LaTeX format. Inline:
        :math: `x^2`. An equation:

        .. math::

        x(n) * y(n) \Leftrightarrow X(e^{j\omega } )Y(e^{j\omega } )\\
        another equation here

        Images are allowed, but should not be central to the explanation; users
        viewing the docstring as text must be able to comprehend its meaning
        without resorting to an image viewer. These additional illustrations
        are included using:

        .. image:: filename

        References
        ----------
        .. [1] O. McNoleg, "The integration of GIS, remote sensing ... "

        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function. This text may explain the example beforehand.

        >>> np.add(1, 2)
        3

        >>> import numpy as np
        >>> import numpy.random
        >>> np.random.rand(2)
        array([ 0.35773152,  0.38568979])  #random

        """

        # Variables use underscore notation
        dummy_variable = 1
        a = 56  # This mini comment uses two spaces after the code!

        # Textual strings use double quotes
        error = "An error occurred. Please fix it!"

        # Non-textual strings use single quotes
        default_character = 'a'

        # Normal comments are proceeded by a single space, and begin with a
        # capital letter
        dummy_variable += 1

        # Longer comments can have several sentences. These should end with a
        # period. Just as in this example.
        dummy_variable += 1

    # Class functions need only 1 blank line.
    # This function is deprecated. Add a warning!
    def function_b(self, **kwargs):
        """
        This is a function that does b.

        .. note:: Deprecated in elephant 0.1
          `function_b` will be removed in elephant 1.0, it is replaced by
          `function_c` because the latter works also with Numpy Ver. 1.6.

        Parameters
        ----------
        kwargs: {divide, over, under, invalid}
            From numpy.errstate.
            Keyword arguments. The valid keywords are the
            possible floating-point exceptions. Each keyword should have a
            string value that defines the treatment for the particular error.
            Possible values are {'ignore', 'warn', 'raise', 'call', 'print',
            'log'}.

        """
        pass


class MyOtherClass(object):
    """
    Class documentation
    """

    def __init__(self, params):
        """
        Constructor
        """

        pass


# Functions also need 2 blank lines between any structures.
def top_level_function(param):
    """
    The same docstring guidelines as in the class above.
    """
    pass


def another_top_level_function(param):
    """
    The same docstring guidelines as in the class above.
    """
    pass

    
*Links to other documentation resources*

Numpy guidelines:
https://github.com/numpy/numpy/blob/master/doc/

Good example for documentation:
http://scikit-learn.org/stable/documentation.html 

    