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























PandaAit 快速开始

首先需要 安装python 2.7 和 pyyaml 支持。
可以执行：
./installpython.py -i

执行完后，程序将会自动更改python版本到2.7。

然后下载需要安装的应用包。
例如：AitApp 中的 java应用。
将应用放入到PandaAit指定目录中。
或者执行命令：
./install.py -p ${PandaAit Path}

程序会自动将应用中的文件放入到PandaAit目录相对应的目录。
例如：java/third_lib  下的三方包  放入到 PandaAit/third_lib 目录下
java/yaml 下的配置文件  放入到 PandaAit/yaml 目录下
java/config_file 下的配置文件 放入到 PandaAit/config_file 目录下

注意：
应用配置文件和引用的三方包，也可以手工添加。可参照手工添加应用配置文件说明。

最后 可以执行命令：
./run.py -a -p java

来安装相应的应用。


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



手工添加 配置文件说明：
目录规范：
    yaml目录 存放yaml配置文件目录。
    名称规则：应用名 + "_config.yaml"。

    third_lib目录 存放应用安装有关的包。
    添加时需要 建一个 以 ${app_name} 为名称的目录。 在该目录下放所有需要应用到的包。
    注意：
        目前应用压缩包格式只支持：zip, tgz, tar, gz。 不支持rar格式的压缩包。

    config_file目录 存放应用安装 所需要的配置文件。
        添加时需要 建一个 以 ${app_name} 为名称的目录。 在该目录下放所有需要应用到的配置文件。

yaml配置规范：

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
        #type = modify, replace, copy, command
        type : modify
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
        item3 : 
            type : replace
            #在文件结尾加 一行 value
            pos : end
            value : magic_quotes_gpc = Off
    nginx.conf : 
        # path 路径 如果不是全路径，则将会从config_file 路径下查找。
        path : nginx.conf
        desc_path : /usr/local/nginx/conf/nginx.conf
        type : replace
        order : 1
    fastdfs_cmmd : 
        type : command
        order : 10
        cmd : [
            "mkdir /home/fastdfs",
            ""
        ]

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
            order : 1                                   #启动顺序
            before_cmd :                                #在command命令之前执行的批量命令。对应的有after_cmd。
                cmd :                                   #批量shell命令配置。
                    - pkill -9 memcached
                    - rm -f /tmp/memcached.pid
                sleep : 1                               #在批量命令执行完后的睡眠时间。以秒为单位。
            command : /usr/local/memcached/bin/memcached -d -m 1024 -u root -l 127.0.0.1 -p 11211 -c 256 -P /tmp/memcached.pid

6.java web应用程序部署：
    war_config : 
        my_app : 
        server_path : /usr/local/tomcat
        file_config : 
            file.properties : 
                path :                                  #指定file.properties文件路径，如果不指定，程序将查找server_path目录下该配置文件。
                                                        #注意：（如果server_path目录下存在多个文件名相同的该配置文件,则将可能导致配置文件修改出错问题。）
                type : config                           #文件配置类型，目前支持config, modify, replace, command
                item :                                  #需要修改的文件配置项。
                    tomcat.webapps.dir : /usr/local/tomcat-file/webapps
                    annexfile.relativedir : /attachFiles/annex
                    #pdf 文件是否删除
                    srcPdfDelete : true
            jdbc.properties : 
                path : 
                type : config
                item : 
                    #hibernate 打印出sql 生产环境 需要设置为false
                    hibernate.show_sql : true
                    hibernate.format_sql : false
                    #数据库
                    jdbc.connection.infos.url : jdbc:oracle:thin:@{ip:port}:sid
                    jdbc.connection.infos.username : {name}
                    jdbc.connection.infos.password : {password}


