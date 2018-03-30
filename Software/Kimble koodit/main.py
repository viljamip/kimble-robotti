import hardware
import peli
import kamera




def main():
    hardware.openSerial()
    hardware.homing()
    
    
    hardware.kuvaAsento()
    kamera.kalibroiPerspektiivi()
    hardware.valo(True)
    
    while True:
        
        
        
        syote = input("Haluatko jatkaa?")
        if (syote == 'Q'):
            break
        
        hardware.valo(False)
        peli.pelaa()
        hardware.valo(True)
        '''
        if (nappi == True):
            hardware.valo(false)
            peli.pelaa()
            hardware.valo(true)
            '''
            #Mahdollinen odotus looppiin, ehka tarpeeton. Aika ilmeisesti sekunteina.
            #time.sleep(1)    
    
    return
main()
hardware.closeSerial()