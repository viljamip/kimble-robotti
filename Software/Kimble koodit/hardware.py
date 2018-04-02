import serial
import time
import kamera

koordinaatit = [(-3.5, -139.5), (-9.48, -139.4), (-15.8, -135.2), (-22.28, -132.0), (-28.8, -135.1), (-35.0, -138.9), (-41.12, -138.7), (-47.28, -138.4), (-53.36, -138.5), (-59.88, -134.4), (-66.28, -131.3), (-72.76, -134.5), (-79.08, -138.4), (-85.2, -138.3), (-91.4, -138.2), (-97.6, -138.3), (-103.88, -134.3), (-110.28, -131.3), (-116.8, -134.3), (-123.2, -138.7), (-129.28, -138.7), (-135.48, -138.9), (-141.68, -138.8), (-148.08, -134.9), (-154.56, -131.7), (-160.96, -135.0), (-167.16, -139.2), (-173.36, -139.2), (-176.36, -125.1), (-176.36, -106.6), (-176.36, -87.7), (-176.36, -69.1), (5.24, -158.3), (1.64, -158.1), (-2.08, -158.0), (-5.76, -157.9), (-38.68, -157.8), (-42.36, -157.6), (-46.16, -157.6), (-49.88, -157.4), (-82.76, -157.2), (-86.48, -157.4), (-90.16, -157.4), (-93.96, -157.2), (-126.76, -157.2), (-130.56, -157.4), (-134.28, -157.4), (-137.96, -157.3), (-132.56, -124.4), (-132.56, -105.7), (-132.56, -87.2), (-132.56, -68.5), (-44.16, -124.6), (-44.16, -105.9), (-44.16, -87.2), (-44.16, -68.5), (-88.36, -124.4), (-88.36, -105.8), (-88.36, -86.8), (-88.36, -68.2)]

kierroksenPituus = 176


def openSerial():
    global s
    s = serial.Serial("/dev/cu.usbserial-DN03VXGO",115200) #/dev/cu.usbserial-DN03VXGO 
    return 1

def closeSerial():
    s.close()
    
def homing():
    # Open grbl serial port
    homing = '$H'
    wakeupcall = '?'
    #Wake up grbl
    lahetaGcode(wakeupcall)
    time.sleep(1)   # Wait for grbl to initialize 
    lahetaGcode(homing)
    odotaPysahtymista()
    return

def kuvaAsento(kaannettu180=False):
    if kaannettu180:
        asento = 'G1 X110 Y-174 Z-1 F8000' 
    else:
        asento = 'G1 X22 Y-174 Z-1 F8000' 
    lahetaGcode(asento)
    return 1

def peliAsento():
    asento = 'G1 X0 Y-174 Z-1 F8000'
    lahetaGcode(asento)
    valo(True)
    return

def painaNoppaa():
    # Ajetaan nopan paalle
    siirto = 'G1 Y0 Z-1 F8000'
    lahetaGcode(siirto)  
    
    #painetaan noppaa
    siirto = 'G1  Z-20 F4000'
    lahetaGcode(siirto)
    siirto = 'G1  Z-27 F1000'
    lahetaGcode(siirto)
    siirto = 'G1  Z-1 F4000'
    lahetaGcode(siirto)
    return 1

def lahetaGcode(koodi):
    # Tämä lisää tai vähentää yhden kierroksen pituuden X:ään, jos matka on siten lyhyempi
    if "X" in koodi:
        muokattuKoodi = koodi.split("X")
        alku = muokattuKoodi[0]
        loppu = muokattuKoodi[1]
        spaceIndex = loppu.find(" ")
        if spaceIndex>-1:
            x = loppu[0:spaceIndex]
            loppuloppu = loppu[spaceIndex:]
            xNum = float(x)
            nykyinenX = kerroX()
            
            if(abs(xNum - (nykyinenX + kierroksenPituus)) < abs(xNum - nykyinenX)):
                xNum -= kierroksenPituus
            elif(abs(xNum - (nykyinenX - kierroksenPituus)) < abs(xNum - nykyinenX)):
                xNum += kierroksenPituus
            
            uusi = '{0}X{1}{2}'.format(alku,xNum,loppuloppu)
            koodi = uusi
            
    #print("lähetetään: {0}".format(koodi))
    s.write('{0}\n'.format(koodi).encode('utf-8'))
    s.flushInput()
    grbl_out = s.readline()
    #print(" Vastaus" , grbl_out.strip())
    
def odotaPysahtymista():
    valmis = False
    count = 0
    while(not valmis):
        time.sleep(0.1)
        s.write('?'.encode('utf-8'))
        s.flushInput()
        grbl_out = s.readline()
        valmis = "Idle" in str(grbl_out)
        if not valmis:
            count = count + 1
    #print('odotuksen wait-määrä {0}'.format(count))
    if count>0:
        time.sleep(1)
        
def kerroX():
    s.write('?'.encode('utf-8'))
    s.flushInput()
    grbl_out = s.readline() # <Run|MPos:-58.080,-173.000,-2.000|FS:840,0>
    asento = str(grbl_out).split("MPos:")
    x = asento[1].split(",")
    return float(x[0])

def siirra(i1,i2):
    print(koordinaatit[i1][0])
    xAlku = koordinaatit[i1][0]
    yAlku = koordinaatit[i1][1]
    xLoppu = koordinaatit[i2][0]
    yLoppu = koordinaatit[i2][1] 

    zYlos = 'G1 Z-1 F4000'
    lahetaGcode(zYlos)

    nappaa = 'G1 X{} Y{} F8000'.format(xAlku, yAlku)
    laske  = 'G1 X{} Y{} F8000'.format(xLoppu, yLoppu)
    
    #Haetaan nappi
    lahetaGcode(nappaa)
    lahetaGcode('G1 Z-32 F4000')
    lahetaGcode('M8')
    lahetaGcode('G1 Z-1 F4000')
    
    #pudotetaan nappi
    lahetaGcode(laske)
    lahetaGcode('G1 Z-32 F4000')
    lahetaGcode('M9')
    lahetaGcode('G1 Z-1 F4000')
    
    return
 
def valo(paalla):
    if paalla:
            lahetaGcode('M3 S1000')
    else:
            lahetaGcode('M5')
    return


#openSerial()
#homing()
#valo(True)
#painaNoppaa()
#valo(False)
#siirra(31, 49)
#closeSerial()
