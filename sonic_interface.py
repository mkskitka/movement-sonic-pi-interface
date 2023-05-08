from pyautogui import press, typewrite, hotkey, write, keyUp, press
import time
import random 
import struct
import time 
import serial 

print("version: ")
print(serial.__version__)
print("waiting for input ...")

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
    

sleep_intervals = ["0.25", "0.5", "0.75"]
i = 0
started = False



#COMMANDS
START = "start"
STOP = "stop" 
#JUMPS 
UP_JUMP = "up_jump"
FORWARD_JUMP = "forard_jump"
SIDE_JUMP = "side_jump"
#BENDS
RIGHT_BEND = "right_bend"
LEFT_BEND = "left_bend"
#OTHER
CIRCLE ="circle"


# if statement states
NONE = "none"
STARTED = "started"
IMPLEMENTED = "implemented"
#if statement conditional options 
# FORWARD_JUMP || SIDE_JUMP 
if_statement = NONE
if_statement_conditional = NONE

IF_BUFFER = "9"
MAIN_BUFFER = "0"



#SONIC PI EXECUATABLES 

def run_script(): 
    hotkey("alt", "r")

def stop_script(): 
    hotkey("alt", "s")
    
def clear_script():
    hotkey("alt", "a")
    time.sleep(.3)
    press('delete')
    time.sleep(1)

def enter():
    time.sleep(.3)
    press('return')
    time.sleep(.3)

def switch_buffer(n):
    hotkey("alt", "shift", n)

def play_note(): 
    midi_note = random.randint(60, 80)
    writ('play ' + str(midi_note))
    enter()

def sleepRand(): 
    sleep_i_idx = random.randint(0, 2)
    sleep_i = sleep_intervals[sleep_i_idx]
    write('sleep ' + sleep_i)
    enter()
    
    
def write_loop(): 
    switch_buffer(MAIN_BUFFER)
    global i
    write("live loop :" + str(i) + " do")
    enter()
    midi_note = random.randint(60, 80)
    write('play ' + str(midi_note))
    enter()

    sleepRand();

    write('end')
    enter()

    i += 1

def write_if(command):
    print("write_if") 
    switch_buffer(IF_BUFFER)
    time.sleep(.3)
    hotkey('ctrl', 'k')
    time.sleep(.3)
    write(command + " =true")
    enter()
    write("play " + str(random.randint(50, 70)) +" , amp: 2 if " + command) 
    time.sleep(.3)
    hotkey("alt", "shift", "u")
    run_script()
    
def write_if_conditional(command):
    switch_buffer(IF_BUFFER)
    run_script()

    
    
            
    

def do_times(n): 
    switch_buffer(MAIN_BUFFER)
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
    
    
rnum = 0
ii = 0

while 1: 
    try: 
        x=ser.readline().strip()
        val = x.decode('utf-8')
        if(val == ''):
            continue
        #print(val)
        val_parsed = val.split(':')
        command = val_parsed[0]
        if(len(val_parsed) > 1):
            magnitude = float(val_parsed[1])
            
    except ValueError: 
       print("value error!")
       continue
    
    if(command == START):
        started = True
    else:
        if(command == CIRCLE):
            print("detected ", CIRCLE, " ->  FOR LOOP")
            do_times(magnitude)
        if(command == UP_JUMP):
            print("detected ", UP_JUMP, " -> CLEAR CODE")
            if_statement = NONE
            clear_script()
            
        if(command == SIDE_JUMP):
            print("detected ", SIDE_JUMP, " -> if:" + if_statement, " , ic: ", if_statement_conditional)
            if if_statement == STARTED:
                if_statement = IMPLEMENTED
                if_statement_conditional = SIDE_JUMP
                write_if(SIDE_JUMP)
            elif if_statement == IMPLEMENTED and if_statement_conditional == SIDE_JUMP:
                write_if_conditional(SIDE_JUMP)
            else: 
                print("")
        if(command == FORWARD_JUMP):
            print("detected ", FORWARD_JUMP, " -> " + if_statement, " , ic: ", if_statement_conditional)
            if if_statement == STARTED:
                if_statement = IMPLEMENTED
                if_statement_conditional = FORWARD_JUMP
                write_if(FORWARD_JUMP)
            elif if_statement == IMPLEMENTED and if_statement_conditional == FORWARD_JUMP:
                write_if_conditional(FORWARD_JUMP)
            else: 
                print("")
            
        if(command == RIGHT_BEND):
            print("detected ", RIGHT_BEND, " -> IF STATEMENT")
            if_statement = STARTED
            
        if(command == LEFT_BEND):
            print("detected ", LEFT_BEND, " -> STOP")
            clear_script()
            run_script()
            started = False
                
        
        
    ii = ii + 1
        





