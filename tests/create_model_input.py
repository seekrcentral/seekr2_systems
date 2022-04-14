"""
create_model_input.py

Create Model input objects for use in tests.
"""

import os

import seekr2.modules.common_base as base
import seekr2.modules.common_prepare as common_prepare
import seekr2.modules.common_cv as common_cv

import seekr2.modules.filetree as filetree
import seekr2.modules.check as check
# Don't remove the following library imports - needed by deserializer

import seekr2.prepare as prepare

TEST_DIRECTORY = os.path.dirname(__file__)
SEEKR_DIRECTORY = os.path.dirname(prepare.__file__)

def assign_amber_params(input_anchor, prmtop_filename, pdb_filename):
    input_anchor.starting_amber_params = base.Amber_params()
    input_anchor.starting_amber_params.prmtop_filename = prmtop_filename
    input_anchor.starting_amber_params.pdb_coordinates_filename = pdb_filename
    return

def create_tryp_ben_mmvt_model_input(root_dir, bd=False):
    """
    Create a trypsin-benzamidine model input object.
    """
    os.chdir(TEST_DIRECTORY)
    model_input = common_prepare.Model_input()
    model_input.calculation_type = "mmvt"
    model_input.calculation_settings = common_prepare.MMVT_input_settings()
    model_input.calculation_settings.md_output_interval = 2500000
    model_input.calculation_settings.md_steps_per_anchor = 250000000
    model_input.temperature = 298.0
    model_input.pressure = 1.0
    model_input.ensemble = "nvt"
    model_input.root_directory = root_dir
    model_input.md_program = "openmm"
    model_input.constraints = "HBonds"
    model_input.rigidWater = True
    model_input.hydrogenMass = None
    model_input.timestep = 0.002
    model_input.nonbonded_cutoff = 0.9
    cv_input1 = common_cv.Spherical_cv_input()
    cv_input1.group1 = [2478, 2489, 2499, 2535, 2718, 2745, 2769, 2787, 2794, 
                        2867, 2926]
    cv_input1.group2 = [3221, 3222, 3223, 3224, 3225, 3226, 3227, 3228, 3229]
    cv_input1.input_anchors = []
    
    radius_list = [0.05, 0.15, 0.25, 0.35, 0.45, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 
                   1.9]
    lower_milestone_radius_list = [None, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 
                                   1.2, 1.4, 1.6, 1.8]
    upper_milestone_radius_list = [0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 
                                   1.4, 1.6, 1.8, None]
    pdb_filename_list = [
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at0.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at1.58.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at2.76.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at3.69.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at4.61.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at7.20.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at9.33.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at11.06.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at12.70.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at14.04.pdb",
        "../systems/trypsin_benzamidine_files/mmvt/tryp_ben_at17.00.pdb",
        ""
    ]
    
    for i, (radius, lower_milestone_radius, upper_milestone_radius, \
            pdb_filename) in enumerate(zip(radius_list, \
            lower_milestone_radius_list, upper_milestone_radius_list, \
            pdb_filename_list)):
        input_anchor = common_cv.Spherical_cv_anchor()
        input_anchor.radius = radius
        input_anchor.lower_milestone_radius = lower_milestone_radius
        input_anchor.upper_milestone_radius = upper_milestone_radius
        input_anchor.starting_amber_params = base.Amber_params()
        input_anchor.starting_amber_params.prmtop_filename \
            = os.path.abspath(
                "../systems/trypsin_benzamidine_files/tryp_ben.prmtop")
        input_anchor.starting_amber_params.pdb_coordinates_filename = \
            os.path.abspath(pdb_filename)
        if i == 0:
            input_anchor.bound_state = True
        else:
            input_anchor.bound_state = False
            
        if i == len(radius_list)-1:
            input_anchor.bulk_anchor = True
        else:
            input_anchor.bulk_anchor = False
        cv_input1.input_anchors.append(input_anchor)
    
    model_input.cv_inputs = [cv_input1]
    
    if bd:
        model_input.browndye_settings_input \
            = common_prepare.Browndye_settings_input()
        model_input.browndye_settings_input.binary_directory = ""
        model_input.browndye_settings_input.receptor_pqr_filename \
            = os.path.abspath("../systems/trypsin_benzamidine_files/trypsin.pqr")
        model_input.browndye_settings_input.ligand_pqr_filename \
            = os.path.abspath(
                "../systems/trypsin_benzamidine_files/benzamidine.pqr")
        model_input.browndye_settings_input.apbs_grid_spacing = 0.5
        model_input.browndye_settings_input.receptor_indices = [
            2478, 2489, 2499, 2535, 2718, 2745, 2769, 2787, 2794, 2867, 2926]
        model_input.browndye_settings_input.ligand_indices = [
            0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        ion1 = base.Ion()
        ion1.radius = 1.14
        ion1.charge = 2.0
        ion1.conc = 0.02
        ion2 = base.Ion()
        ion2.radius = 1.67
        ion2.charge = -1.0
        ion2.conc = 0.1
        ion3 = base.Ion()
        ion3.radius = 4.0
        ion3.charge = 1.0
        ion3.conc = 0.06
        model_input.browndye_settings_input.ions = [ion1, ion2, ion3]
        model_input.browndye_settings_input.num_bd_milestone_trajectories = 1000
        model_input.browndye_settings_input.num_b_surface_trajectories = 10000
        model_input.browndye_settings_input.max_b_surface_trajs_to_extract = 100
        model_input.browndye_settings_input.n_threads = 1
    else:
        model_input.browndye_settings_input  = None
    
    return model_input
    
def create_tryp_ben_elber_model_input(root_dir, bd=False):
    """
    Create a trypsin-benzamidine model input object.
    """
    os.chdir(TEST_DIRECTORY)
    model_input = common_prepare.Model_input()
    model_input.calculation_type = "elber"
    model_input.calculation_settings = common_prepare.Elber_input_settings()
    model_input.calculation_settings.temperature_equil_progression = [
        300., 310., 320., 330., 340., 350., 340., 330., 320., 310., 300.]
    model_input.calculation_settings.num_temperature_equil_steps = 1000
    model_input.calculation_settings.num_umbrella_stage_steps = 500000000
    model_input.calculation_settings.umbrella_force_constant = 5000.0
    model_input.calculation_settings.fwd_rev_interval = 100000
    model_input.temperature = 298.0
    model_input.pressure = 1.0
    model_input.ensemble = "nvt"
    model_input.root_directory = root_dir
    model_input.md_program = "openmm"
    model_input.constraints = "HBonds"
    model_input.rigidWater = True
    model_input.hydrogenMass = None
    model_input.timestep = 0.002
    model_input.nonbonded_cutoff = 0.9
    cv_input1 = common_cv.Spherical_cv_input()
    cv_input1.group1 = [2478, 2489, 2499, 2535, 2718, 2745, 2769, 2787, 2794, 
                        2867, 2926]
    cv_input1.group2 = [3221, 3222, 3223, 3224, 3225, 3226, 3227, 3228, 3229]
    cv_input1.input_anchors = []
    
    radius_list = [0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
    pdb_filename_list = [
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at1.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at1.5.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at2.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at3.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at4.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at6.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at8.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at10.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at12.pdb",
        "../systems/trypsin_benzamidine_files/elber/tryp_ben_at14.pdb",
        ""
    ]
    
    for i, (radius, pdb_filename) in enumerate(
            zip(radius_list, pdb_filename_list)):
        input_anchor = common_cv.Spherical_cv_anchor()
        input_anchor.radius = radius
        input_anchor.starting_amber_params = base.Amber_params()
        input_anchor.starting_amber_params.prmtop_filename \
            = os.path.abspath(
                "../systems/trypsin_benzamidine_files/elber/tryp_ben.prmtop")
        input_anchor.starting_amber_params.pdb_coordinates_filename = \
            os.path.abspath(pdb_filename)
        if i == 0:
            input_anchor.bound_state = True
        else:
            input_anchor.bound_state = False
            
        if i == len(radius_list)-1:
            input_anchor.bulk_anchor = True
        else:
            input_anchor.bulk_anchor = False
        cv_input1.input_anchors.append(input_anchor)
    
    model_input.cv_inputs = [cv_input1]
    
    if bd:
        model_input.browndye_settings_input \
            = common_prepare.Browndye_settings_input()
        model_input.browndye_settings_input.binary_directory = ""
        model_input.browndye_settings_input.receptor_pqr_filename \
            = os.path.abspath("../systems/trypsin_benzamidine_files/trypsin.pqr")
        model_input.browndye_settings_input.ligand_pqr_filename \
            = os.path.abspath(
                "../systems/trypsin_benzamidine_files/benzamidine.pqr")
        model_input.browndye_settings_input.apbs_grid_spacing = 0.5
        model_input.browndye_settings_input.receptor_indices = [
            2478, 2489, 2499, 2535, 2718, 2745, 2769, 2787, 2794, 2867, 2926]
        model_input.browndye_settings_input.ligand_indices = [
            0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        ion1 = base.Ion()
        ion1.radius = 1.14
        ion1.charge = 2.0
        ion1.conc = 0.02
        ion2 = base.Ion()
        ion2.radius = 1.67
        ion2.charge = -1.0
        ion2.conc = 0.1
        ion3 = base.Ion()
        ion3.radius = 4.0
        ion3.charge = 1.0
        ion3.conc = 0.06
        model_input.browndye_settings_input.ions = [ion1, ion2, ion3]
        model_input.browndye_settings_input.num_bd_milestone_trajectories = 1000
        model_input.browndye_settings_input.num_b_surface_trajectories = 10000
        model_input.browndye_settings_input.max_b_surface_trajs_to_extract = 100
        model_input.browndye_settings_input.n_threads = 1
    else:
        model_input.browndye_settings_input  = None
    
    return model_input
    
def create_sod_mmvt_model_input(root_dir):
    """
    Create a generic host-guest model input object.
    """
    os.chdir(TEST_DIRECTORY)
    input_xml_filename = os.path.abspath(
        "../systems/superoxide_dismutase_files/input_sod.xml")
    model_input = common_prepare.Model_input()
    model_input.deserialize(input_xml_filename, user_input=True)
    model_input.root_directory = root_dir
    os.chdir(os.path.dirname(input_xml_filename))
    return model_input

def create_rmsd_mmvt_model_input(root_dir):
    """
    Create a RMSD TRP cage model input.
    """
    os.chdir(TEST_DIRECTORY)
    model_input = common_prepare.Model_input()
    model_input.calculation_type = "mmvt"
    model_input.calculation_settings = common_prepare.MMVT_input_settings()
    model_input.calculation_settings.md_output_interval = 10000
    model_input.calculation_settings.md_steps_per_anchor = 100000 #1000000
    model_input.temperature = 298.15
    model_input.pressure = 1.0
    model_input.ensemble = "nvt"
    model_input.root_directory = root_dir
    model_input.md_program = "openmm"
    model_input.constraints = "HBonds"
    model_input.rigidWater = True
    model_input.hydrogenMass = None
    model_input.timestep = 0.002
    model_input.nonbonded_cutoff = None
    
    cv_input1 = common_cv.RMSD_cv_input()
    cv_input1.group = [4, 16, 26, 47, 57, 74, 98, 117, 139, 151, 158, 173, 
                       179, 190, 201, 208, 240, 254, 268, 274]
    cv_input1.ref_structure = os.path.abspath(
        "../systems/trp_cage_files/trp_cage.pdb")
    cv_input1.input_anchors = []
    
    values_list = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    amber_prmtop_filename = os.path.abspath(
        "../systems/trp_cage_files/trp_cage.prmtop")
    forcefield_built_in_ff_list = ["amber14/tip3pfb.xml"]
    forcefield_custom_ff_list = ["../systems/hostguest_files/hostguest.xml"]
    
    pdb_filenames = [os.path.abspath(
        "../systems//trp_cage_files/trp_cage.pdb"), 
                     os.path.abspath(
        "../systems//trp_cage_files/trp_cage_0.40.pdb"), 
                     os.path.abspath(
        "../systems/trp_cage_files/trp_cage_0.60.pdb"), 
                     os.path.abspath(
        "../systems/trp_cage_files/trp_cage_0.80.pdb"), 
                     os.path.abspath(
        "../systems/trp_cage_files/trp_cage_1.00.pdb"), 
                     ""]
    for i, (value, pdb_filename) in enumerate(zip(values_list, pdb_filenames)):
        input_anchor = common_cv.RMSD_cv_anchor()
        input_anchor.value = value
        assign_amber_params(input_anchor, amber_prmtop_filename, 
                            pdb_filename)
        
        if i == 0:
            input_anchor.bound_state = True
        else:
            input_anchor.bound_state = False
            
        if i == len(values_list)-1:
            input_anchor.bulk_anchor = True
        else:
            input_anchor.bulk_anchor = False
        #input_anchor.bulk_anchor = False
    
        cv_input1.input_anchors.append(input_anchor)
    
    model_input.cv_inputs = [cv_input1]
    model_input.browndye_settings_input = None
    
    return model_input

def create_smoluchowski_mmvt_model_input(root_dir, num_input_anchors=5):
    """
    Create a Smoluchowski MMVT model input object.
    """
    os.chdir(TEST_DIRECTORY)
    model_input = common_prepare.Model_input()
    model_input.calculation_type = "mmvt"
    model_input.calculation_settings = common_prepare.MMVT_input_settings()
    model_input.calculation_settings.md_output_interval = 0
    model_input.calculation_settings.md_steps_per_anchor = 0
    model_input.temperature = 300.0
    model_input.pressure = 1.0
    model_input.ensemble = "nvt"
    model_input.root_directory = root_dir
    model_input.md_program = "smoluchowski"
    model_input.constraints = "none"
    model_input.rigidWater = False
    model_input.hydrogenMass = None
    model_input.timestep = 0.002
    model_input.nonbonded_cutoff = 0.0
    cv_input1 = common_cv.Spherical_cv_input()
    cv_input1.group1 = [0]
    cv_input1.group2 = [1]
    cv_input1.input_anchors = []
    
    for i in range(num_input_anchors):
        input_anchor = common_cv.Spherical_cv_anchor()
        input_anchor.radius = i + 0.5
        input_anchor.starting_amber_params = None
        if i == 0:
            input_anchor.bound_state = True
        else:
            input_anchor.bound_state = False
        
        if i == num_input_anchors-1:
            input_anchor.bulk_anchor = True
        else:
            input_anchor.bulk_anchor = False
        cv_input1.input_anchors.append(input_anchor)
    
    model_input.cv_inputs = [cv_input1]
    
    model_input.browndye_settings_input  = None
    
    return model_input

def create_smoluchowski_elber_model_input(root_dir, num_input_anchors=5):
    """
    Create a Smoluchowski Elber model input object.
    """
    os.chdir(TEST_DIRECTORY)
    model_input = create_smoluchowski_mmvt_model_input(root_dir)
    model_input.calculation_type = "elber"
    model_input.calculation_settings = common_prepare.Elber_input_settings()
    model_input.calculation_settings.num_umbrella_stage_steps = 100000
    model_input.calculation_settings.umbrella_force_constant = 9000.0
    model_input.calculation_settings.fwd_rev_interval = 500
    model_input.calculation_settings.rev_output_interval = None
    model_input.calculation_settings.fwd_output_interval = None
    
    cv_input1 = common_cv.Spherical_cv_input()
    cv_input1.group1 = [0]
    cv_input1.group2 = [1]
    cv_input1.input_anchors = []
    cv_input1.input_anchors = []
    
    for i in range(num_input_anchors):
        input_anchor = common_cv.Spherical_cv_anchor()
        input_anchor.radius = i + 1.0
        input_anchor.starting_amber_params = None
        if i == 0:
            input_anchor.bound_state = True
        else:
            input_anchor.bound_state = False
        
        if i == num_input_anchors-1:
            input_anchor.bulk_anchor = True
        else:
            input_anchor.bulk_anchor = False
        cv_input1.input_anchors.append(input_anchor)
    
    model_input.cv_inputs = [cv_input1]
    model_input.browndye_settings_input  = None
    return model_input

def prepare_model(model_input_filename, tmp_path, in_directory):
    force_overwrite = True
    skip_checks = False
    
    model_input = common_prepare.Model_input()
    model_input.deserialize(model_input_filename, user_input = True)
    
    basename = os.path.split(model_input.root_directory.strip("/"))[-1]
    model_input.root_directory = os.path.join(tmp_path, basename)
    os.chdir(in_directory)
    model, xml_path = prepare.prepare(model_input, force_overwrite)
    if model.anchor_rootdir == ".":
        model_dir = os.path.dirname(xml_path)
        model.anchor_rootdir = os.path.abspath(model_dir)
    if not skip_checks:
        check.check_pre_simulation_all(model)
    assert os.path.exists(model.anchor_rootdir)
    return