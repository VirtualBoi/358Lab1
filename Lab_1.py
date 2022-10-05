import random
import math
import sys
from struct import pack
from tabnanny import check

#Defined by Qiuestion (default)
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
run_time = 100
question_state = ""

if len(sys.argv) != 3:
    print("Please use appropriate arguments (refer to lab report)")
    sys.exit()

else:
    question_state = sys.argv[1] #keeps track of what question we want to run 

    if sys.argv[2] == "50":
        run_time = 50

    elif sys.argv[2] == "100":
        run_time = 100

    elif sys.argv[2] == "150":
        run_time = 150

    elif sys.argv[2] == "200":
        run_time = 200
    
    else:
        print("Please enter a valid run time argument (50, 100, 150, 200). EX: 'py Lab_1.py X 100'")
        sys.exit()

print("The simulation will have a execution time of: ", run_time)

observe_count = 0
average_arrival_time = 0
average_service_time = 0
average_packet_size = 0
average_queue_size_sum = 0
num_of_packets = 0
packets_lost = 0
last_check_timestamp = 0

class packet(object):
     #calculate and populate the bellow variables on creation of packet
     def __init__(self, RV_A_length, RV_length, tick_count):
        self.RV_A_length = RV_A_length #random time taken to arrive
        self.RV_length = RV_length #random length of packet (bits)
        self.A_time = tick_count + RV_A_length #Arrival time
        self.service_length = RV_length/C #Service time
        self.D_time = 0 #Departure time

def find_parameters(lam): #used to update parameters depending on the question #
    global lambda1
    global rho
    global alpha
    global check_period

    lambda1 = lam  #rate parameter, Average number of packets generated /arrived (packets per second)
    rho = L*lambda1/C         #Utilization of the queue (= input rate/service rate = L λ/C)
    alpha = 60/((1/lambda1)/5)      #Average number of observer events per second
    check_period = (1/lambda1)/5

def rand_return(tick_count):
    U = random.uniform(0, 1) #uniform random variable (for arrival time)
    V = random.uniform(0, 1) #uniform random variable (for size)
    return packet(-(1/lambda1) * math.log(1 - U), -(1/(1/L)) * math.log(1 - V), tick_count)

#funciton holding the main network_sim algorithm    T = # of ticks -> how long the fn runs (T = 100)
#                                                size = size of queue
def network_sim(size_of_queue, T): 
    global num_of_packets
    global average_arrival_time
    global average_service_time
    global average_packet_size
    global E_N
    global P_idle
    global P_loss
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
            average_packet_size += current_packet.RV_length
            #print("---------------------------------", current_packet.RV_length)

        if departure_check(tick_count, T):
            if not queue:
                is_empty = True

        if observer_check(tick_count, time_of_last_check):
            time_of_last_check = tick_count

        if is_empty:
            P_idle += tick_increment

        tick_count += tick_increment
    
    E_N = average_queue_size_sum/observe_count
    #print ("#obs: ", observe_count)
    #print ("que sum: ", average_queue_size_sum)
    #print ("en: ", E_N)
    P_idle = P_idle/T
    P_loss = packets_lost/num_of_packets

def arrival_check(tick_count, packet):
    if tick_count >= packet.A_time:
        if question_state == "2" or question_state == "5":
            print ("ARRIVED  at Tick: ", tick_count, " new size of queue: ", len(queue) + 1)
        return True

    return False

def departure_check(tick_count, T):

    if queue:
        #print ("DEPARTing.... current d time ", queue[0].D_time)
        if tick_count >= queue[0].D_time or queue[0].D_time > T:
            queue.pop(0)
            if question_state == "2" or question_state == "5":
                print ("DEPARTED at Tick: ", tick_count, " new size of queue: ", len(queue))
            return(True)

    return (False)

def observer_check(tick_count, time_of_last_check):
    global average_queue_size_sum
    global observe_count

    if tick_count >= (time_of_last_check + check_period):
        average_queue_size_sum += len(queue)
        observe_count += 1
        if question_state == "2" or question_state == "5":
            print ("CHECK    at Tick: ", tick_count)
        return (True)
    
    return(False)

def add_to_queue(packet, tick_count):
    global average_service_time

    sum = 0
    queue.append(packet)

    for p in queue:
        sum += p.service_length

    sum += tick_count
    queue[-1].D_time = sum
    average_service_time += queue[-1].D_time - tick_count

if question_state == "1":
    count = 1000
    mean = 0
    var = 0
    rand_num = rand_return(0)

    while count > 1: #main loop - creates the specified number of randomly gnerated 
                     #packets with exponentially distrobuted arrival times
        rand_num = rand_return(0)

        #sums all arrival times for the mean and varriance calculation
        mean += rand_num.A_time
        var = var + pow(rand_num.A_time - 1/lambda1, 2) 
        count -= 1

    #outputs the theoretical and experimental mean and varriance
    print ("Expected mean:     ", 1/lambda1)
    print ("Mean:              ", mean/1000)
    print ("Expected variance: ", 1/(lambda1**2))
    print ("Variance           ",  var/1000)

elif question_state == "2": #explain infinite queue design - produces exmple timestamps and outputs metrics
    network_sim(math.inf, run_time)
    print("-------------end of sim-------------")
    print("total num of packets: ", num_of_packets)
    print("average arrival wait time: ", average_arrival_time/num_of_packets)
    print("average service wait time: ", average_service_time/num_of_packets)
    print("average packet size (bits): ", average_packet_size/num_of_packets)
    print("check - arrival ratio: ", observe_count/num_of_packets)

elif question_state == "3":
    for x in range(8):
        find_parameters (125 + 50*x)
        network_sim(math.inf, run_time)
        print("For rho = ", round(0.25 + 0.1*x, 2), " - E[n]: ", round(E_N, 2), " - P_idle: ", P_idle)
        print(round(0.25 + 0.1*x, 2), ",", round(E_N, 2), ",", P_idle)

elif question_state == "4":
    find_parameters (600)
    network_sim(math.inf, run_time)
    print("For rho = ", 1.2, " - E[n]: ", round(E_N, 2), " - P_idle: ", P_idle)

elif question_state == "5": #explain finite queue design - produces exmple timestamps and outputs metrics
    find_parameters (750)
    network_sim(10, run_time)
    print("-------------end of sim-------------")
    print("number of packets lost: ", packets_lost)
    print("total num of packets:   ", num_of_packets)
    print("P_loss:                 ", P_loss)

elif question_state == "6":
    print("For queue of 10...")
    for x in range(11):
        find_parameters (250 + 50*x)
        network_sim(10, run_time)
        print("For rho = ", round(0.5 + 0.1*x, 2), " - E[n]: ", round(E_N, 2), " - P_idle: ", P_loss)
        #print(round(0.5 + 0.1*x, 2), ",", round(E_N, 2), ",", P_loss)

    print("For queue of 25...")
    for x in range(11):
        find_parameters (250 + 50*x)
        network_sim(25, run_time)
        print("For rho = ", round(0.5 + 0.1*x, 2), " - E[n]: ", round(E_N, 2), " - P_idle: ", P_loss)
        #print(round(0.5 + 0.1*x, 2), ",", round(E_N, 2), ",", P_loss)

    print("For queue of 50...")
    for x in range(11):
        find_parameters (250 + 50*x)
        network_sim(50, run_time)
        print("For rho = ", round(0.5 + 0.1*x, 2), " - E[n]: ", round(E_N, 2), " - P_idle: ", P_loss)

elif question_state == "":
    print("Please enter a valid Q# argument (1 - 6). EX: 'py Lab_1.py 3'")

else:
    print("Please enter a valid Q# argument (1 - 6). EX: 'py Lab_1.py 3 XXX'")
