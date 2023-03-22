.. _api_ref:

=============
API Reference
=============

Welcome to the API reference for ``skbase``.

The API reference provides a technical manual, describing the class and
function interface provided by the package. See the :ref:`user_guide` for
additional details.

.. automodule:: skbase
    :no-members:
    :no-inherited-members:

.. _base_ref:

Base Classes
============

.. currentmodule:: skbase.base

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: class.rst

    BaseObject
    BaseEstimator

.. _global_config:

Configure ``skbase``
====================

.. automodule:: skbase.config
    :no-members:
    :no-inherited-members:

.. currentmodule:: skbase.config

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    get_config
    get_default_config
    set_config
    reset_config
    config_context

.. _obj_retrieval:

Object Retrieval
================

.. currentmodule:: skbase.lookup

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    all_objects
    get_package_metadata

.. _obj_validation:

Object Validation and Comparison
================================

.. currentmodule:: skbase.validate

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    check_sequence
    check_sequence_named_objects
    check_type
    is_sequence
    is_sequence_named_objects

.. _obj_testing:

Testing
=======

.. automodule:: skbase.testing
    :no-members:
    :no-inherited-members:

.. currentmodule:: skbase.testing

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: class.rst

    BaseFixtureGenerator
    QuickTester
    TestAllObjects

Utils
=====

.. automodule:: skbase.utils
    :no-members:
    :no-inherited-members:

.. currentmodule:: skbase.utils

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    flatten
    is_flat
    unflat_len
    unflatten
