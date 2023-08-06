#########################
[plum] Pack/Unpack Memory
#########################

.. image:: https://gitlab.com/dangass/plum/badges/master/pipeline.svg
    :target: https://gitlab.com/dangass/plum/commits/master
    :alt: Pipeline Status

.. image:: https://gitlab.com/dangass/plum/badges/master/coverage.svg
    :target: https://gitlab.com/dangass/plum/commits/master
    :alt: Coverage Report

.. image:: https://readthedocs.org/projects/plum-py/badge/?version=latest
    :target: https://plum-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The |plum| Python package provides classes and utility functions to
efficiently pack and unpack memory bytes and conveniently access the
memory data. The package offers a collection of basic types which may
be further customized and combined in any combination to handle
complex data structures. Most significant features include:

    - Arbitrary Nesting (e.g. structure of array of structure of bitfields of bitfields)
    - Easy to Create Custom Types
    - Speed Potential (goal of nearing :mod:`struct` performance)
    - Visual Memory Summaries (including partial dumps in exception messages)
    - Extensible API


