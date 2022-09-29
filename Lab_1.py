import random
import math

#Defined by Qiuestion
lambda1 = 75  #rate parameter, Average number of packets generated /arrived (packets per second)
L = 2000          #Average length of a packet in bits.
C = 1000000         #The transmission rate of the output link in bits per second.
rho = 0         #Utilization of the queue (= input rate/service rate = L λ/C)
alpha = 60/((1/lambda1)/5)      #Average number of observer events per second

queue = []

E_N = 0                         #Average number of packets in the buffer/queue
P_idle = 0                      #The proportion of time the server is idle, i.e., no packets in the queue nor a packet is being transmitted.
P_loss = 0                      #The packet loss probability (for M/M/1/K queue). It is the ratio of the total number of packets lost due to buffer full condition to the total number of generated packets

class packet(object):
     #calculate and populate the bellow variables on creation of packet
     def __init__(self, RV_A_length, RV_length, tick_count):
        self.RV_A_length = RV_A_length #random time taken to arrive
        self.RV_length = RV_length #random length of packet
        self.A_time = tick_count + RV_A_length #Arrival time
        self.service_length = RV_length/C #Service time
        self.D_time = 0 #Departure time

def rand_return(tick_count):
    U = random.uniform(0, 1) #uniform random variable (for arrival time)
    V = random.uniform(0, 1) #uniform random variable (for size)
    return packet(-(1/lambda1) * math.log(1 - U), -(1/(1/L)) * math.log(1 - V), tick_count)

def DES(size, T): #funciton holding the main DES algorithm T = 
    tick_count = 0
    tick_increment = 0.00001
    current_packet = rand_return(0)

    while tick_count <= T:
        if arrival_check(tick_count, current_packet):
            add_to_queue(current_packet)
            current_packet = rand_return(tick_count)

        departure_check(tick_count, current_packet)
        observer_check(tick_count)
        tick_count += tick_increment

        #calculate E[N], P_idle, P_loss
        if not queue:
            P_idle += tick_increment


def arrival_check(tick_count, packet):
    if tick_count == packet.A_time:
        print ("ARRIVED")
        return True

    return False

def departure_check(tick_count, packet):
    if tick_count == packet.D_time:
        print ("DEPARTED")

def observer_check(tick_count):
    if tick_count % ((1/lambda1)/5):
        print ("CHECk")

def add_to_queue(packet, tick_count):
    sum = 0
    queue.append(packet)

    for p in queue:
        sum += p.service_length
    sum += tick_count

    queue[-1].D_time = sum

def question_1():
    count = 1000
    mean = 0
    var = 0
    rand_num = 0
    queue = 0
    while count > 1:
        rand_num = rand_return()
        mean += rand_num
        var = var + pow(rand_num - 1/lambda1, 2) 
        count -= 1
    print ("Expected mean: ", 1/lambda1)
    print ("Mean: ", mean/1000)
    print ("Expected variance: ", 1/(lambda1**2))
    print ("Variance",  var/1000)

#question_1()    
#DES(math.inf, 2)
#DES(X, 2)