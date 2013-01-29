#! /usr/bin/python 
#_*_ coding:UTF-8 _*_ 
#Filename: installpython.py 
import sys, os, time, optparse
from path import Path
from fileconfig import ContextHolder
from fileinstall import FileInstall

f_install = FileInstall();
cxt_holder = ContextHolder();
root_path = Path().curr_file_path();

context_param = {
    "def_config_file" : root_path + "/config_file",
    "def_stemp_file" : root_path + "/stemp_file",
    "def_third_lib" : root_path + "/third_lib",
    "config_file" : root_path + "/config_file/python",
    "stemp_file" : root_path + "/stemp_file/python",
    "third_lib" : root_path + "/third_lib/python",
}

third_lib = {
    "python" : {
        'name' : 'Python',
        'path' : '',
        'order' : '1',
        'after_cmd' :{
            'cmd' : [
                './configure',
                'make',
                'make install',
                "rm -rf /usr/bin/python",
                "ln /usr/local/bin/python2.7 /usr/bin/python"
            ]
        }
    },
    "pyyaml" : {
        'name' : 'PyYAML',
        'path' : '',
        'order' : '10',
        'after_cmd' : {
            'cmd' : [
                'python setup.py build',
                'python setup.py install'
            ]
        }

    }
}

def init ():
    cxt_holder.addparams(context_param);
    f_install.set_cxt_holder(cxt_holder);

def help ():
    reload(sys);
    sys.setdefaultencoding('utf8');
    p = optparse.OptionParser(usage="%prog [-i]", version="PandaAit 1.0.0_beta");
    p.add_option('--all', '-a', default=None, action="store_true", metavar="", help='python 2.7.2版本及pyyaml组件安装。');
    p.add_option('--yaml', '-y', default=None, action="store_true", metavar="", help='安装python 2.7.2版本的pyyaml组件。');
    
    options, arguments = p.parse_args();

    return options;

def main ():
    options = help();
    init();
    f_install.set_appname("python");
    if( options.all ):
        f_install.all_lib_install(third_lib);
    if( options.yaml ):
        #删除python安装项
        third_lib.pop("python");
        f_install.all_lib_install(third_lib);

if  __name__ == "__main__":
    main();
