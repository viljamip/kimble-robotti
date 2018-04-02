import hardware
import peli
import kamera




def main():
    hardware.openSerial()
    hardware.homing()
    
    hardware.kuvaAsento()
    kamera.kalibroiPerspektiivi()
    hardware.peliAsento()
    
    while True:
        
        syote = input("Haluatko jatkaa?\n")
        if (syote == 'Q'):
            break
        if syote == 'H':
            hardware.homing()
        
        hardware.valo(False)
        peli.pelaa()
        hardware.valo(True)
        #Mahdollinen odotus looppiin, ehka tarpeeton. Aika ilmeisesti sekunteina.
        #time.sleep(1)    
    
    return
main()
hardware.closeSerial()
