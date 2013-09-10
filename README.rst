YAUML
~~~~~

A script for generating UML diagrams from `YAML <http://www.yaml.org/>`__
files.

Example
-------

The script lets you use the the YAML language in order to build a UML conception
diagram. Let the following file ``./example/ex1/1.yaml``::

    - class: A
      attributes:
        - int a
      methods:
        - int get_a()
    
    - class: B
      attributes:
        - int b
      methods:
        - int get_b()
    
    - class: C
      attributes:
        - int c
      methods:
        - int get_c()

Writting this::

    yauml ./example/ex1/1.yaml

would output the resulting ``dot`` file on **stdout** according to the specified
template. In order to get an image, **dot** has to treat the data going out
from ``yauml`` like so::

    yauml ./example/ex1/1.yaml | dot -Tpng -o ./example/ex1/1.png

Using the default template given with this program, the result
after passing the output to ``dot`` would be:

.. image:: ./example/ex1/1.png

Let's add some particularities to this conception::

    - class: A
      attributes:
        - int a
      methods:
        - int get_a()
    
    - class: B
      inherits:
        - A
      attributes:
        - int b
      methods:
        - int get_b()
    
    - class: C
      inherits:
        - A
      attributes:
        - int c
      methods:
        - int get_c()
    
and the output through ``yauml`` and ``dot`` would now be:

.. image:: ./example/ex1/2.png

So far YAUML handles:

- Classes (can be abstract)
    - attributes
    - methods
- Interfaces
- Relations
    - Inheritance
    - Use
    - Is part of
    - Implement

A more complete example would look like:

.. image:: ./example/ex1/3.png

Documentation
-------------

This comes with a manual explaining all you need to know to use the script. For
more information about the ``dot`` language and the the way to set up template,
see **Graphviz** documentation.

Installation
------------

First, you can configurate some variables to suit your needs in the Makefile.
Then, simply run::

    make

and::

    make install

Bash completion
===============

In order for the bash completion to be installed when you install the program,
you have to configure the ``BASH_COMPLETION_DIR`` variable in the Makefile.
Because it depends on the OS you're using.


Dependencies
------------

To run the script, the following softwares are needed :

- Python
- `PyYAML <https://bitbucket.org/xi/pyyaml>`__
- `Graphviz <http://www.graphviz.org/>`__ (optionnal, but the whole point is to use it)

