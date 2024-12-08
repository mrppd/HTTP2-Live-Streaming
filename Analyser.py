# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 21:27:56 2018

@author: Pronaya
"""
import socket
import h2.connection
import h2.events
import json
import pickle
import numpy as np
import cv2
from VideoStreamV2 import VideoStream
import time
from threading import Thread
from Queue import Queue
import matplotlib.pyplot as plt
import tkinter as Tk
import math

root = 'F:/Work/Educational info/Gottingen/Internet Technologies/server/'
bitVSrtt = []
x = []
y = []
bandwidth_ar = []
def plotBandwidth(push, RTT):
    signature='_push'+str(push)+'_aqlt_rtt'+str(RTT)
    global bandwidth_ar
    path = root+'Arrays_video1_SD/'
    with open(path+'bandwidth_ar'+signature+'.txt', 'rb') as fp:
        bandwidth_ar = pickle.load(fp)
    with open(path+'frame_ar'+signature+'.txt', 'rb') as fp:
        frame_ar = pickle.load(fp)
    with open(path+'cum_frame_ar'+signature+'.txt', 'rb') as fp:
        cum_frame_ar = pickle.load(fp)
    with open(path+'rtt_ar'+signature+'.txt', 'rb') as fp:
        rtt_ar = pickle.load(fp)
    with open(path+'time_ar'+signature+'.txt', 'rb') as fp:
        time_ar = pickle.load(fp)
    
    #cum_frame_ar = np.cumsum(frame_ar)/(np.array(time_ar)+1)
    
    
    pushString = {1: 'push1(http2)/ http1.1', 2: 'push2', 3: 'push3', 4: 'push4'}
    rttString = {0: 'default RTT', 100: 'RTT 100', 200: 'RTT 200', 300: 'RTT 300', 400: 'RTT 400'}
    #ploting bandwidth trace    
    plt.figure(1)
    #plt.subplot(111)
    plt.grid(True)
    plt.title('Bandwidth trace for '+pushString[push]+' and '+rttString[RTT])
    plt.plot(time_ar, bandwidth_ar)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Bandwidth (Kbps)")
    #ax.set_xlim([0, sec])
    #plt.gcf().subplots_adjust(bottom=0.50)
    #plt.annotate(("Mean: %.2f\nStandard deviation: %.2f" %(mean(cnt_df0['count']), stddev(cnt_df0['count']))), (0,0), (0, -90), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.savefig(root+'Plots/Bandwidth'+signature+'.png', format='png', dpi=600, bbox_inches="tight")


    #ploting frame trace  
    plt.figure(2)
    #ay = fig.add_subplot(111)
    #1(http2)/http1.1
    plt.grid(True)
    plt.title('Frames per second for '+pushString[push]+' and '+rttString[RTT])
    plt.plot(time_ar, frame_ar)
    plt.plot(time_ar, cum_frame_ar)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frames")
    plt.savefig(root+'Plots/Frames'+signature+'.png', format='png', dpi=600, bbox_inches="tight")
    
    #fig  = plt.figure()
    #az = fig.add_subplot(111)
    #az.grid(True)
    #az.plot(time_ar, rtt_ar)
    #plt.subplot(213)
    
    

def findBitrateRTT(signature, x, y):
    path = root+'Arrays_video1_SD/'
    with open(path+'bandwidth_ar'+signature+'.txt', 'rb') as fp:
        bandwidth_ar = pickle.load(fp)
    with open(path+'rtt_ar'+signature+'.txt', 'rb') as fp:
        rtt_ar = pickle.load(fp)    
    #rtt vs average bitrate
    a = int(sum(rtt_ar)/len(rtt_ar))
    b = int(sum(bandwidth_ar)/len(bandwidth_ar))
    x.append(a)
    y.append(b)
    return (x, y)


def plotBitrateRTT():   
    x = []
    y = []
    (x, y) = findBitrateRTT('_push1_aqlt_rtt0', x, y)
    (x, y) = findBitrateRTT('_push1_aqlt_rtt100', x, y)
    (x, y) = findBitrateRTT('_push1_aqlt_rtt200', x, y)
    (x, y) = findBitrateRTT('_push1_aqlt_rtt300', x, y)
    (x, y) = findBitrateRTT('_push1_aqlt_rtt400', x, y)
    x1, y1 = x, y

    #ploting BitrateVSRTT   
    plt.figure(3)
    #plt.subplot(111)
    plt.grid(True)
    plt.title('Average video bitrate (adaptive quality) with large buffer size 65500KB')
    p1 = plt.plot(x1, y1, label = 'Http1.1')
    plt.plot(x1, y1, 'bo')
    plt.xlabel("RTT (miliseconds)")
    plt.ylabel("Average bitrate (Kbps)")
    #plt.legend((p1), ('Http1.1',))
    #ax.set_xlim([0, sec])
    #plt.gcf().subplots_adjust(bottom=0.50)
    #plt.annotate(("Mean: %.2f\nStandard deviation: %.2f" %(mean(cnt_df0['count']), stddev(cnt_df0['count']))), (0,0), (0, -90), xycoords='axes fraction', textcoords='offset points', va='top')
    #plt.savefig(root+'Plots/Bandwidth'+signature+'.png', format='png', dpi=600, bbox_inches="tight")

    x = []
    y = []
    (x, y) = findBitrateRTT('_push2_aqlt_rtt0', x, y)
    (x, y) = findBitrateRTT('_push2_aqlt_rtt100', x, y)
    (x, y) = findBitrateRTT('_push2_aqlt_rtt200', x, y)
    (x, y) = findBitrateRTT('_push2_aqlt_rtt300', x, y)
    (x, y) = findBitrateRTT('_push2_aqlt_rtt400', x, y)
    x2, y2 = x, y
    p2 = plt.plot(x2, y2, label = 'Http2 push2')
    plt.plot(x2, y2, 'ys')
    plt.xlabel("RTT (miliseconds)")
    plt.ylabel("Average bitrate (Kbps)")
    #plt.legend( [p1[0],p2[0]], ['Http1.1', 'Http2 push2'])
    
    x = []
    y = []
    (x, y) = findBitrateRTT('_push3_aqlt_rtt0', x, y)
    (x, y) = findBitrateRTT('_push3_aqlt_rtt100', x, y)
    (x, y) = findBitrateRTT('_push3_aqlt_rtt200', x, y)
    (x, y) = findBitrateRTT('_push3_aqlt_rtt300', x, y)
    (x, y) = findBitrateRTT('_push3_aqlt_rtt400', x, y)
    x3, y3 = x, y
    p3 = plt.plot(x3, y3, label = 'Http2 push3')
    plt.plot(x3, y3, 'g^')
    plt.xlabel("RTT (miliseconds)")
    plt.ylabel("Average bitrate (Kbps)")
    #plt.legend( [p1[0], p2[0], p3[0]], ['Http1.1', 'Http2 push2', 'Http2 push3'])

    x = []
    y = []
    (x, y) = findBitrateRTT('_push4_aqlt_rtt0', x, y)
    (x, y) = findBitrateRTT('_push4_aqlt_rtt100', x, y)
    (x, y) = findBitrateRTT('_push4_aqlt_rtt200', x, y)
    (x, y) = findBitrateRTT('_push4_aqlt_rtt300', x, y)
    (x, y) = findBitrateRTT('_push4_aqlt_rtt400', x, y)
    x4, y4 = x, y
    p4 = plt.plot(x4, y4, label = 'Http2 push4')
    plt.plot(x4, y4, 'rD')
    plt.xlabel("RTT (miliseconds)")
    plt.ylabel("Average bitrate (Kbps)")
    plt.legend( [p1[0], p2[0], p3[0], p4[0]], ['Http1.1', 'Http2 push2', 'Http2 push3', 'Http2 push4'])
    plt.savefig(root+'Plots/bitrateVSrtt.png', format='png', dpi=600, bbox_inches="tight")
    


def plotInterruptions():
    buffer = [16000, 32000, 48000, 65000]
    """
    faultsPush1 = [1583, 0, 0, 0]  
    faultsPush2 = [3170, 0, 64, 582]  
    faultsPush3 = [4756, 0, 64, 582]  
    faultsPush4 = [6344, 0, 64, 582]
    """
    faultsPush1 = [1583, 0, 0, 0]  
    faultsPush2 = [3170, 0, 44, 344]  
    faultsPush3 = [4756, 215, 354, 1383]  
    faultsPush4 = [6344, 1228, 2708, 1928]
    
    #ploting number of frame interruptions
    plt.figure(4)
    plt.grid(True)
    plt.title('Impact of buffer size on the number of frame interruptions.')
    p1 = plt.plot(buffer, faultsPush1, label = 'Http1.1')
    plt.plot(buffer, faultsPush1, 'bo')
    plt.xlabel("Buffer size (KB)")
    plt.ylabel("Number of interruption (frames)")
    
    p2 = plt.plot(buffer, faultsPush2, label = 'Http2 push2')
    plt.plot(buffer, faultsPush2, 'ys')
    
    p3 = plt.plot(buffer, faultsPush3, label = 'Http2 push3')
    plt.plot(buffer, faultsPush3, 'g^')
    
    p4 = plt.plot(buffer, faultsPush4, label = 'Http2 push4')
    plt.plot(buffer, faultsPush4, 'rD')
    plt.legend( [p1[0], p2[0], p3[0], p4[0]], ['Http1.1', 'Http2 push2', 'Http2 push3', 'Http2 push4'])
    plt.savefig(root+'Plots/interruptionsFramesVSbufferAuto.png', format='png', dpi=600, bbox_inches="tight")
    

    #ploting duration of interruptions
    plt.figure(5)
    plt.grid(True)
    plt.title('Impact of buffer size on the duration of interruptions.')
    p1 = plt.plot(buffer, np.array(faultsPush1)/24, label = 'Http1.1')
    plt.plot(buffer, np.array(faultsPush1)/24, 'bo')
    plt.xlabel("Buffer size (KB)")
    plt.ylabel("Total duration of interruption (s)")
    
    p2 = plt.plot(buffer, np.array(faultsPush2)/24, label = 'Http2 push2')
    plt.plot(buffer, np.array(faultsPush2)/24, 'ys')
    
    p3 = plt.plot(buffer, np.array(faultsPush3)/24, label = 'Http2 push3')
    plt.plot(buffer, np.array(faultsPush3)/24, 'g^')
    
    p4 = plt.plot(buffer, np.array(faultsPush4)/24, label = 'Http2 push4')
    plt.plot(buffer, np.array(faultsPush4)/24, 'rD')
    plt.legend( [p1[0], p2[0], p3[0], p4[0]], ['Http1.1', 'Http2 push2', 'Http2 push3', 'Http2 push4'])
    plt.savefig(root+'Plots/interruptionsDurationVSbufferAuto.png', format='png', dpi=600, bbox_inches="tight")



def plotInterruptions2():
    buffer = [1, 2, 3, 4, 5, 6]
    """
    faultsPush1 = [1583, 0, 0, 0]  
    faultsPush2 = [3170, 0, 64, 582]  
    faultsPush3 = [4756, 0, 64, 582]  
    faultsPush4 = [6344, 0, 64, 582]
    """
    faultsPush1 = np.array([24, 7, 3, 1, 0, 0])/3  
    faultsPush2 = np.array([21, 12, 5, 5, 3, 1])/3  
    faultsPush3 = np.array([32, 18, 15, 12, 9, 6])/3  
    faultsPush4 = np.array([49, 14, 1, 0, 0, 0])/3
    
    #ploting number of frame interruptions
    plt.figure(6)
    plt.grid(True)
    plt.title('Impact of buffer size on the number of interruptions.')
    p1 = plt.plot(buffer, faultsPush1, label = 'Http1.1')
    plt.plot(buffer, faultsPush1, 'bo')
    plt.xlabel("Buffer size (Second)")
    plt.ylabel("Number of interruption ")
    
    p2 = plt.plot(buffer, faultsPush2, label = 'Http2 push2')
    plt.plot(buffer, faultsPush2, 'ys')
    
    p3 = plt.plot(buffer, faultsPush3, label = 'Http2 push3')
    plt.plot(buffer, faultsPush3, 'g^')
    
    p4 = plt.plot(buffer, faultsPush4, label = 'PAT')
    plt.plot(buffer, faultsPush4, 'rD')
    plt.legend( [p1[0], p2[0], p3[0], p4[0]], ['Http1.1', 'Http2 push2', 'Http2 push3', 'PAT'])
    plt.savefig(root+'Plots/interruptionsVSbufferAuto.png', format='png', dpi=600, bbox_inches="tight")
    
    """
    #ploting duration of interruptions
    plt.figure(7)
    plt.grid(True)
    plt.title('Impact of buffer size on the duration of interruptions.')
    p1 = plt.plot(buffer, faultsPush1, label = 'Http1.1')
    plt.plot(buffer, faultsPush1, 'bo')
    plt.xlabel("Buffer size (KB)")
    plt.ylabel("Total duration of interruption (s)")
    
    p2 = plt.plot(buffer, np.array(faultsPush2)/24, label = 'Http2 push2')
    plt.plot(buffer, np.array(faultsPush2)/24, 'ys')
    
    p3 = plt.plot(buffer, np.array(faultsPush3)/24, label = 'Http2 push3')
    plt.plot(buffer, np.array(faultsPush3)/24, 'g^')
    
    p4 = plt.plot(buffer, np.array(faultsPush4)/24, label = 'PAT')
    plt.plot(buffer, np.array(faultsPush4)/24, 'rD')
    plt.legend( [p1[0], p2[0], p3[0], p4[0]], ['Http1.1', 'Http2 push2', 'Http2 push3', 'PAT'])
    plt.savefig(root+'Plots/interruptionsDurationVSbufferAuto.png', format='png', dpi=600, bbox_inches="tight")
    """
        
#plotBitrateRTT()      
plotBandwidth(push=3, RTT=0)  
#plotInterruptions()
#plotInterruptions2()
    