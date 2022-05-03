"""
Compare the RMSD of two different structures whose RMSD is known.
"""

import pytest
import numpy as np
from scipy.spatial import transform

try:
    import openmm
except ImportError:
    import simtk.openmm as openmm
    
try:
    import openmm.app as openmm_app
except ImportError:
    import simtk.openmm.app as openmm_app
from parmed import unit


def test_rmsd_scipy():
    group = [4, 16, 26, 47, 57, 74, 98, 117, 139, 151, 158, 173, 179, 190, 
             201, 208, 240, 254, 268, 274]

    pdb_filename1 = "../systems/trp_cage_files/trp_cage.pdb"
    pdb_filename2 = "../systems/trp_cage_files/trp_cage_0.40.pdb"

    expected_rmsd = 0.3946
    
    pdb_file1 = openmm_app.PDBFile(pdb_filename1)
    ref_positions = pdb_file1.positions
    
    pdb_file2 = openmm_app.PDBFile(pdb_filename2)
    positions = pdb_file2.positions
    
    pos_subset = []
    ref_subset = []
    
    print("scipy align atoms:", group)
    
    for atom_index in group:
        pos_subset.append(positions[atom_index].value_in_unit(unit.nanometers))
        ref_subset.append(ref_positions[atom_index].value_in_unit(unit.nanometers))

    pos_subset = np.array(pos_subset)
    ref_subset = np.array(ref_subset)

    print("pos_subset:", pos_subset)
    print("ref_subset:", ref_subset)
    
    print("pos_subset[:,0]:", pos_subset[:,0])
    print("np.mean(pos_subset[:,0]):", np.mean(pos_subset[:,0]))
    
    avg_pos = np.array([float(np.mean(pos_subset[:,0])), float(np.mean(pos_subset[:,1])), float(np.mean(pos_subset[:,2]))])
    print("avg_pos:", avg_pos)
    avg_ref = np.array([np.mean(ref_subset[:,0]), np.mean(ref_subset[:,1]), np.mean(ref_subset[:,2])])
    print("avg_ref:", avg_ref)
    
    pos_subset_centered = pos_subset - avg_pos
    print("pos_subset_centered:", pos_subset_centered)
    
    ref_subset_centered = ref_subset - avg_ref
    print("ref_subset_centered:", ref_subset_centered)
    
    rotation, value = transform.Rotation.align_vectors(
        pos_subset_centered, ref_subset_centered)
    
    scipy_rmsd = value / np.sqrt(len(group))
    print("rotation:", rotation)
    print("value:", value)
        
    print("Scipy RMSD:", scipy_rmsd)
    print("expected RMSD:", expected_rmsd)
    assert np.isclose(scipy_rmsd, expected_rmsd, atol=1e-3)

@pytest.mark.needs_cuda
def test_rmsd_openmm():
    group = [4, 16, 26, 47, 57, 74, 98, 117, 139, 151, 158, 173, 179, 190, 
             201, 208, 240, 254, 268, 274]
    prmtop_filename = "../systems/trp_cage_files/trp_cage.prmtop"
    inpcrd_filename = "../systems/trp_cage_files/trp_cage.inpcrd"
    pdb_filename1 = "../systems/trp_cage_files/trp_cage.pdb"
    pdb_filename2 = "../systems/trp_cage_files/trp_cage_0.40.pdb"

    expected_rmsd = 0.3946
    
    prmtop = openmm_app.AmberPrmtopFile(prmtop_filename)
    inpcrd = openmm_app.AmberInpcrdFile(inpcrd_filename)
    system = prmtop.createSystem(nonbondedMethod=openmm_app.NoCutoff, constraints=openmm_app.HBonds)

    num_steps = 1
    time_step = 0.000002
    
    pdb_file1 = openmm_app.PDBFile(pdb_filename1)
    rmsd_force = openmm.RMSDForce(pdb_file1.positions, group)
    rmsd_force.setForceGroup(1)
    system.addForce(rmsd_force)
    
    mypdb = openmm_app.PDBFile(pdb_filename2)

    integrator = openmm.LangevinIntegrator(277.8*unit.kelvin, 1/unit.picosecond, time_step*unit.picoseconds)
    platform = openmm.Platform.getPlatformByName('CUDA')
    properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
    simulation = openmm_app.Simulation(prmtop.topology, system, integrator, platform, properties)
    simulation.context.setPositions(mypdb.positions)
    #simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors + 0.2)
    #simulation.minimizeEnergy()
    simulation.context.setVelocitiesToTemperature(0.0 * unit.kelvin)

    simulation.step(num_steps)
    
    state = simulation.context.getState(getEnergy=True, groups={1})
    value = state.getPotentialEnergy().value_in_unit(unit.kilojoules / unit.mole)
        
    print("openmm RMSD:", value)
    print("expected RMSD:", expected_rmsd)
    assert np.isclose(value, expected_rmsd, atol=1e-3)
