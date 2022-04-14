"""
test_common_base.py
"""
import os

import numpy as np
from parmed import unit
import seekr2.modules.common_base as base

TEST_DIRECTORY = os.path.dirname(__file__)

def test_get_box_vectors_from_pdb():
    expected_box_vectors = unit.Quantity(
        [[61.359, 0.0, 0.0], 
         [-20.451767557539473, 57.850255701875476, 0.0], 
         [-20.451767557539473, -28.92251350474921, 50.101300355778946]], 
                      unit=unit.angstrom)
    test_pdb_filename = os.path.join(
        TEST_DIRECTORY, 
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at0.pdb")
    result = base.get_box_vectors_from_pdb(test_pdb_filename)
    assert np.isclose(expected_box_vectors.value_in_unit(unit.angstroms), 
                      result.value_in_unit(unit.angstroms)).all()
