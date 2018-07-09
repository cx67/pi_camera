#!/usr/bin/env python3
from pyparticleio.ParticleCloud import ParticleCloud
import picamera, datetime, time, os, os.path, subprocess
from time import strftime

access_token = "7194c612c12123160921e81ebdd7c36fd6bc2460"
particle_cloud = ParticleCloud(access_token)

def takeVideo(eventData):
    #date to string
    date1 = datetime.datetime.now()
    datestring = date1.strftime("%m-%d-%Y-%H%M%S")

    #make file
    dirString = os.getcwd()
    data_folder = os.path.join(dirString,"ShareBoxVideos",datestring)
    my_file = open(data_folder+'.h264', 'wb')
    
    #take video
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_recording(my_file)
    camera.wait_recording(10)
    camera.stop_recording()

    # At this point my_file.flush() has been called, but the file has
    # not yet been closed
    my_file.close()
    camera.close()
    
    # Sync with GoogleDrive
    os.system("rclone sync /home/pi/ShareBoxVideos sbTest:folder", shell=True)

particle_cloud.quit.subscribe("doorOpen",(takeVideo))

while(True):
    time.sleep(100)
