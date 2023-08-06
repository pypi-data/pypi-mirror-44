# -*- coding: utf-8 -*-
'''
>>> import os
>>> from art import *
>>> from art.art_param import TEST_FILTERED_FONTS
>>> for i in sorted(TEST_FILTERED_FONTS):
...	    tprint("test",font=i)
ϝԍƨϝ
ɈƨǝɈ
ʇsǝʇ
>>> for i in sorted(TEST_FILTERED_FONTS):
...	    Data = tsave("test@34",font=i,filename=i)
Saved!
Filename: flip.txt
Saved!
Filename: mirror.txt
Saved!
Filename: mirror_flip.txt
>>> os.remove("flip.txt")
>>> os.remove("mirror.txt")
>>> os.remove("mirror_flip.txt")

'''
