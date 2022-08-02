"""
Run all the systems to ensure that inputs work correctly.
"""

import os
import glob
import tempfile

from seekr2.modules.common_prepare import Browndye_settings_input, \
    MMVT_input_settings, Elber_input_settings, Toy_settings_input

from seekr2.modules.common_prepare import MMVT_input_settings

from seekr2.modules.common_base import Ion, Amber_params, Forcefield_params, \
    Box_vectors
from seekr2.modules.common_cv import Spherical_cv_anchor, Spherical_cv_input, \
    RMSD_cv_input, RMSD_cv_anchor, Toy_cv_input, Toy_cv_anchor, Grid_combo, \
    State_point
import seekr2.run as run

import create_model_input

TEST_DIRECTORY = os.path.dirname(__file__)
SYSTEMS_DIRECTORY = os.path.join(TEST_DIRECTORY, "../systems/")

def run_1_system():
    tmp_path = tempfile.TemporaryDirectory()
    #model_input_filename = os.path.join(TEST_DIRECTORY, "../systems/trypsin_benzamidine_files/input_tryp_ben_mmvt.xml")
    #model_input_filename = os.path.join(TEST_DIRECTORY, "../systems/trypsin_benzamidine_files/input_tryp_ben_elber.xml")
    #model_input_filename = os.path.join(TEST_DIRECTORY, "../systems/trp_cage_files/input_trp_cage.xml")
    model_input_filename = os.path.join(TEST_DIRECTORY, "../systems/superoxide_dismutase_files/input_sod.xml")
    create_model_input.prepare_model(model_input_filename, tmp_path.name, in_directory=SYSTEMS_DIRECTORY)
    return

def run_all_systems():
    tmp_path = tempfile.TemporaryDirectory()
    system_dir = os.path.join(TEST_DIRECTORY, "../systems")
    for dir in os.listdir(system_dir):
        glob_expr = os.path.join(system_dir, dir, "input*.xml")
        glob_list = glob.glob(glob_expr)
        for input_filename in glob_list:
            print("Preparing system:", input_filename)
            model_input_filename = os.path.join(TEST_DIRECTORY, input_filename)
            model = create_model_input.prepare_model(model_input_filename, tmp_path.name, in_directory=SYSTEMS_DIRECTORY)
            if not model.using_toy():
                if model.get_type() == "elber":
                    model.calculation_settings.fwd_rev_interval = 10
                    model.calculation_settings.num_umbrella_stage_steps = 100
                run.run(model, "0", min_total_simulation_length=1000)

if __name__ == "__main__":
    #run_1_system()
    run_all_systems()
