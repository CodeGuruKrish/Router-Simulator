################################Networks Border Router Simulator#############################
#Hithesh Krishnamurthy
#Saif Mohhamed
#Ameya Patil

from functools import partial
from random import randint
from time import sleep
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
		
inputCounter_a = 0
inputCounter_b = 0
inputCounter_c = 0
outputCounter_a = 0
outputCounter_b = 0
outputCounter_c = 0
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

dest1 = 1
dest2 = 2
dataadr1 = 4
dataadr2 = 5

############Input packet reader, address and data retrieval############
def inputreader(inputPort, filename):
	global inputCounter_a
	global inputCounter_b
	global inputCounter_c
	
	with open(filename, 'rb') as openfileobject:
		for content in iter(partial(openfileobject.read, 500), ''):
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
	
			data = content[60:500]
	
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
    global limiter
    limiter = 0.001
    
    print 'Please enter the speeds on the below input ports (Kbps) : '
    portSpeed001 = int(raw_input('Enter Speeds on port001:  '))
    portSpeed002 = int(raw_input('Enter Speeds on port002:  '))
    portSpeed003 = int(raw_input('Enter Speeds on port003:  '))
    
    response = raw_input('Would you like to reglate speeds on the output port as well? (y/n) : ')
    if response == 'y':
       outputportSpeed001 = int(raw_input('Enter Speeds on output port001:  '))
       outputportSpeed002 = int(raw_input('Enter Speeds on output port002:  '))
       outputportSpeed003 = int(raw_input('Enter Speeds on output port003:  '))
       
    
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
          
          for x in range(0, 1000):
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
    """A sample implementation of a First-In-First-Out
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
		count1 = 0
		count2 = 0
		count3 = 0
		q1=Queue()
		q2=Queue()
		q3=Queue()
		
		dest_Port = check_for_IP(destaddr)
		
		print 'Processsing packet to destination : ', destaddr
		
		highest = float(det_highest(outputportSpeed001, outputportSpeed002, outputportSpeed003))
		speedFactor001  = float(highest/outputportSpeed001)-1
		speedFactor002  = float(highest/outputportSpeed002)-1
		speedFactor003  = float(highest/outputportSpeed003)-1
		
		if dest_Port == '1':
			q1.push(data)
			start = timeit.default_timer()
			time.sleep((randint(1,2)/10)*speedFactor001)
			write_Output('outputPort1', q1.pop())
			stop = timeit.default_timer()
			lista.append(stop-start)
			if stop-start > 0.009:
			   dropped_a = dropped_a + 1
			   print 'Packet to Destination ', destaddr , ' dropped out on Queue 1'
			else:
			   outputCounter_a = outputCounter_a + 1
			if stop-start > 0.006:
			   residence_a = residence_a + 1
		elif dest_Port == '2':
			q2.push(data)
			start = timeit.default_timer()
			time.sleep((randint(1,2)/10)*speedFactor002)
			write_Output('outputPort2', q2.pop())
			stop = timeit.default_timer()
			listb.append(stop-start)
			if stop-start > 0.009:
			   dropped_b = dropped_b + 1
			   print 'Packet to Destination ' ,destaddr ,' dropped out on Queue 2'
			else:
			   outputCounter_b = outputCounter_b + 1
			if stop-start > 0.006:
			   residence_b = residence_b + 1
		elif dest_Port == '3':
			q3.push(data)
			start = timeit.default_timer()
			time.sleep((randint(1,2)/10)*speedFactor003)
			write_Output('outputPort3', q3.pop())
			stop = timeit.default_timer()
			listc.append(stop-start)
			if stop-start > 0.009:
			   dropped_c = dropped_c + 1
			   print 'Packet to Destination ' ,destaddr ,' dropped out on Queue 3'
			else:
			   outputCounter_c = outputCounter_c + 1
			if stop-start > 0.006:
			   residence_c = residence_c + 1
			
		return {'outputLink - 1':outputCounter_a, 'outputLink - 2':outputCounter_b, 'outputLink - 3':outputCounter_c , 'Dropped on - 1':dropped_a, 'Dropped on - 2':dropped_b, 'Dropped on - 3':dropped_c}
		
		
##############Forward table check logic###########
def collect_ForwardTable():
   with open('forwardingtable1', 'rb') as openfileobject:
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
			
			if forward_counter == 0:
			    forward_list0.append(srcaddr)
			    forward_list0.append(destaddr)
			    forward_list0.append(maskaddr)
			    forward_list0.append(destprt)
			    forward_list0.append(cidr_count)
			elif forward_counter == 1:
			    forward_list1.append(srcaddr)
			    forward_list1.append(destaddr)
			    forward_list1.append(maskaddr)
			    forward_list1.append(destprt)
			    forward_list1.append(cidr_count)
			elif forward_counter == 2:
			    forward_list2.append(srcaddr)
			    forward_list2.append(destaddr)
			    forward_list2.append(maskaddr)
			    forward_list2.append(destprt)
			    forward_list2.append(cidr_count)
			elif forward_counter == 3:
			    forward_list3.append(srcaddr)
			    forward_list3.append(destaddr)
			    forward_list3.append(maskaddr)
			    forward_list3.append(destprt)
			    forward_list3.append(cidr_count)
			elif forward_counter == 4:
			    forward_list4.append(srcaddr)
			    forward_list4.append(destaddr)
			    forward_list4.append(maskaddr)
			    forward_list4.append(destprt)
			    forward_list4.append(cidr_count)
			elif forward_counter == 5:
			    forward_list5.append(srcaddr)
			    forward_list5.append(destaddr)
			    forward_list5.append(maskaddr)
			    forward_list5.append(destprt)
			    forward_list5.append(cidr_count)
			elif forward_counter == 6:
			    forward_list6.append(srcaddr)
			    forward_list6.append(destaddr)
			    forward_list6.append(maskaddr)
			    forward_list6.append(destprt)
			    forward_list6.append(cidr_count)
			
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
		   return forward_list0[3]
	 elif n[1].Contains(a):
		   return forward_list1[3]
	 elif n[2].Contains(a):
		   return forward_list2[3]
	 elif n[3].Contains(a):
		   return forward_list3[3]
	 elif n[4].Contains(a):
		   return forward_list4[3]
	 elif n[5].Contains(a):
		   return forward_list5[3]
	 else:
	       return str(2)
	    
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
Output_counters = {}

try:
   user_inputs()
except ValueError:
   print("That's not an int!")
   
collect_ForwardTable()

Input_counters = inputreader(1,'link14flow')

Input_counters = inputreader(2,'link24flow')

Input_counters = inputreader(3,'link34flow')

Output_counters = forward_addr(portSpeed001, portSpeed002, portSpeed003, outputportSpeed001, outputportSpeed002, outputportSpeed003)

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
print 'Maximum residence time in output link A (Max Tr) : ',max(lista)
print 'Maximum residence time in output link B (Max Tr) : ',max(listb)
print 'Maximum residence time in output link C (Max Tr) : ',max(listc)
print '\n'
print 'Mean residence time in output link A (Mean Tr) : ',mean_res_a
print 'Mean residence time in output link B (Mean Tr) : ',mean_res_b
print 'Mean residence time in output link C (Mean Tr) : ',mean_res_c
print '\n'
print 'Mean number of items in residence at link A : ' ,mean_no_item_a
print 'Mean number of items in residence at link B : ' ,mean_no_item_b
print 'Mean number of items in residence at link C : ' ,mean_no_item_c
print '\n'
print 'Maximum number in residence : ', det_highest(mean_no_item_a, mean_no_item_b, mean_no_item_c)
print "Executed succesfully!"