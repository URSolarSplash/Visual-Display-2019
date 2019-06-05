import socket
import sys
import time
import warnings
import serial
import serial.tools.list_ports
from omxplayer.player import OMXPlayer
from pathlib import Path

arduino_ports = []

for p in serial.tools.list_ports.comports():
    print p
    if '/dev/cu.usbmodem' in p[0] or '/dev/ttyACM' in p[0]:
        arduino_ports.append(p[0])

if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

print "Connected to Arduino!\n"
ser = serial.Serial(port=arduino_ports[0],timeout=None)

timestamps = [333,531,0,1018,840]

#Sleep some time to allow the computer to start up
print "Waiting for system startup...\n"
time.sleep(10)

VIDEO_PATH = Path("./CombinedVideoTest.mp4")
player = OMXPlayer(VIDEO_PATH,args=["--loop","--no-osd"])
player.set_aspect_mode("stretch")
player.set_video_pos(0,0,1280,800)
player.mute()
#player.set_alpha(100)
print "Started Video!\n"

try:
    while True:
        message = ser.readline().rstrip().lstrip()
        print message
	if message.startswith('START'):
            id = int(message[5])
            player.set_position(timestamps[id])
            player.unmute()
	if message.startswith('TIMEOUT'):
            player.mute()
	if message.startswith('QUIT'):
            break
except KeyboardInterrupt:
	print "Interrupted"
except Exception as exception:
	#continue and quit
	print "Exception:"
	print exception

ser.close()
player.quit()
