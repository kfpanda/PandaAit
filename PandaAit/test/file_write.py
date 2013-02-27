#! /usr/bin/python 
#_*_ coding:UTF-8 _*_
#Filename: file_write.py
import sys, os, time, shutil, optparse, textwrap

def file_write (file_path, arr_line, append=False):
    '''将多行内容写入到文件中。append=True 则在文件末尾追加多行。'''
    if( append ):
        nf = open(file_path, 'ab+');
    else:
        nf = open(file_path, 'wb+');
    nf.writelines(arr_line);
    nf.flush();
    nf.close();
        

def main():
    arr_line = ["sdsdd\r\nsdfsf\n","ssdfsf\nsgdsfsf"];
    file_path = "/tmp/test.txt";
    arr_line[0] = arr_line[0].replace("sds", "aaaa");
    file_write(file_path, arr_line);
        
if  __name__ == "__main__":
    main();

