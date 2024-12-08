# HTTP2 Live Streaming
 HTTP2 Push-Based Low-Delay Live Streaming


# Dependency
Please download and install python 3.* from the following site,
https://www.python.org/downloads/

You also need the following modules,
Hyper-h2
cv2
pickle (if not available with python package)
I think other modules, such as threading, time, matplotlib, and socket, are available with the Python package.

Module installation:
Ensure you have installed pip module first. For Linux, I think it will be installed with the python package. Otherwise please follow the link to install pip,
https://www.tecmint.com/install-pip-in-linux/

In windows, please follow the link to install pip,
https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation

Hyper-h2 installation (run it on a command prompt or a terminal) 
pip install h2

OpenCV installation 
pip install opencv-python
or
pip install opencv-contrib-python

pickle installation 
pip install pickle-mixin



# Input guide/ Running procedure:
For Server
Format:
python h2server.py "PUSH" "PATH INCLUDING NAME OF THE FILE EXCEPT LAST PART" "VIDEO EXTENTION"

Here, PUSH value is between 1 to 3
      "PATH INCLUDING NAME OF THE FILE EXCEPT LAST PART" is a string which is path to the video archive. It also contains the filename except the last part and extension. Video file name has a specific format and consist of 3 parts and extension. It will be discussed separately.  



Example:
python h2server.py 3 "F:\Work\Educational info\Gottingen\Internet Technologies\video_archive\forest_SD" "mp4"


For Client
Format:
python h2client3.py "BUFFER" "MIN_BUFFER" "QUALITY" "AUTO_QUALITY" "SHOW_OUTPUT" "SHOW_VIDEO" "RTT"

Here, BUFFER value is between 1 to 6
      MIN_BUFFER value can be between 0 to 5
      QUALITY value ranges from 1 to 7
      AUTO_QUALITY value is either 1 or 0. For our case we should always put it 1
      SHOW_OUTPUT value is either 1 or 0. If you want to see the running statistics then put it 1.
      SHOW_VIDEO value is either 1 or 0. If 1 then you will be able to see the playback which is not important for the statistics. I prefer it to be 0 cause for some reason it slowing down the whole process.
      RTT values are 0 100 200 300 400. If you want default RTT then put 0 which is not 0 in real-time.

*Client can also be run without the parameters. In this case it will start with its default values.
Format:
python h2client3.py

Here the default values are BUFFER=6, MIN_BUFFER=0, QUALITY=3, AUTO_QUALITY=1, SHOW_OUTPUT=1, SHOW_VIDEO=0 and RTT=0

Example:
python h2client3.py 6 0 3 1 1 0 0
or
python h2client3.py 

If you want to assign parameters, then assign all otherwise none.
Client will run for 214 seconds and at the end, it will write some files in the source directory. This files can be used to generate plots.
