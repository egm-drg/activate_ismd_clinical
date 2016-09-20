import re
import pandas as pd
import os
import sys
import getopt
from __future__ import division
from collections import OrderedDict as od

#################################################################
# this is for code dictionaries
base_file = r'/Users/emoldovan/Desktop/activate/deriving_codes/auto_match/'
# this is for search string
base_file_search_string = r'/Users/emoldovan/Desktop/activate/insmed_clinical/pt1.data_pull.code_selection/'

#read in six dictionary files and list of terms to match
flstr_ICD_9 = base_file + r'ICD_9_codes.txt'
cols_keeprename_ICD_9 = od({ 'DIAGNOSIS_CODE':'code', 'LONG_DESCRIPTION':'description'})
sep_ICD_9 = ','
ICD_9_dict = pd.read_csv(flstr_ICD_9, sep = sep_ICD_9, dtype = object)[\
  cols_keeprename_ICD_9.keys()
  ].rename(columns = cols_keeprename_ICD_9)

flstr_ICD_9_proc = base_file + r'ICD_9_procedures_for_string_query.txt'
cols_keeprename_ICD_9_proc = od({ 'PROCEDURE_CODE':'code', 'LONG_DESCRIPTION':'description'})
sep_ICD_9_proc = '|'
ICD_9_dict_proc = pd.read_csv(flstr_ICD_9_proc, sep = sep_ICD_9_proc, dtype = object)[\
  cols_keeprename_ICD_9_proc.keys()
  ].rename(columns = cols_keeprename_ICD_9_proc)

flstr_ICD_10 = base_file + r'ICD_10_codes.txt'
cols_keeprename_ICD_10 = od({ 'DIAGNOSIS_CODE':'code', 'LONG_DESCRIPTION':'description'})
sep_ICD_10 = ','
ICD_10_dict = pd.read_csv(flstr_ICD_10, sep = sep_ICD_10, dtype = object)[\
  cols_keeprename_ICD_10.keys()
  ].rename(columns = cols_keeprename_ICD_10)

# ICD 10 INPUT FORMAT TO BE CHANGED
# ICD_10_procedures_for_string_query.txt

# flstr_ICD_10_proc = base_file + r'ICD_10_procedures_for_string_query.txt'
# with open(flstr_ICD_10_proc) as f:
#     ICD_10_proc_dict_raw = f.read().splitlines()
# ICD_10_proc_dict = pd.DataFrame(columns = {'code','description'})
# i = 0
# for line in ICD_10_proc_dict_raw:
#   split_line = line.split(' ', 1)
#   ICD_10_proc_dict.loc[i, 'code'] = split_line[0]
#   ICD_10_proc_dict.loc[i, 'description'] = split_line[1]
#   i += 1

flstr_NDC = base_file + r'omop_meta_dictionary.csv'
cols_keeprename_NDC = od({ 'CONCEPT_NAME':'description',\
                        'CONCEPT_CODE':'code'})
sep_NDC = ','
NDC_dict = pd.read_csv(flstr_NDC, sep = sep_NDC, dtype = object)[\
  cols_keeprename_NDC.keys()
  ].rename(columns = cols_keeprename_NDC)

flstr_HCPCS = base_file + r'hcpc_levels_1_and_2.txt'
cols_keeprename_HCPCS = od({'HCPC':'code', \
                   'LONG_DESCRIPTION':'description'})
sep_HCPCS = '|'
HCPCS_dict = pd.read_csv(flstr_HCPCS, sep = sep_HCPCS, dtype = object)[\
  cols_keeprename_HCPCS.keys()
  ].rename(columns = cols_keeprename_HCPCS)

#this file does not have a column name, so commands that reference a column name are moot
flstr_to_match_dx = base_file_search_string + r'search_patterns.for_codes.dx.txt'
sep_to_match_dx = ','
to_match_dx = pd.read_csv(flstr_to_match_dx, sep = sep_to_match_dx, dtype = object, header = None)

flstr_to_match_rx = base_file_search_string + r'search_patterns.for_codes.rx.txt'
sep_to_match_rx = ','
to_match_rx = pd.read_csv(flstr_to_match_rx, sep = sep_to_match_rx, dtype = object, header = None)

flstr_to_match_px = base_file_search_string + r'search_patterns.for_codes.px.txt'
sep_to_match_px = ','
to_match_px = pd.read_csv(flstr_to_match_px, sep = sep_to_match_px, dtype = object, header = None)

#################################################################

to_match_dx[0] = to_match_dx[0].str.lower()
to_match_rx[0] = to_match_rx[0].str.lower()
to_match_px[0] = to_match_px[0].str.lower()

def match_terms(terms_to_match, database_to_search):
    all_matches = pd.DataFrame(columns = database_to_search.columns)
    all_matches['match_term'] = ''
    for terms in terms_to_match:
       boolean_column = [False] * len(database_to_search)
       for index, row in database_to_search.iterrows():
             try:
               if re.match('.*' + terms + '.*', row['description'], re.I):
                     boolean_column[index] = True   
             except:
               pass
       if not (True in boolean_column):
          print 'did not find: ' + str(terms)      
       match_term = pd.DataFrame([terms] * sum(boolean_column), columns = ['match_term'])
       match_rows = database_to_search[boolean_column].reset_index(drop = True)
       all_matches = all_matches.append(pd.concat([match_term,match_rows], axis=1))
    return all_matches

ICD_9_matches_dx = match_terms(to_match_dx[0], ICD_9_dict)
ICD_10_matches_dx = match_terms(to_match_dx[0], ICD_10_dict)
NDC_matches_rx = match_terms(to_match_rx[0], NDC_dict)
HCPCS_matches_px = match_terms(to_match_px[0], HCPCS_dict)
ICD_9_proc_matches_px =  match_terms(to_match_px[0], ICD_9_dict_proc)
ICD_10_proc_dict_matches_px = match_terms(to_match_px[0], ICD_10_proc_dict)

ICD_9_matches_dx['code_type'] = 'ICD_9'
ICD_10_matches_dx['code_type'] = 'ICD_10'
NDC_matches_rx['code_type'] = 'NDC'
HCPCS_matches_px['code_type'] = 'HCPCS'
ICD_9_proc_matches_px['code_type'] = 'ICD_9_procedure'
ICD_10_proc_matches_px['code_type'] = 'ICD_10_procedure'

concat_matches_dx_rx_px = pd.concat([ICD_9_matches_dx, ICD_10_matches_dx, NDC_matches_rx, \
                                    HCPCS_matches_px, ICD_9_proc_matches_px, ICD_10_proc_matches_px])
concat_matches_dx_rx_px['inclusion_exclusion'] = ''
concat_matches_dx_rx_px = concat_matches_dx_rx_px[~concat_matches_dx_rx_px['code'].isnull()]
concat_matches_dx_rx_px.code = concat_matches_dx_rx_px.code.str.lower()

#################################################################

out_file = '/Users/emoldovan/Desktop/activate/insmed_part2/pt1.data_pull.code_selection/'

concat_matches_dx_rx_px.to_csv(out_file + 'dx_rx_px_codes_for_pull.txt', index = False, sep = '|')



