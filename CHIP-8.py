#coding:utf-8

#import Display as display

import core as Co

coreprocess = Co.CPU("rom/IBM.ch8", "font/chip48font.txt")

coreprocess.load_font()
coreprocess.load_rom()

coreprocess.decode()
coreprocess.pipeline()