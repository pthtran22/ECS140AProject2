from socket import *
import time
import math

# IP address of the receiver. "" implies localhost
IP_ADDRESS = ""

# Port number on localhost on which receiver runs
PORT = int(input("Enter the Port number you want your sender to run: "))

# Size of the buffer, defining the maximum data that can be buffered for transmission at a time
BUFFER_SIZE = 1000

# Initialize
timeoutSeconds = 5
windowSize = 5
allDelays = []
allThroughput = []


# Instatiating a UDP Socket
sender_socket = socket(AF_INET, SOCK_DGRAM)

# Open text file to read
fileToSend = open("./message.txt", "r")

sequenceNumber = 0
packetsToSend = []
line = ""
i = 0
while i < windowSize:
    sequenceNumber += 1
    line = str(sequenceNumber) + "|"
    line += fileToSend.read(BUFFER_SIZE)
    packetsToSend.append(line)
    i += 1

j = 0
while line:
    i = 0
    allStartTransmissions = []
    while i < windowSize:
        startOfTransmissionOfPacket = time.time()
        allStartTransmissions.append(startOfTransmissionOfPacket)
        sender_socket.sendto(packetsToSend[j].encode(),(IP_ADDRESS, PORT))
        i += 1
        j += 1

    i = 0
    y = j - 4
    while i < windowSize:
        currentWindow = "["
        for x in range(j-4, j+1):
            currentWindow += str(x) + ", "
        currentWindow += "]"
        acknowledgementMessage, serverAddress = sender_socket.recvfrom(2048)

        pointOfReceiptOfAck = time.time()
        startTime = allStartTransmissions[i]
        delay = pointOfReceiptOfAck-startTime
        allDelays.append(delay*1000) # Multiply by 1000 to go from seconds to milliseconds
        throughput = (BUFFER_SIZE*8)/(delay/1000) # * 8 to go bytes to bits and / 1000 to go milliseconds to seconds
        allThroughput.append(throughput)

        print()
        print("Current Window: " + currentWindow)
        print("Sequence Number of Packet Sent: " + str(y))
        print("Acknowledgment Number Received: " + acknowledgementMessage.decode())
        print()

        y += 1
        i += 1

    i = 0
    while i < windowSize:
        sequenceNumber += 1
        line = fileToSend.read(BUFFER_SIZE)
        if line: # If we read in something then we can attach a sequence number to it
            line = str(sequenceNumber) + "|" + line
            packetsToSend.append(line)
        i += 1

# Calculate required metrics once entire message.txt file has been transmitted
Delay = sum(allDelays) / len(allDelays)
print("Average Delay = <" + str(Delay) + ">")
Throughput = sum(allThroughput) / len(allThroughput)
print("Average Throughput = <" + str(Throughput) + ">")
print("Performance = " + str(math.log10(Throughput) - math.log10(Delay)))
# # Create first packet to send
# sequenceNumber = 0
# sequenceNumber += 1
# line = str(sequenceNumber) + "|"
# line += fileToSend.read(BUFFER_SIZE)
# sequenceNumber2 = sequenceNumber
# sequenceNumber2 += 1
# line2 = str(sequenceNumber2) + "|"
# line2 += fileToSend.read(BUFFER_SIZE)

# sender_socket.sendto(line.encode(),(IP_ADDRESS, PORT))
# sender_socket.sendto(line2.encode(),(IP_ADDRESS, PORT))
# acknowledgementMessage, serverAddress = sender_socket.recvfrom(2048)
# print(acknowledgementMessage.decode())
# acknowledgementMessage, serverAddress = sender_socket.recvfrom(2048)
# print(acknowledgementMessage.decode())

# allDelays = []
# allThroughput = []

# # Loop to send packets until we reach end of the file
# while line:  
#     # Send a receive
#     sender_socket.settimeout(timeoutSeconds)
#     startOfTransmissionOfPacket = time.time()
#     sender_socket.sendto(line.encode(),(IP_ADDRESS, PORT))
#     sender_socket.sendto(line2.encode(),(IP_ADDRESS, PORT))
#     # sender_socket.sendto(line3.encode(),(IP_ADDRESS, PORT))
#     # sender_socket.sendto(line4.encode(),(IP_ADDRESS, PORT))
#     # sender_socket.sendto(line5.encode(),(IP_ADDRESS, PORT))
#     try:
#         acknowledgementMessage, serverAddress = sender_socket.recvfrom(2048)
#         acknowledgementMessage2, serverAddress = sender_socket.recvfrom(2048)

#         # Add stats for metrics
#         pointOfReceiptOfAck = time.time()
#         delay = pointOfReceiptOfAck-startOfTransmissionOfPacket
#         allDelays.append(delay*1000) # Multiply by 1000 to go from seconds to milliseconds
#         throughput = (BUFFER_SIZE*8)/(delay/1000) # * 8 to go bytes to bits and / 1000 to go milliseconds to seconds
#         allThroughput.append(throughput)
        
#         # Print required information after packet is transmitted and ack is received
#         print()
#         print("Current Window: [" + str(sequenceNumber) + ", " + str(sequenceNumber2) + "]")
#         print("Sequence Number of Packet Sent: " + str(sequenceNumber))
#         print("Acknowledgment Number Received: " + acknowledgementMessage.decode())
#         print()

#         sequenceNumber += 1
#         line = fileToSend.read(BUFFER_SIZE)
#         sequenceNumber += 1
#         line2 = fileToSend.read(BUFFER_SIZE)
#         if line: # If we read in something then we can attach a sequence number to it
#             line = str(sequenceNumber) + "|" + line
#         if line2:
#             line = str(sequenceNumber) + "|" + line
#     except timeout:
#         sender_socket.sendto(line.encode(),(IP_ADDRESS, PORT))

# # Calculate required metrics once entire message.txt file has been transmitted
# Delay = sum(allDelays) / len(allDelays)
# print("Average Delay = <" + str(Delay) + ">")
# Throughput = sum(allThroughput) / len(allThroughput)
# print("Average Throughput = <" + str(Throughput) + ">")
# print("Performance = " + str(math.log10(Throughput) - math.log10(Delay)))
sender_socket.close()
