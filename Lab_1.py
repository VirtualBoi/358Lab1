import random
import math
from struct import pack
from tabnanny import check

#Defined by Qiuestion
lambda1 = 75  #rate parameter, Average number of packets generated /arrived (packets per second)
L = 2000          #Average length of a packet in bits.
C = 1000000         #The transmission rate of the output link in bits per second.
rho = L*lambda1/C         #Utilization of the queue (= input rate/service rate = L λ/C)
alpha = 60/((1/lambda1)/5)      #Average number of observer events per second
check_period = (1/lambda1)/5

queue = []

E_N = 0                         #Average number of packets in the buffer/queue
P_idle = 0                      #The proportion of time the server is idle, i.e., no packets in the queue nor a packet is being transmitted.
P_loss = 0                      #The packet loss probability (for M/M/1/K queue). It is the ratio of the total number of packets lost due to buffer full condition to the total number of generated packets

#debugging vars, get rid of for final version
check_count = 0
observe_count = 0
average_arrival_time = 0
average_service_time = 0
average_queue_size_sum = 0
num_of_packets = 0
packets_lost = 0
last_check_timestamp = 0

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

#funciton holding the main DES algorithm    T = # of ticks -> how long the fn runs
#                                        size = size of queue
def DES(size_of_queue, T): 
    global num_of_packets
    global average_arrival_time
    global average_service_time
    global P_idle
    global packets_lost

    tick_count = 0
    tick_increment = 0.00001
    current_packet = rand_return(0)
    time_of_last_check = 0
    is_empty = True

    while tick_count <= T:                                  #---main loop---
        if arrival_check(tick_count, current_packet):
            if len(queue) < size_of_queue:
                add_to_queue(current_packet, tick_count)
            else:
                packets_lost += 1
                #print("---PACKET LOST--- Size of queue", len(queue))

            is_empty = False
            current_packet = rand_return(tick_count) #create new packet, assuming the current one has "arrived"
            num_of_packets += 1
            average_arrival_time += current_packet.RV_A_length
            average_service_time += current_packet.RV_length

        if departure_check(tick_count):
            if not queue:
                is_empty = True

        if observer_check(tick_count, time_of_last_check):
            time_of_last_check = tick_count

        if is_empty:
            P_idle += tick_increment

        tick_count += tick_increment
    
    P_idle = P_idle/T
    P_loss = packets_lost/num_of_packets
    #print("average arrival wait time: ", average_arrival_time/num_of_packets)
    #print("average service wait time: ", average_service_time/num_of_packets)
    #print("check - arrival ratio: ", check_count/num_of_packets)

    #print("E[n]: ", average_queue_size_sum/observe_count) #Question 3a and 6a
    #print(P_idle) #Question 3b
    #print("num of losses: ", packets_lost)
    #print("total num of packets: ", num_of_packets)
    #print(P_loss) #Question 6b


def arrival_check(tick_count, packet):
    if tick_count >= packet.A_time:
        #print ("ARRIVED:  ", tick_count)
        return True

    return False

def departure_check(tick_count):

    if queue:
        if tick_count >= queue[0].D_time:
            #print ("DEPARTED: ", tick_count, " size of queue: ", len(queue))
            queue.pop(0)
            return(True)

    return (False)

def observer_check(tick_count, time_of_last_check):
    global average_queue_size_sum
    global observe_count

    if tick_count >= (time_of_last_check + check_period):
        average_queue_size_sum += len(queue)
        observe_count += 1
        #print ("CHECK at Tick: ", tick_count)
        return (True)
    
    return(False)

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
    rand_num = rand_return(0)
    queue = 0
    while count > 1:
        rand_num = rand_return(0)
        mean += rand_num.A_time
        var = var + pow(rand_num.A_time - 1/lambda1, 2) 
        count -= 1
    print ("Expected mean: ", 1/lambda1)
    print ("Mean: ", mean/1000)
    print ("Expected variance: ", 1/(lambda1**2))
    print ("Variance",  var/1000)

#question_1()    
#DES(100, 2)
#DES(50, 100)