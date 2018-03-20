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
	for line in DSSPresult[header_start:].split("\n"):
		print line
		# id, res, aa, acc = line[4:6], line[9:11], line[14:15], line[35:38]
		
	#DSSPhandle = StringIO(DSSPresult[header_start:])
	#DSSPheader = DSSPhandle.readline().strip().split()
	#DSSPbody = [line.strip().split() for line in list(DSSPhandle.readlines())]
	##DSSPdf = pd.read_csv(DSSPhandle, sep = '\\s')  	
	return DSSPdf

if __name__ == '__main__': 
	parser =  argparse.ArgumentParser(
		description = 'this is a program that annotates and describes physical properties of a protein structure.')

	parser.add_argument('--single_input', type = str, help  = 'name of input file path in pdb format')

	parser.add_argument('--dssp', action = 'store_false', help = 'prevent prgm from using dssp information to compute surface area information.')

	parser.add_argument('--hydroph_contacts', action = 'store_false', help = 'prevent prgm from using hydrophobic contacts for the given protein')

	parser.add_argument('--outfile', type=str , help = 'name of output file')

	parser.add_argument('--debug', action= 'store_true', help = 'print debug data')

	args = parser.parse_args() 

	warnings.filterwarnings('ignore')

	if args.debug:
		logging.basicConfig(level = logging.INFO)	

	dssp_output =  runDSSP(args.single_input)
	
	parsedDSSP = parseDSSP(dssp_output)

	logging.info(parsedDSSP.head())

	print list(parsedDSSP)

	logging.info('colnames: ', str(list(parsedDSSP)))	