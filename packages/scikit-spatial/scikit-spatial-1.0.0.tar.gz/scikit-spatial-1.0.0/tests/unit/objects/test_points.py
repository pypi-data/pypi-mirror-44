import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Points


@pytest.mark.parametrize(
    "array",
    [
        # The array cannot be empty.
        [],
        [[]],
        [[], []],
        # The array cannot be 1D.
        [0],
        [5],
        [0, 1],
        [0, 1, 2],
        # The array cannot have one element.
        [[0]],
        [[5]],
        # The points cannot have different lengths.
        [[0, 1], [0, 1, 0]],
    ],
)
def test_failure(array):

    with pytest.raises(Exception):
        Points(array)


@pytest.mark.parametrize(
    "points, dim_expected",
    [
        (Points([[0], [1]]), 1),
        (Points([[0, 0], [1, 1]]), 2),
        (Points([[0, 0], [0, 0], [0, 0]]), 2),
        (Points([[0, 0, 1], [1, 2, 1]]), 3),
        (Points([[4, 3, 9, 1], [3, 7, 8, 1]]), 4),
    ],
)
def get_dimension(points, dim_expected):

    assert points.get_dimension() == dim_expected


@pytest.mark.parametrize(
    "points, dim_expected",
    [
        (Points([[1], [-5]]), 3, Points([[1, 0, 0], [-5, 0, 0]])),
        (Points([[0, 0], [1, 1]]), 3, Points([[0, 0, 0], [1, 1, 0]])),
        (Points([[0, 0], [1, 1]]), 4, Points([[0, 0, 0, 0], [1, 1, 0, 0]])),
    ],
)
def set_dimension(points, dim, points_expected):

    assert_array_equal(points.set_dimension(dim), points_expected)
