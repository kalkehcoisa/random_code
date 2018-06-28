# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:36:59 2015

@author: VanessaRM
"""

from Bio import Phylo
import pandas
from pandas import DataFrame
import numpy

# imput files
# substitute by ArgumentParser
tree_file_path = "RAxML_bipartitions.Conc_Aln.nwk"
tree = Phylo.read(tree_file_path, "newick")
tree.rooted = True

otu_table = pandas.read_csv('output.csv')
# first column is the name of the otus
otu_table.index = otu_table.OTU
otus_ids = otu_table['OTU']

#set column names
columns = otu_table.columns[1:]
my_output = DataFrame(columns=columns)
row_range = range(1, len(columns))

for leaf in tree.get_terminals():
    if leaf.name in otus_ids:
        # if we have data about it, get all the data
        my_output.loc[leaf.name] = numpy.minimum(otu_table.ix[leaf.name], 1)
    else:
        my_output.loc[leaf.name] = 'NA'

#Save file:
my_output.to_csv("var_table.txt", sep='\t')
