# -*- coding: utf-8 -*-
"""
Client Auto Script
Created on Wed Jan  2 01:00:24 2019

@author: Pronaya
"""

import h2client2 as client
import _thread as thread
import time
import sys
import os
import subprocess
import signal

#output_stop = subprocess.check_output('docker stop '+containerName, shell=True)
#output_stop = output_stop.decode("utf-8")

PUSH = 3
RTT = 0
#cmdStr =  
# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups 








