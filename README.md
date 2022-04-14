# seekr2_systems

A set of example systems that can be used for SEEKR2 calculations, as well
as additional tests for SEEKR2 validation.

## Overview of systems

The input files can be found at:
```
systems/
    trp_cage_files/
        input_trp_cage.xml
    superoxide_dismutase_files/
        input_sod.xml
    trypsin_benzamidine_files/
        input_tryp_ben_elber.xml
        input_tryp_ben_multidim.xml
        input_tryp_ben_mmvt_namd.xml
        input_tryp_ben_mmvt.xml
        input_tryp_ben_mmvt_hmr.xml
```

Any one of these input files may be used as input to a SEEKR2 calculation.

Example:
```
python ~/seekr2/seekr2/prepare.py systems/trp_cage_files/input_tryp_ben_mmvt.xml
```

Additionally, these input files are intended to be useful as references for
crafting SEEKR2 input files for your own systems of interest.

## Tests

This repository also contains a number of tests that further validate SEEKR2
on the systems in this repository. They can be run with the following 
command:

```
cd tests
pytest
```

To test all input scripts (for validation purposes), run the following script:
```
python tests/run_me_test_systems.py
```