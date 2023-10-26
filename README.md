![Logo](logo.png)

# ToolBoxSF - Robustly interrogating machine learning based scoring functions: what are they learning?

## Introduction

This repository contains the raw code and built singularity containers for the scoring function platform and toolbox described in the preprint "Robustly interrogating machine learning based scoring functions: what are they learning?" by Guy Durant, Fergus Boyles, Kris Birchall, Brian Marsden, and Charlotte M. Deane.

## Installation

Singularity containers for each scoring function and baseline models in the paper, the data for benchmarks for any docking or modified poses and training scripts can be found at the following link:

- [link](https://zenodo.org/records/8410136)

The singularity containers can be built from scratch using .def files provided in the singularity_defs folder with the following commands:

```bash
singularity build <SINGULARITY_CONTAINER_NAME>.sif <SINGULARITY_RECIPE_FILE>.def
```

The original code can also be accessed rom the model_repos folder.

Note that the PDBBind crystal structures are not provided to download and instead require running of the scripts described in the data section below.

## Data processing

PDBbind 2020 General data can be downloaded from the following link:

- [PDBBind Website](http://www.pdbbind.org.cn/)

To process the raw files, use the following command, which requires the latest update of RDKit and tqdm to be installed:

`python scripts/pdbbind_processing.py --pdbbind_dir <PDBBIND_DATA_DIR> --output_dir <OUTPUT_DIR>`

The data can be processed as described in the paper using the following scripts:

```bash
python scripts/pdbbind_processing.py --pdbbind_dir <RAW_PDBBIND_DATA_DIR> --output_dir <OUTPUT_DIR>
```

## Usage

It is recommended to use the singularity containers to run the scoring functions, they should be downloaded into their own separate folders.

N.B. PointVS requires the pre-trained weights (48_compact\_\_0 at ) for pose classification to be in the same folder.

The following commands can be used to run the scoring functions:

For training:

```bash
singularity exec --nv--home $(dirname $PWD) <SINGULARITY_CONTAINER_NAME>.sif bash toolboxsf --train --csv_file ../toolboxsf_training_csvs/casf_2016_train.csv --data_dir ../pdbbind_2020_general --model_name <MODEL_NAME>
```

For validation:

```bash
singularity exec --nv --home $(dirname $PWD) <SINGULARITY_CONTAINER_NAME>.sif bash toolboxsf --predict --val_csv_file ../toolboxsf_benchmarks/csv_files/casf_2016_test.csv --val_data_dir ../pdbbind_2020_general --model_name <TRAINED_MODEL_NAME>
```

## Creating training/test splits

The training/test splits used in the paper can be found in the training_csvs folder. To create new training/test splits, create csv files with the following columns:

- key: Unique key for each protein-ligand pair (typically a PDB code)
- pk: Binding affinity as a pK value
- protein: Relative path to protein structure PDB file (when combined with the data_dir argument, should point to the full path)
- ligand: Relative path to ligand structure SDF file (when combined with the data_dir argument, should point to the full path)

The data_dir argument should point to the upper directory containing both the protein and ligand structure files.
