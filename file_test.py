# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:43:00 2019

@author: Pronaya
"""

in_file = open("F:\Work\Educational info\Gottingen\Internet Technologies\ed_2sec1.m4s", "rb") # opening for [r]eading as [b]inary
data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
in_file.close()

"""
out_file = open("out-file", "wb") # open for [w]riting as [b]inary
out_file.write(data)
out_file.close()
"""