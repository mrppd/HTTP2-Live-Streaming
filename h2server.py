import socket
import h2.connection
import h2.events
import json
import pickle
import numpy as np
import cv2
import math
from VideoStreamV2 import VideoStream
from threading import Thread
import matplotlib.pyplot as plt
import time
import sys

VIDEO_PATH = r'F:\Work\Educational info\Gottingen\Internet Technologies\video_archive\forest_SD'
EXT = 'mp4'
PUSH = 3
QUALITY = 3

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"
RUNNING_TIME = 0
RUNNING_FRAME = 0
FAULT = 0
LAST_CHANGE_TIME = 0
STABILITY = 0


def writeFrame(data, frameno):
    """Write the received frame to a temp image file. Return the image file."""
    cachename = CACHE_FILE_NAME + CACHE_FILE_EXT
    file = open(cachename, "wb")
    file.write(data)
    file.close()    
    return cachename


def split_frame(bdata, chankSize=2300):
    blen = len(bdata)
    #print(blen)
    noOfSlice = int(math.ceil(blen/chankSize))
    #print(noOfSlice)
    a = 0
    b = int(math.ceil(blen/noOfSlice))
    diff = b-a
    #print(a)
    #print(b)
    splitedFrameContainer = [b'']*noOfSlice
    i=0
    while(i!=noOfSlice-1):
        splitedFrameContainer[i] = bdata[a:b]
        #print(splitedFrameContainer[i])
        #print(a)
        #print(b-1)
        a = b
        b = diff*(i+2)
        i = i+1


    b = blen
    splitedFrameContainer[i] = bdata[a:b]
    
    #print(a)
    #print(b-1)
    #total = b''.join(splitedFrameContainer)
    #print(total)
    return splitedFrameContainer
        




def send_response(conn, event, frame_data, kk):
    stream_id = event.stream_id
    #response_data = json.dumps(dict(event.headers)).encode('utf-8')
    conn.max_outbound_frame_size = 65535
    if(kk==0):
        conn.send_headers (
                stream_id=stream_id,
                headers=[
                        (':status', '200'),
                        ('server', 'basic-h2-server/1.0'),
                        #('content-length', str(len(response_data))),
                        #('content-type', 'application/json'),
                        ],                
                        )
       
        conn.send_data(
                stream_id=stream_id,
                data=frame_data,
                end_stream=False
                )
    
    else:
        conn.send_data(
                stream_id=stream_id,
                data=frame_data,
                end_stream=False
                )
    
headers=[
        (':status', '200'),
        ('server', 'basic-h2-server/1.0'),
        #('content-length', str(len(response_data))),
        #('content-type', 'application/json'),
        ]   


def optimalSegment(VS, conn, event, window_set = 0, quality = 7):
    global LAST_CHANGE_TIME
    global RUNNING_TIME
    global STABILITY
    
    max_quality = quality
    
    window_size = conn.local_flow_control_window(event.stream_id)
    if(window_set>0):
        window_size = (window_set if window_set <= window_size else window_size)
    
    data = b''
    while(max_quality):
        data = VS.getFrame(VS.frameNbr(), max_quality)
        if(len(data)<=window_size):
            print("Quality: "+str(max_quality))
            return (data, True)
        else:
            if((RUNNING_TIME-LAST_CHANGE_TIME)>=2 or not(STABILITY==1)):
                VS.frameReduce()
                max_quality -= 1
                LAST_CHANGE_TIME = RUNNING_TIME
            else:
                VS.frameReduce()
    
    return (data, False)
            
        
def simulateTime():
    global RUNNING_TIME
    while(True):
        cv2.waitKey(1000)
        RUNNING_TIME +=1


def showStat(start_time):
    global RUNNING_TIME
    global FAULT
    global RUNNING_FRAME
    
    while(True):
        # Create a black image
        img = np.zeros((150,400,3), np.uint8)
        
        #print(frame_per_sec)
        text = "Running segments: "+ str(int(RUNNING_FRAME/48)) + " \n" + \
        "Running time: "+ str(RUNNING_TIME) + " Sec \n" #+ \
        #"Fault: "+ str(FAULT) + " \n"
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
        cv2.imshow('fault',img)
        if cv2.waitKey(500) & 0xFF == ord('q'):
            img.release()
            cv2.destroyAllWindows()
            break

        

def handle(sock):
    global FAULT
    global RUNNING_FRAME
    global RUNNING_TIME
    global LAST_CHANGE_TIME
    global VIDEO_PATH
    global EXT
    global PUSH
    global QUALITY
    
    LAST_CHANGE_TIME = 0
    #File name should be without bitrate and extension
    VS = VideoStream(VIDEO_PATH, ext=EXT)
    
    """
    setting = h2.settings.Settings(client=False)
    setting.initial_window_size = 48000
    h2.settings.ChangedSetting(setting=h2.settings.INITIAL_WINDOW_SIZE, original_value=65535, new_value=48000)
    p = setting.acknowledge()
    print(p)
    print("hi")
    print(setting.initial_window_size)
    """
    conn = h2.connection.H2Connection(client_side=False)
    #conn.update_settings(p)
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    #print(conn.local_flow_control_window(1))
    
    
    quality = QUALITY
    push = PUSH
    
    
    max_frame_no = 5000
    max_stat_time = 200
    window_size = 0     #0 for default
    ev=[]
    i=0
    fault = 0
    error_sending = 0
    while True:

        data = sock.recv(65535)
        if not data:
            break

        if(i==0):
            RUNNING_TIME = 0
            Thread(target=showStat, args=(time.time(), )).start()
            
        events = conn.receive_data(data)
        
        print(i)
        #print(data)
        print(repr(events))  
        
        error_sending = 1
        
        for event in events:
            if isinstance(event, h2.events.RequestReceived):
                while(True):    
                    kk=0
                    ev = event
                    for i in range(push):
                        (data, success) = optimalSegment(VS, conn, event, window_size, quality)
                        print(len(data))
                    
                        if(success==False and RUNNING_FRAME < max_frame_no):
                            fault += 1
                    
                        if data and success:
                            #frameno = VS.frameNbr()
                            #cv_img = cv2.imread(writeFrame(data, frameno))
                            send_response(conn, event, data, kk)
                            kk = kk + 1
                            error_sending = 0
                    if(error_sending==1):
                        VS.frameIncrease()
                    else:
                        break
            
            elif isinstance(event, h2.events.DataReceived):
                
                #conn.acknowledge_received_data(len(event.data), event.stream_id)
                
                while(True):
                    kk=1
                
                    qlty = int.from_bytes(event.data, 'big')
                    if(qlty>=1 and qlty<=7):
                        quality = qlty
                        
                    #print('push: '+str(push))
                    for i in range(push):
                        (data, success) = optimalSegment(VS, conn, event, window_size, quality)
                        print(len(data))
                    
                        if(success==False and RUNNING_FRAME < max_frame_no):
                            fault += 1
                        
                        if data and success:
                            #frameno = VS.frameNbr()
                            #print("Flow size: "+str(conn.local_flow_control_window(event.stream_id)))
                            send_response(conn, ev, data, kk)
                            error_sending = 0
                            
                    if(error_sending==1):
                        print('flow_window: '+str(conn.local_flow_control_window(event.stream_id)))
                        send_response(conn, ev, b'd', kk)
                        VS.frameIncrease()
                        break
                    else:
                        break
                    
        RUNNING_FRAME = VS.frameNbr()        
        data_to_send = conn.data_to_send()
        if data_to_send:
            sock.sendall(data_to_send)
        #conn.clear_outbound_data_buffer()
     
        i=i+1
        FAULT = fault


if len(sys.argv) > 1:
    PUSH = int(sys.argv[1])
    temp_video_path = "%r"%sys.argv[2]
    VIDEO_PATH = temp_video_path[1:-1]
    EXT = sys.argv[3]

print("Server started! Waiting for the client...")

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 8080))
sock.listen(5)
Thread(target=simulateTime, args=()).start()
while True:
    ss = sock.accept()[0]
    thread = Thread(target=handle, args=(ss, ))
    thread.start()
    thread.join()
    
    #handle(ss)