#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: conifg.py
import sys, os, time, optparse, textwrap
import fileinstall, fileconfig
from yamlparse import YamlParse

root_path = None;
appname = None;
config_item = [];
cxt_holder = fileconfig.ContextHolder();
f_install = fileinstall.FileInstall();

def put_cxt_param (cxt_param):
    '''将系统全局参数放入上下文。'''
    app_param = (appname and appname.strip() != '') and appname or '';
    for key in cxt_param :
        cxt_param[key] = cxt_param[key].replace('${appname}', app_param);

    cxt_holder.addparams(cxt_param);

def _init_defualt_param ():
    '''获取默认的配置文件中，对应应用appname的配置项'''
    def_yaml_path = cxt_holder.get_value("def_yaml");
    if( (not appname) or (appname.strip() == '') or (not os.path.isfile(def_yaml_path)) ):
        return None;

    yp = YamlParse(def_yaml_path);
    param_list = yp.get_items(appname + "_context_param");
    cxt_holder.addparams(param_list);
    default_config = {};
    for itm in config_item :
        default_config[itm] = yp.get_items(appname + "_" + itm, cxt_param=cxt_holder.get_cxt_param());
        default_config[itm] = yp.get_items(appname + "_" + itm, cxt_param=cxt_holder.get_cxt_param());
    
    return default_config;

def _init_param ():
    '''获取appname的配置文件中的配置项'''
    cfg = {};
    cfg["defualt_config"] = _init_defualt_param();
    #如果appname为空，则使用默认的配置文件，否则使用对应项目配置文件。
    yaml_path = (not appname or appname.strip() == '') and cxt_holder.get_value("def_yaml") or cxt_holder.get_value("yaml_file");
    if( not os.path.isfile(yaml_path) ):
        return None;
    yp = YamlParse(yaml_path);
    param_list = yp.get_items("context_param");
    cxt_holder.addparams(param_list);
    app_config = {};
    for itm in config_item :
        app_config[itm] = yp.get_items(itm, cxt_param=cxt_holder.get_cxt_param());
        app_config[itm] = yp.get_items(itm, cxt_param=cxt_holder.get_cxt_param());
    cfg["app_config"] = app_config;
    
    #传参
    f_install.set_appname(appname);
    f_install.set_cxt_holder(cxt_holder);
    return cfg;

def file_install (third_lib, lib_name=None):
    os.chdir(root_path);
    if( not third_lib ):
        return None;
    f_install.all_lib_install(third_lib, lib_name);

def file_config (file_config_list, appname=None):
    os.chdir(root_path);
    #php 配置
    if( not file_config_list ):
        return None;
    fileconf = fileconfig.FileConfig();
    fileconf.set_cxt_holder(cxt_holder);
    fileconf.file_config(file_config_list, appname);

def war_config (war_config_list, war_name=None, war_del=False):
    os.chdir(root_path);
    #php 配置
    if( not war_config_list ):
        return None;
    fileconf = fileconfig.FileConfig();
    fileconf.set_cxt_holder(cxt_holder);
    fileconf.war_config(war_config_list, war_name, war_del);

def server_test (server_list, server_name=None):
    os.chdir(root_path);
    
    f_install.server_test(server_list, server_name);

def server_restart (server_config):
    os.chdir(root_path);
    f_install.set_cxt_holder(cxt_holder);
    f_install.server_restart(server_config);
        
if  __name__ == "__main__":
    None;
