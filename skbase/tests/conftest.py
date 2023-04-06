# -*- coding: utf-8 -*-
"""Common functionality for skbase unit tests."""
from typing import List

from skbase.base import BaseEstimator, BaseObject

__all__: List[str] = [
    "SKBASE_BASE_CLASSES",
    "SKBASE_MODULES",
    "SKBASE_PUBLIC_MODULES",
    "SKBASE_PUBLIC_CLASSES_BY_MODULE",
    "SKBASE_CLASSES_BY_MODULE",
    "SKBASE_PUBLIC_FUNCTIONS_BY_MODULE",
    "SKBASE_FUNCTIONS_BY_MODULE",
]
__author__: List[str] = ["fkiraly", "RNKuhns"]

SKBASE_BASE_CLASSES = (BaseObject, BaseEstimator)
SKBASE_MODULES = (
    "skbase",
    "skbase._exceptions",
    "skbase.base",
    "skbase.base._base",
    "skbase.base._meta",
    "skbase.base._serialize",
    "skbase.base._tagmanager",
    "skbase.lookup",
    "skbase.lookup.tests",
    "skbase.lookup.tests.test_lookup",
    "skbase.lookup._lookup",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils._conditional_fixtures",
    "skbase.testing.utils._dependencies",
    "skbase.testing.utils.deep_equals",
    "skbase.testing.utils.inspect",
    "skbase.testing.utils.tests",
    "skbase.testing.utils.tests.test_deep_equals",
    "skbase.tests",
    "skbase.tests.conftest",
    "skbase.tests.test_base",
    "skbase.tests.test_baseestimator",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.utils",
    "skbase.utils._iter",
    "skbase.utils._nested_iter",
    "skbase.validate",
    "skbase.validate._named_objects",
    "skbase.validate._types",
)
SKBASE_PUBLIC_MODULES = (
    "skbase",
    "skbase.base",
    "skbase.lookup",
    "skbase.lookup.tests",
    "skbase.lookup.tests.test_lookup",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils.deep_equals",
    "skbase.testing.utils.inspect",
    "skbase.testing.utils.tests",
    "skbase.testing.utils.tests.test_deep_equals",
    "skbase.tests",
    "skbase.tests.conftest",
    "skbase.tests.test_base",
    "skbase.tests.test_baseestimator",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.utils",
    "skbase.validate",
)
SKBASE_PUBLIC_CLASSES_BY_MODULE = {
    "skbase._exceptions": ("FixtureGenerationError", "NotFittedError"),
    "skbase.base": ("BaseEstimator", "BaseMetaEstimator", "BaseObject"),
    "skbase.base._base": ("BaseEstimator", "BaseObject"),
    "skbase.base._meta": ("BaseMetaEstimator",),
    "skbase.lookup._lookup": ("ClassInfo", "FunctionInfo", "ModuleInfo"),
    "skbase.testing": ("BaseFixtureGenerator", "QuickTester", "TestAllObjects"),
    "skbase.testing.test_all_objects": (
        "BaseFixtureGenerator",
        "QuickTester",
        "TestAllObjects",
    ),
}
SKBASE_CLASSES_BY_MODULE = SKBASE_PUBLIC_CLASSES_BY_MODULE.copy()
SKBASE_CLASSES_BY_MODULE.update(
    {
        "skbase.base._meta": ("BaseMetaEstimator",),
        "skbase.base._tagmanager": ("_FlagManager",),
    }
)
SKBASE_PUBLIC_FUNCTIONS_BY_MODULE = {
    "skbase.base._serialize": ("load",),
    "skbase.lookup": ("all_objects", "get_package_metadata"),
    "skbase.lookup._lookup": ("all_objects", "get_package_metadata"),
    "skbase.testing.utils._conditional_fixtures": (
        "create_conditional_fixtures_and_names",
    ),
    "skbase.testing.utils.deep_equals": ("deep_equals",),
    "skbase.validate": (
        "check_sequence_named_objects",
        "check_sequence",
        "check_type",
        "is_sequence",
        "is_sequence_named_objects",
    ),
    "skbase.validate._named_objects": (
        "check_sequence_named_objects",
        "is_sequence_named_objects",
    ),
    "skbase.utils": (
        "flatten",
        "is_flat",
        "unflat_len",
        "unflatten",
    ),
    "skbase.utils._nested_iter": (
        "flatten",
        "is_flat",
        "unflat_len",
        "unflatten",
    ),
    "skbase.validate._types": ("check_sequence", "check_type", "is_sequence"),
}
SKBASE_FUNCTIONS_BY_MODULE = SKBASE_PUBLIC_FUNCTIONS_BY_MODULE.copy()
SKBASE_FUNCTIONS_BY_MODULE.update(
    {
        "skbase.lookup._lookup": (
            "_determine_module_path",
            "_get_return_tags",
            "_is_ignored_module",
            "all_objects",
            "_is_non_public_module",
            "get_package_metadata",
            "_make_dataframe",
            "_walk",
            "_filter_by_tags",
            "_filter_by_class",
            "_import_module",
            "_check_object_types",
            "_get_module_info",
        ),
        "skbase.testing.utils._dependencies": (
            "_check_soft_dependencies",
            "_check_python_version",
        ),
        "skbase.testing.utils.deep_equals": (
            "_pandas_equals",
            "_dict_equals",
            "_is_pandas",
            "_is_npnan",
            "_tuple_equals",
            "_fh_equals",
            "deep_equals",
            "_is_npndarray",
            "_coerce_list",
        ),
        "skbase.testing.utils.inspect": ("_get_args",),
        "skbase.utils._iter": (
            "_format_seq_to_str",
            "_remove_type_text",
            "_scalar_to_seq",
        ),
        "skbase.utils._nested_iter": (
            "flatten",
            "is_flat",
            "_remove_single",
            "unflat_len",
            "unflatten",
        ),
        "skbase.validate._named_objects": (
            "check_sequence_named_objects",
            "is_sequence_named_objects",
            "_named_baseobject_error_msg",
        ),
        "skbase.validate._types": (
            "check_sequence",
            "check_type",
            "is_sequence",
            "_convert_scalar_seq_type_input_to_tuple",
            # "_check_iterable_of_class_or_error",
            # "_check_list_of_str",
            # "_check_list_of_str_or_error",
        ),
    }
)


# Fixture class for testing tag system
class Parent(BaseObject):
    """Parent class to test BaseObject's usage."""

    _tags = {"A": "1", "B": 2, "C": 1234, "3": "D"}

    def __init__(self, a="something", b=7, c=None):
        """Initialize the class."""
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def some_method(self):
        """To be implemented by child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class Child(Parent):
    """Child class that is child of FixtureClassParent."""

    _tags = {"A": 42, "3": "E"}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass
