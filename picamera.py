#!/usr/bin/env python3
from pyparticleio.ParticleCloud import ParticleCloud
import picamera, datetime, time
from time import strftime

#username = "mattvlaw@gmail.com"
#password = "s-tech123~"
#particle_cloud = ParticleCloud(username, password)
access_token = "7194c612c12123160921e81ebdd7c36fd6bc2460"
particle_cloud = ParticleCloud(username_or_access_token=access_token)
#all_devices = particle_cloud.devices
#for device in all_devices:
    # make array if we want to loop through all devices

def takeVideo():
    print("it's working")
    #date to string
    date1 = datetime.datetime.now()
    datestring = date1.strftime("%m-%d-%Y-%H:%M")

    #make file
    my_file = open(datestring+'.h264', 'wb')

    #take video
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_recording(datestring+'.h264')
    camera.wait_recording(10)
    camera.stop_recording()

    print("OK");
    # At this point my_file.flush() has been called, but the file has
    # not yet been closed
    my_file.close()

particle_cloud.quit.subscribe("doorOpen",(takeVideo()))

while(true):
    sleep(100)