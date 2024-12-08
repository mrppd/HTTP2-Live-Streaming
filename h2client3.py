# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 05:31:37 2018

@author: Pronaya
"""

import socket
import h2.connection
import h2.events
import json
from h2.events import (
        ConnectionTerminated, DataReceived, RequestReceived, StreamEnded,
        )
import pickle
import numpy as np
import cv2
from VideoStreamV2 import VideoStream
import time
from threading import Thread
from Queue import Queue
import matplotlib.pyplot as plt
import tkinter as Tk
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server

RUNNING_TIME = 0.0
FRAME_COUNT = 0
BANDWIDTH = 0
BANDWIDTH_PER_SEC = 0
FRAME_PER_SEC = 0
CUM_FRAME_PER_SEC = 0
CUM_FRAME_COUNT = 0
RTT = 0.0
INTERRUPTIONS = 0

BUFFER = 6          #max 6, min 2
MIN_BUFFER = 0      #For PAT MIN_BUFFER is half of BUFFER
PUSH = 3
QUALITY = 3
AUTO_QUALITY = 1    #1 for yes. 0 for no.
SHOW_OUTPUT = 1     #1 for yes. 0 for no.
SHOW_VIDEO = 0      #1 for yes. 0 for no.
ARTIFICIAL_RTT = 400  #only value greater than 100 or equal have an effect
MAX_TIME = 212
MIN_BUFFER_FR = MIN_BUFFER*24

DATA_Q = Queue()

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

def writeFrame(data, frameno):
    """Write the received frame to a temp image file. Return the image file."""
    cachename = CACHE_FILE_NAME + CACHE_FILE_EXT
    file = open(cachename, "wb")
    file.write(data)
    file.close()
    
    return cachename

def checkFinish():
    if(RUNNING_TIME>201):
        return 1
    else:
        return 0

def get_upgrade_response(connection):
    """
    This function reads from the socket until the HTTP/1.1 end-of-headers
    sequence (CRLFCRLF) is received. It then checks what the status code of the
    response is.
    
    This is not a substitute for proper HTTP/1.1 parsing, but it's good enough
    for example purposes.
    """
    data = b''
    while b'\r\n\r\n' not in data:
        data += connection.recv(65535)
        
    headers, rest = data.split(b'\r\n\r\n', 1)
    
    # An upgrade response begins HTTP/1.1 101 Switching Protocols. Look for the
    # code. In production code you should also check that the upgrade is to
    # h2c, but here we know we only offered one upgrade so there's only one
    # possible upgrade in use.
    split_headers = headers.split()
    if split_headers[1] != b'101':
        raise RuntimeError("Not upgrading!")
        
    # We don't care about the HTTP/1.1 data anymore, but we do care about
    # any other data we read from the socket: this is going to be HTTP/2 data
    # that must be passed to the H2Connection.
    return rest

def showPlot():
    global BANDWIDTH
    global FRAME_PER_SEC
    global RTT
    global BANDWIDTH_PER_SEC
    global CUM_FRAME_PER_SEC
    signature_str = "_push"+str(PUSH)+"_aqlt_rtt"+str(ARTIFICIAL_RTT)
    sec = 0
    cv2.waitKey(10000)
    
    bandwidth_ar = []
    frame_ar = []
    cum_frame_ar = []
    rtt_ar = []
    time_ar = []
    while(sec<200):
        bandwidth_ar.append(BANDWIDTH_PER_SEC)
        frame_ar.append(FRAME_PER_SEC)
        rtt_ar.append(RTT)
        time_ar.append(sec)
        cum_frame_ar.append(CUM_FRAME_PER_SEC)
        #plt.show()
        #plt.pause(0.0001)
        cv2.waitKey(1000)
        sec += 1
    
    
    with open('bandwidth_ar'+signature_str+'.txt', 'wb') as fp:
        pickle.dump(bandwidth_ar, fp)
    with open('frame_ar'+signature_str+'.txt', 'wb') as fp:
        pickle.dump(frame_ar, fp)
    with open('cum_frame_ar'+signature_str+'.txt', 'wb') as fp:
        pickle.dump(cum_frame_ar, fp)
    with open('rtt_ar'+signature_str+'.txt', 'wb') as fp:
        pickle.dump(rtt_ar, fp)
    with open('time_ar'+signature_str+'.txt', 'wb') as fp:
        pickle.dump(time_ar, fp)
        
    fig  = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.plot(time_ar, bandwidth_ar)
    #ax.set_xlim([0, sec])

    fig  = plt.figure()
    ay = fig.add_subplot(111)
    ay.grid(True)
    ay.plot(time_ar, frame_ar)
    
    fig  = plt.figure()
    az = fig.add_subplot(111)
    az.grid(True)
    az.plot(time_ar, rtt_ar)
    #plt.subplot(213)
    #plt.plot(time_ar, RTT)
    #fig.show()
    #Tk.mainloop()
    #plt.pause(1000)
    
    
def simulateTime():
    global RUNNING_TIME
    global MAX_TIME
    while(True):
        cv2.waitKey(100)
        RUNNING_TIME +=0.1
        
        if(RUNNING_TIME >= MAX_TIME):
            break
        

def qualityBit(Q):
    qbitdic = {1: 50, 2: 150, 3:300, 4:600, 5:1200, 6:2500, 7: 4000}
    return qbitdic[Q]
  
    
def showStat(start_time):
    global BANDWIDTH
    global FRAME_PER_SEC
    global RTT
    global QUALITY
    global AUTO_QUALITY
    global BANDWIDTH_PER_SEC
    global FRAME_COUNT
    global CUM_FRAME_PER_SEC
    global CUM_FRAME_COUNT
    global MAX_TIME
    global INTERRUPTIONS
    
    threadShowPlot = Thread(target=showPlot, args=())
    threadShowPlot.start()
    #threadShowPlot.join()
    threadSimulateTime = Thread(target=simulateTime, args=())
    threadSimulateTime.start()
    #threadSimulateTime.join()
    
    while(True):
        # Create a black image
        img = np.zeros((300,400,3), np.uint8)
        
        time_e = (float(time.time() - start_time)+0.01)
      
        #print('time: '+str(time_e))
        bandwidth_per_sec = 0
        if(time_e>1.01):
            bandwidth_per_sec = round((BANDWIDTH*8)/1024, 2)
            BANDWIDTH_PER_SEC = bandwidth_per_sec
            BANDWIDTH = 0
            
            CUM_FRAME_PER_SEC = round(CUM_FRAME_COUNT/time_e, 2)
            
            FRAME_PER_SEC = FRAME_COUNT
            FRAME_COUNT = 0
        
        #print(frame_per_sec)
        text = "Running time: "+ str(round(RUNNING_TIME)) + " Sec \n" + \
        "Frame rate: "+ str(FRAME_PER_SEC) + " FPS \n" + \
        "Bandwidth: "+str(bandwidth_per_sec) + " Kbps \n" + \
        "Average RTT: " + str(RTT)+ ' ms \n' + \
        "Quality: " + str(QUALITY) + " (" + str(qualityBit(QUALITY)) + " kbit) \n"+ \
        "Quality optimization: " + ("ON \n" if AUTO_QUALITY==1 else "OFF \n") + \
        "Interruptions: " + str(INTERRUPTIONS) + " \n" 
        y0, dy = 50, 30
        for i, line in enumerate(text.split('\n')):
            y = y0 + i*dy
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            position = (30, y)
            scale = 0.6
            color = (255, 255, 0)
            lineType = 2
            cv2.putText(img, line, position, font, scale, color, lineType)

        #Display the image
        cv2.imshow('Frame_per_sec',img)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            #start_time = time.time()
            img.release()
            cv2.destroyAllWindows()
            break
        
        if(RUNNING_TIME >= MAX_TIME):
            break


def intelligentPush(min_quality = 1, max_quality = 7): 
    global QUALITY
    global RUNNING_TIME
    global MAX_TIME      
    global MIN_BUFFER_FR
    
    quality_throughput = QUALITY
    quality_buffer = QUALITY
    while(True):
        
        #cv2.waitKey(5000)
        if(FRAME_PER_SEC>35):
            if(quality_throughput+1>=min_quality and quality_throughput+1<=max_quality):
                quality_throughput += 1
        elif(FRAME_PER_SEC<30):
            if(quality_throughput-1>=min_quality and quality_throughput-1<=max_quality):
                quality_throughput -= 1
        
        BufferMin = MIN_BUFFER_FR
        quality_buffer = max(int((((DATA_Q.size() - BufferMin) * (max_quality - min_quality)) / float(24*BUFFER - BufferMin)) + min_quality), 1)
        
        QUALITY = min(quality_buffer, quality_throughput)
        cv2.waitKey(2000)
        
        if(RUNNING_TIME >= MAX_TIME):
            break
    
    
    
def showFrame():
    global DATA_Q
    global RUNNING_TIME
    global MAX_TIME
    global INTERRUPTIONS
    global SHOW_VIDEO
    #print(DATA_Q.size())
    while(True):
        if(DATA_Q.size()>0):
            data = DATA_Q.dequeue()
            
            if(SHOW_VIDEO):
                cv_img = cv2.imread(writeFrame(data, 1))
                cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
                cv2.resizeWindow('image', 214,120)
                cv2.imshow('frame', cv_img)
                
            if cv2.waitKey(20) & 0xFF == ord('q'):
                #cv_img.release()
                #cv2.destroyAllWindows()  
                break
                #print("end")
        else:
            INTERRUPTIONS += 1
            while(DATA_Q.size()<24*BUFFER):
                "Do Something"
        
        if(RUNNING_TIME >= MAX_TIME):
            break
    
def handle(sock):
    global FRAME_COUNT
    global BANDWIDTH
    global DATA_Q
    global RTT
    global ARTIFICIAL_RTT
    global FRAME_PER_SEC
    global CUM_FRAME_COUNT
    global RUNNING_TIME
    global MAX_TIME
    global CUM_FRAME_PER_SEC
    global BANDWIDTH_PER_SEC
    global INTERRUPTIONS
    
    INTERRUPTIONS = 0
    RUNNING_TIME = 0
    FRAME_COUNT = 0
    BANDWIDTH = 0
    BANDWIDTH_PER_SEC = 0
    FRAME_PER_SEC = 0
    CUM_FRAME_PER_SEC = 0
    CUM_FRAME_COUNT = 0
    RTT = 0.0
    
    send_time = 0
    recv_time = 0
    
    config = h2.config.H2Configuration()
    conn = h2.connection.H2Connection(config=config)
    #conn.update_settings(p)
    #conn.settings = h2.settings.ENABLE_PUSH=2
    conn.max_inbound_frame_size=65535
    #conn.initiate_connection()
    settings_header_value = conn.initiate_connection()
    sock.sendall(conn.data_to_send())
    
    """
    request = (
            b"GET / HTTP/2.0\r\n" +
            b"Host: localhost\r\n" +
            b"Upgrade: h2c\r\n" +
            b"HTTP2-Settings: " + settings_header_value + b"\r\n" +
            b"\r\n" )
    #sock.sendall(request)
    """
    request_headers = [
            (':method', 'GET'),
            (':authority', 'localhost'),
            (':scheme', 'http'),
            (':path', '/'),
            ('user-agent', 'hyper-h2/1.0.0'),
            ]

    conn.send_headers(1, request_headers, end_stream=False)
    sock.sendall(conn.data_to_send())
    
    data = b''
    currentRTT = 0.0
    tmpRTT = 0.0
    i=0   
    while b'\r\n\r\n' not in data:
        if(RUNNING_TIME >= MAX_TIME):
            break
        if(True):
            data = sock.recv(65535)
            if not data:
                break
        
            events = conn.receive_data(data)
        
            recv_time = time.time()
            if(i>1):
                currentRTT = (recv_time - send_time)*1000    
            
                #Simulating artificial RTT
                diffRTT = 0
                if(ARTIFICIAL_RTT>=100):
                    diffRTT = ARTIFICIAL_RTT - int(currentRTT)
                    if(diffRTT>0):
                        #print("diff: " +str(diffRTT))
                        cv2.waitKey(diffRTT)        
                #calculating average RTT        
                tmpRTT += (currentRTT + diffRTT)
                RTT = round(tmpRTT/float(i-1), 2)
        
            print(i)
            print(events)
        
            ev=1
            frame_recv=0
            processed_data_size = 0
        
            #counting frame per second
            if(i==0):
                #show statistics
                threadShowStat = Thread(target=showStat, args=(time.time(), ))
                threadShowStat.start()
                #threadShowStat.join()
            
                #show output video
                if(SHOW_OUTPUT):
                    threadShowFrame = Thread(target=showFrame, args=())
                    threadShowFrame.start()
                    #threadShowFrame.join()
                
                #decide optimal push
                if(AUTO_QUALITY):
                    threadIntelligentPush = Thread(target=intelligentPush, args=())
                    threadIntelligentPush.start()
                    #threadIntelligentPush.join()
                    #frame_thread.join()
                    #frameRate(time.time())
            
            for event in events:
                if(isinstance(event, DataReceived)):
                    ev = event
                    print("E"+str(frame_recv))
                
                    if(len(event.data)>500):
                        DATA_Q.enqueue(event.data)
            
                    #print(event.data.decode('utf-8'))
                    #cv_img = cv2.imread(writeFrame(event.data, 1))
                    # Display the resulting frame
                    #cv2.imshow('frame',cv_img)
                    #if cv2.waitKey(20) & 0xFF == ord('q'):
                        #cv_img.release()
                        #cv2.destroyAllWindows()  
                        #break
                    processed_data_size = processed_data_size + len(event.data)
                    conn.acknowledge_received_data(processed_data_size, event.stream_id)
                    if(len(event.data)>500):
                        frame_recv += 1
                        FRAME_COUNT += 1
                        CUM_FRAME_COUNT += 1 
                        BANDWIDTH += len(event.data)
                
                elif(isinstance(event, h2.events.ConnectionTerminated)):
                    #cv_img.release()
                    cv2.destroyAllWindows()  
 
    

            #conn.increment_flow_control_window(1, event.stream_id)
            #conn.push_stream(event.stream_id, event.stream_id, request_headers)
            try:
                #print(ev.stream_id)
                conn.send_data(
                        stream_id=ev.stream_id,
                        data=QUALITY.to_bytes(2, byteorder='big'),
                        end_stream=False
                        )
                send_time =  time.time()
            except:
                print("some error occured!")
            sock.sendall(conn.data_to_send())
            
            while(DATA_Q.size()>24*BUFFER):
                "Do Something"

            i=i+1


        
def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.bind((HOST, PORT))
    #sock.listen(5)
    sock.connect((HOST, PORT))
    handle(sock)


    
if len(sys.argv) > 1:
    BUFFER  = int(sys.argv[1])
    MIN_BUFFER = int(sys.argv[2])
    QUALITY = int(sys.argv[3])
    AUTO_QUALITY = int(sys.argv[4])
    SHOW_OUTPUT = int(sys.argv[5])
    SHOW_VIDEO = int(sys.argv[6])
    ARTIFICIAL_RTT = int(sys.argv[7])

threadConnect = Thread(target=connect, args=())
threadConnect.start()