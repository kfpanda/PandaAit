#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: path.py
import sys, os

class Path:
	# _init_ 在创建实例时执行。类似java中的构造方法。
	def __init__(self):
		print("");
	def curr_file_path(self):
		##path = os.getcwd();
		path = sys.path[0];
		if(os.path.isdir(path)):
			return path;
		elif( os.path.isfile(path)):
			return os.path.dirname(path);


