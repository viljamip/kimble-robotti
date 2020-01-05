import hardware
import peli
import kamera
import RPi.GPIO as GPIO

def main():
    hardware.openSerial()
    hardware.homing()
    
    hardware.kuvaAsento()
    kamera.kalibroiPerspektiivi()
    hardware.peliAsento()
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set 
    
    while True:
        
        #syote = input("Haluatko jatkaa?\n")
        while True:
            if GPIO.input(40) == GPIO.LOW:
                print('Button pressed')
                break
        '''
        if (syote == 'Q'):
            break
        if syote == 'H':
            hardware.homing()
        '''
        hardware.valo(False)
        peli.pelaa()
        hardware.valo(True)
        #Mahdollinen odotus looppiin, ehka tarpeeton. Aika ilmeisesti sekunteina.
        #time.sleep(1)    
    
    return
main()
hardware.closeSerial()
