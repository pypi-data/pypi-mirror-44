import pytest

import astropy.units as u
from astropy.modeling.core import Model
from astropy.modeling.models import Identity, Multiply, Pix2Sky_AZP, Shift
from astropy.modeling.separable import is_separable

from dkist.utils.model_tools import (make_forward_input_map, make_tree_input_map,
                                     re_model_trees, remove_input_frame)

## Fixtures used in this file are defined in conftest.py


def test_input_map(triple_input_flat):
    ti_map = make_tree_input_map(triple_input_flat._tree)
    assert len(ti_map) == 2
    assert "x00" in list(ti_map.values())[0]
    assert "x01" in list(ti_map.values())[0]
    assert "x0" in list(ti_map.values())[1]


def test_not_and(single_non_separable):
    tree = single_non_separable._tree
    ti = make_tree_input_map(tree)
    assert len(ti) == 1
    assert tree in ti.keys()


def test_leaf_map(triple_input_nested):
    tree = triple_input_nested._tree
    ti_map = make_tree_input_map(tree)
    assert list(ti_map.keys())[1] is tree.right
    assert isinstance(list(ti_map.keys())[1].value, Model)


def test_spatial_imap(spatial_like):
    tree = spatial_like._tree
    trees = make_tree_input_map(tree.left)
    assert len(trees) == 1
    assert len(list(trees.values())[0]) == 2


def test_spatial_remove(spatial_like):
    tree = spatial_like._tree
    trees = remove_input_frame(tree, "x01")
    assert len(trees) == 1
    assert len(trees[0].inputs) == 2


def test_remove_non_sep(single_non_separable):
    tree = single_non_separable._tree
    trees = remove_input_frame(tree, "x")
    assert len(trees) == 1
    assert trees[0] is tree

    trees = remove_input_frame(tree, "x", remove_coupled_trees=True)
    assert len(trees) == 0


def test_remove_non_sep_double(double_non_separable):
    tree = double_non_separable._tree
    trees = remove_input_frame(tree, "x")
    assert len(trees) == 2
    assert trees[0] is tree.left
    assert trees[1] is tree.right

    trees = remove_input_frame(tree, "x", remove_coupled_trees=True)
    assert len(trees) == 1
    assert trees[0] is tree.right


def test_remove_no_input(single_non_separable):
    tree = single_non_separable._tree
    trees = remove_input_frame(tree, "x00000")
    assert len(trees) == 1
    assert trees[0] is tree


def test_remove_frame_flat(triple_input_flat):
    # x0 is the last input
    trees = remove_input_frame(triple_input_flat._tree, "x0")
    assert len(trees) == 1
    assert len(trees[0].inputs) == 2


def test_remove_frame_flat_split(triple_input_flat):
    # x0 is the last input
    trees = remove_input_frame(triple_input_flat._tree, "x01")
    assert len(trees) == 2
    assert len(trees[0].inputs) == 1
    assert len(trees[1].inputs) == 1


def test_remove_frame_nested(triple_input_nested):
    # x01 is the second input, therefore splitting the tree
    trees = remove_input_frame(triple_input_nested._tree, "x01")
    assert len(trees) == 2
    assert len(trees[0].inputs) == 1
    assert len(trees[1].inputs) == 1


def test_re_model_nested(triple_input_nested):
    # x01 is the second input, therefore splitting the tree
    trees = remove_input_frame(triple_input_nested._tree, "x01")
    assert len(trees) == 2
    model = re_model_trees(trees)
    assert isinstance(model, Model)
    assert len(model.inputs) == 2


def test_drop_one_half_input_tree(spatial_like):
    """
    This test checks that if the input we want to drop is the sole input to one
    half of the original tree, then we drop that half and keep the other.
    """
    tree = spatial_like._tree
    drop_input = "x01"

    # Work out based on name which tree we are dropping.
    ginp_map = make_tree_input_map(tree)
    r_ginp_map = {tuple(v): k for k, v in ginp_map.items()}
    drop_tree = r_ginp_map[(drop_input,)]

    trees = remove_input_frame(tree, drop_input)

    # Work out which tree we are keeping
    keep_trees = [tree.left, tree.right]
    keep_trees.remove(drop_tree)

    # Check we have kept and dropped the correct trees
    assert drop_tree not in trees
    assert keep_trees[0] in trees


def test_dont_drop_one_half(spatial_like):
    """
    Test the situation where we are not just dropping one half of the tree.
    """
    spatial_like = spatial_like & Identity(1)
    tree = spatial_like._tree
    ginp_map = make_tree_input_map(tree)
    r_ginp_map = {tuple(v): k for k, v in ginp_map.items()}

    trees = remove_input_frame(tree, "x01")
    assert r_ginp_map[("x0",)] in trees
    assert tree.left not in trees
