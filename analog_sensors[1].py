import time
import RPi.GPIO as GPIO
import spidev

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=5000

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))#-50 40
  temp = round(temp,places)
  return temp

def SENSOR_TEMP():
    temp_level = ReadChannel(0)
    temp_volts = ConvertVolts(temp_level,2)
    temp       = ConvertTemp(temp_level,2)
    temp = temp+10;
    print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))

def SENSOR_ECG():
    ecg_level = ReadChannel(0)
    print("ECG : {}".format(ecg_level))      


while 1:

  SENSOR_TEMP()
  SENSOR_ECG()

  time.sleep(1)
