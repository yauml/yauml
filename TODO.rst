- handle syntax errors more efficiently..

- add support for automatically generate the appropriate source files for the
  developper depending on the language (specified). E.g::

    Given the following yaml file `example.yaml` as example:

    - class: A
      method:
        - int a()

    - class: B
      inherits:
        - A

    using a syntax like this one: ``yauml -l java --source-skel -d . example.yaml``
    would generate the files A.java, B.java with the appropriate code skeletons
    inside.

- add support for domain class diagrams (not only conception class diagram,
  which is what is currently supported).
