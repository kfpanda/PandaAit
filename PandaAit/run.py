#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: run.py
import sys, os, time, shutil, optparse, textwrap
import config, path

root_path = path.Path().curr_file_path();
context_param = {
    "def_config_file" : root_path + "/config_file",
    "def_stemp_file" : root_path + "/stemp_file",
    "def_third_lib" : root_path + "/third_lib",
    "def_yaml" : root_path + "/config.yaml",
    "config_file" : root_path + "/config_file/${appname}",
    "stemp_file" : root_path + "/stemp_file/${appname}",
    "third_lib" : root_path + "/third_lib/${appname}",
    "yaml_file" : root_path + "/yaml/${appname}_config.yaml"
}
config_item = [
    "third_lib",
    "file_config",
    "server_test",
    "server_config",
    "war_config"
]

def app_config (options, cfg, appname=None):
    df_cfg = {}; app_cfg = {};
    defualt_config = cfg.has_key("default_config") and cfg["defualt_config"] or {};
    df_cfg["third_lib"] = defualt_config.has_key("third_lib") and defualt_config["third_lib"] or None;
    df_cfg["file_config"] = defualt_config.has_key("file_config") and defualt_config["file_config"] or None;
    df_cfg["server_test"] = defualt_config.has_key("server_test") and defualt_config["server_test"] or None;
    df_cfg["server_config"] = defualt_config.has_key("server_config") and defualt_config["server_config"] or None;
    df_cfg["war_config"] = defualt_config.has_key("war_config") and defualt_config["war_config"] or None;
        
    app_config = cfg.has_key("app_config") and cfg["app_config"] or {};
    app_cfg["third_lib"] = app_config.has_key("third_lib") and app_config["third_lib"] or None;
    app_cfg["file_config"] = app_config.has_key("file_config") and app_config["file_config"] or None;
    app_cfg["server_test"] = app_config.has_key("server_test") and app_config["server_test"] or None;
    app_cfg["server_config"] = app_config.has_key("server_config") and app_config["server_config"] or None;
    app_cfg["war_config"] = app_config.has_key("war_config") and app_config["war_config"] or None;
    
    if not options.all and options.install :
        config.file_install( app_cfg["third_lib"], options.install );
        config.file_install( df_cfg["third_lib"], options.install );
    if not options.all and options.config :
        config.file_config(app_cfg["file_config"], appname);
        config.file_config(df_cfg["file_config"], appname);
    if not options.all and options.test :
        config.server_test(app_cfg["server_test"], options.test);
        config.server_test(df_cfg["server_test"], options.test);
    if not options.all and options.start :
        config.server_restart(app_cfg["server_config"]);
        config.server_restart(df_cfg["server_config"]);
    if not options.all and options.war :
        config.war_config(app_cfg["war_config"], war_name=options.war, war_del=options.delete);
        config.war_config(df_cfg["war_config"], war_name=options.war, war_del=options.delete);
    if options.all :
        config.file_install( app_cfg["third_lib"] );
        config.file_install( df_cfg["third_lib"] );
        config.file_config(app_cfg["file_config"], appname);
        config.file_config(df_cfg["file_config"], appname);
        config.war_config(app_cfg["war_config"], war_del=options.delete);
        config.war_config(df_cfg["war_config"], war_del=options.delete);
        config.server_test(app_cfg["server_test"]);
        config.server_test(df_cfg["server_test"]);
        config.server_restart(app_cfg["server_config"]);
        config.server_restart(df_cfg["server_config"]);

def init_config (appname=None):
    '''config应用初始化参数'''
    config.appname = appname;
    config.root_path = root_path;
    config.config_item = config_item;
    config.put_cxt_param(context_param);
        

def main():
    reload(sys);
    sys.setdefaultencoding('utf8');
    p = optparse.OptionParser(description="PandaAit Version 1.0.0_beta ( 2012 May 11, compiled May 20 2012 09:09:09 )", usage="%prog [-acs] [-i <xyz>] [-t <xyz>] [-w <xyz>] [-p appname]", version="PandaAit 1.0.0_beta");
    p.add_option('--app', '-p', default=None, action="store", metavar="appname", help='应用名，多个用空格分割。例如：--app appname');
    p.add_option('--all', '-a', default=False, action="store_true", help='应用程序安装，配置及服务启动。');
    p.add_option('--install', '-i', default=None, action="append", dest="install", metavar="libname", help='三方包安装。例如：--install libname1 --install libname2 或 --install all  安装所有包。');
    p.add_option('--test', '-t', default=None, action="store", metavar="svrname", help='应用服务测试。例如：--test svrname1 svrname2 或  --test all 执行所有测试。');
    p.add_option('--config', '-c', default=False, action="store_true", help='应用程序配置。');
    p.add_option('--war', '-w', default=None, action="append", dest="war", metavar="warname", help='war应用程序部署。--war warname1 --war warname2  或  --war all 安装所有war包');
    p.add_option('--param', '-m', default=None, action="append", dest="param", metavar="param", help='上下文参数设置，--param param1=value1 --param param2=value2');
    p.add_option('--delete', '-d', default=False, action="store_true", help='在部署war时，是否先删除原来老的war拷贝先war到服务器目录下。');
    p.add_option('--start', '-s', default=False, action="store_true", help='应用程序启动。');

    options, arguments = p.parse_args();
    
    #清空临时目录
    if( os.path.isdir(root_path + "/stemp_file") ):
        shutil.rmtree(root_path + "/stemp_file");
    os.mkdir(root_path + "/stemp_file/");
    
    init_config(options.app);
    
    cfg = config._init_param(options.param);
    app_config(options, cfg, options.app);
        
if  __name__ == "__main__":
    main();








def ttserver_install ():
    ttserver_ip = "127.0.0.1";
    ttserver_port = "11211";
    ttserver_host = ttserver_ip + ":" + ttserver_port;
    '''ttserver 安装'''
    fileOper.fileInstall("tokyocabinet");
    fileOper.fileInstall("tokyotyrant");
    
    if( not os.path.isdir("/ttserver") ):
        os.mkdir("/ttserver");
    if os.path.isfile("/ttserver/ttserver.pid"):
        os.remove("/ttserver/ttserver.pid");
    os.system("ulimit -SHn 51200");
    os.system("pkill -9 ttserver");
    time.sleep(1);
    os.system("ttserver -host " + ttserver_ip + " -port " + ttserver_port + " -thnum 8 -dmn -pid /ttserver/ttserver.pid -log /ttserver/ttserver.log -le -ulog /ttserver/ -ulim 128m -sid 1 -rts /ttserver/ttserver.rts /ttserver/database.tcb#lmemb=1024#nmemb=2048#bnum=10000000");
    time.sleep(3);
    cmmd = os.popen("curl -X PUT http://" + ttserver_host + "/key -d value", "r");
    if(cmmd.read().strip() == "Created") :
        cmmd = os.popen("curl http://" + ttserver_host + "/key", "r");
        if(cmmd.read().strip() == "value"):
            print( "ttserver install success, ttserver is start. (ttserver 服务安装成功，并且正常启动。)" );
        else:
            print( "ttserver error. (ttserver 服务未正常启动或程序安装出错。)" );
    else:
        print( "ttserver error. (ttserver 服务未正常启动或程序安装出错。)" );

