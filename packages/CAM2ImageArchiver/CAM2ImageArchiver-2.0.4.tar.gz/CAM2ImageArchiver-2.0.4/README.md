# README #

### Citation ###

If you use this software, please include the following statement in acknowledgments

"The image archiving program is provided by the CAM2 (Continuous Analysis
of Many CAMeras) project at Purdue University."

### What is this repository for? ###

* This repository stores the source code for retrieving data (image
  or video) from network cameras.

* This is part of Purdue's CAM2 (Continuous Analysis of Many CAMeras)
  project. The project's web site is https://www.cam2project.net/

* Please read the terms of use
https://www.cam2project.net/terms/

In particular, "You agree not to use the Platform to determine the
identity of any specific individuals contained in any video or video
stream."

* Software licensed under Apache license.  See LICENSE.txt for details.

* The lead investigator is Dr. Yung-Hsiang Lu, yunglu@purdue.edu. Please
send your questions, comments, or suggestions to him.

### Motivation ###

Thousands of network cameras are connected to the Internet and provide
real-time visual data (image or video).  Many network cameras require
no password and anyone connected to the Internet can retrieve the
data,i.e., the data is publicly available.  This program considers
only publicly available camera data.

Even though the data is publicly available to anyone interested
seeing, there are several problems. First, there is no central
repository where network cameras must register.  Thus, significant
efforts must be taken to find various sources of data. Second,
different brands of network cameras need different methods to retrieve
the data.  The cameas may also provide different data formats: some
provide individual JPEG images; some provide motion JPEG (MJPEG)
video; some others provide H.264 video.

Many organizations (such as departments of transportation) aggregate
streams of multiple cameras and put these streams on web sites.
However, these web sites have different formats and styles.  Some web
sites use simple HTML; some use CSS; some use Javascript. Some web
sites have fixed URLs for different cameras. Some web site have
dynamically generated URLs reflecting the time (thus, the URLs are
always changing).

To solve these problems, researchers at Purdue University are
developing the software to retrieve data from heterogeneous sources.

### Documentation ###
Full documentation can be found at https://purduecam2project.github.io/CAM2ImageArchiver/index.html

### Installation ###

* To install from our [PyPi Repository](https://pypi.org/project/CAM2ImageArchiver/) use PIP:
```
 pip install CAM2ImageArchiver
```

* To install from source, download this repository and run:
```
python setup.py install
```


### Files ###

* ```CAM2ImageArchiver.py``` is the main Python module. It archives images from a single camera.
* ```camera.py``` provides classes to communicate with different types of cameras: IP cameras, non-IP cameras, and stream cameras.
* ```StreamParser.py``` is used by ```camera.py``` to parse JPEG and MJPEG streams.
* ```error.py``` contains custom Python Exceptions.
* ```CamerHandler.py``` splits the retrieval job into threads for parallel processing.

### Usage ###

We recommend using the CAM2 Image Archiver with the [CAM2 Camera Database Python Client](https://github.com/PurdueCAM2Project/CameraDatabaseClient).

The CAM2 Image Archiver accepts Camera objects directly from the [CAM2 Camera Client](https://github.com/PurdueCAM2Project/CameraDatabaseClient) users can also create their own camera object on the fly as shown below. The `archive()` method expects a list of dictionary objects with camera_type, cameraID, and snapshot_url fields. 
```
[{'camera_type': 'non_ip', 'cameraID':'1', 'snapshot_url':'<The URL to the Camera Image Data>'}]
```
Below is an example of how to archive the image data from one camera. More example usage can be found in [the documentation](https://purduecam2project.github.io/CAM2ImageArchiver/index.html).
```
from CAM2ImageArchiver import CAM2ImageArchiver
cams = [{'camera_type': 'non_ip', 'cameraID':'1', 'snapshot_url':'http://example.com/camera1'}]
cam2 = CAM2ImageArchiver(num_processes=3)
cam2.archive(cams, duration=<duration(sec) to archive data>, interval=<interval(sec) to archive data>)	
```

