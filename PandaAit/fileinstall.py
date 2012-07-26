#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: fileinstall.py
import os, sys, re, time
import zipfile, tarfile, gzip, subprocess
from switch import switch

#通过正则表达式，递归搜索文件函数  recursive是否递归搜索目录。
def search_file(pattern, dirPath, recursive=False, fileAndDir=False):  
    file_list = [];
    if os.path.isdir(dirPath): 
        fnlist = os.listdir(dirPath);
        for fname in fnlist :
            fpath = dirPath + "/" + fname;
            if(os.path.isdir(fpath)):
                '''目录也查询'''
                if(fileAndDir) :
                    m = re.match(pattern, fname );
                    if m and m .group():
                        file_list.append(fpath);
                if(recursive) :
                    file_list.extend( search_file(pattern, fpath, recursive, fileAndDir) );
            else:
                '''非目录文件查询形式'''
                m = re.match(pattern, fname );
                if m and m .group():
                    file_list.append(fpath);
        
        return file_list;
    else:
        print("warning: %s is not exists. \r\n(警告：%s 目录路径不存在。)"  %(dirPath, dirPath));

def path_search_file (pattern, dirPath, recursive=False, fileAndDir=False):
    result_path = "";
    file_list = search_file(pattern, dirPath, recursive, fileAndDir);
    if( len(file_list) > 0 ):
        for path in file_list :
            if( "/" != path ):
                result_path = path;
                break;
    return result_path;

def tom_reboot(tom_path):
    curr_dir = os.getcwd();
    os.system(curr_dir + "/shell/tom_reboot.sh " + tom_path);
    
def java_version():
    version = None;
    #ret = os.popen("java -showversion").readline();#("java --version 2>&1 | awk '/java version/{print $3}'");
    cp = subprocess.Popen('java -version',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
    ret=cp.stderr.readline();
    ptn = re.compile(r'\"\d.\d.[\d_]+\"');
    m = ptn.search(ret);
    if(m and m.group()):
        version = m.group();
        version = version.replace('"',"");
    return version;

def order_asc (item_list, order='order'):
    result = {};
    for key in item_list.keys():
        dct = item_list[key];
        value = dct.has_key(order) and dct[order] or 10000;
        result[key] = value;
    itms = result.items();
    itms.sort(key=lambda x:x[1]);
    return itms;

def cmd_exec (cmd_lib):
    if( not cmd_lib ):
        return None;
    cmd_list = cmd_lib.has_key("cmd") and cmd_lib["cmd"] or [];
    for _cmd in cmd_list :
        os.system(_cmd);
    if( cmd_lib.has_key("sleep") ):
        time.sleep(cmd_lib["sleep"]);
    return None;

def isblank (arg0=None):
    if(not arg0 or arg0.isspace()) :
        return True;
    return False;

def isnotblank (arg0=None):
    if( isblank(arg0) ):
        return False;
    else:
        return True;
    
class FileZip:
    #['rar','zip','7z','ace','arj','bz2','cab','gz','iso','jar','lzh','tar','uue','z'];
    file_format = { 'zip' : 'zip', 
                'bz2' : 'tar', 'gz' : 'tar', 'tgz' : 'tar', 'tar' : 'tar',
                'gzip' : 'gzip' };

    unzip_path = None;#文件解压缩目录

    def __init__ (self, unzip_path=None):
        self.unzip_path = unzip_path;

    def untar (self, file_path, untar_path, root_del=False):
        result_path = None;
        tar = tarfile.open(file_path, "r");
        root_dir = tar.getnames()[0];
        if( root_dir.find("/") > 0 ) :
            idx = root_dir.find("/");
            root_dir = root_dir[0:idx];
        for tarinfo in tar :
            if root_del :
                #移除根目录
                fl_path = tarinfo.name.replace(root_dir + "/", "");
                if(fl_path.strip() == "") :
                    continue;
                tar._extract_member(tarinfo, os.path.join(untar_path, fl_path));
            else:
                tar.extract(tarinfo.name, untar_path);
        tar.close();
        result_path = root_del and untar_path or (untar_path + "/" + root_dir);
        result_path = result_path.replace("//", "/");
        return result_path;

    def unzip (self, file_path, unzip_path, root_del=False):
        result_path = None;
        zip_obj = zipfile.ZipFile(file_path, 'r');
        root_dir = zip_obj.namelist()[0].strip("/");
        if( root_dir.find("/") > 0 ) :
            idx = root_dir.find("/");
            root_dir = root_dir[0:idx];
        if(root_del):
            for f_info in zip_obj.infolist() :
                fl_path = f_info.filename.replace(root_dir + "/", "");
                fl_path = os.path.join(unzip_path, fl_path);
                if( f_info.compress_type > 0 ):
                    dir_path = os.path.dirname(fl_path);
                    if( not os.path.isdir(dir_path) ):
                        os.makedirs(dir_path);
                    try:
                        ff = open(fl_path, 'a');
                        ff.writelines(zip_obj.open(f_info.filename));
                    finally:
                        ff.close();
        else:
            zip_obj.extractall(unzip_path, zip_obj.namelist());
        result_path = root_del and unzip_path or (unzip_path + "/" + root_dir);
        result_path = result_path.replace("//", "/");
        return result_path;

    def zip_file (self, file_path, unzip_path=None, root_del=False):
        result_path = None;
        if( unzip_path and (not os.path.isdir(unzip_path)) ) :
            os.makedirs(unzip_path);
        un_path = unzip_path and unzip_path or self.unzip_path;
        if( not os.path.isfile(file_path) ):
            print("warning: %s is not exists. （警告：%s 文件不存在 ）" %(file_path, file_path) );
            return result_path;
        suffix = os.path.splitext(file_path)[1][1:];
        if( not self.file_format.has_key(suffix) ):
            print("warning: %s  the type is not unzip. （警告：%s 不支持此后缀名的文件解压）" %(suffix, suffix) );
            return result_path;
        file_type = self.file_format[suffix];

        for case in switch(file_type):
            if case('zip'):
                result_path = self.unzip(file_path, un_path, root_del);
                break;
            if case('tar'):
                result_path = self.untar(file_path, un_path, root_del);
                break;
            if case('gzip'):
                '''file = gzip.GzipFile(file_path, "r");
                outFile = open(un_path ,"w");
                outFile.write(file.read());
                outFile.close();'''
                break;
            if case(): 
                print( "something else!" );

        return result_path;

class FileInstall:
    '''应用程序安装'''
    appname = None;
    cxt_holder = None;

    def __init__(self, appname=None, cxt_holder=None):
        self.appname = appname;
        self.cxt_holder = cxt_holder;
    
    def set_appname (self, appname):
        self.appname = appname;
    def set_cxt_holder (self, cxt_holder):
        self.cxt_holder = cxt_holder;

    def all_lib_install (self, lib_list, lib_name_list=None):
        currDir = os.getcwd();
        key_list = order_asc(lib_list);
        count = 0;
        
        if( lib_name_list ):
            for libname in lib_name_list:
                if( libname and libname == "all" ):
                    #如果包含all的话将安装所有包
                    lib_name_list = None;
                    break;
        #lib_name_list = (isnotblank(lib_name) and lib_name.strip() != "all") and lib_name.strip().split(" ") or None;

        for key in key_list:
            lname = key[0];
            if( not self.is_server_run(lname, lib_name_list) ):
                continue;
            lib_item = lib_list[lname];
            self.lib_install(lib_item);
            count = count + 1;
        os.chdir(currDir);
        return count;
    
    def lib_install (self, lib_item):
        '''三方包安装'''
        curr_dir = os.getcwd();
        #解压文件
        unzip_dir = lib_item.has_key("unzip_dir") and lib_item["unzip_dir"] or self.cxt_holder.get_value("stemp_file");
        root_del = unzip_dir.find("${root_del}") > 0 and True or False;
        unzip_dir = unzip_dir.replace("${root_del}","");
        file_zip = FileZip();
        
        #获取包路径
        if( (not lib_item.has_key("path")) or isblank(lib_item["path"]) ):
            file_name = lib_item["name"];
            pattern = r"^[\w\W]*" + file_name + "[\w\W]*$";
            third_lib_path = self.cxt_holder.get_value("third_lib");
            #third_lib_path = third_lib_path.replace("//", "/");#去掉多余的斜杠.
            lib_item["path"] = path_search_file(pattern, third_lib_path);
        
        print( "------------------------------------------------------------------------");
        print( "------------  " + lib_item["name"] + "  start install  ------------"); 
        print( "------------------------------------------------------------------------");

        if( lib_item.has_key("before_cmd") ):
            cmd_exec(lib_item["before_cmd"]);

        unzip_path = file_zip.zip_file(lib_item["path"], unzip_dir, root_del);
        os.chdir(unzip_path);

        if( lib_item.has_key("after_cmd") ):
            cmd_exec(lib_item["after_cmd"]);
        #返回根目录
        os.chdir(curr_dir);
        return None;

    def is_server_run (self, svr_name, svr_list):
        if( not svr_name ):
            return False;
        if(not svr_list or len(svr_list) < 1):
            return True;
        for svr_key in svr_list :
            if( svr_name == svr_key ):
                return True;
        return False;
    
    def server_test (self, server_list, server_name=None):
        '''服务测试'''
        if( not server_list ):
            return None;
        
        svr_name_list = (isnotblank(server_name) and server_name.strip() != "all") and server_name.strip().split(" ") or None;
        
        for svr_key in server_list :
            if( not self.is_server_run(svr_key, svr_name_list) ):
                continue;
            error_flag = False;
            svr_item = server_list[svr_key];
            for itm in svr_item :
                cmd_item = itm["command"];
                cmmd = os.popen( cmd_item["cmd"] );
                end_info = cmmd.read();
                if( cmd_item.has_key("success") and isnotblank(cmd_item["success"]) ):
                    succ = cmd_item["success"];
                    if( end_info and (end_info.find(succ) > -1) ):
                        print( "( " + cmd_item["cmd"] + " ) command execute success.");
                    else : 
                        error_flag = True;
                        print( "( " + cmd_item["cmd"] + " ) command execute error.");
                else:
                    print("( " + cmd_item["cmd"] + " ) execute result : " + end_info);
            if( error_flag ):
                print("---------------- " + svr_key + " test error. ----------------");
            else :
                print("---------------- " + svr_key + " test success. ----------------");
        
        return None;

    def server_restart (self, server_config):
        '''服务重启'''
        if( not server_config ):
            return None;
        
        for svr_item in server_config :
            svr = server_config[svr_item];
            
            if( svr.has_key("before_cmd") ):
                cmd_exec(svr["before_cmd"]);
            
            commd = svr.has_key("command") and svr["command"] or "";
            os.system(commd);

            if( svr.has_key("after_cmd") ):
                cmd_exec(svr["after_cmd"]);
            
            print(svr_item + " restart success.");
            
        return None;

if  __name__ == "__main__":
    fz = FileZip("/home/app/stemp/");
    print( fz.zip_file(sys.argv[1],'d:/tttt', root_del=True) );