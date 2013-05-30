#!/bin/bash
# Compile java files with hadoop jar library
# Usage:
# jc.sh src/a.java ...

dir=`basename $1`
dir=${dir%.?*}  #note, in glob, '.' is '.', doesn't represent a single character as in RE

if [ ! -d class/$dir ];then
	mkdir "class/$dir" -p
fi

HADOOP_HOME='/usr/local/hadoop'

files="$@"

javac -classpath ${HADOOP_HOME}/hadoop-core-0.20.2-cdh3u5.jar:${HADOOP_HOME}/lib/commons-cli-1.2.jar:\
${HADOOP_HOME}/lib/commons-lang-2.4.jar:${HADOOP_HOME}/lib/commons-logging-1.0.4.jar \
-d class/$dir $@
#-s ${files// /;}

if [ $? -eq 0 ]; then
	jar -cvf ${dir}.jar -C class/$dir .
fi

