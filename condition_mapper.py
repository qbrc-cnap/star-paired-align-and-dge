import os
import json

def map_inputs(user, unmapped_data, id_list):
    '''
    This maps the array of group identifiers from the front-end
    and places them in an array
    '''
    return {id_list[0]: unmapped_data}
