from socket import *
import time
import math
import matplotlib.pyplot as plt

# from jello import BUFFER_SIZE

IP_ADDRESS = ""
print("inside part2")
PORT = int(input("Enter the Port number you want your sender to run: "))

PACKET_SIZE = 1000

timeoutSeconds = 5
windowSize = 5
allDelays = []
allThroughput = []

sender_socket = socket(AF_INET, SOCK_DGRAM)

fileToSend = open("./message.txt", "r")

sequenceNumber = 0
packetsToSend = []
ackNumbersReceived = []
packet = ""
timeoutcount = 0

# start reading first 5 packets
for i in range(windowSize):
    sequenceNumber += 1
    packet = str(sequenceNumber) + "|"
    packet += fileToSend.read(PACKET_SIZE)
    packetsToSend.append(packet)

responseACKNumber = -1
while True:
    # sending packet to server 5 times
    allStartTransmissions = []
    for i in range(windowSize):
        sender_socket.settimeout(timeoutSeconds)
        allStartTransmissions.append(time.time())
        sender_socket.sendto(packetsToSend[sequenceNumber-windowSize+i].encode(),(IP_ADDRESS, PORT))
    
    resend = False # checks if the packet resent back because it was not received
    breakOuterLoop = False
    receivedACK = False
    timeoutcheck = False

    while True:
        receivedACK = False
        try:
            if not resend:
                # receives response # from packets sent before
                for i in range(windowSize):
                    # print("inside try not resend")
                    response, serverAddress = sender_socket.recvfrom(2048)
                    delay = time.time() - allStartTransmissions[i]
                    allDelays.append(delay * 1000)
                    allThroughput.append(PACKET_SIZE/ (delay/1000))
                    # print("response: " + str(response.decode()))
                    ackNumbersReceived.append(int(response.decode()))
            # receives response # of missed packet
            else: 
                # print("inside resend")
                response, serverAddress = sender_socket.recvfrom(2048)
                if timeoutcheck == True:
                    # print("ack Num: " + str(response.decode()))
                    ackNumbersReceived.append(int(response.decode()))
                    # print("len ackNum: " + str(len(ackNumbersReceived)))
                #     timeoutcheck = False
                    
                    
                # resend = False
                

            responseACKNumber = int(response.decode())
            if type(responseACKNumber) is int and responseACKNumber >= 0:
                receivedACK = True
                # if responseACKNumber == sequenceNumber:
                    # print("successfully sent and received all")
                    # print("move window over by 5")
                # elif responseACKNumber < sequenceNumber:
                    # print("resend responseACKNumber + 1 packet")
                # elif responseACKNumber > sequenceNumber:
                    # print("TO-DO")
        except:
            # Resend responseACKNumber + 1 packet
            receivedACK = False
            # timeoutcheck = True
            # resend = True
            # print("Failed to receive packet")
            # print("Seq number: " + str(sequenceNumber))
            # print("Response Ack Number: " + str(responseACKNumber))
            # sequenceNumber = responseACKNumber

        
        if receivedACK:
            currentWindow = "["
            for i in range(len(packetsToSend)-4, len(packetsToSend)+1):
                currentWindow += str(i) + ", "
            currentWindow += "]"

            if not resend:
                # print("inside if not resend")
                for i in range(windowSize):
                    # print("\n")
                    sliced_text = slice(len(currentWindow)-3)
                    print("Current Window: " + currentWindow[sliced_text] + "]")
                    print("Sequence Number of Packet Sent: " + packetsToSend[sequenceNumber-windowSize+i].split("|")[0])
                    # print("check sequenceNumber-windowSize+i = ", str(sequenceNumber-windowSize+i) + " len: " + str(len(ackNumbersReceived)))
                    print("Acknowledgment Number Received: " + str(ackNumbersReceived[sequenceNumber-windowSize+i]))
                    print("\n")
            else:
                # print("\n")
                # print("inside resend")
                sliced_text = slice(len(currentWindow)-3)
                print("Current Window: " + currentWindow[sliced_text] + "]")
                print("Sequence Number of Packet Sent: " + str(sequenceNumber+1))
                print("Acknowledgment Number Received: " + str(responseACKNumber))
                print("\n")

            if resend == True:
                sequenceNumber = responseACKNumber

            elif responseACKNumber == sequenceNumber:
                sequenceNumber = sequenceNumber
                break
            elif responseACKNumber < sequenceNumber:
                sequenceNumber = responseACKNumber
                resend = True
            elif responseACKNumber > sequenceNumber:
                sequenceNumber = responseACKNumber
                break

        else:
            # timeout occured
            timeoutcount = timeoutcount + 1
            
            sender_socket.settimeout(timeoutSeconds)
            print("sequence Numbver: " + str(sequenceNumber))
            sequenceNumber = responseACKNumber
            print("sequence Numbver: " + str(sequenceNumber))
            sender_socket.sendto(packetsToSend[sequenceNumber].encode(),(IP_ADDRESS, PORT))
            resend = True
            timeoutcheck = True
            
            continue



        if sequenceNumber == len(packetsToSend):
            # print("inside sequence number == len(packetsToSend")
            break
        elif sequenceNumber < len(packetsToSend):
            # print("inside sequence number < len(packetsToSend")
            sender_socket.settimeout(timeoutSeconds)
            sender_socket.sendto(packetsToSend[sequenceNumber].encode(),(IP_ADDRESS, PORT))
    for i in range(windowSize):
        sequenceNumber += 1
        packet = str(sequenceNumber) + "|"
        contentToAdd = fileToSend.read(PACKET_SIZE)
        if not contentToAdd:
            # print("inside not contentToAdd")
            breakOuterLoop = True
            break
        else:
            # print("inside contentToAdd")
            packet += contentToAdd
            packetsToSend.append(packet)
    
    # work on if the window is three packets left you send the window and end communication
    if breakOuterLoop:
        # print("breakOuterLoop")
        break
            

Delay = sum(allDelays) / len(allDelays)
print("Average Delay = <" + str(Delay) + ">")
Throughput = sum(allThroughput) / len(allThroughput)
print("Average Throughput = <" + str(Throughput) + ">")
print("Performance = <" + str(math.log10(Throughput) - math.log10(Delay)) + ">")
sender_socket.close()

print("timeoutCount:" + str(timeoutcount))
plt.plot(range(0, len(allDelays)), allDelays)
plt.title('Plot of per-packet delays')
plt.xlabel('Packets')
plt.ylabel('Delays')
plt.show()

plt.plot(range(0, len(allThroughput)), allThroughput)
plt.title('Plot of per-packet throughputs')
plt.xlabel('Packets')
plt.ylabel('Throughput')
plt.show()
