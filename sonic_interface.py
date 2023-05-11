from pyautogui import press, typewrite, hotkey, write, keyUp, press
import time
import random 
import struct
import time 
import serial 

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)
f = open(current_time, "a")

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

def print_time():
    current_time = time.strftime("%H:%M:%S", t)  
    f.write(current_time + ":")

#SONIC PI EXECUATABLES 

def run_script(): 
    hotkey("alt", "r")
    print_time()
    f.write("alt r\n")

def stop_script(): 
    hotkey("alt", "s")
    print_time()
    f.write("alt s\n")
    
def clear_script():
    hotkey("alt", "a")
    print_time()   
    f.write("alt a\n") 
    time.sleep(.3)
    press('delete')
    print_time() 
    f.write("delete\n")
    time.sleep(1)

def enter():
    time.sleep(.3)
    press('return')
    print_time() 
    f.write("return\n")
    time.sleep(.3)

def switch_buffer(n):
    hotkey("alt", "shift", n)
    f.write("alt shift n\n")

def play_note(b): 
    if(b):
        write('use_synth :blade')
        print_time() 
        f.write("use_synth :blade")
        enter()
    else:
        write('use_synth :organ_tonewheel')
        print_time() 
        f.write('use_synth :organ_tonewheel')
        enter()
        
    enter()
    print_time() 
    f.write("enter\n")
    midi_note = random.randint(60, 80)
    write('play ' + str(midi_note))
    print_time() 
    f.write("play " + str(midi_note)+"\n")
    enter()
    print_time() 
    f.write("enter\n")
    sleepRand()
    run_script()

def sleepRand(): 
    sleep_i_idx = random.randint(0, 2)
    sleep_i = sleep_intervals[sleep_i_idx]
    write('sleep ' + sleep_i)
    print_time() 
    f.write("sleep " + sleep_i + "\n")
    enter()
    print_time() 
    f.write("enter\n")
    
    
def write_loop(b): 
    switch_buffer(MAIN_BUFFER)
    global i
    write("live_loop :loop" + str(i) + " do")
    print_time()     
    f.write("live loop :" + str(i) + " do\n")
    enter()
    print_time() 
    f.write("enter\n")
    midi_note = random.randint(60, 80)
    if(b):
        write("sample :drum_bass_hard")
        enter()
    else: 
        write("sample :drum_cymbal_closed")
        enter()
    print_time() 
    f.write("sample :drum_bass_hard")
    time.sleep(.3)
    enter()
    print_time() 
    f.write("enter\n")
    sleepRand();

    write('end')
    print_time() 
    f.write("end\n")
    enter()
    print_time() 
    f.write("enter\n")
    i += 1
    run_script()

def write_if(command):
    print("write_if") 
    switch_buffer(IF_BUFFER)
    time.sleep(.3)
    hotkey('ctrl', 'k')
    print_time() 
    f.write("ctrl k\n")
    time.sleep(.3)
    write(command + " =true")
    print_time() 
    f.write("command = true\n")
    enter()
    f.write("enter")
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
    print_time() 
    f.write("use_random_seed " + str(n) + "\n")
    time.sleep(.3)
    enter()
    print_time() 
    f.write("enter\n")
    write(str(n) + ".times do")
    print_time() 
    f.write(str(n) + ".times do\n")
    enter()
    print_time() 
    f.write("enter\n")
    write("play (scale :e3, :minor_pentatonic).pick, release: 0.1")
    print_time() 
    f.write("play (scale :e3, :minor_pentatonic).pick, release: 0.1\n")
    time.sleep(1)
    enter()
    print_time() 
    f.write("enter\n")
    sleepRand()
    enter()
    print_time() 
    f.write("enter\n")
    write("end")
    print_time() 
    f.write("end\n")
    enter()
    print_time() 
    f.write("enter\n")
    run_script()   
    
rnum = 0
ii = 0
drum_type = True

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
            print("detected ", CIRCLE, " ->  DO TIMES")
            do_times(magnitude)
        if(command == UP_JUMP):
            print("detected ", UP_JUMP, " -> CLEAR CODE")
            write_loop(drum_type)
            drum_type = not drum_type
            #if_statement = NONE
            #clear_script()
            
        if(command == SIDE_JUMP):
            print("detected ", SIDE_JUMP, " -> if:" + if_statement, " , ic: ", if_statement_conditional)
            play_note(True)
           #if if_statement == STARTED:
               #if_statement = IMPLEMENTED
               #if_statement_conditional = SIDE_JUMP
               #write_if(SIDE_JUMP)
            #elif if_statement == IMPLEMENTED and if_statement_conditional == SIDE_JUMP:
                #write_if_conditional(SIDE_JUMP)
            #else: 
                #print("")
        if(command == FORWARD_JUMP):
            print("detected ", FORWARD_JUMP, " -> " + if_statement, " , ic: ", if_statement_conditional)
            play_note(False)
            #if if_statement == STARTED:
                #if_statement = IMPLEMENTED
                #if_statement_conditional = FORWARD_JUMP
                #write_if(FORWARD_JUMP)
            #elif if_statement == IMPLEMENTED and if_statement_conditional == FORWARD_JUMP:
                #write_if_conditional(FORWARD_JUMP)
            #else: 
                #print("")
            
        if(command == RIGHT_BEND):
            print("detected ", RIGHT_BEND, " -> IF STATEMENT")
            run_script()
            
        if(command == LEFT_BEND):
            print("detected ", LEFT_BEND, " -> STOP")
            clear_script()
            stop_script()
            started = False
                
        
        
    ii = ii + 1
        





