# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 09:12:48 2019

@author: liangh
"""

def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)