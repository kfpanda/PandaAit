#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: install.py
import sys, os, shutil, optparse

ait_path = None;

dir_item = [
    "third_lib",
    "config_file",
    "yaml"
]

def curr_file_path():
    path = sys.path[0];
    if(os.path.isdir(path)):
        return path;
    elif( os.path.isfile(path)):
        return os.path.dirname(path);

curr_path = curr_file_path();

def help ():
    reload(sys);
    sys.setdefaultencoding('utf8');
    p = optparse.OptionParser(usage="%prog [-d path]", version="PandaAit 1.0.0_beta");
    p.add_option('--dir', '-d', default=None, action="store", metavar="path", help=" 1.0.指定PandaAit主程序路径。如果不指定路径，默认路径为同级目录。");
    
    options, arguments = p.parse_args();
    return options;

def main():
    options = help();
    #获取PandaAit 主程序目录路径。
    if( options.dir ):
        ait_path = options.dir;
    else:
        ait_path = os.path.split(curr_path)[0];
        ait_path = ait_path + "/PandaAit";
    
    if( not os.path.isdir(ait_path) ):
        print("warning: %s is not exists. \r\n（警告：%s PandaAit主目录路径不存在，请重新指定 -d path。 ）" %(ait_path, ait_path) );
        return ;
    #拷贝各个目录到主程序的对应目录下。
    for itm in dir_item :
        src_dir = os.path.join(curr_path, itm);
        dst_dir = os.path.join(ait_path, itm);
        if( os.path.isdir( src_dir ) ):
            for f_name in os.listdir( src_dir ):
                src = os.path.join(src_dir, f_name);
                dst = os.path.join(dst_dir, f_name);
                if( not os.path.isfile(dst) and not os.path.isdir(dst) ):
                    if( os.path.isfile(src) ):
                        shutil.copyfile(src, dst);
                    else:
                        shutil.copytree(src, dst);
    
if  __name__ == "__main__":
    main();

