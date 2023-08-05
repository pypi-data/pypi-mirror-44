import pytest

from skspatial.objects import Points, Vector, Line


@pytest.mark.parametrize(
    "array_u, array_v, bool_expected",
    [
        ([1, 0], [0, 1], True),
        ([0, 1], [-1, 0], True),
        ([0, 1], [-1, 0], True),
        ([-1, 0], [0, -1], True),
        ([1, 1], [-1, -1], False),
        ([1, 1], [1, 1], False),
        # The zero vector is perpendicular to all vectors.
        ([0, 0], [-1, 5], True),
        ([0, 0, 0], [1, 1, 1], True),
    ],
)
def test_is_perpendicular(array_u, array_v, bool_expected):
    """Test checking if vector u is perpendicular to vector v."""
    vector_u = Vector(array_u)

    assert vector_u.is_perpendicular(array_v) == bool_expected


@pytest.mark.parametrize(
    "array_u, array_v, bool_expected",
    [
        ([0, 1], [0, 1], True),
        ([1, 0], [0, 1], False),
        ([0, 1], [4, 0], False),
        ([0, 1], [0, 5], True),
        ([1, 1], [-1, -1], True),
        ([1, 1], [-5, -5], True),
        ([0, 1], [0, -1], True),
        ([0.1, 5, 4], [3, 2, 0], False),
        ([1, 1, 1, 1], [-2, -2, -2, 4], False),
        ([1, 1, 1, 1], [-2, -2, -2, -2], True),
        ([5, 0, -6, 7], [0, 1, 6, 3], False),
        ([6, 0, 1, 0], [-12, 0, -2, 0], True),
        # The zero vector is parallel to all vectors.
        ([0, 0], [1, 1], True),
        ([5, 2], [0, 0], True),
        ([5, -3, 2, 6], [0, 0, 0, 0], True),
    ],
)
def test_is_parallel(array_u, array_v, bool_expected):
    """Test checking if vector u is parallel to vector v."""
    vector_u = Vector(array_u)

    assert vector_u.is_parallel(array_v) == bool_expected


@pytest.mark.parametrize(
    "array_a, array_b, value_expected",
    [
        ([0, 1], [0, 1], 0),
        ([0, 1], [0, 9], 0),
        ([0, 1], [0, -20], 0),
        ([0, 1], [1, 1], 1),
        ([0, 1], [38, 29], 1),
        ([0, 1], [1, 0], 1),
        ([0, 1], [1, -100], 1),
        ([0, 1], [1, -100], 1),
        ([0, 1], [-1, 1], -1),
        ([0, 1], [-1, 20], -1),
        ([0, 1], [-1, -20], -1),
        ([0, 1], [-5, 50], 1),
    ],
)
def test_vector_side(array_a, array_b, value_expected):

    Vector(array_a).side(array_b) == value_expected


@pytest.mark.parametrize(
    "points, bool_expected",
    [
        ([[0, 0], [0, 0], [0, 0]], True),
        ([[1, 0], [1, 0], [1, 0]], True),
        ([[0, 0], [0, 1], [0, 2]], True),
        ([[0, 0], [0, 1], [1, 2]], False),
        ([[0, 1], [0, 0], [0, 2]], True),
        ([[0, 0], [-1, 0], [10, 0]], True),
        ([[0, 0], [1, 1], [2, 2], [-4, -4], [5, 5]], True),
        ([[0, 0, 0], [1, 1, 1], [2, 2, 2]], True),
        ([[0, 0, 0], [1, 1, 1], [2, 2, 2.5]], False),
        ([[0, 0, 0], [1, 1, 0], [2, 2, 0], [-4, -4, 10], [5, 5, 0]], False),
    ],
)
def test_are_collinear(points, bool_expected):
    """Test checking if multiple points are collinear."""

    assert Points(points).are_collinear() == bool_expected


@pytest.mark.parametrize(
    "line_a, line_b, bool_expected",
    [
        (Line([0, 0], [1, 1]), Line([0, 0], [0, 1]), True),
        (Line([-6, 7], [5, 90]), Line([1, 4], [-4, 5]), True),
        (Line([0, 0, 1], [1, 1, 0]), Line([0, 0, 0], [0, 1, 0]), False),
        (Line([0, 0, 1], [1, 1, 0]), Line([0, 0, 1], [0, 1, 0]), True),
        (Line([0, 0, 1], [1, 0, 1]), Line([0, 0, 1], [2, 0, 2]), True),
    ],
)
def test_is_coplanar(line_a, line_b, bool_expected):
    """Test checking if two lines are coplanar."""

    assert line_a.is_coplanar(line_b) == bool_expected
