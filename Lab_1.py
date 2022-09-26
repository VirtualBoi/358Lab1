import random
import math


#Defined by Qiuestion
lambda1 = 75  #rate parameter, Average number of packets generated /arrived (packets per second)
L = 2000          #Average length of a packet in bits.
C = 1000000         #The transmission rate of the output link in bits per second.
rho = 0         #Utilization of the queue (= input rate/service rate = L λ/C)

#
alpha = 0      #Average number of observer events per second
E_N = 0         #Average number of packets in the buffer/queue
P_idle = 0      #The proportion of time the server is idle, i.e., no packets in the queue nor a packet is being transmitted.
P_loss = 0      #The packet loss probability (for M/M/1/K queue). It is the ratio of the total number of packets lost due to buffer full condition to the total number of generated packets

class packet:
    RV_A_time = 0
    RV_size = 0
    size = 0 #size in bits
    A_time = 0 #Arrival time
    S_time = 0 #Service time
    D_time = 0 #Departure time

def rand_return():
    U = random.uniform(0, 1) #uniform random variable
    return -(1/lambda1) * math.log(1 - U) #exponential random variable


def no_queue():
    print ("NO QUEUE")

def infinite_queue():
    print ("INFINITE QUEUE")

def question_1():
    count = 1000
    mean = 0
    var = 0
    rand_num = 0
    print ("NO QUEUE")
    while(count > 1):
        rand_num = rand_return()
        mean += rand_num
        var = var + pow(rand_num - 1/lambda1, 2) 
        count -= 1
    print ("mean: ", mean/1000)
    print ("Variance",  var/1000)

question_1()    
#no_queue()
#infinite_queue()