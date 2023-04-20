from pyautogui import press, typewrite, hotkey, write, keyUp, press
import time
import random 
import struct
import time 
import serial 

print("version: ")
print(serial.__version__)
print(" ...end")

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
ser.flush()
ser.flushInput()
    
curr_bin = []
bin_averages = []
# num_bins = 10
numReadingsInBin = 100

#PARAMETERS TO CONFIGUREcOn
MIN_CIRCLE_BINS = 10; # min number of steps needed to complete a circle 
#DIFF_CAP = 360 / MIN_CIRCLE_BINS; # max difference between circle steps 
DIFF_CAP = 120
DIFF_MIN = 5 # min number of degrees needed to turn to count as a step 

CONSEC_CIRCLE_BINS = 0; 
# roll states (increasing/ decreasing corresponds to roughly left turn/ right turning )
INCREASING = "increasing"
DECREASING = "decreasing"  
ROLL_STATE = INCREASING; # going to be Positive, Negative, or None 

# Algorithm for detecting a loop 
    # Increasing consequetively for at least MIN_CIRCLE_BINS averages
    # crosses past start point 


sleep_intervals = ["0.25", "0.5", "0.75"]
i = 0

def enter():
    time.sleep(.3)
    press('return')
    time.sleep(.3)

def play_note(): 

    midi_note = random.randint(60, 80)
    write('play ' + str(midi_note))
    enter()
    51.78

def sleepRand(): 
    sleep_i_idx = random.randint(0, 2)
    sleep_i = sleep_intervals[sleep_i_idx]
    write('sleep ' + sleep_i)
    enter()
    
    
def write_loop(): 
    write("live loop :" + str(i) + " do")
    enter()
    midi_note = random.randint(60, 80)
    write('play ' + str(midi_note))
    enter()

    sleepRand();

    write('end')
    enter()

    i += 1

def do_times(n): 
    write("use_random_seed " + str(n))
    enter()
    write(str(n) + ".times do")
    enter()
    write("play (scale :e3, :minor_pentatonic).pick, release: 0.1")
    time.sleep(1)
    enter()
    write("sleep 0.125")
    enter()
    write("end")
    enter()
    run_script()

def run_script(): 
    hotkey("alt", "r")

def stop_script(): 
    hotkey("alt", "s")
    
            
def detectedCircle():
    print("\n\n***********************************************************")
    print("\n\n DETECTED CIRCLE !!! \n\n")
    print("************************************************************\n\n")
    play_note()
    sleepRand()
    run_script()
    # reset circle tracking 
    CONSEC_CIRCLE_BINS = 0
    circle_start = bin_averages[len(bin_averages)-1]
    
def isNeg(n):
    return n < 0
def isPos(n): 
    return n >= 0
def isAtEdge(n1, n2):
    if(n1 >= 180-DIFF_CAP and n2 <= -180 + DIFF_CAP) or (n1 <= -180 + DIFF_CAP and n2 >= 180-DIFF_CAP):
            return True;
    else: 
        return False; 
        
    
def checkForCircle():
    if(len(curr_bin) > 1):
            global CONSEC_CIRCLE_BINS
            global ROLL_STATE
            prev_bin = curr_bin[len(curr_bin)-2]
            now_bin = curr_bin[len(curr_bin)-1]
            if(isAtEdge(prev_bin, now_bin) and isNeg(prev_bin)):
                print("is at edge - dec")
                
                rel_to_last = DECREASING
                diff_from_last = (180 + prev_bin) +  (180 - now_bin) 
                
                print(ROLL_STATE == rel_to_last)
                print("diff to last" + str(diff_from_last))
            elif(isAtEdge(prev_bin, now_bin) and isPos(prev_bin)):
                print("is at edge - inc")
                rel_to_last = INCREASING
                diff_from_last = (180 + now_bin) +  (180 - prev_bin) 
                print("diff to last" + str(diff_from_last))
                print(ROLL_STATE == rel_to_last)
            else:
                diff_from_last = prev_bin - now_bin
                if(diff_from_last < 0):
                    rel_to_last = INCREASING
                else:
                    rel_to_last = DECREASING
            
            if(abs(diff_from_last) <= DIFF_CAP and  abs(diff_from_last) >= DIFF_MIN):
                print("consec circle bins: " + str(CONSEC_CIRCLE_BINS))
                CONSEC_CIRCLE_BINS += 1
            else:
                if(CONSEC_CIRCLE_BINS >= MIN_CIRCLE_BINS):
                    do_times(CONSEC_CIRCLE_BINS)
                # reset circle tracking 
                ROLL_STATE = rel_to_last  
                CONSEC_CIRCLE_BINS = 0
                circle_start = curr_bin[len(bin_averages)-1]

    
rnum = 0
ii = 0

while 1: 
    try: 
        x=ser.readline().strip()
        #val = x.decode('utf-8')
        #print(x)
        val = float(x)
    except ValueError: 
       print("value error!")
       continue
    
    #print(val)
    #print(str(rnum) + ", " +  str(val))
    rnum += 1
    rel_to_last = None; 
    diff_from_last = None; 
    if(ii % numReadingsInBin == 0):
        #average = round(sum(curr_bin)/len(curr_bin), 2)
        #print(average)
        #print(val)
        #bin_averages.append(average)
        curr_bin.append(val)
        checkForCircle()
    #else: 
        #curr_bin.append(round(float(val), 2))
        
    ii = ii + 1
        





