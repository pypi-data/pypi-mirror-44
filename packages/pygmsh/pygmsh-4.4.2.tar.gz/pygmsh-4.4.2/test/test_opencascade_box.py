# -*- coding: utf-8 -*-
import pytest

import pygmsh

from helpers import compute_volume


@pytest.mark.skipif(pygmsh.get_gmsh_major_version() < 3, reason="requires Gmsh >= 3")
def test():
    geom = pygmsh.opencascade.Geometry()

    geom.add_box([0.0, 0.0, 0.0], [1, 2, 3], char_length=0.1)

    ref = 6
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == "__main__":
    import meshio

    meshio.write_points_cells("opencascade_box.vtu", *test())
