#!/usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: fileconfig.py
import os, sys, re, time
import shutil
import fileinstall
from switch import switch
#from file_oper import FileOper

class ContextHolder:
    cxt_param = {};
    def __init__ (self, cxt_param=None):
        self.cxt_param = cxt_param and cxt_param or {};
    
    def addparams (self, dict_param):
        '''添加参数到全局变量中'''
        if( not dict_param ):
            return None;

        for key in dict_param :
            self.cxt_param[key] = dict_param[key];
        
        return None;
    
    def get_cxt_param (self):
        return self.cxt_param;

    def get_value (self, key):
        if( not self.cxt_param or not self.cxt_param.has_key(key) ):
            return None;
        return self.cxt_param[key];

    def paramparse (self, arg0):
        '''解析传入的字符串中的变量'''
        result = arg0;
        if( not self.cxt_param ):
            return result;
        for param in self.cxt_param.keys() :
            result = result.replace("${" + param + "}", self.cxt_param[param]);

        return result;

class FileConfig:
    ''''''
    cxt_holder = ContextHolder();
    
    def set_cxt_holder (self, cxt_holder):
        if(cxt_holder) :
            self.cxt_holder = cxt_holder;
    
    def file_sample_replace(self, file_path, item_param):
        fname = os.path.split(file_path);
        contentList = [];
        f = open(file_path, 'rU');
        for line in f.readlines() :
            #下标移动
            #f.seek(totalNum, 0);
            #totalNum = totalNum + len(line);
            '''过滤掉注释， 以#开头行为注释，去掉空行。'''
            if(line.startswith("#")  or line.strip() == ""):
                contentList.append(line);
                continue;
            line_param = line.split("=");
            if( len(line_param) > 0 ) :
                for itm_key in item_param.keys() :
                    if( itm_key == line_param[0].strip() ):
                        line = itm_key + "=" + str(item_param[itm_key]) + "\r\n";
                        #删除该条目
                        item_param.pop(itm_key);
                        print(line);
                        break;
            contentList.append(line);
        for itm_key in item_param :
            '''添加新配置项。'''
            line = itm_key + "=" + str(item_param[itm_key]) + "\r\n";
            print(line);
            contentList.append(line);
        f.flush();
        f.close();
        #写入文件
        self.file_write(file_path, contentList);
    
    def file_write (self, file_path, arr_line, append=False):
        '''将多行内容写入到文件中。append=True 则在文件末尾追加多行。'''
        if( append ):
            nf = open(file_path, 'ab+');
        else:
            nf = open(file_path, 'wb+');
        nf.writelines(arr_line);
        nf.flush();
        nf.close();
                
    #文件内容替换方法, fileParam total 表示替换的总数, 默认值使用要小心。修改默认值后，下次函数调用将继续保留上次修改的值。
    def file_content_replace(self, file_path, file_item, total=None):
        #fileParam = [ {'key' : 'test', 'value' : 'values', 'total' : '1' } , {'key' : 'test2', 'value' : 'values2', 'total' : '10' } ]
        contentList = [];
        print('file %s replace beginning' %(file_path));
        print("");
        if( file_item.has_key("pos") and file_item["pos"] == "end" ) :
            self.file_write(file_path, file_item["value"], True);
        else:
            f = open(file_path, 'rU');
            for line in f.readlines() :
                '''过滤掉注释， 以#开头行为注释，去掉空行。'''
                if(line.startswith(";") or line.startswith("#")  or line.strip() == ''):
                    contentList.append(line);
                    continue;

                if( line.find(file_item["key"], 0) > -1 ) : 
                    ttl = file_item.has_key("total") and file_item["total"] or total;
                    ct = file_item.has_key("count") and file_item["count"] or 0;
                    if( (not ttl) or ( ttl and ct < ttl ) ) :
                        line = line.replace(file_item["key"], file_item["value"]);
                        file_item["count"] = ct + 1;
                    else:
                        file_item.remove(file_item);                  

                contentList.append(line);

            f.flush();
            f.close();
            self.file_write(file_path, contentList);
        print('file %s replace end' %(file_path));
        print("");
    
    def is_server_run (self, svr_name, svr_list):
        if( not svr_name ):
            return False;
        if(not svr_list or len(svr_list) < 1):
            return True;
        for svr_key in svr_list :
            if( svr_name == svr_key ):
                return True;
        return False;

    def war_config (self, war_config_list, war_name=None, war_del=False):
        '''文件配置模块'''
        curr_dir = os.getcwd();
        if( not war_config_list ):
            return None;

        java_version = fileinstall.java_version();
        if(java_version < "1.6.0") : 
            print("java version(%s) less than 1.6. please install jdk 1.6. \r\n" \
                "java 版本（%s） 小于 1.6 ，请安装 1.6及以上的jdk版本。" %(java_version, java_version));
            return None;
        
        war_name_list = (fileinstall.isnotblank(war_name) and war_name.strip() != "all") and war_name.strip().split(" ") or None;
        
        war_filter_list = {};

        #首先删除老war包，拷贝新war到指定的tomcat目录下。
        for war_key in war_config_list :
            if( not self.is_server_run(war_key, war_name_list) ):
                continue;
            war_item = war_config_list[war_key];
            server_path = war_item.has_key("server_path") and war_item["server_path"] or "";
            if( not os.path.isdir(server_path) ) : 
                print ("warning: server path(%s) is not exist." \
                    "警告：服务器路径（%s） 不存在。" %(server_path, server_path) );
                continue;
            war_filter_list[war_key] = war_item;
            if( war_del ) : 
                server_webapps_path = server_path + "/webapps/";
                if( os.path.isfile(server_webapps_path + war_key + ".war") ):
                    os.remove(server_webapps_path + war_key + ".war");
                if( os.path.isdir(server_webapps_path + war_key) ):
                    shutil.rmtree(server_webapps_path + war_key);
                war_file = self.cxt_holder.get_value("config_file") + "/" + war_key + ".war";
                if( os.path.isfile(war_file) ):
                    shutil.copy(war_file, server_webapps_path);
                else:
                    print("warning: war [%s] is not found.\r\n(" \
                        "警告：war包【%s】无法找到。"  %(war_file, war_file) );
        if( war_del ): 
            #重启tomcat;
            for _name in war_filter_list:
                war_item = war_filter_list[_name];
                server_path = war_item["server_path"];
                fileinstall.tom_reboot(server_path);
            print("==========start sleep 8============");
            time.sleep(8);

        count = 0;
        for war_key in war_filter_list :
            war_item = war_config_list[war_key];
            server_path = war_item["server_path"];
            file_config_list = war_item.has_key("file_config") and war_item["file_config"] or {};
            key_list = fileinstall.order_asc(file_config_list);
            print("-----------------------------------");
            print('%s config start' %(war_key));
            print("-----------------------------------");
            for key in key_list:
                #获取配置文件名
                fc_name = key[0];
                file_item = file_config_list[fc_name];
                c_type = file_item.has_key("type") and file_item["type"] or "modify";
                file_path = file_item.has_key("path") and file_item["path"] or "";
                
                for case in switch(c_type):
                    if case('modify'):
                        self.file_modify(file_item);
                        break;
                    if case('replace'):
                        self.file_replace(file_item, server_path, True);
                        break;
                    if case('command'):
                        self.file_command(file_item);
                        break;
                    if case('config'):
                        #获取文件路径
                        if( not (os.path.isfile(file_path) or os.path.isdir(file_path))):
                            pattern = r"^[\w\W]*" + fc_name + "[\w\W]*$";
                            file_path = fileinstall.path_search_file(pattern, server_path, True, True);
                        file_item["path"] = file_path;
                        print("[ " + fc_name + " ]");
                        print("");
                        self.war_file_config(file_item);
                        break;
                    if case(): 
                        None;
                count = count + 1;
            print("-----------------------------------");
            print('%s config end' %(war_key));
            print("-----------------------------------");
        os.chdir(curr_dir);

        #重启tomcat;
        for _name in war_filter_list:
            war_item = war_filter_list[_name];
            server_path = war_item["server_path"];
            fileinstall.tom_reboot(server_path);

        return count;
    
    def file_config (self, file_config_list, appname=None):
        '''文件配置模块'''
        curr_dir = os.getcwd();
        if( not file_config_list ):
            return None;
        key_list = fileinstall.order_asc(file_config_list);
        count = 0;
        for key in key_list:
            file_item = file_config_list[key[0]];
            c_type = file_item.has_key("type") and file_item["type"] or "modify";
            for case in switch(c_type):
                if case('modify'):
                    self.file_modify(file_item);
                    break;
                if case('replace'):
                    self.file_replace(file_item, self.cxt_holder.get_value("config_file"));
                    break;
                if case('command'):
                    self.file_command(file_item);
                    break;
                if case(): 
                    None;
            count = count + 1;
        os.chdir(curr_dir);
        return count;

    def file_command (self, file_item):
        cmd_list = [];
        if( file_item.has_key("cmd" ) ) :
            cmd_list = file_item["cmd"];
        for command in cmd_list :
            os.system(command);
        else:
            None;
        return None;
    
    def file_modify (self, file_item):
        '''文件修改'''
        for item_key in file_item :
            key_value = len(item_key.strip()) > 4 and item_key.strip()[0:4] or item_key.strip();
            if( key_value == "item" ):
                #获取以item开头的字典，配置项。
                cf_item = file_item[item_key];
                self.item_config(file_item["path"], cf_item);
        return None;
    
    def item_config (self, file_path, file_item):
        c_type = file_item.has_key("type") and file_item["type"] or None;
        for case in switch(c_type):
            if case('replace'):
                self.file_content_replace(file_path, file_item);
                break;
            if case(): 
                None;
        return None;
    
    def file_replace (self, file_item, search_path=None, recursive=False):
        curr_dir = os.getcwd();
        if( not file_item.has_key("path") or not file_item.has_key("replace_path") ):
            return None;
        src_file_path = file_item.has_key("path");
        if( not os.path.isfile(src_file_path) and not os.path.isdir(src_file_path) and search_path ) :
            pattern = r"^[\w\W]*" + src_file_path + "[\w\W]*$";
            src_file_path = fileinstall.path_search_file(pattern, search_path, recursive, True);
        
        replace_path = file_item.has_key("replace_path");
        #如果是文件删除
        if( os.path.isfile(replace_path) ):
            os.remove(replace_path);
        command = "cp -Rf " + src_file_path + "  " + replace_path;
        os.system(command);
        return ;

    def war_file_config(self, file_item):
        if( not file_item or not file_item.has_key("item") ):
            return None;
        item_param = file_item["item"];
        file_path = file_item["path"];
        if( not os.path.isfile(file_path) ):
            print("warning: %s is not exists. \r\n(警告：%s 文件不存在。)"  %(file_path, file_path));
            return None;
        self.file_sample_replace(file_path, item_param);
        
    def file_replace22 (self, file_replace_list):
        curr_dir = os.getcwd();
        def_path = self.cxt_holder.get_value("config_file");
        for key in file_replace_list.keys() :
            file_item = file_config_list[key];
            replace_path = file_item.has_key("replace_path") and file_item["replace_path"] or "";
            if( os.path.isfile(replace_path) ) :
                src_file_path = file_item.has_key("path") and file_item["path"] or None;
                if( (not src_file_path) and file_item.has_key("name") ):
                    src_file_path = def_path + "/" + file_item["name"];
                
                if( os.path.isfile(src_file_path) ) :
                    os.remove(replace_path);
                    os.system("cp " + src_file_path + "  " + replace_path);
            elif( os.path.isdir(replace_path) ) :
                src_file_path = file_item.has_key("path") and file_item["path"] or None;
                if( (not src_file_path) and file_item.has_key("name") ):
                    src_file_path = def_path + "/" + file_item["name"];
                if( (not os.path.isdir(src_file_path)) and (not os.path.isfile(src_file_path)) ) :
                    continue;
                if( file_item.has_key("cover") and file_item["cover"] == "delete" ):
                    if( file_item.has_key("name") ):
                        r_path = replace_path + "/" + file_item["name"];
                        os.system("rm -rf " + r_path.replace("//", "/") );
                        os.system("cp -R " + src_file_path + "  " + replace_path);
                else:
                    os.system("cp -Rf " + src_file_path + "  " + replace_path);
        return None;

if __name__ == '__main__':
    None;    
    
