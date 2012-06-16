#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: yamlparse.py
import sys, os, time
import yaml

config_file = "";

class YamlParseError (Exception):
    def __init__(self, msg):
        self.msg = msg;

    def __str__(self):
        return self.msg;

class YamlParse :
    '''detail'''
    yaml_file = "config.yaml";
    yml = None;
    def __init__(self, yaml_file) :
        self.yaml_file = yaml_file;
    
    def _set_yaml_file (self, yaml_file):
        self.yaml_file = yaml_file;

    def load (self, yaml_file = None):
        '''获取一个yaml对象，如果yaml_file为None，
        则返回对象的yml属性（来自self.yaml_file配置文件）'''
        if( yaml_file and os.path.isfile(yaml_file) ) :
            f = open(yaml_file);
            return yaml.load(f);
        else:
            if( not self.yml ) :
                f = open(self.yaml_file);
                self.yml = yaml.load(f);
            return self.yml;
    
    def get_items (self, item_name, yaml_file=None, cxt_param=None):
        '''返回值，如果不存在item，则返回None'''
        y = self.load(yaml_file);
        result = y.has_key(item_name) and y[item_name] or None;
        if( result and cxt_param ):
            result = str(result);
            for key in cxt_param.keys() :
                result = result.replace("${" + key + "}", str(cxt_param[key]) );
                
            result = eval(result);
        
        return result;
        
    def destroy(self):
        """see YamlParse.destroy()."""
        print("destroy");