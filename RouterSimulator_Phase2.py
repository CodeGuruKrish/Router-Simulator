################################Networks Border Router Simulator#############################
#Hithesh Krishnamurthy
#Saif Mohhamed
#Ameya Patil

from functools import partial
from random import randint
from time import sleep
from pylab import *
import itertools
import time
import timeit
import binascii
import sys
import operator
import ipaddr

#############################All Variables required for the simulation######################

global congestionFlag    #Congestion Flag to determine of output queue is over flooding
congestionFlag = 0
global inputCounter_a
global inputCounter_b
global inputCounter_c
global outputCounter_a
global outputCounter_b
global outputCounter_c
global lista
global listb
global listc
global forward_list0
global forward_list1
global forward_list2
global forward_list3
global forward_list4
global forward_list5
global forward_list6
global runMode
global packetlength
		
inputCounter_a = 0
inputCounter_b = 0
inputCounter_c = 0
outputCounter_a = 0
outputCounter_b = 0
outputCounter_c = 0
queue_1_a_cnt = 0
queue_1_b_cnt = 0
queue_2_a_cnt = 0
queue_2_b_cnt = 0
queue_3_a_cnt = 0
queue_3_b_cnt = 0
dropped_a = 0
dropped_b = 0
dropped_c = 0
residence_a = 0
residence_b = 0
residence_c = 0
lista = []
listb = []
listc = []
forward_list0 = []
forward_list1 = []
forward_list2 = []
forward_list3 = []
forward_list4 = []
forward_list5 = []
forward_list6 = []
outputCounter = {}


info1=[]
info2=[]
info3=[]
	    

###########Function to read the size of the first packet coming into the input link###########
def firstpackSize(filename):
   with open(filename, 'rb') as ofb:	     
		for content in iter(partial(ofb.read, 10), ''): 
			firstpacklength = content[2:4]
			if firstpacklength != '':
			   firstpacklength = int(binascii.hexlify(firstpacklength), 16)
			   return firstpacklength
			   print "First packet length: ", firstpacklength
			else:
			   return 0

##############Function to get the size of the (n+1)th packet while processing nth packet###############
def getNextPackLength(filename, chunksize):
    with open(filename, 'rb') as ofbj:	
        allContent = ofbj.read(chunksize + 10)
        nextPackSize = allContent[chunksize + 2 : chunksize + 4]
        if nextPackSize != '':
           nextPackSize = int(binascii.hexlify(nextPackSize), 16)
           return nextPackSize
        else:
           return 0
           
############Input packet reader, address and data retrieval############
def inputreader(inputPort, filename, packetlength):

	inputCounter = {}
	global chunksize
	chunksize = 0
	packetlength = int(packetlength)
	with open(filename, 'rb') as openfileobject:	
		 while True:
			content = openfileobject.read(packetlength)
			content = content [(packetlength * -1): ]
			if content:
				inputCounter = splitcontent(content, inputPort, packetlength)
				chunksize = packetlength + chunksize
				if getNextPackLength(filename, chunksize) > 0:
				   packetlength = getNextPackLength(filename, chunksize)
				elif getNextPackLength(filename, chunksize) == 0:
				   packetlength = 60
				else:
				   break
			else:
				break
	return inputCounter	    

################ Extract contents of the header and the data from the IP packets###########
def splitcontent(content,inputPort, pktsize): 
	global inputCounter_a
	global inputCounter_b
	global inputCounter_c

	sourceip1 = content[12:13]
	sourceip2 = content[13:14]
	sourceip3 = content[14:15]
	sourceip4 = content[15:16]

	destip1 = content[16:17]
	destip2 = content[17:18]
	destip3 = content[18:19]
	destip4 = content[19:20]

	sourceport = content[40:42]

	destport = content[42:44]

	data = content[60: ]
	
	sa = int(binascii.hexlify(sourceip1), 16)
	sb = int(binascii.hexlify(sourceip2), 16)
	sc = int(binascii.hexlify(sourceip3), 16)
	sd = int(binascii.hexlify(sourceip4), 16)

	da = int(binascii.hexlify(destip1), 16)
	db = int(binascii.hexlify(destip2), 16)
	dc = int(binascii.hexlify(destip3), 16)
	dd = int(binascii.hexlify(destip4), 16)

	data = int(binascii.hexlify(data), 16)

	srcp=int(binascii.hexlify(sourceport), 16)
	drcp=int(binascii.hexlify(destport), 16)

	srcaddr = str(sa)+"."+str(sb)+"."+str(sc)+"."+str(sd)
	destaddr = str(da)+"."+str(db)+"."+str(dc)+"."+str(dd)
	srcprt = str(srcp)
	destprt = str(drcp)
	
	if inputPort == 1:
		info1.append(srcaddr)
		info1.append(destaddr)
		info1.append(srcprt)
		info1.append(destprt)
		info1.append(data)
		inputCounter_a = inputCounter_a + 1
	elif inputPort == 2:
		info2.append(srcaddr)
		info2.append(destaddr)
		info2.append(srcprt)
		info2.append(destprt)
		info2.append(data)
		inputCounter_b = inputCounter_b + 1
	elif inputPort == 3:
		info3.append(srcaddr)
		info3.append(destaddr)
		info3.append(srcprt)
		info3.append(destprt)
		info3.append(data)
		inputCounter_c = inputCounter_c + 1
	else:
		print 'Wrong port number in function inputreader()'
		
	return {'input Link - 1':inputCounter_a, 'input Link - 2':inputCounter_b, 'input Link - 3':inputCounter_c, }	 
   
############Function to take user inputs on speeds#################

def user_inputs():
	global portSpeed001
	global portSpeed002
	global portSpeed003
	global outputportSpeed001
	global outputportSpeed002
	global outputportSpeed003
	global queueSpeed001_a
	global queueSpeed001_b
	global queueSpeed002_a
	global queueSpeed002_b
	global queueSpeed003_a
	global queueSpeed003_b
	global limiter
	global debugFlag
	global inputfile1
	global inputfile2
	global inputfile3
	global forward_table
	outputportSpeed001 = 0
	outputportSpeed002 = 0
	outputportSpeed003 = 0
	queueSpeed001_a = 0
	queueSpeed001_b = 0
	queueSpeed002_a = 0
	queueSpeed002_b = 0
	queueSpeed003_a = 0
	queueSpeed004_b = 0
	limiter = 0.001

	debugFlag = raw_input('Run the program on debug mode? (y/n) : ')
	
	inputfile1 = raw_input('Enter input file 1 : ')
	inputfile2 = raw_input('Enter input file 2 : ')
	inputfile3 = raw_input('Enter input file 3  : ')
	
	forward_table = raw_input('Enter forward table file : ')

	print 'Please enter the speeds on the below input ports (Kbps) : '
	portSpeed001 = int(raw_input('Enter Speeds on port001:  '))
	portSpeed002 = int(raw_input('Enter Speeds on port002:  '))
	portSpeed003 = int(raw_input('Enter Speeds on port003:  '))

	runMode = raw_input('Run the program on M/M/1 or M/D/1 mode? (m/d) : ')
	
	if runMode == 'm':
		queueSpeed001_a = int(raw_input('Enter Speeds on queue 1 of port001:  '))
		queueSpeed001_b = int(raw_input('Enter Speeds on queue 2 of port001:  '))
		queueSpeed002_a = int(raw_input('Enter Speeds on queue 1 of port002:  '))
		queueSpeed002_b = int(raw_input('Enter Speeds on queue 2 of port002:  '))
		queueSpeed003_a = int(raw_input('Enter Speeds on queue 1 of port003:  '))
		queueSpeed003_b = int(raw_input('Enter Speeds on queue 2 of port003:  '))
	
	else:

		response = raw_input('Would you like to reglate speeds on the three output Ports as well? (y/n) : ')
		if response == 'y':
		   outputportSpeed001 = int(raw_input('Enter Speeds on output port001:  '))
		   outputportSpeed002 = int(raw_input('Enter Speeds on output port002:  '))
		   outputportSpeed003 = int(raw_input('Enter Speeds on output port003:  '))
		else:
		   outputportSpeed001 = portSpeed001;
		   outputportSpeed002 = portSpeed002;
		   outputportSpeed003 = portSpeed003;
       
    
###########Function to determine highest value of speeds#####################
def det_highest(a, y, z):
    Max = a
    if y > Max:
        Max = y    
    if z > Max:
        Max = z
        if y > z:
            Max = y
    return Max

############Forwarding the packets based on speeds set by the user###########

def forward_addr(speed001, speed002, speed003, outspeed001, outspeed002, outspeed003):
     global outputCounter
     outputCounter = {}
     if congestionFlag != 1:
          #Speed control simulation on input port
          highest = float(det_highest(speed001, speed002, speed003))
          speedFactor001  = float(highest/speed001)-1
          speedFactor002  = float(highest/speed002)-1
          speedFactor003  = float(highest/speed003)-1
          
          for x in range(0, det_highest(inputCounter_a ,inputCounter_b ,inputCounter_c)):
                time.sleep(speedFactor001*limiter)
                outputCounter = ouput_forward(info1[1+(5*x):2+(5*x)], info1[4+(5*x):5+(5*x)], outspeed001, outspeed002, outspeed003)
                time.sleep(speedFactor002*limiter)
                outputCounter = ouput_forward(info2[1+(5*x):2+(5*x)], info2[4+(5*x):5+(5*x)], outspeed001, outspeed002, outspeed003, )
                time.sleep(speedFactor003*limiter)
                outputCounter = ouput_forward(info3[1+(5*x):2+(5*x)], info3[4+(5*x):5+(5*x)], outspeed001, outspeed002, outspeed003)
          return  outputCounter
     else:
         print("Congestion in the output Queue")
              
############Queue DataPackets in the output queue##############
class Queue:
    """An implementation of a First-In-First-Out
       data structure."""
    def __init__(self):
        self.in_stack = []
        self.out_stack = []
    def push(self, obj):
        self.in_stack.append(obj)
    def pop(self):
        if not self.out_stack:
            self.in_stack.reverse()
            self.out_stack = self.in_stack
            self.in_stack = []
        return self.out_stack.pop()
    def size(self):
         return len(self.in_stack)

############Output forward to Queues###########
def ouput_forward(destaddr, data, outputportSpeed001, outputportSpeed002, outputportSpeed003):
		global outputCounter_a
		global outputCounter_b
		global outputCounter_c
		global dropped_a
		global dropped_b
		global dropped_c
		global residence_a
		global residence_b
		global residence_c
		global lista
		global listb
		global listc
		global queue_1_a_cnt
		global queue_1_b_cnt
		global queue_2_a_cnt
		global queue_2_b_cnt
		global queue_3_a_cnt
		global queue_3_b_cnt
		count1 = 0
		count2 = 0
		count3 = 0
		q1a=Queue()
		q2a=Queue()
		q3a=Queue()
		q1b=Queue()
		q2b=Queue()
		q3b=Queue()
		dest_Port_queue = []
		
		
		dest_Port_queue = check_for_IP(destaddr)
		
		if debugFlag == 'y' :
		    print 'Processsing packet to destination : ', destaddr
		    
		if outputportSpeed001 != 0 and outputportSpeed002 != 0 and outputportSpeed003 != 0: 
			highest = float(det_highest(outputportSpeed001, outputportSpeed002, outputportSpeed003))
			speedFactor001  = float(highest/outputportSpeed001)-1
			speedFactor002  = float(highest/outputportSpeed002)-1
			speedFactor003  = float(highest/outputportSpeed003)-1
		else:
			outputport001 = float (queueSpeed001_a + queueSpeed001_a) /2
			outputport002 = float (queueSpeed002_a + queueSpeed002_a) /2
			outputport003 = float (queueSpeed003_a + queueSpeed003_a) /2
			highest = float(det_highest(outputport001, outputport002, outputport003))
			speedFactor001 = float(highest/outputport001)-1
			speedFactor002 = float(highest/outputport002)-1
			speedFactor003 = float(highest/outputport003)-1
		
		if dest_Port_queue[0] == '1':
			if (dest_Port_queue[1] == '1'):          
				q1a.push(data)
				queue_1_a_cnt = queue_1_a_cnt + 1
				
			else:
			    q1b.push(data)
			    queue_1_b_cnt = queue_1_b_cnt + 1
			start = timeit.default_timer()
			time.sleep((randint(1,2)/10)*speedFactor001)
			if (dest_Port_queue[1] == '1'):  
			    write_Output('outputPort1', q1a.pop())
			else:
			    write_Output('outputPort1', q1b.pop())
			stop = timeit.default_timer()
			lista.append(stop-start)
			if stop-start > 0.009:
			   dropped_a = dropped_a + 1
			   if debugFlag == 'y' : 
			       print 'Packet to Destination ', destaddr , ' dropped out on Queue 1'
			else:
			   outputCounter_a = outputCounter_a + 1
			if stop-start > 0.006:
			   residence_a = residence_a + 1
			    
		elif dest_Port_queue[0] == '2':
			if (dest_Port_queue[1] == '1'):          
				q2a.push(data)
				queue_2_a_cnt = queue_2_a_cnt + 1
			else:
			    q2b.push(data)
			    queue_2_b_cnt = queue_2_b_cnt + 1
			start = timeit.default_timer()
			time.sleep((randint(1,2)/10)*speedFactor002)
			if (dest_Port_queue[1] == '1'):  
			    write_Output('outputPort2', q2a.pop())
			else:
			    write_Output('outputPort2', q2b.pop())
			stop = timeit.default_timer()
			listb.append(stop-start)
			if stop-start > 0.009:
			   dropped_b = dropped_b + 1
			   if debugFlag == 'y' :
			       print 'Packet to Destination ' ,destaddr ,' dropped out on Queue 2'
			else:
			   outputCounter_b = outputCounter_b + 1
			if stop-start > 0.006:
			   residence_b = residence_b + 1
			   
		elif dest_Port_queue[0] == '3':
			if (dest_Port_queue[1] == '1'):          
				q3a.push(data)
				queue_3_a_cnt = queue_3_a_cnt + 1
			else:
			    q3b.push(data)
			    queue_3_b_cnt = queue_3_b_cnt + 1
			start = timeit.default_timer()
			time.sleep((randint(1,2)/10)*speedFactor003)
			if (dest_Port_queue[1] == '1'):  
			    write_Output('outputPort3', q3a.pop())
			else:
			    write_Output('outputPort3', q3b.pop())
			stop = timeit.default_timer()
			listc.append(stop-start)
			if stop-start > 0.009:
			   dropped_c = dropped_c + 1
			   if debugFlag == 'y' :
			       print 'Packet to Destination ' ,destaddr ,' dropped out on Queue 3'
			else:
			   outputCounter_c = outputCounter_c + 1
			if stop-start > 0.006:
			   residence_c = residence_c + 1
			    
		else:
		    print "Invalid port found"
			
		return {'outputLink - 1':outputCounter_a, 'outputLink - 2':outputCounter_b, 'outputLink - 3':outputCounter_c , 'Dropped on - 1':dropped_a, 'Dropped on - 2':dropped_b, 'Dropped on - 3':dropped_c}
		 
		
##############Forward table check logic###########
def collect_ForwardTable():
   with open(forward_table, 'rb') as openfileobject:
		forward_counter = 0
		for content in iter(partial(openfileobject.read, 22), ''):
		     
			sourceip1 = content[0:1]
			sourceip2 = content[1:2]
			sourceip3 = content[2:3]
			sourceip4 = content[3:4]

			destip1 = content[4:5]
			destip2 = content[5:6]
			destip3 = content[6:7]
			destip4 = content[7:8]
			
			mask1 = content[8:9]
			mask2 = content[9:10]
			mask3 = content[10:11]
			mask4 = content[11:12]
			
			hop1 = content[12:13]
			hop2 = content[13:14]
			hop3 = content[14:15]
			hop4 = content[15:16]

			output_port_no = content[16:17]
			
			output_port_Q_no = content[17:18]
			
			ecn_bit = content[18:19]
            	
			fsa = int(binascii.hexlify(sourceip1), 16)
			fsb = int(binascii.hexlify(sourceip2), 16)
			fsc = int(binascii.hexlify(sourceip3), 16)
			fsd = int(binascii.hexlify(sourceip4), 16)

			fda = int(binascii.hexlify(destip1), 16)
			fdb = int(binascii.hexlify(destip2), 16)
			fdc = int(binascii.hexlify(destip3), 16)
			fdd = int(binascii.hexlify(destip4), 16)
	
			fma = int(binascii.hexlify(mask1), 16)
			fmb = int(binascii.hexlify(mask2), 16)
			fmc = int(binascii.hexlify(mask3), 16)
			fmd = int(binascii.hexlify(mask4), 16)
			
			fha = int(binascii.hexlify(hop1), 16)
			fhb = int(binascii.hexlify(hop2), 16)
			fhc = int(binascii.hexlify(hop3), 16)
			fhd = int(binascii.hexlify(hop4), 16)

			otp = int(binascii.hexlify(output_port_no), 16)
			
			otqp = int(binascii.hexlify(output_port_Q_no), 16)
			
			ecnb = int(binascii.hexlify(ecn_bit), 16)
			
			cidr_count = str(bin(fma).count("1") + bin(fmb).count("1") + bin(fmc).count("1") + bin(fmd).count("1"))
			
			srcaddr = str(fsa)+"."+str(fsb)+"."+str(fsc)+"."+str(fsd)
			destaddr = str(fda)+"."+str(fdb)+"."+str(fdc)+"."+str(fdd)
			maskaddr = str(fma)+"."+str(fmb)+"."+str(fmc)+"."+str(fmd)
			destprt = str(otp)
			outputQ = str(otqp)	
			
			if forward_counter == 0:
			    forward_list0.append(srcaddr)
			    forward_list0.append(destaddr)
			    forward_list0.append(maskaddr)
			    forward_list0.append(destprt)
			    forward_list0.append(cidr_count)
			    forward_list0.append(outputQ)
			elif forward_counter == 1:
			    forward_list1.append(srcaddr)
			    forward_list1.append(destaddr)
			    forward_list1.append(maskaddr)
			    forward_list1.append(destprt)
			    forward_list1.append(cidr_count)
			    forward_list1.append(outputQ)
			elif forward_counter == 2:
			    forward_list2.append(srcaddr)
			    forward_list2.append(destaddr)
			    forward_list2.append(maskaddr)
			    forward_list2.append(destprt)
			    forward_list2.append(cidr_count)
			    forward_list2.append(outputQ)
			elif forward_counter == 3:
			    forward_list3.append(srcaddr)
			    forward_list3.append(destaddr)
			    forward_list3.append(maskaddr)
			    forward_list3.append(destprt)
			    forward_list3.append(cidr_count)
			    forward_list3.append(outputQ)
			elif forward_counter == 4:
			    forward_list4.append(srcaddr)
			    forward_list4.append(destaddr)
			    forward_list4.append(maskaddr)
			    forward_list4.append(destprt)
			    forward_list4.append(cidr_count)
			    forward_list4.append(outputQ)
			elif forward_counter == 5:
			    forward_list5.append(srcaddr)
			    forward_list5.append(destaddr)
			    forward_list5.append(maskaddr)
			    forward_list5.append(destprt)
			    forward_list5.append(cidr_count)
			    forward_list5.append(outputQ)
			elif forward_counter == 6:
			    forward_list6.append(srcaddr)
			    forward_list6.append(destaddr)
			    forward_list6.append(maskaddr)
			    forward_list6.append(destprt)
			    forward_list6.append(cidr_count)
			    forward_list6.append(outputQ)
			
			forward_counter = forward_counter + 1
			
##############Check for entry in Forwarding table#############
def check_for_IP(destaddr):
	 n = []
	 a = ipaddr.IPAddress(str(destaddr[0]))
	 
	 #print str(destaddr[0])
	 n.append(ipaddr.IPNetwork(str(forward_list0[1] + '/' + forward_list0[4])))
	 n.append(ipaddr.IPNetwork(str(forward_list1[1] + '/' + forward_list1[4])))
	 n.append(ipaddr.IPNetwork(str(forward_list2[1] + '/' + forward_list2[4])))
	 n.append(ipaddr.IPNetwork(str(forward_list3[1] + '/' + forward_list3[4])))
	 n.append(ipaddr.IPNetwork(str(forward_list4[1] + '/' + forward_list4[4])))
	 n.append(ipaddr.IPNetwork(str(forward_list5[1] + '/' + forward_list5[4])))
	 n.append(ipaddr.IPNetwork(str(forward_list6[1] + '/' + forward_list6[4])))

	 
	 if n[0].Contains(a):
		   return [forward_list0[3], forward_list0[5]]
	 elif n[1].Contains(a):
		   return [forward_list1[3], forward_list1[5]]
	 elif n[2].Contains(a):
		   return [forward_list2[3], forward_list2[5]]
	 elif n[3].Contains(a):
		   return [forward_list3[3], forward_list3[5]]
	 elif n[4].Contains(a):
		   return [forward_list4[3], forward_list4[5]]
	 elif n[5].Contains(a):
		   return [forward_list5[3], forward_list5[5]]
	 else:
	       return [str(2), str(1)]
	    
##############Function to write the data to file#############
def write_Output(fileName, data):
	file = open(fileName, "a")
	data = str(data[0])
	if fileName == 'outputPort1':
		file.write("Packet of file 1 :")
		file.write(' '.join(format(ord(i), 'b') for i in data))
	elif fileName == 'outputPort2':
		file.write("Packet of file 2 :")
		file.write(' '.join(format(ord(i), 'b') for i in data))
	else:
	    file.write("Packet of file 3 :")
	    file.write(' '.join(format(ord(i), 'b') for i in data))
	#file.close()
              
############Main function calling for the programme###########
Input_counters = {}
Output_counters = {}s

residencetime_queue_1_a = 0
residencetime_queue_1_b = 0
residencetime_queue_2_a = 0
residencetime_queue_2_b = 0
residencetime_queue_3_a = 0
residencetime_queue_3_b = 0

try:
   user_inputs()
   print 'Processing....'
except ValueError:
   print("That's not an int!")
   
collect_ForwardTable()

Input_counters = inputreader(1,inputfile1,firstpackSize(inputfile1))
chunksize_a = chunksize
Meanpacksize_a = float(chunksize_a) / Input_counters.get('input Link - 1', "none")
if outputportSpeed001 != 0:
	utilization_a = float((chunksize_a / Input_counters.get('input Link - 1', "none"))) / (outputportSpeed001 * 1000)
#print "a: ",utilization_a


Input_counters = inputreader(2,inputfile2, firstpackSize(inputfile2))
chunksize_b = chunksize
Meanpacksize_b = float(chunksize_b) / Input_counters.get('input Link - 2', "none")
if outputportSpeed002 != 0:
	utilization_b = float((chunksize_b / Input_counters.get('input Link - 2', "none"))) / (outputportSpeed002 * 1000)
Lambda_b = chunksize_b/(portSpeed002 * 1000)
#print "b: ",utilization_b


Input_counters = inputreader(3,inputfile3, firstpackSize(inputfile3))
chunksize_c = chunksize
Meanpacksize_c = float(chunksize_c) / Input_counters.get('input Link - 3', "none")
if outputportSpeed003 != 0:
	utilization_c = float((chunksize_c / Input_counters.get('input Link - 3', "none"))) / (outputportSpeed003 * 1000)
Lambda_c = chunksize_c/(portSpeed003 * 1000)
#print "c: ",utilization_c

Output_counters = forward_addr(portSpeed001, portSpeed002, portSpeed003, outputportSpeed001, outputportSpeed002, outputportSpeed003)

#########queue 1 calculations###########
queue_1_a_cnt_percent = float(queue_1_a_cnt) / (Input_counters.get('input Link - 1', "none"))
queue_1_b_cnt_percent = float(queue_1_b_cnt) / Input_counters.get('input Link - 1', "none")

Lambda_a = float(chunksize_a)/(portSpeed001 * 1000)  ###lambda calculation
Lambda_queue_1_a = float(chunksize_a * queue_1_a_cnt_percent) /(portSpeed001 * 1000)
Lambda_queue_1_b = float(chunksize_a * queue_1_b_cnt_percent) /(portSpeed001 * 1000)


queue_1_a_meanpackssize = float(queue_1_a_cnt_percent) * Meanpacksize_a
queue_1_b_meanpackssize = float(queue_1_b_cnt_percent) * Meanpacksize_a

if queueSpeed001_a != 0 and queueSpeed001_a != 0:
   queue_1_a_sercivetime = float(queue_1_a_meanpackssize) / (queueSpeed001_a * 1000)
   queue_1_b_sercivetime = float(queue_1_b_meanpackssize) / (queueSpeed001_b * 1000)
   
if queueSpeed001_a != 0 and queueSpeed001_b != 0:
   if queue_1_a_cnt != 0: 
		utilization_queue_1_a = float(chunksize_a / queue_1_a_cnt) / (queueSpeed001_a * 1000)
		residencetime_queue_1_a = float(utilization_queue_1_a * queue_1_a_sercivetime )/ (1 - utilization_queue_1_a)
   else:
	    utilization_queue_1_a = 0
	
   if queue_1_b_cnt != 0: 
	   utilization_queue_1_b = float(chunksize_a / queue_1_b_cnt) / (queueSpeed001_b * 1000)
	   residencetime_queue_1_b = float(utilization_queue_1_b * queue_1_b_sercivetime )/ (1 - utilization_queue_1_b)
   else:
	   utilization_queue_1_b = 0
	    

#########queue 2 calculations###########
queue_2_a_cnt_percent = float(queue_2_a_cnt) / Input_counters.get('input Link - 2', "none")
queue_2_b_cnt_percent = float(queue_2_b_cnt) / Input_counters.get('input Link - 2', "none")


Lambda_b = float(chunksize_b)/(portSpeed002 * 1000)  ###lambda calculation
Lambda_queue_2_a = float(chunksize_b * queue_2_a_cnt_percent) /(portSpeed002 * 1000)
Lambda_queue_2_b = float(chunksize_b * queue_2_b_cnt_percent) /(portSpeed002 * 1000)


queue_2_a_meanpackssize = float(queue_2_a_cnt_percent) * Meanpacksize_b
queue_2_b_meanpackssize = float(queue_2_b_cnt_percent) * Meanpacksize_b

if queueSpeed002_a != 0 and queueSpeed002_a != 0:
   queue_2_a_sercivetime = float(queue_2_a_meanpackssize) / (queueSpeed002_a * 1000)
   queue_2_b_sercivetime = float(queue_2_b_meanpackssize) / (queueSpeed002_b * 1000)
   
if queueSpeed002_a != 0 and queueSpeed002_b != 0:
   if queue_2_a_cnt != 0: 
		utilization_queue_2_a = float(chunksize_a / queue_2_a_cnt) / (queueSpeed002_a * 1000)
		residencetime_queue_2_a = float(utilization_queue_2_a * queue_2_a_sercivetime )/ (1 - utilization_queue_2_a)
   else:
	    utilization_queue_2_a = 0
	
   if queue_2_b_cnt != 0: 
	   utilization_queue_2_b = float(chunksize_a / queue_2_b_cnt) / (queueSpeed002_b * 1000)
	   residencetime_queue_2_b = float(utilization_queue_2_b * queue_2_b_sercivetime )/ (1 - utilization_queue_2_b)
   else:
	   utilization_queue_2_b = 0


#########queue 3 calculations###########
queue_3_a_cnt_percent = float(queue_3_a_cnt) / Input_counters.get('input Link - 3', "none")
queue_3_b_cnt_percent = float(queue_3_b_cnt) / Input_counters.get('input Link - 3', "none")

Lambda_c = float(chunksize_b)/(portSpeed002 * 1000)  ###lambda calculation
Lambda_queue_3_a = float(chunksize_c * queue_3_a_cnt_percent) /(portSpeed003 * 1000)
Lambda_queue_3_b = float(chunksize_c * queue_3_b_cnt_percent) /(portSpeed003 * 1000)

queue_3_a_meanpackssize = float(queue_3_a_cnt_percent) * Meanpacksize_c
queue_3_b_meanpackssize = float(queue_3_b_cnt_percent) * Meanpacksize_c


if queueSpeed003_a != 0 and queueSpeed003_a != 0:
   queue_3_a_sercivetime = float(queue_3_a_meanpackssize) / (queueSpeed003_a * 1000)
   queue_3_b_sercivetime = float(queue_3_b_meanpackssize) / (queueSpeed003_b * 1000)
   
if queueSpeed003_a != 0 and queueSpeed003_b != 0:
   if queue_3_a_cnt != 0: 
		utilization_queue_3_a = float(chunksize_a / queue_3_a_cnt) / (queueSpeed003_a * 1000)
		residencetime_queue_3_a = float(utilization_queue_3_a * queue_3_a_sercivetime )/ (1 - utilization_queue_3_a)
   else:
	    utilization_queue_3_a = 0
	
   if queue_3_b_cnt != 0: 
	   utilization_queue_3_b = float(chunksize_a / queue_3_b_cnt) / (queueSpeed003_b * 1000)
	   residencetime_queue_3_b = float(utilization_queue_3_b * queue_3_b_sercivetime )/ (1 - utilization_queue_3_b)
   else:
	    utilization_queue_3_b = 0
   
   
##########################################


mean_res_a = (sum(lista) / float(len(lista)))*10
mean_res_b = (sum(listb) / float(len(listb)))*10
mean_res_c = (sum(listc) / float(len(listc)))*10

mean_no_item_a = (mean_res_a)*3 
mean_no_item_b = (mean_res_b)*3 
mean_no_item_c = (mean_res_c)*3 

print '\n\n\n'
print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*Analysis Report-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
print '\n\n\n'

print 'Input Packets Processed : ', Input_counters
print 'Output Packets Processed : ', Output_counters
print '\n'

if outputportSpeed001 == 0:
	print 'Packets processed in Input Queue 1-A : ', queue_1_a_cnt
	print 'Packets processed in Input Queue 1-B : ', queue_1_b_cnt
	print '\n'
	print 'Packets processed in Input Queue 2-A : ', queue_2_a_cnt
	print 'Packets processed in Input Queue 2-B : ', queue_2_b_cnt
	print '\n'
	print 'Packets processed in Input Queue 3-A : ', queue_3_a_cnt
	print 'Packets processed in Input Queue 3-B : ', queue_3_b_cnt
	print '\n'
	print 'Mean Residence times in Output Queue 1-A  : ' , residencetime_queue_1_a * 10
	print 'Mean Residence times in Output Queue 1-B  : ' , residencetime_queue_1_b * 10
	print '\n'
	print 'Mean Residence times in Output Queue 2-A  : ' , residencetime_queue_2_a * 10
	print 'Mean Residence times in Output Queue 2-B  : ' , residencetime_queue_2_b * 10
	print '\n'
	print 'Mean Residence times in Output Queue 3-A  : ' , residencetime_queue_3_a * 10
	print 'Mean Residence times in Output Queue 3-B  : ' , residencetime_queue_3_b * 10
	print '\n'
else: 
	print 'Maximum residence time in output link A (Max Tr) : ',max(lista) * 10
	print 'Maximum residence time in output link B (Max Tr) : ',max(listb) * 10
	print 'Maximum residence time in output link C (Max Tr) : ',max(listc) * 10
	print '\n'
	print 'Mean residence time in output link A (Mean Tr) : ',mean_res_a * 10
	print 'Mean residence time in output link B (Mean Tr) : ',mean_res_b * 10
	print 'Mean residence time in output link C (Mean Tr) : ',mean_res_c * 10
	print '\n'
	print 'Mean number of items in residence at link A : ' ,mean_no_item_a
	print 'Mean number of items in residence at link B : ' ,mean_no_item_b
	print 'Mean number of items in residence at link C : ' ,mean_no_item_c
	print '\n'
	print 'Maximum number in residence : ', det_highest(mean_no_item_a, mean_no_item_b, mean_no_item_c)

print "Executed succesfully!"
