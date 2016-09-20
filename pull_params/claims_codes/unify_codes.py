
################################################################################

import pandas as pd
import numpy  as np
from collections import OrderedDict as od


################################################################################

flstr_in_dx_icd10_addtnl_by_hand        = \
    'codes.in/codes.dx.icd10.addtnl_by_hand.16_05_14.csv'
sep_in_dx_icd10_addtnl_by_hand          = ','
col_val_omitrow_dx_icd10_addtnl_by_hand = ('inclusion_exclusion' , 'n')
col_code_dx_icd10_addtnl_by_hand        = 'code'
col_descript_dx_icd10_addtnl_by_hand    = 'search_term'
val_datasource_dx_icd10_addtnl_by_hand  = 'dx_icd10'
#
flstr_in_dx_icd10_by_search             = \
    'codes.in/codes.dx.icd10.by_search.with_inclusion_exclusion.16_05_14.csv'
sep_in_dx_icd10_by_search               = ','
col_val_omitrow_dx_icd10_by_search      = ('inclusion_exclusion' , 'n')
col_code_dx_icd10_by_search             = 'code'
col_descript_dx_icd10_by_search         = 'search_term'
val_datasource_dx_icd10_by_search       = 'dx_icd10'
#
flstr_in_dx_icd9_addtnl_by_hand         = \
    'codes.in/codes.dx.icd9.addtnl_by_hand.16_05_14.csv'
sep_in_dx_icd9_addtnl_by_hand           = ','
col_val_omitrow_dx_icd9_addtnl_by_hand  = ('inclusion_exclusion' , 'n')
col_code_dx_icd9_addtnl_by_hand         = 'code'
col_descript_dx_icd9_addtnl_by_hand     = 'search_term'
val_datasource_dx_icd9_addtnl_by_hand   = 'dx_icd9'
#
flstr_in_dx_icd9_by_search              = \
    'codes.in/codes.dx.icd9.by_search.with_inclusion_exclusion.16_05_14.csv'
sep_in_dx_icd9_by_search                = ','
col_val_omitrow_dx_icd9_by_search       = ('inclusion_exclusion' , 'n')
col_code_dx_icd9_by_search              = 'code'
col_descript_dx_icd9_by_search          = 'search_term_adj'
val_datasource_dx_icd9_by_search        = 'dx_icd9'
#
flstr_in_px                             = \
    'codes.in/codes.px.mixed_type.by_search.16_05_14.csv'
sep_in_px                               = '|'
col_val_omitrow_px                      = ('HCPCS' , '')
col_code_px                             = 'HCPCS'
col_descript_px                         = 'match_term'
val_datasource_px                       = 'px_hcpcs'
#
flstr_in_rx                             = \
    'codes.in/codes.rx.mixed_type.by_search.16_05_14.csv'
sep_in_rx                               = ','
col_val_omitrow_rx                      = ('PRODUCTNDC' , '')
col_code_rx                             = 'PRODUCTNDC'
col_descript_rx                         = 'match_term'
val_datasource_rx                       = 'rx_ncd'


################################################################################

# flstr_in_dx_icd10_addtnl_by_hand
# flstr_in_dx_icd10_by_search     
# flstr_in_dx_icd9_addtnl_by_hand 
# flstr_in_dx_icd9_by_search      
# flstr_in_px                     
# flstr_in_rx                     


################################################################################
dx_icd10_addtnl_by_hand = pd.read_csv(  flstr_in_dx_icd10_addtnl_by_hand
                                      , sep = sep_in_dx_icd10_addtnl_by_hand 
                                      , dtype = str )
codes_dx_icd10_addtnl_by_hand = dx_icd10_addtnl_by_hand.loc[
     dx_icd10_addtnl_by_hand[ col_val_omitrow_dx_icd10_addtnl_by_hand[0] ]
  != col_val_omitrow_dx_icd10_addtnl_by_hand[1]                        
     ][ [   col_code_dx_icd10_addtnl_by_hand
          , col_descript_dx_icd10_addtnl_by_hand ]
  ].rename( columns = { col_code_dx_icd10_addtnl_by_hand     : 'code' 
                       ,col_descript_dx_icd10_addtnl_by_hand : 'descript' } )
codes_dx_icd10_addtnl_by_hand[ 'code_type' ] = \
    val_datasource_dx_icd10_addtnl_by_hand
#
dx_icd10_by_search = pd.read_csv(  flstr_in_dx_icd10_by_search
                                 , sep = sep_in_dx_icd10_by_search
                                 , dtype = str )
codes_dx_icd10_by_search = dx_icd10_by_search.loc[
     dx_icd10_by_search[ col_val_omitrow_dx_icd10_by_search[0] ]
  != col_val_omitrow_dx_icd10_by_search[1]                        
     ][ [   col_code_dx_icd10_by_search
          , col_descript_dx_icd10_by_search ]
  ].rename( columns = { col_code_dx_icd10_by_search     : 'code' 
                       ,col_descript_dx_icd10_by_search : 'descript' } )
codes_dx_icd10_by_search[ 'code_type' ] = \
    val_datasource_dx_icd10_by_search
#
dx_icd9_addtnl_by_hand = pd.read_csv(  flstr_in_dx_icd9_addtnl_by_hand
                                      , sep = sep_in_dx_icd9_addtnl_by_hand 
                                      , dtype = str )
codes_dx_icd9_addtnl_by_hand = dx_icd9_addtnl_by_hand.loc[
     dx_icd9_addtnl_by_hand[ col_val_omitrow_dx_icd9_addtnl_by_hand[0] ]
  != col_val_omitrow_dx_icd9_addtnl_by_hand[1]                        
     ][ [   col_code_dx_icd9_addtnl_by_hand
          , col_descript_dx_icd9_addtnl_by_hand ]
  ].rename( columns = { col_code_dx_icd9_addtnl_by_hand     : 'code' 
                       ,col_descript_dx_icd9_addtnl_by_hand : 'descript' } )
codes_dx_icd9_addtnl_by_hand[ 'code_type' ] = \
    val_datasource_dx_icd9_addtnl_by_hand
#
dx_icd9_by_search = pd.read_csv(  flstr_in_dx_icd9_by_search
                                 , sep = sep_in_dx_icd9_by_search
                                 , dtype = str )
codes_dx_icd9_by_search = dx_icd9_by_search.loc[
     dx_icd9_by_search[ col_val_omitrow_dx_icd9_by_search[0] ]
  != col_val_omitrow_dx_icd9_by_search[1]                        
     ][ [   col_code_dx_icd9_by_search
          , col_descript_dx_icd9_by_search ]
  ].rename( columns = { col_code_dx_icd9_by_search     : 'code' 
                       ,col_descript_dx_icd9_by_search : 'descript' } )
codes_dx_icd9_by_search[ 'code_type' ] = \
    val_datasource_dx_icd9_by_search
#
rx = pd.read_csv(  flstr_in_rx
                                 , sep = sep_in_rx
                                 , dtype = str )
codes_rx = rx.loc[
     rx[ col_val_omitrow_rx[0] ]
  != col_val_omitrow_rx[1]                        
     ][ [   col_code_rx
          , col_descript_rx ]
  ].rename( columns = { col_code_rx     : 'code' 
                       ,col_descript_rx : 'descript' } )
codes_rx[ 'code_type' ] = \
    val_datasource_rx
#
px = pd.read_csv(  flstr_in_px
                                 , sep = sep_in_px
                                 , dtype = str )
codes_px = px.loc[
     px[ col_val_omitrow_px[0] ]
  != col_val_omitrow_px[1]                        
     ][ [   col_code_px
          , col_descript_px ]
  ].rename( columns = { col_code_px     : 'code' 
                       ,col_descript_px : 'descript' } )
codes_px[ 'code_type' ] = \
    val_datasource_px

to_concat = [
    codes_dx_icd10_addtnl_by_hand
  , codes_dx_icd10_by_search     
  , codes_dx_icd9_addtnl_by_hand 
  , codes_dx_icd9_by_search      
  , codes_px                     
  , codes_rx                     
]
concated = pd.concat( to_concat , axis = 0 , ignore_index = True )
concated = concated.loc[ ~ concated.duplicated( keep='first' ) ]

################################################################################

flstr_out = 'codes.out/codes.all.unified.csv'
sep_out   = ','

concated.to_csv( flstr_out , sep = sep_out , index = False )

