"""
Script for processing PDBBind files for Robustly interrogating machine learning-based
scoring functions: what are they learning?
"""

import os
from tqdm import tqdm
from rdkit import Chem
import re


def process_protein_file(protein_file, pdb_code, output_dir):
    with open(protein_file, "r") as f:
        pattern1 = re.compile(str("^ATOM"), re.DOTALL)
        if not os.path.exists(f"{output_dir}/{pdb_code}"):
            os.makedirs(f"{output_dir}/{pdb_code}")
        with open(f"{output_dir}/{pdb_code}/{pdb_code}_protein_cleaned.pdb", "w") as g:
            for line in f.readlines():
                if re.match(pattern1, line):
                    g.write(line)
    return None


def process_ligand_file(ligand_file, pdb_code, output_dir):
    mol = Chem.MolFromMol2File(ligand_file, sanitize=True)
    Chem.MolToMolFile(mol, f"{output_dir}/{pdb_code}/{pdb_code}_ligand.sdf")
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdbbind_dir",
        type=str,
        help="Path to downloaded PDBBind directory, e.g. /home/user/pdbbind_2020_general",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to output procssed PDBBind data e.g. /home/user/pdbbind_2020_general_processed",
    )
    args = parser.parse_args()
    with open("toolboxsf_pdb_codes.txt", "r") as f:
        pdbs = f.readlines()
    pdbs = [x.strip() for x in pdbs]
    for pdb_code in tqdm(pdbs):
        try:
            protein_file = f"{args.pdbbind_dir}/{pdb_code}/{pdb_code}_protein.pdb"
            ligand_file = f"{args.pdbbind_dir}/{pdb_code}/{pdb_code}_ligand.mol2"
            process_protein_file(protein_file, pdb_code, args.output_dir)
            process_ligand_file(ligand_file, pdb_code, args.output_dir)
        except Exception as e:
            print(f"Failed to process {pdb_code} due to {e}")
