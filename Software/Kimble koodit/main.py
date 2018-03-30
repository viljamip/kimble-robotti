import hardware

def main():
    hardware.homing()
    hardware.kuvaAsento()
    kamera.kalibroiPerspektiivi()
    hardware.valo(true)
    
    while True:
        if (nappi == True):
            hardware.valo(false)
            peli.pelaa()
            hardware.valo(true)
            
            #Mahdollinen odotus looppiin, ehka tarpeeton. Aika ilmeisesti sekunteina.
            #time.sleep(1)    
    
    return