
import sys, os, threading, serial, time, csv
from time import localtime, strftime

# serial library is installed with "pip install pyserial"

#define mouse parameters
mousename = "H01"
sessionday = 'Session X'

#make filepath into below line
dir = r"C:\Users\break\Documents\testing pyhon\\" + sessionday 
if not os.path.exists(dir):
    os.mkdir(dir)


# define function ------------------------------
def read_serial():
   ser = serial.Serial(COMPORT, BAUDRATE, timeout=1)

   time.sleep(1)

  # send parameters
   ser.write(b'1')

   running = 1

   while (running == 1):
       line = ser.readline()
       line = line[0:len(line)-1].decode("utf-8")

       if (line != ""):

          # print line for live display
          print(line)

          # append file
          with open(dir +"\\" + fn,"a") as f:
              writer = csv.writer(f,delimiter=",")
              writer.writerow([line])

          # stop connection following stop command
          if (int(line.split(" ")[0]) == 0):
            print("stop read_serial")
            ser.close()
            running = 0
            
   
# **parameters** -------------------------------------
COMPORT = "COM5";
BAUDRATE = 9600;

subject='test'

# excecution -----------------------------------------
# output fn format: subject_yyyy_mm_dd
# - if file already exists, local time will be appended to fn (e.g. yyyy_mm_dd_subject_hhmmss)

fn = strftime(mousename + '_' + "%Y_%m_%d", localtime()) + '_' + subject + '.csv'

if os.path.exists(fn):
    fn = strftime("%Y_%m_%d", localtime()) + '_' + subject + '_' + strftime("%H%M%S", localtime()) + '.csv'


print ("start read_serial")
read_serial()
