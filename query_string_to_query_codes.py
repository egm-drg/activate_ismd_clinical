import re
import pandas as pd
import os
import sys
import getopt
from __future__ import division
from collections import OrderedDict as od

#################################################################
#read in four dictionary files and list of terms to match

# this is for code dictionaries
base_file = r'/Users/emoldovan/Desktop/activate/deriving_codes/auto_match/'
# this is for search string
base_file_search_string = r'/Users/emoldovan/Desktop/activate/insmed_part2/pt1.data_pull.code_selection'

flstr_ICD_9 = base_file + r'ICD_9_codes.txt'
cols_keeprename_ICD_9 = od({ 'DIAGNOSIS_CODE':'code', 'LONG_DESCRIPTION':'description'})
sep_ICD_9 = ','
ICD_9_dict = pd.read_csv(flstr_ICD_9, sep = sep_ICD_9, dtype = object)[\
  cols_keeprename_ICD_9.keys()
  ].rename(columns = cols_keeprename_ICD_9)

flstr_ICD_10 = base_file + r'ICD_10_codes.txt'
cols_keeprename_ICD_10 = od({ 'DIAGNOSIS_CODE':'code', 'LONG_DESCRIPTION':'description'})
sep_ICD_10 = ','
ICD_10_dict = pd.read_csv(flstr_ICD_10, sep = sep_ICD_10, dtype = object)[\
  cols_keeprename_ICD_10.keys()
  ].rename(columns = cols_keeprename_ICD_10)

flstr_NDC = base_file + r'ndc_package_and_product_codes.txt'
cols_keeprename_NDC = od({ 'NDCPACKAGECODE':'code',\
                        'PROPRIETARYNAME':'PROPRIETARYNAME',\
                     'NONPROPRIETARYNAME':'NONPROPRIETARYNAME',\
                          'SUBSTANCENAME':'SUBSTANCENAME',\
                          'PHARM_CLASSES':'PHARM_CLASSES',\
                          'DOSAGEFORMNAME':'doseage_format'})
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

flstr_to_match_rx = base_file_search_string + r'search_patterns.for_codes.px.txt'
sep_to_match_rx = ','
to_match_rx = pd.read_csv(flstr_to_match_rx, sep = sep_to_match_rx, dtype = object, header = None)

flstr_to_match_px = base_file_search_string + r'search_patterns.for_codes.rx.txt'
sep_to_match_px = ','
to_match_px = pd.read_csv(flstr_to_match_px, sep = sep_to_match_px, dtype = object, header = None)

#################################################################

to_match_dx[0] = to_match_dx[0].str.lower()
to_match_rx[0] = to_match_rx[0].str.lower()
to_match_px[0] = to_match_px[0].str.lower()

NDC_dict['description'] = NDC_dict['PROPRIETARYNAME'] + ' ' + NDC_dict['NONPROPRIETARYNAME'] +  ' ' + \
                            NDC_dict['SUBSTANCENAME'] +  ' ' + NDC_dict['PHARM_CLASSES']

del [NDC_dict['PROPRIETARYNAME'], NDC_dict['NONPROPRIETARYNAME'], NDC_dict['SUBSTANCENAME'], NDC_dict['PHARM_CLASSES']]

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
NDC_matches_dx = match_terms(to_match_dx[0], NDC_dict)
HCPCS_matches_dx = match_terms(to_match_dx[0], HCPCS_dict)

ICD_9_matches_rx = match_terms(to_match_rx[0], ICD_9_dict)
ICD_10_matches_rx = match_terms(to_match_rx[0], ICD_10_dict)
NDC_matches_rx = match_terms(to_match_rx[0], NDC_dict)
HCPCS_matches_rx = match_terms(to_match_rx[0], HCPCS_dict)

ICD_9_matches_px = match_terms(to_match_px[0], ICD_9_dict)
ICD_10_matches_px = match_terms(to_match_px[0], ICD_10_dict)
NDC_matches_px = match_terms(to_match_px[0], NDC_dict)
HCPCS_matches_px = match_terms(to_match_px[0], HCPCS_dict)

ICD_9_matches_dx['code_type'] = 'ICD_9'
ICD_10_matches_dx['code_type'] = 'ICD_10'
NDC_matches_dx['code_type'] = 'NDC'
HCPCS_matches_dx['code_type'] = 'HCPCS' 

ICD_9_matches_rx['code_type'] = 'ICD_9'
ICD_10_matches_rx['code_type'] = 'ICD_10'
NDC_matches_rx['code_type'] = 'NDC'
HCPCS_matches_rx['code_type'] = 'HCPCS' 

ICD_9_matches_px['code_type'] = 'ICD_9'
ICD_10_matches_px['code_type'] = 'ICD_10'
NDC_matches_px['code_type'] = 'NDC'
HCPCS_matches_px['code_type'] = 'HCPCS' 

################################################################################################

def fda_to_cms_code_conversion(list_of_codes):
    list_of_codes = pd.DataFrame(list_of_codes, columns = {'code'})
    list_of_codes['new_code'] = ''
    for index, line in list_of_codes.iterrows():
      try:
        code = line['code']
        pattern_packaging_code = re.compile(r'[0-9].*-[0-9].*-[0-9].*')
        has_packaging_code = False
        if pattern_packaging_code.match(code):
            has_packaging_code = True
        
        pattern1 = re.compile(r'[0-9]{4}-[0-9]{4}')
        pattern2 = re.compile(r'[0-9]{5}-[0-9]{3}')
        pattern3 = re.compile(r'[0-9]{5}-[0-9]{4}')
    	
        if pattern1.match(code):
    	   #4-4-2
    	   #Insert 0 before first four digits, % at end if no packaging code
            code = '0' + code
        elif pattern3.match(code):
            #5-4-1
    	    #Insert 0 before last digit, % at end if no packaging code
            if has_packaging_code:
                code = code[0:len(code)-2] + '0' + code[len(code)-1]
        elif pattern2.match(code):
            #5-3-2
            #Insert 0 after first five digits, % at end if no packaging code
            code = code[0:5] + '0' + code[5:len(code)]
        else:
            print 'The following code does not conform to FDA template: ' + code
            print "The gov't expects the following number of digits with a dash between them:"
            print '4-4-2, 5-3-2, 5-4-1.'
            
        code = code.replace("-", "")
        list_of_codes['new_code'].loc[index] = code
      except:
        # note that some fields return emty code names; these cause error so we check that this is
        # why errors actually happen
        print 'problem with: '
        print index, line
    return list_of_codes

NDC_matches_dx = NDC_matches_dx.reset_index().drop('index', axis = 1)
NDC_matches_converted_dx = fda_to_cms_code_conversion(list(NDC_matches_dx['code']))
NDC_matches_old_and_converted_dx = pd.merge(left = NDC_matches_dx, left_on = 'code',
                                        right = NDC_matches_converted_dx, right_on = 'code')
NDC_matches_dx = NDC_matches_old_and_converted_dx.drop('code', axis = 1).rename(columns = {'new_code':'code'})

NDC_matches_rx = NDC_matches_rx.reset_index().drop('index', axis = 1)
NDC_matches_converted_rx = fda_to_cms_code_conversion(list(NDC_matches_rx['code']))
NDC_matches_old_and_converted_rx = pd.merge(left = NDC_matches_rx, left_on = 'code',
                                        right = NDC_matches_converted_rx, right_on = 'code')
NDC_matches_rx = NDC_matches_old_and_converted_rx.drop('code', axis = 1).rename(columns = {'new_code':'code'})

NDC_matches_px = NDC_matches_px.reset_index().drop('index', axis = 1)
NDC_matches_converted_px = fda_to_cms_code_conversion(list(NDC_matches_px['code']))
NDC_matches_old_and_converted_px = pd.merge(left = NDC_matches_px, left_on = 'code',
                                        right = NDC_matches_converted_px, right_on = 'code')
NDC_matches_px = NDC_matches_old_and_converted_px.drop('code', axis = 1).rename(columns = {'new_code':'code'})

#################################################################

# I'm including the doseage_format option for anlyses that require drugs in a particular format
# try:
#   NDC_matches['pharmacokinetics'] = None
#   for index, row in NDC_matches.iterrows():
#     if (('spray' in row['doseage_format'].lower()) | ('nebuli' in row['doseage_format'].lower()) | ('atomi' in row['doseage_format'].lower())):
#       NDC_matches.loc[index, 'pharmacokinetics'] = 'inhalant'
#     else:
#       NDC_matches.loc[index, 'pharmacokinetics'] = 'n/a'
#   del NDC_matches['doseage_format']
#   ICD_9_matches['pharmacokinetics'] = 'n/a'
#   ICD_10_matches['pharmacokinetics'] = 'n/a'
#   HCPCS_matches['pharmacokinetics'] = 'n/a'
# except:
#   del NDC_matches['pharmacokinetics']
# del NDC_matches['doseage_format']

concat_matches_dx = pd.concat([ICD_9_matches_dx, ICD_10_matches_dx, NDC_matches_dx, HCPCS_matches_dx])
concat_matches_dx['inclusion_exclusion'] = ''
concat_matches_dx = concat_matches_dx[~concat_matches_dx['code'].isnull()]
    
concat_matches_rx = pd.concat([ICD_9_matches_rx, ICD_10_matches_rx, NDC_matches_rx, HCPCS_matches_rx])
concat_matches_rx['inclusion_exclusion'] = ''
concat_matches_rx = concat_matches_rx[~concat_matches_rx['code'].isnull()]

concat_matches_px = pd.concat([ICD_9_matches_px, ICD_10_matches_px, NDC_matches_px, HCPCS_matches_px])
concat_matches_px['inclusion_exclusion'] = ''
concat_matches_px = concat_matches_px[~concat_matches_px['code'].isnull()]

#################################################################

out_file = '/Users/emoldovan/Desktop/activate/insmed_part2/pt1.data_pull.code_selection'

concat_matches_dx.to_csv(out_file + 'dx_codes_for_pull.txt', index = False, sep = '|')
concat_matches_rx.to_csv(out_file + 'rx_codes_for_pull.txt', index = False, sep = '|')
concat_matches_px.to_csv(out_file + 'px_codes_for_pull.txt', index = False, sep = '|')




