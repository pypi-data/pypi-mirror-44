'''
@since: 15 Sep 2015
@author: Girish Kumar <gkumar1@lenovo.com>, Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module provides interactive command class which provides base 
implementation for all command classes 
'''

import sys,getopt,os,json,logging, traceback

from pylxca.pylxca_api import lxca_api
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError
from pylxca.pylxca_cmd import lxca_view

cmd_data_json_file   = "lxca_cmd_data.json"
pylxca_cmd_data   = os.path.join(os.getenv('PYLXCA_CMD_PATH'), cmd_data_json_file)

class InteractiveCommand(object):
    def __init__(self, shell=None ):
        self.shell = shell
        fp = open(pylxca_cmd_data, 'r')
        self.command_data = json.load(fp)

    def get_options(self):
        return {}

    def get_name(self):
        return self.__class__.__name__
    
    def get_char_options(self):
        return self.command_data[self.__class__.__name__][0]
    
    def get_long_options(self):
        return self.command_data[self.__class__.__name__][1]

    def get_short_desc(self):
        return self.command_data[self.__class__.__name__][2]
    
    def invalid_input_err(self):
        self.sprint("Invalid Input ")
        self.sprint("for help type command -h")
        return
    
    def sprint(self,str):
        if self.shell: self.shell.sprint(str)
        
    def parse_args(self, opts, argv):
        opt_dict = {}
        
        for opt, arg in opts:
            opt_dict[opt.strip('-')] = arg
        
        return opt_dict

    def handle_no_input(self,con_obj):
        #no_opt action can differ command to command so override this function if required
        obj = None
        try:
            api = lxca_api()
            obj = api.api(self.get_name(), None,con_obj)
        except ConnectionError:
            self.sprint("Connection is not Initialized, Try connect")
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception as err:
            self.sprint("Exception occurred: %s" %(err)) 
        return obj
    
    def handle_input(self, dict_handler,con_obj = None):
        obj = None
        api = lxca_api()
        obj = api.api(self.get_name(),dict_handler,con_obj)
        return obj
    
    def show_output(self, py_obj,view_filter = "default"):

        ostream = sys.__stdout__
        if self.shell:
            ostream = self.shell.ostream
        view = lxca_view.lxca_view(ostream)
        view.show_output(py_obj,self.get_name(),view_filter)
        return
    
    def handle_output(self, py_obj):
        return
    
    def handle_command(self, opts, args):
        
        con_obj = None
        
        try:
            opts, argv = getopt.getopt(args, self.get_char_options(), self.get_long_options())
        except getopt.GetoptError as e:
            self.invalid_input_err()
            return
        except AttributeError as e:
            extype, ex, tb = sys.exc_info()
            formatted = traceback.format_exception_only(extype, ex)[-1]
            message = "Check getopt short and long options  %s" % (formatted)
            raise RuntimeError(message, tb)

        for opt, arg in opts:
            if '-h' in opt:
                self.sprint(self.__doc__)
                return
            if 'con' in opt:
                con_obj = arg
        
        out_obj = None
        opt_dict = None
        view_filter = "default"
        
        try:
            if not opts:
                out_obj = self.handle_no_input(con_obj)
            else:
                opt_dict = self.parse_args(opts, argv)
                out_obj = self.handle_input(opt_dict,con_obj)
                if opt_dict:
                    view_filter = next((item for item in [opt_dict.get('v') , opt_dict.get('view')] if item is not None),'default')
        
            if out_obj:
                if isinstance(out_obj, dict):
                    self.show_output(out_obj,view_filter)
                else:
                    self.handle_output(out_obj)
        except ConnectionError:
            self.sprint("Connection is not Initialized, Try connect")
        except HTTPError as re:
            self.sprint("Exception %s occurred while executing command."%(re.response.content))
        except ConnectionError as re:
            self.sprint("Exception %s occurred while executing command."%(re.response.content))
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception as err:
            self.sprint("Exception occurred: %s" %(err)) 
            
        return out_obj