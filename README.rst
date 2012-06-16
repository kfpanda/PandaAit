[PandaAit] 版本 1.0.0_beta
作者:	liuhualuo
日期:	2012/05/10
描述：
    PandaAit(Panda Application Installation Tool) 是一个应用流程化安装工具。它能够将一个应用的安装，给以流程化的形式描述出来，
从而达到流程化安装应用的效果。只要第一次描述好流程，以后的安装将会变得非常简单。

文档：
    相关文档在docs 目录下。
    快速开始，可以看tutorial.rst 文件。

版本要求：
    1.Python 2.7
    2.pyyaml

English

[PandaAit] version 1.0.0_beta
author：liuhualuo
date：  2012/05/10

PandaAit ( Panda Application Installation Tool ) is an application of the process of the installation tool. 
It can be an application installation, to describe the process of To achieve the process of installing the application effect. 
As long as the first description of the flow, the installation will become very simple.

Documentation：
    Relevant documents in the "docs" directory.
    Quick start, can read "tutorial.rst" files.

Requirements：
    1.Python 2.7
    2.pyyaml























应用流程化安装工具使用帮助：

执行命令： ./run.py --help

Usage: run.py [-acs] [-i <xyz>] [-t <xyz>] [-w <xyz>] [-p appname]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p appname, --app=appname
                        应用名，多个用空格分割。例如：--app
                        appname
  -a, --all             应用程序安装，配置及服务启动。
  -i libname, --install=libname
                        三方包安装。例如：--install libname1 libname2
                        或 --install all  安装所有包。
  -t svrname, --test=svrname
                        应用服务测试。例如：--test svrname1 svrname2
                        或  --test all 执行所有测试。
  -c, --config          应用程序配置。
  -w warname, --war=warname
                        war应用程序部署。--war warname1 warname2  或
                        --war all 安装所有war包
  -d, --delete          在部署war时，是否先删除原来老的war拷贝
                        先war到服务器目录下。
  -s, --start           应用程序启动。


实例：
安装linux  ntp服务：
使用命令：./run.py -a -p ntp
安装 hexin 主站应用：
使用命令：./run.py -a -p hexincs

注意：
1.在python不是2.7及以上版本时，需要先执行命令：./installpython.py 来更新python版本到2.7版本。


yaml配置文件规则：

一个yaml配置文件分为5个模块（随着功能的完善模块将会相应增加），分别为：
1.全局参数定义选项：
    字典格式：
        context_param :                             #如果定义全局参数，则在上下文中可以是用${ttserver_ip}来引用参数。
            ttserver_ip : 127.0.0.1

2.三方包安装选项：
    字典格式：
        third_lib : 
            libevent : 
                name : libevent-1.4.9                     #libevent 名称，在搜索路径时有用。
                path :                                    #如果path未定义或为空，则在third_lib目录下，根据name来模糊查找相应的压缩包。
                unzip_dir :                               #将压缩包解压到指定路径。如加上${del_root}，则解压后将删除根级目录。
                order : 1                                 #定义三方包安装顺序
                after_cmd :                               #after_cmd 是在三方包解压后执行的命令，对应的有before_cmd是在三方包解压前执行。
                    cmd : [                               #命令是按数组顺序执行。
                        './configure --prefix=/usr/local/libevent',
                        'make & make install',
                        'ln -s /usr/lib/libevent-1.4.so.2 /usr/local/libevent/lib/libevent-1.4.so.2'
                    ]
3.文件配置选项：
    file_config : 
    php.ini : 
        path : /usr/local/php/etc/php.ini
        order : 1
        type : modify, replace, copy, command
        item1 : 
            type : replace
            key : extension_dir = "./"
            value : extension_dir = "/usr/local/php/lib/php/extensions/no-debug-non-zts-20060613/" \nextension = "memcache.so"
            total : 1
        item2 : 
            type : replace
            key : magic_quotes_gpc = On
            value : magic_quotes_gpc = Off
            total : 1

4.服务测试选项：
    server_test : 
        ttserver :                                      #配置需要测试的服务名，在字典中不能重复服务名。
            - command : 
                cmd : curl -X PUT http://${ttserver_ip}:${ttserver_port}/key -d value       #配置测试命令。
                success :                                #测试命令结果预定义，执行完测试命令后将会判断结构是否符合预定义值。符合则测试成功，否则失败。
            - command : 
                cmd : curl http://${ttserver_ip}:${ttserver_port}/key
                success : value

5.服务启动选项：
    server_config :                                     #服务器启动配置项
        memcached :                                     #需要启动的服务。
            before_cmd :                                #在command命令之前执行的批量命令。对应的有after_cmd。
                cmd :                                   #批量shell命令配置。
                    - pkill -9 memcached
                    - rm -f /tmp/memcached.pid
                sleep : 1                               #在批量命令执行完后的睡眠时间。以秒为单位。
            command : /usr/local/memcached/bin/memcached -d -m 1024 -u root -l 127.0.0.1 -p 11211 -c 256 -P /tmp/memcached.pid

6.java web应用程序部署：
    war_config : 
        daq : 
        server_path : /usr/local/tomcat_daq
        file_config : 
            file.properties : 
                path :                                  #指定file.properties文件路径，如果不指定，程序将查找server_path目录下该配置文件。
                                                        #注意：（如果server_path目录下存在多个文件名相同的该配置文件,则将可能导致配置文件修改出错问题。）
                type : config                           #文件配置类型，目前支持config, modify, replace, command
                item :                                  #需要修改的文件配置项。
                    tomcat.webapps.dir : /usr/local/tomcat-file/webapps
                    annexfile.relativedir : /attachFiles/annex
                    #行业新闻生成文件保存路径  已经无效
                    #hexincs.path : /hxdata/hqserver/text/
                    #swftool 配置
                    swftoolsPath : /usr/local/tomcat3/webapps/swftools/bin/pdf2swf
                    xpdfLanguageDir : /usr/local/tomcat3/webapps/swftools/share/xpdf/chinese-simplified
                    #pdf 文件是否删除
                    srcPdfDelete : true
            jdbc.properties : 
                path : 
                type : config
                item : 
                    #hibernate 打印出sql 生产环境 需要设置为false
                    hibernate.show_sql : true
                    hibernate.format_sql : false
                    
                    #资讯库
                    jdbc.connection.infos.url : jdbc:oracle:thin:@10.1.130.47:1521:zxinfo
                    jdbc.connection.infos.username : csp_infos
                    jdbc.connection.infos.password : csp_infos
                    jdbc.connection.users.url : jdbc:oracle:thin:@10.1.130.47:1521:zxinfo
                    jdbc.connection.users.username : csp_users
                    jdbc.connection.users.password : csp_users


数据采集程序：

脚本安装的三方包有：
1.python 2.7.2
2.dbwgc-libatomic
3.pymongo-2.11
4.web.py-0.36
5.uwsgi-1.0.4
6.mongodb-2.1
7.nginx-1.1.16
    nginx引入的组件有：nginx-gridfs-v0.8-11 和 pcre-8.30.

所以需要将上述版本的包加入到 thirdlib目录下（脚本发布默认已经存在）。

数据采集程序部署，只需要运行./config.py  --install 。
如果脚本运行没有权限，请先执行chmod -R uog+x ./*。

程序部署，默认设置：
默认mongodb 服务开启, 默认端口为 127.0.0.1:27017。
默认开启uwsgi 服务端口为 127.0.0.1:3031。
默认开启nginx 服务端口为 127.0.0.1:80 。