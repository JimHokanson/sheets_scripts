# -*- coding: utf-8 -*-
"""


"""

import sys
import os
from os.path import dirname
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#JAH TODO: Post response to mine
#https://stackoverflow.com/questions/56669721/get-the-key-value-when-calling-matplolib-pyplot-waitforbuttonpress
#https://stackoverflow.com/questions/15582956/how-to-pause-a-pylab-figure-until-a-key-is-pressed-or-mouse-is-clicked
#https://stackoverflow.com/questions/67747014/manipulate-matplotlib-plots-with-paused-python-execution-replicating-matlab-pau

the_key = None

def press(event):
    global the_key
    the_key = event.key

def pause():
    #TODO: Support a fig input and a target key (or something that indicates any key)
    #TODO: Only do this once per figure (not sure if that is critical or not)
    plt.gcf().canvas.mpl_connect('key_press_event', press)
    keyboardClick=False
    while keyboardClick != True:
        keyboardClick = plt.waitforbuttonpress()
        #True for
        
        #left
        #right
        
        if keyboardClick:
            keyboardClick = the_key == 'enter'
            #print(the_key)
        plt.draw()

def pause2(i):
    #TODO: Support a fig input and a target key (or something that indicates any key)
    #TODO: Only do this once per figure (not sure if that is critical or not)
    plt.gcf().canvas.mpl_connect('key_press_event', press)
    keyboardClick = False
    while keyboardClick != True:
        keyboardClick = plt.waitforbuttonpress()
        #print("wtf")
        #print(the_key)
        #print(keyboardClick)
        #True for
        
        #left
        #right
        
        if keyboardClick:
            if (the_key == 'enter') or (the_key == 'right'):
                plt.draw()  
                return i+1
            elif (the_key == 'left') and (i>0):
                plt.draw()  
                return i-1
            else:
                keyboardClick=False
                plt.draw()  
                
            #print(the_key)
            
          



_last_progress_message = ""
_last_progress_total = 0

def progress_bar(message=None, current=None, total=None, finish=False):
    """
    This will print things out nicely on a single line.
    Call progress_bar() to initialize (start new line) -> not thrilled
        with this part, may change ...

    """
    
    global _last_progress_message
    global _last_progress_total
    
     
    if finish is True:
        progress_message = _last_progress_message + ": %d%% [%d / %d]" % (100, _last_progress_total, _last_progress_total)  
        sys.stdout.write("\r" + progress_message + "\n")
        sys.stdout.flush()
    elif message is None:
        #Set's up a new line - not needed ...
        #print('')
        _last_progress_message = ""
        _last_progress_total = 0
    else:
        _last_progress_message = message
        _last_progress_total = total
        
        # :/
        # I'm not sure how to make this more explcit
        # in loops we start at 0 and go to n-1
        # but I want n-1 to be 100%
        current+=1
        progress_message = message + ": %d%% [%d / %d]" % (current / total * 100, current, total)
        # Don't use print() as it will print in new line every time.
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

def get_root_path(*folders):
    
    #root/uds_routh/uds_routh/utils.py
    mod_path = dirname(os.path.abspath(__file__))
    root = dirname(dirname(mod_path))
    
    return os.path.join(root,*folders)

class _Quotes(str):
    pass


def quotes(input_value):
    if input_value is None:
        return None
    elif isinstance(input_value, int):
        return input_value
    else:
        return _Quotes(input_value)


def display_class(class_instance, pv):
    return '\n%s:\n\n' % type(class_instance) + property_values_to_string(pv,
                                                                          extra_indentation=4)


def property_values_to_string(pv, extra_indentation=0):
    """
    Parameters
    ----------
    pv : OrderedDict
        Keys are properties, values are values
    """

    # Max length

    keys = pv[::2]
    values = pv[1::2]
    values = ['"%s"' % x if isinstance(x, _Quotes) else x for x in values]

    key_lengths = [len(x) for x in keys]
    max_key_length = max(key_lengths) + extra_indentation
    space_padding = [max_key_length - x for x in key_lengths]
    key_display_strings = [' ' * x + y for x, y in zip(space_padding, keys)]

    str = u''
    for (key, value) in zip(key_display_strings, values):
        str += '%s: %s\n' % (key, value)

    return str


def get_list_class_display(value):
    """
    TODO: Go from a list of objects to:
    [class name] len(#)
    """
    if value is None:
        return 'None'
    elif isinstance(value, list):
        # Check for 0 length
        try:
            if len(value) == 0:
                return u'[??] len(0)'
            else:
                return u'[%s] len(%d)' % (
                value[0].__class__.__name__, len(value))
        except:
            import pdb
            pdb.set_trace()
            # run the code
    elif isinstance(value,pd.Series):
        return u'<%s:%s> %s' % ('pandas.Series',value.name,str(value.shape))
    elif isinstance(value,pd.DataFrame):
        return u'<%s> %s' % ('pandas.DataFrame',str(value.shape))
    elif isinstance(value,np.ndarray):
        #TODO: Consider: https://stackoverflow.com/questions/16964467/isinstance-without-importing-candidates
        return u'<numpy %s ndarray> %s' % (value.dtype,str(value.shape))
    #TODO: Support pandas dataframes ...
    else:
        return u'<%s>' % (value.__class__.__name__)


def get_truncated_display_string(input_string: str, max_length: int = 30):
    """

    :param input_string:
    :param max_length:
    :return:
    """
    if input_string is None:
        return 'None'
    elif len(input_string) > max_length:
        return input_string[:max_length] + '...'
    else:
        return input_string

def float_or_none_to_string(x):
    if x is None:
        return 'None'
    else:
        return '%0.2f' % x

def user_name_to_file_name(user_name):
    """
    Provides a standard way of going from a user_name to something that will
    be unique (should be ...) for files

    NOTE: NO extensions are added

    See Also:
    utils.get_save_root
    """

    # Create a valid save name from the user_name (email)
    # ----------------------------------------------------------------------
    # Good enough for now ...
    # Removes periods from email addresses, leaves other characters
    return user_name.replace('.', '')


def get_unnasigned_json(json_data, populated_object):
    """
       Given an object which has had fields assigned to it, as well as the
       JSON dict from which these values were retrieved, this function returns
       a list of keys that were not used for populating the object.

       In order to match the attribute names and dictionary keys must have the
       same names.
    """
    if len(json_data) == 0:
        return {}
    else:
        temp_keys = populated_object.__dict__.keys()
        return dict((key, json_data[key]) for key in set(json_data) if key not in temp_keys)


def assign_json(json_data, field_name, optional=True, default=None):
    """
    This function can be used to make an assignment to an object. Since the
    majority of returned json repsonses contain optional fields.
    """

    if field_name in json_data:
        return json_data[field_name]
    elif optional:
        return default
    else:
        raise Exception("TODO: Fix me")