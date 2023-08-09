
"""
Written by Seedorfe
"""


import os
import sys


import config


def find_root_path():
    ''' finding root directory path of this file'''

    _temp_init_1 = __file__.split("/")

    _temp_init_1.pop()

    _temp_init_2 = ""

    for _ in _temp_init_1:
        if _ != '':
            _temp_init_2 += "/"
            _temp_init_2 += _
        elif _ == "":
            pass # do nothig 
    
    config.ROOT_PATH = _temp_init_2

    return _temp_init_2




def make_needed_dir():
    '''make needed directory'''

    try:
        os.mkdir(config.ROOT_PATH + "/data")
        os.mkdir(config.ROOT_PATH + "/temp")
        os.mkdir(config.ROOT_PATH + "/file")
        os.mkdir(config.ROOT_PATH + "/export")
    except FileExistsError:
        pass # do nothing 
    except:
        print("--------\nwe have a problem when making needed dirs\n-------- ")
        sys.exit(1)



        
def get_files(dir):
    return next(os.walk(config.ROOT_PATH + dir, (None, None, [])))[2]



def clear_files(dir):

    _location = config.ROOT_PATH + dir

    for _ in get_files(dir):
        _path = os.path.join(_location, _)
        os.remove(_path)


def delete_file(dir, file):

    _location = config.ROOT_PATH + dir

    _path = os.path.join(_location, file)

    os.remove(_path)
    
        

