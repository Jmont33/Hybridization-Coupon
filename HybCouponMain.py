from simple_rpc import Interface
import time
import datetime
from threading import Lock, Thread

def setSpeed( speed ):
    arduino.lock.acquire( timeout = 2 )
    try:
        ret = arduino.setSpeed( speed );
    finally:
        arduino.lock.release()
def setGoal( steps ):
    arduino.lock.acquire( timeout = 2 )
    try:
        ret = arduino.setGoal(steps)
    finally:
        arduino.lock.release()


#half stroke workflow
def halfStroke(mixduration = 20):
    print("Start Half Stroke")
    print("Duration of mixing in minutes will be: ", mixduration)
    
    setSpeed(1000)
    setGoal(0)

    t_end = time.time() + (mixduration * 60)

    #20minute shuttle mix
    while time.time() < t_end:
     
        try:   
            setGoal(0)
            setGoal(900) 
            time.sleep(3)
            setGoal(0)
            time.sleep(3.5)
        
        except KeyboardInterrupt as ke:
            print ("stopping")
            break
        
    setGoal(0)
    print("End Half Stroke")

#quarter stroke workflow
def quarterStroke(mixduration = 20):
    print("Start quarter Stroke")
    print("Duration of mixing in minutes will be: ", mixduration)
    
    setSpeed(1000)
    setGoal(0)
    
    t_end = time.time() + (mixduration * 60)

    #20minute shuttle mix
    while time.time() < t_end:
     
        try:   
            setGoal(0)
            time.sleep(2)
            setGoal(600)
            time.sleep(2)
            setGoal(0)
            time.sleep(2)
            setGoal(-600)
            time.sleep(2)
    
        except KeyboardInterrupt as ke:
            print ("stopping")
            break
        
    setGoal(0)
    print("End quarter Stroke")


def cooldown(duration = 300):
    input("Remove Coupon. Cool down for 5 minutes - input random keystroke to start timer")
    print("cooldown duration in seconds: ", duration)
    time.sleep(duration)

#picode retention protocol
def picodeRetention(strokedist = 3250):
    setSpeed(350)
    input("Place coupon on magnet")
    print("Stroke distance is set to : ", strokedist)

    for i in range(5):
        try:
            setGoal(strokedist)
            time.sleep(10)
            setGoal(0)
            time.sleep(10)

        except KeyboardInterrupt as ke:
            print ("stopping")
            break
    print("Picode retention done")

def reset():
    input("Disconnect syringe pump  - input random keystroke to continue")
    setSpeed(1000)
    setGoal(0)
    arduino.close()
    print("Reset complete")

def selectHybMixing(duration = 20):
    print("mixing duration in minutes :", duration)
    while True:
        userin = input("Input 1 for Halfstroke, input 2 for Quarter Stroke")
        if userin == "1":
            print("Selected : 1 aka HALF STROKE")
            halfStroke(duration)
            break
        elif userin == "2":
            print("Selected : 2 aka QUARTER STROKE")
            quarterStroke(duration)
            break
        else:
            print("incorrect input, try again")

def wash(cycles = 3 , washduration = 2):
    print("remove hybmix from coupon and replace with 150uL of Wash buffer")
    print("remove coupon from magnet")
    for i in range (cycles):
        print("This is the start of cycle: ", i + 1)
        input("press any key when ready to begin the wash cycle")
        quarterStroke(washduration)
        print("Start picode retention within wash")
        picodeRetention(strokedist = 1625)
        print("remove wash buffer and replace with fresh washbuffer")
        print("remove coupon from magnet")

    print("washing completed")
                      
def hybonly():
    #to change the mixduration pass integer in minutes
    #to select hyb mixing
    selectHybMixing()
    cooldown()
    picodeRetention()
    reset()

def hybAndWash():
    selectHybMixing()
    cooldown()
    picodeRetention()
    wash()
    reset()

def main():
    hybAndWash()
    
if __name__ == '__main__':
    arduino = Interface( "/dev/ttyACM0", baudrate=115200 )
    arduino.lock = Lock()
    print("Arduino initilized")
    
    try:
        main()
    except KeyboardInterrupt as ke:
        print ("stopping")
        
        
    arduino.close()
    print("Arduino closed")
