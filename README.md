<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README</title>
</head>
<body>

    <h1>Dependency</h1>
    <p>
        Please download and install Python 3.* from the following site:<br>
        <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
    </p>
    <p>You also need the following modules:</p>
    <ul>
        <li>Hyper-h2</li>
        <li>cv2</li>
        <li>pickle (if not available with Python package)</li>
    </ul>
    <p>I think other modules such as threading, time, matplotlib, and socket are available with the Python package.</p>

    <h2>Module Installation:</h2>
    <p>
        Ensure you have installed the pip module first. For Linux, I think it will be installed with the Python package. Otherwise, please follow the link to install pip:<br>
        <a href="https://www.tecmint.com/install-pip-in-linux/">https://www.tecmint.com/install-pip-in-linux/</a>
    </p>
    <p>
        In Windows, please follow the link to install pip:<br>
        <a href="https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation">https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation</a>
    </p>
    <h3>Hyper-h2 Installation</h3>
    <p><code>pip install h2</code></p>

    <h3>OpenCV Installation</h3>
    <p>
        <code>pip install opencv-python</code><br>
        or<br>
        <code>pip install opencv-contrib-python</code>
    </p>

    <h3>pickle Installation</h3>
    <p><code>pip install pickle-mixin</code></p>

    <h1>Video Archive</h1>
    <p>
        The video archive should contain videos with bitrates 50, 150, 300, 600, 1200, 2500, and 4000. We have to follow a specific naming format for the files. The name has three parts and the extension. For example:
    </p>
    <p>Here, the three parts of the video name are separated by underscores ('_') and the extension is '.mp4'. The first part is the name of the video, the second part is the resolution information, and the third part is the bitrate.</p>
    <p>
        You can download the video from the following dataset library, rename them according to the described format, and put them in a folder:<br>
        <a href="http://www-itec.uni-klu.ac.at/dash/?page_id=207">http://www-itec.uni-klu.ac.at/dash/?page_id=207</a>
    </p>
    <p>
        (For simplicity, I have uploaded a video set in Google Drive. Those can be downloaded from the link:<br>
        <a href="https://goo.gl/vpnEAd">https://goo.gl/vpnEAd</a>)
    </p>

    <h1>Input Guide/Running Procedure:</h1>
    <h2>For Server</h2>
    <p>Format:</p>
    <pre><code>python h2server.py "PUSH" "PATH INCLUDING NAME OF THE FILE EXCEPT LAST PART" "VIDEO EXTENSION"</code></pre>
    <p>
        Here:
        <ul>
            <li><strong>PUSH</strong> value is between 1 to 3</li>
            <li><strong>PATH INCLUDING NAME OF THE FILE EXCEPT LAST PART</strong> is a string which is the path to the video archive. It also contains the filename except the last part and extension. Video file names have a specific format consisting of three parts and an extension.</li>
        </ul>
    </p>

    <p>Example:</p>
    <pre><code>python h2server.py 3 "F:\Work\Educational info\Gottingen\Internet Technologies\video_archive\forest_SD" "mp4"</code></pre>

    <h2>For Client</h2>
    <p>Format:</p>
    <pre><code>python h2client3.py "BUFFER" "MIN_BUFFER" "QUALITY" "AUTO_QUALITY" "SHOW_OUTPUT" "SHOW_VIDEO" "RTT"</code></pre>
    <p>
        Here:
        <ul>
            <li><strong>BUFFER</strong> value is between 1 to 6</li>
            <li><strong>MIN_BUFFER</strong> value can be between 0 to 5</li>
            <li><strong>QUALITY</strong> value ranges from 1 to 7</li>
            <li><strong>AUTO_QUALITY</strong> value is either 1 or 0 (for our case, always put it 1)</li>
            <li><strong>SHOW_OUTPUT</strong> value is either 1 or 0 (if you want to see the running statistics, put it 1)</li>
            <li><strong>SHOW_VIDEO</strong> value is either 1 or 0 (if 1, you will see the playback, which may slow down the process; preferred value: 0)</li>
            <li><strong>RTT</strong> values are 0, 100, 200, 300, 400 (default: 0)</li>
        </ul>
    </p>

    <p>Client can also be run without parameters. In this case, it will start with its default values:</p>
    <pre><code>python h2client3.py</code></pre>

    <p>Default values:</p>
    <ul>
        <li><strong>BUFFER:</strong> 6</li>
        <li><strong>MIN_BUFFER:</strong> 0</li>
        <li><strong>QUALITY:</strong> 3</li>
        <li><strong>AUTO_QUALITY:</strong> 1</li>
        <li><strong>SHOW_OUTPUT:</strong> 1</li>
        <li><strong>SHOW_VIDEO:</strong> 0</li>
        <li><strong>RTT:</strong> 0</li>
    </ul>

    <p>Examples:</p>
    <pre><code>python h2client3.py 6 0 3 1 1 0 0</code></pre>
    <pre><code>python h2client3.py</code></pre>

    <p>
        If you want to assign parameters, assign all; otherwise, assign none. The client will run for 214 seconds and, at the end, it will write some files in the source directory. These files can be used to generate plots.
    </p>
</body>
</html>
