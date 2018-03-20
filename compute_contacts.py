from Bio.PDB import PDBParser 
import argparse
import os
import warnings
import logging
import shutil 
import subprocess
import numpy as np
import pandas as pd
from cStringIO import StringIO
import commands

def loadPdb(filename):
	pdb_parser = PDBParser()
	structure = pdb_parser.get_structure(filename, filename)
	return structure

def runDSSP(filename):
	cmd = 'dssp ' + filename
	logging.info(cmd)
	DSSPresult = commands.getstatusoutput(cmd)[1]
	#logging.info(DSSPresult[:100])
	#logging.info(subprocess.check_output('ls'))
	return DSSPresult

def parseDSSP(DSSPresult):
	logging.info('# in result? -- > ', "#" in DSSPresult)
	header_start = DSSPresult.index('#')
	ids = []
	res_num = []
	amino_acids = []
	accessibility = []

	# split lines into list and remove header line
	DSSPresult = DSSPresult[header_start:].split("\n")[1:]

	for line in DSSPresult:
		id, res, aa, acc = line[4:6], line[9:11], line[14:15], line[35:38]
		ids.append(id)
		res_num.append(res)
		amino_acids.append(aa)
		accessibility.append(acc)
	
	DSSPdf = pd.DataFrame(list(zip(ids, res_num, amino_acids, accessibility)),
              columns=['id','res_num', 'aa', 'acc'])

	return DSSPdf

def color_pdb(DSSPdf, pdb_file, treshold):

	core_res = df.loc[DSSPdf.acc <= treshold]

	logging.info(core_res.head())
if __name__ == '__main__': 
	parser =  argparse.ArgumentParser(
		description = 'this is a program that annotates and describes physical properties of a protein structure.')

	parser.add_argument('--single_input', type = str, help  = 'name of input file path in pdb format')

	parser.add_argument('--no_dssp', action = 'store_false', help = 'prevent prgm from using dssp information to compute surface area information.')

	parser.add_argument('--no_hydroph_contacts', action = 'store_false', help = 'prevent prgm from using hydrophobic contacts for the given protein')

	parser.add_argument('--outfile', type=str , help = 'name of output file')

	parser.add_argument('--treshold', nargs = '?', default = 50, help = 'solvent accessible treshold to decide if residue is in core or not. Under or equal to treshhold means burried in core')

	parser.add_argument('--color_structures', action = 'store_true', help = 'colors the pdb structure according to acc profile and saves png')

	parser.add_argument('--debug', action= 'store_true', help = 'print debug data')

	args = parser.parse_args() 

	warnings.filterwarnings('ignore')

	if args.debug:
		logging.basicConfig(level = logging.INFO)	

	dssp_output =  runDSSP(args.single_input)
	
	parsedDSSP = parseDSSP(dssp_output)

	logging.info(parsedDSSP.head())

	logging.info('colnames: ', str(list(parsedDSSP)))	

	if args.color_structures:

		pdb_file = args.single_input
		
		color_pdb(parseDSSP, pdb_file, args.treshold)

	parsedDSSP.to_csv(args.outfile, sep = "\t")









