
import numpy as np
import matplotlib.pyplot as plt

#%% INITIALIZATION

min_voltage = 0 # [V]
max_voltage = 8 # [V]
num_bits = 8

resolution = (max_voltage-min_voltage)/2**num_bits

range_voltage = np.zeros((num_bits,1))
range_voltage[0] = max_voltage/2
for ii in range(1,num_bits):
    range_voltage[ii] = range_voltage[ii-1]/2
    
#%% CALCULATION VALUES

def ADC(analogue,range_voltage,num_bits):
    '''
    This function transforms an analogue signal into a binary number. 
    Parameters
    ----------
    analogue : number that we want to digitalize.
    range_voltage : voltage values represented by the bits.
    num_bits : Tnumber of bits used to store the data.

    Returns
    -------
    digital_number : number in binary code
    analogue_approx : approximation of the analogue value with the given 
                      resolution
    QE : approximation error (absolute)
    '''
    digital_number= np.zeros((num_bits,1))
    analogue_approx = range_voltage.copy()[0]
    for ii in range(0,num_bits):  
            if analogue > analogue_approx:
                digital_number[ii] = 1
                if ii == 0: #first value
                    analogue_approx += range_voltage[ii+1]
                    
                elif ii== num_bits-1: #last value
                    analogue_approx += 0
                else: #values in the middle
                    analogue_approx += range_voltage[ii+1]
            else:
                digital_number[ii] = 0
                if ii == 0:
                    analogue_approx = 0
                    analogue_approx += range_voltage[ii+1]
                elif ii== num_bits-1:
                    analogue_approx = analogue_approx-range_voltage[ii]
                else:
                    analogue_approx = analogue_approx-range_voltage[ii+1]
                
    QE = np.abs(analogue-analogue_approx)
    return digital_number.flatten(),analogue_approx,QE

#%% MAIN
analogue = [1.00, 6.65, 4.68, 4.40, 7.34, 2.29, 6.00, 6.03, 3.04, 8.00]

digital_number = np.zeros((len(analogue),8))
analogue_approx = np.zeros((len(analogue),1))
QE = np.zeros((len(analogue),1))
for ii in range(0,len(analogue)):
    digital_number[ii],analogue_approx[ii],QE[ii] = ADC(analogue[ii],range_voltage,num_bits)
        
