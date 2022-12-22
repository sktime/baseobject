# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for skbase lookup functionality.

tests in this module:

    test_is_non_public_module  - tests _is_non_public_module logic
"""
import importlib
import pathlib
from types import ModuleType
from typing import List

import pandas as pd
import pytest

from skbase import BaseObject
from skbase.lookup import all_objects
from skbase.lookup._lookup import (
    _filter_by_class,
    _filter_by_tags,
    _import_module,
    _is_ignored_module,
    _is_non_public_module,
    _walk,
)
from skbase.mock_package.mock_package import (
    CompositionDummy,
    InheritsFromBaseObject,
    NotABaseObject,
)

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = []


MOD_NAMES = {
    "public": ("skbase", "skbase.lookup", "some_module.some_sub_module"),
    "non_public": (
        "skbase.lookup._lookup",
        "some_module._some_non_public_sub_module",
        "_skbase",
    ),
}


# Fixture class for testing tag system
class FixtureClassParent(BaseObject):
    """Fixture class to test BaseObject's usage."""

    _tags = {"A": "1", "B": 2, "C": 1234, 3: "D"}

    def __init__(self, a="something", b=7, c=None):
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def some_method(self):
        """To be implemented by child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class FixtureClassChild(FixtureClassParent):
    """Fixture class that is child of FixtureClassParent."""

    _tags = {"A": 42, 3: "E"}

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass


@pytest.fixture
def mod_names():
    """Pytest fixture to return module names for tests."""
    return MOD_NAMES


@pytest.fixture
def fixture_object():
    """Pytest fixture of BaseObject class."""
    return BaseObject


@pytest.fixture
def fixture_not_a_base_object():
    """Pytest fixture for NotABaseObject."""
    return NotABaseObject


@pytest.fixture
def fixture_composition_dummy():
    """Pytest fixture for CompositionDummy."""
    return CompositionDummy


@pytest.fixture
def fixture_inherits_from_base_object():
    """Pytest fixture for InheritsFromBaseObject."""
    return InheritsFromBaseObject


@pytest.fixture
def fixture_class_parent():
    """Pytest fixture for FixtureClassParent."""
    return FixtureClassParent


@pytest.fixture
def fixture_class_child():
    """Pytest fixture for FixtureClassChild."""
    return FixtureClassChild


# Fixture class for testing tag system, object overrides class tags
@pytest.fixture
def fixture_tag_class_object():
    """Fixture class for testing tag system, object overrides class tags."""
    fixture_class_child = FixtureClassChild()
    fixture_class_child._tags_dynamic = {"A": 42424241, "B": 3}
    return fixture_class_child


def test_is_non_public_module(mod_names):
    """Test _is_non_public_module correctly indentifies non-public modules."""
    for mod in mod_names["public"]:
        assert _is_non_public_module(mod) is False
    for mod in mod_names["non_public"]:
        assert _is_non_public_module(mod) is True


def test_is_non_public_module_raises_error():
    """Test _is_non_public_module raises a ValueError for non-string input."""
    with pytest.raises(ValueError):
        _is_non_public_module(7)


def test_is_ignored_module(mod_names):
    """Test _is_ignored_module correctly identifies modules in ignored sequence."""
    # Test case when no modules are ignored
    for mod in mod_names["public"]:
        assert _is_ignored_module(mod) is False

    # No modules should be flagged as ignored if the ignored moduels aren't encountered
    modules_to_ignore = ("a_module_not_encountered",)
    for mod in mod_names["public"]:
        assert _is_ignored_module(mod, modules_to_ignore=modules_to_ignore) is False

    modules_to_ignore = ("_some",)
    for mod in mod_names["non_public"]:
        assert _is_ignored_module(mod, modules_to_ignore=modules_to_ignore) is False

    # When ignored modules are encountered then they should be flagged as True
    modules_to_ignore = ("skbase",)
    for mod in MOD_NAMES["public"]:
        if "skbase" in mod:
            expected_to_ignore = True
        else:
            expected_to_ignore = False
        assert (
            _is_ignored_module(mod, modules_to_ignore=modules_to_ignore)
            is expected_to_ignore
        )


def test_filter_by_class(
    fixture_object,
    fixture_not_a_base_object,
    fixture_composition_dummy,
    fixture_inherits_from_base_object,
):
    """Test _filter_by_class correctly identifies classes."""
    # Test case when no class filter is applied (should always return True)
    assert _filter_by_class(fixture_composition_dummy) is True

    # Test case where a signle filter is applied
    assert _filter_by_class(fixture_composition_dummy, fixture_object) is True
    assert _filter_by_class(fixture_not_a_base_object, fixture_object) is False
    assert (
        _filter_by_class(fixture_not_a_base_object, fixture_inherits_from_base_object)
        is False
    )

    # Test case when sequence of classes supplied as filter
    assert (
        _filter_by_class(
            fixture_composition_dummy,
            (fixture_object, fixture_inherits_from_base_object),
        )
        is True
    )
    assert (
        _filter_by_class(
            fixture_composition_dummy,
            (fixture_not_a_base_object, fixture_inherits_from_base_object),
        )
        is False
    )


def test_filter_by_tags(
    fixture_object,
    fixture_not_a_base_object,
    fixture_composition_dummy,
    fixture_class_parent,
):
    """Test _filter_by_tags correctly filters classes by their tags or tag values."""
    # Test case when no tag filter is applied (should always return True)
    assert _filter_by_tags(fixture_composition_dummy) is True
    # Even if the class isn't a BaseObject
    assert _filter_by_tags(fixture_not_a_base_object) is True

    # Check when tag_filter is a str and present in the class
    assert _filter_by_tags(fixture_class_parent, tag_filter="A") is True
    # Check when tag_filter is str and not present in the class
    assert _filter_by_tags(fixture_object, tag_filter="A") is False

    # Test functionality when tag present and object doesn't have tag interface
    # assert _filter_by_tags(NotABaseObject, tag_filter="A") is True

    # Test functionality where tag_filter is Iterable of str
    # all tags in iterable are in the class
    assert _filter_by_tags(fixture_class_parent, ("A", "B", "C")) is True
    # Some tags in iterable are in class and others aren't
    assert _filter_by_tags(fixture_class_parent, ("A", "B", "C", "D", "E")) is False

    # Test functionality where tag_filter is Dict[str, Any]
    # All keys in dict are in tag_filter and values all match
    assert _filter_by_tags(fixture_class_parent, {"A": "1", "B": 2}) is True
    # All keys in dict are in tag_filter, but at least 1 value doesn't match
    assert _filter_by_tags(fixture_class_parent, {"A": 1, "B": 2}) is False
    # Atleast 1 key in dict is not in tag_filter
    assert _filter_by_tags(fixture_class_parent, {"E": 1, "B": 2}) is False

    # Iterable tags should be all strings
    with pytest.raises(ValueError, match=r"`tag_filter` should be.*"):
        assert _filter_by_tags(fixture_class_parent, ("A", "B", 3))

    # Tags that aren't iterable have to be strings
    with pytest.raises(ValueError, match=r"`tag_filter` should be.*"):
        assert _filter_by_tags(fixture_class_parent, 7.0)

    # Dictionary tags should have string keys
    with pytest.raises(ValueError, match=r"`tag_filter` should be.*"):
        assert _filter_by_tags(fixture_class_parent, {7: 11})


def test_walk_returns_expected_format():
    """Check walk function returns expected format."""

    def _test_walk_return(p):
        assert (
            isinstance(p, tuple) and len(p) == 3
        ), "_walk shoul return tuple of length 3"
        assert (
            isinstance(p[0], str)
            and isinstance(p[1], bool)
            and isinstance(p[2], importlib.machinery.FileFinder)
        )

    # Test with string relative path
    for p in _walk(pathlib.Path("../")):
        _test_walk_return(p)

    # Test with string absolute path
    for p in _walk(str(pathlib.Path("../").absolute())):
        _test_walk_return(p)

    # Test with pathlib.Path
    for p in _walk(pathlib.Path("../")):
        _test_walk_return(p)


def test_walk_returns_expected_exclude():
    """Check _walk returns expected result when using exclude param."""
    results = list(_walk(pathlib.Path("../"), exclude="tests"))
    assert len(results) == 1
    assert results[0][0] == "_lookup" and results[0][1] is False


@pytest.mark.parametrize("suppress_import_stdout", [True, False])
def test_import_module_returns_module(suppress_import_stdout):
    """Test that _import_module returns a module type."""
    # Import module based on name case
    imported_mod = _import_module(
        "skbase", suppress_import_stdout=suppress_import_stdout
    )
    assert isinstance(imported_mod, ModuleType)

    # Import module based on SourceFileLoader for a file path
    # First specify path to _lookup.py relative to this file
    path = str(pathlib.Path(".").absolute().parent / "_lookup.py")
    loader = importlib.machinery.SourceFileLoader("_lookup", path)
    imported_mod = _import_module(loader, suppress_import_stdout=suppress_import_stdout)
    assert isinstance(imported_mod, ModuleType)


@pytest.mark.parametrize("as_dataframe", [True, False])
@pytest.mark.parametrize("return_names", [True, False])
def test_all_objects_returns_expected_types(as_dataframe, return_names):
    """Check that all_objects return argument has correct type."""
    objs = all_objects(
        package_name="skbase.mock_package",
        return_names=return_names,
        as_dataframe=as_dataframe,
    )
    # We expect at least one object to be returned
    assert len(objs) > 0

    if as_dataframe:
        expected_columns = 2 if return_names else 1
        assert isinstance(objs, pd.DataFrame) and objs.shape[1] == expected_columns
        # Verify all objects in the object columns are BaseObjects
        for i in range(len(objs)):
            expected_obj_column = 1 if return_names else 0
            assert issubclass(objs.iloc[i, expected_obj_column], BaseObject)
            if return_names:
                # Value in name column should be a string
                assert isinstance(objs.iloc[i, 0], str)
                # Value in name column should be name of object in object column
                assert objs.iloc[i, 0] == objs.iloc[i, 1].__name__

    else:
        # Should return a list
        assert isinstance(objs, list)
        # checks return type specification (see docstring)
        if return_names:
            for obj in objs:
                assert issubclass(obj[1], BaseObject)
                if return_names:
                    assert isinstance(obj, tuple) and len(obj) == 2
                    assert isinstance(obj[0], str)
                    assert obj[0] == obj[1].__name__