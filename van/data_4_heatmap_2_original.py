# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:36:59 2015

@author: VanessaRM
"""

os.chdir('./prepare_dataset')

from Bio import Phylo
import re
import pandas
from pandas import DataFrame

# imput files
tree_file_path = "RAxML_bipartitions.Conc_Aln.nwk" # substitute by ArgumentParser
tree = Phylo.read(tree_file_path, "newick")
tree.rooted = True

otu_table = pandas.read_csv("output.csv")
otu_table.index = otu_table.OTU # first column is the name of the otus
otus_ids = otu_table["OTU"]


#get headers
first_row = otu_table.iloc[:0]
store_all_we_want = DataFrame(columns=(first_row))

counter = 0
for leaf in tree.get_terminals():
    counter += 1
    if leaf.name in otus_ids:
        print leaf.name
        wanted_info = (otu_table.ix[leaf.name])
        store_all_we_want = store_all_we_want.append(wanted_info)
    else:
        print counter
        for i in xrange(1:len(first_row))
            store_all_we_want.loc[counter]= leaf.name
        

#Save file:
#store_all_we_want = store_all_we_want.reset_index()
store_all_we_want.to_csv("var_table.txt", sep='\t')
