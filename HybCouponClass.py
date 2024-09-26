from simple_rpc import Interface
import time
import datetime
from threading import Lock, Thread

class Coupon:
    def setSpeed(self, speed ):
        arduino.lock.acquire( timeout = 2 )
        try:
            ret = arduino.setSpeed( speed )
        finally:
            arduino.lock.release()
    def setgoal(self, steps ):
        arduino.lock.acquire( timeout = 2 )
        try:
            ret = arduino.setGoal(steps)
        finally:
            arduino.lock.release()


    #half stroke workflow
    def halfStroke(self, mixduration = 20):
        print("Start Half Stroke")
        print("Duration of mixing in minutes will be: ", mixduration)
        
        self.setSpeed(1000)
        self.setgoal(0)

        t_end = time.time() + (mixduration * 60)

        #20minute shuttle mix
        while time.time() < t_end:
        
            try:   
                self.setgoal(0)
                self.setgoal(900) 
                time.sleep(3)
                self.setgoal(0)
                time.sleep(3.5)
            
            except KeyboardInterrupt as ke:
                print ("stopping")
                break
            
        self.setgoal(0)
        print("End Half Stroke")

    #quarter stroke workflow
    def quarterStroke(self, mixduration = 20):
        print("Start quarter Stroke")
        print("Duration of mixing in minutes will be: ", mixduration)
        
        self.setSpeed(1000)
        self.setgoal(0)
        
        t_end = time.time() + (mixduration * 60)

        #20minute shuttle mix
        while time.time() < t_end:
        
            try:   
                self.setgoal(0)
                time.sleep(2)
                self.setgoal(600)
                time.sleep(2)
                self.setgoal(0)
                time.sleep(2)
                self.setgoal(-600)
                time.sleep(2)
        
            except KeyboardInterrupt as ke:
                print ("stopping")
                break
            
        self.setgoal(0)
        print("End quarter Stroke")


    def cooldown(self, duration = 300):
        input("Remove Coupon. Cool down for 5 minutes - input random keystroke to start timer")
        print("cooldown duration in seconds: ", duration)
        time.sleep(duration)

    #picode retention protocol
    def picodeRetention(self, strokedist = 3250):
        self.setSpeed(350)
        input("Place coupon on magnet")
        print("Stroke distance is set to : ", strokedist)

        for i in range(5):
            try:
                self.setgoal(strokedist)
                time.sleep(10)
                self.setgoal(0)
                time.sleep(10)

            except KeyboardInterrupt as ke:
                print ("stopping")
                break
        print("Picode retention done")

    def reset(self):
        input("Disconnect syringe pump  - input random keystroke to continue")
        self.setSpeed(1000)
        self.setgoal(0)
        arduino.close()
        print("Reset complete")

    def selectHybMixing(self, duration = 20):
        print("mixing duration in minutes :", duration)
        while True:
            userin = input("Input 1 for Halfstroke, input 2 for Quarter Stroke")
            if userin == "1":
                print("Selected : 1 aka HALF STROKE")
                self.halfStroke(duration)
                break
            elif userin == "2":
                print("Selected : 2 aka QUARTER STROKE")
                self.quarterStroke(duration)
                break
            else:
                print("incorrect input, try again")

    def wash(self, cycles = 3 , washduration = 2, stepdist = 1625):
        print("remove hybmix from coupon and replace with 150uL of Wash buffer")
        print("remove coupon from magnet")
        for i in range (cycles):
            print("This is the start of cycle: ", i + 1)
            input("press any key when ready to begin the wash cycle")
            self.quarterStroke(washduration)
            print("Start picode retention within wash")
            self.picodeRetention(stepdist)
            print("remove wash buffer and replace with fresh washbuffer")
            print("remove coupon from magnet")

        print("washing completed")
                        
