from simple_rpc import Interface
import time
import datetime
from threading import Lock, Thread
from HybCouponClass import Coupon

########### INSTRUCTIONS ON HOW TO PASS ARGUMENTS #############

###selctHybMixing
    #to change the mixduration pass integer in minutes
    #to selectHybMixing

###cooldown
    #to change cooldown duration pass integer in seconds
    #to cooldown()

###picodeRetention
    #to change syringe steps in picodeRetention
    #pass integer indicating steps

###wash
    #you can adjust cycles number change variable to desired cycle count
    #adjust the washduration by passing integer value in minutes
    #adjust the picode retention syringe step by adjusting stepdist 

###############################################################

c1 = Coupon()

def hybonly():
    c1.selectHybMixing(mixduration = 20)
    c1.cooldown(duration = 300)
    c1.picodeRetention(steps = 3250)
    c1.reset()

def hybAndWash():
    c1.selectHybMixing(mixduration = 20)
    c1.cooldown(duration = 300)
    c1.picodeRetention(steps = 3250)
    c1.wash(cycles = 3 , washduration = 2, stepdist = 1625)
    c1.reset()




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
