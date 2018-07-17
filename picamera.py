#!/usr/bin/env python3
from pyparticleio.ParticleCloud import ParticleCloud
import picamera, datetime, time, os, os.path, subprocess
import RPi.GPIO as GPIO
from time import strftime

# Particle cloud settings
access_token = "7194c612c12123160921e81ebdd7c36fd6bc2460"
particle_cloud = ParticleCloud(access_token)

# LED settings
chan_list = [19,37]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(chan_list, GPIO.OUT)

def takeVideo(eventData):
    #date to string
    date1 = datetime.datetime.now()
    datestring = date1.strftime("%m-%d-%Y-%H%M%S")

    #make file
    dirString = os.getcwd()
    data_folder = os.path.join(dirString,"ShareBoxVideos",datestring)
    my_file = open(data_folder+'.h264', 'wb')
    
    # turn on light
    GPIO.output(chan_list, True)
    
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
    
    # turn off light
     GPIO.output(chan_list, False)
    
    # Sync with GoogleDrive
    # make sure to copy rclone.config file to root folder if running service as root 
    subprocess.run(args="rclone sync /home/pi/ShareBoxVideos sbTest:folder", shell=True)

particle_cloud.quit.subscribe("doorOpen",(takeVideo))

while(True):
    time.sleep(100)
