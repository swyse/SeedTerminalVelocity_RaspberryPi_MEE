
# LICENSING
#This code is licensed according to the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
#International License.

#------------------------------------------------------------------------------

import time
import picamera
import numpy as np
import os
import matplotlib.image as mpimg


if 'terminal_velocity_results.txt' not in os.listdir():
    outfile = open('terminal_velocity_results.txt', 'w')
    outfile.write('SeedID' + "\t" + 'TerminalVelocity_ms' + "\t" + 'fps' + "\n")
    outfile.close()
    

outfile = open('terminal_velocity_results.txt', 'a')

    
SeedID = input("Seed ID number: ")

frames = 400

#clear out folder (TVimages) that the image files will be written to
files = os.listdir('TVimages')
for f in files:
    os.remove('TVimages/' + f)


input("Press Enter to start camera...")

#settings that worked for our system, may need tweaking...
#drop your seed when the screen prints "starting..."
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 90
    camera.sensor_mode = 7
    camera.awb_mode = 'off'
    camera.awb_gains = (1.5, 1.9)
    camera.brightness = 60
    camera.iso = 100
    camera.shutter_speed = 4000
    camera.contrast = 60
    time.sleep(2)
    print('starting...')
    time.sleep(1)
    start = time.time()
    camera.capture_sequence([
        'TVimages/img%02d.jpg' % i
        for i in range(frames)
        ], use_video_port = True)
    finish = time.time()
    fps = frames / (finish - start)
print('Captured %d frames at %.2ffps' % (
    frames,
    fps))


#distance from the back wall to our camera (mm)
distance_wall = 633

frame1 = mpimg.imread('TVimages/img01.jpg')
frame1 = frame1.astype('int16')
frame1 = frame1[0:480, 0:640, 0] + frame1[0:480, 0:640, 1] + frame1[0:480, 0:640, 2]


seed_frames = []
seed_frame_names = []

for n in os.listdir('TVimages'):
    frameNext = mpimg.imread('TVimages/' + n)
    frameNext = frameNext.astype('int16')
    frameNext = frameNext[0:480, 0:640, 0] + frameNext[0:480, 0:640, 1] + frameNext[0:480, 0:640, 2]
    difference = frame1 - frameNext
    maxDiff = np.amax(difference)
    seed_frame_name = float(n.split('img')[1].split('.jpg')[0])

    
  #need to calibrate this and work out the optimal value to go in as the "difference", 
  #100 worked well for us  
    if maxDiff > 100:
        time_write = os.path.getmtime('TVimages/' + n)
        seed_frames.append(time_write)
        seed_frame_names.append(seed_frame_name)

    
time_viewed = max(seed_frames) - min(seed_frames)
print(time_viewed)

distance_seedWall = input("Seed landing distance from wall (mm): ")
distance_seedWall = float(distance_seedWall) + 45 #our frame is 45mm

#calculate distance travelled based on the known distance from the seed to the camera
#we calibrated this to get the equation used below
distance_travelled = ((0.389*(distance_wall-distance_seedWall))-14.46)

velocity = (distance_travelled/1000)/time_viewed
print(velocity)


#if you're happy with the run, write out the result. If something went wrong, tell
#it not to write out and re-do it
write_out = input("Write result? (Y/N): ")
write_out = write_out.upper()

if write_out == 'Y':
    outfile.write(SeedID + "\t" + str(round(velocity, 2)) + "\t" + str(round(fps, 2)) + "\n")

outfile.close()
