#!/bin/bash

. /etc/profile
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi
if [ -f ~/.bash_profile ]; then
	. ~/.bash_profile
fi

TOMCATPATH=$1

echo "==========tomcat reboot start============"

pid=`ps aux | grep tomcat | grep $TOMCATPATH/bin | grep -v grep | awk '{print $2}'`
echo $pid
if [ -n "$pid" ]; then
    echo "==========start sleep 2s============"
    sleep 2
	echo "==========stop tomcat============"
	${TOMCATPATH}/bin/shutdown.sh

    echo "==========start sleep 4s============"
	sleep 4

	pid=`ps aux | grep tomcat | grep $TOMCATPATH/bin | grep -v grep | awk '{print $2}'`
	if [ -n "$pid" ]; then
		echo "======to kill the tomcat pid $pid========"
		kill -9 $pid
        sleep 1
	fi

	echo "==========start tomcat again============"
	${TOMCATPATH}/bin/startup.sh

else
	echo "===============start tomcat============="
	${TOMCATPATH}/bin/startup.sh
fi

echo "==========start sleep 2s============"
sleep 2

exit
