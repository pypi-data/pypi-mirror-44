import enum
import re
import inspect
import sys

from textwrap import dedent
from termcolor import cprint, colored

import eosfactory.core.setup as setup

class Verbosity(enum.Enum):
    COMMENT = ['green', None, []]
    INFO = ['blue', None, []]
    TRACE = ['cyan', None, []]
    ERROR = ['red', None, ['reverse']]
    ERROR_TESTING = ['green', None, ['reverse']]
    OUT = [None, None, []]
    DEBUG = ['yellow', None, []]
    NONE = None


__verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
def verbosity(verbosity):
    global __verbosity
    __verbosity = verbosity


def COMMENT(msg):
    frame = inspect.stack()[1][0]
    test_name = inspect.getframeinfo(frame).function
    color = Verbosity.COMMENT.value
    cprint(
        "\n###  " + test_name + ":\n" + condition(msg) + "\n",
        color[0], color[1], attrs=color[2])


def SCENARIO(msg):
    COMMENT(msg)


__trace_buffer = ""
def TRACE(msg=None, verbosity=None, translate=True):
    '''TRACE message logger.

    Print the message, translated is the *translate* flag is set. Store the
    processed message in a buffer. The stored message is returned if the 
    function is called empty.

    Args:
        msg (str): The message to be printed. If not set, return the buffer.
        verbosity ([.core.logger.Verbosity]): The message is printed and 
            buffered if, and only if, its name is in the *verbosity* list.
            If not set, the value set with the function 
            :func:`.core.logger.verbosity` is assumed, or a default value is 
            assumed.
    '''
    if not msg:
        return __trace_buffer

    if msg and Verbosity.TRACE in \
                        (verbosity if not verbosity is None else __verbosity):
        msg = condition(msg, translate)
        __trace_buffer = msg        
        color = Verbosity.TRACE.value
        cprint(msg, color[0], color[1], attrs=color[2])


__info_buffer = ""
def INFO(msg=None, verbosity=None, translate=True):
    '''INFO message logger.

    Print the message, translated is the *translate* flag is set. Store the
    processed message in a buffer. The stored message is returned if the 
    function is called empty.

    Args:
        msg (str): The message to be printed. If not set, return the buffer.
        verbosity ([.core.logger.Verbosity]): The message is printed and 
            buffered if, and only if, its name is in the *verbosity* list.
            If not set, the value set with the function 
            :func:`.core.logger.verbosity` is assumed, or a default value is 
            assumed.
    '''
    global __info_buffer
    if not msg:
        return __info_buffer

    v = verbosity if not verbosity is None else __verbosity
    if msg and (Verbosity.TRACE in v or Verbosity.INFO in v):
        msg = condition(msg, translate)
        __info_buffer = msg        
        color = Verbosity.INFO.value
        cprint(msg, color[0], color[1], attrs=color[2])        


__out_buffer = ""
def OUT(msg=None, verbosity=None, translate=True):
    '''OUT message logger.

    Print the message, translated is the *translate* flag is set. Store the
    processed message in a buffer. The stored message is returned if the 
    function is called empty.

    Args:
        msg (str): The message to be printed. If not set, return the buffer.
        verbosity ([.core.logger.Verbosity]): The message is printed and 
            buffered if, and only if, its name is in the *verbosity* list.
            If not set, the value set with the function 
            :func:`.core.logger.verbosity` is assumed, or a default value is 
            assumed.
    '''
    global __out_buffer
    if not msg:
        return __out_buffer

    if msg and Verbosity.OUT in \
                        (verbosity if not verbosity is None else __verbosity):
        msg = condition(msg, translate)
        __out_buffer = msg
        color = Verbosity.OUT.value
        cprint(msg, color[0], color[1], attrs=color[2])


__debug_buffer = ""
def DEBUG(msg=None, verbosity=None, translate=True):
    '''DEBUG message logger.

    Print the message, translated is the *translate* flag is set. Store the
    processed message in a buffer. The stored message is returned if the 
    function is called empty.

    Args:
        msg (str): The message to be printed. If not set, return the buffer.
        verbosity ([.core.logger.Verbosity]): The message is printed and 
            buffered if, and only if, its name is in the *verbosity* list.
            If not set, the value set with the function 
            :func:`.core.logger.verbosity` is assumed, or a default value is 
            assumed.
    '''
    global __debug_buffer    
    if not msg:
        return __debug_buffer
    
    if msg and Verbosity.DEBUG in \
                        (verbosity if not verbosity is None else __verbosity):
        msg = condition(msg, translate)
        __debug_buffer = msg        
        color = Verbosity.DEBUG.value
        cprint(msg, color[0], color[1], attrs=color[2])


def ERROR(msg, translate=True, raise_exception=False):      
    print(error(msg, translate))


__is_testing_errors = False
def set_is_testing_errors(status=True):
    '''Changes the color of the ``ERROR`` logger printout.

    Makes it less alarming.
    '''
    global _is_testing_errors
    if status:
        __is_testing_errors = True
    else:
        __is_testing_errors = False


def error(msg, translate=True, details=""):
    color = Verbosity.ERROR_TESTING.value \
        if __is_testing_errors else Verbosity.ERROR.value
    return colored(
        "ERROR{}:\n{}".format(details, condition(msg, translate)),  
        color[0], color[1], attrs=color[2])


def condition(message, translate=True):
    import eosfactory.core.manager as manager
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    message = ansi_escape.sub('', message)
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    if translate:
       message = manager.accout_names_2_object_names(message)

    return message
