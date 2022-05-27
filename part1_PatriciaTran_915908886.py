from socket import *
import time
import math
import matplotlib.pyplot as plt

# IP address of the receiver. "" implies localhost
IP_ADDRESS = ""

# Port number on localhost on which receiver runs
PORT = int(input("Enter the Port number you want your sender to run: "))

# Size of the buffer, defining the maximum data that can be buffered for transmission at a time
BUFFER_SIZE = 1000

timeoutSeconds = 5

# Instatiating a UDP Socket
sender_socket = socket(AF_INET, SOCK_DGRAM)
sender_socket.settimeout(timeoutSeconds)

fileToSend = open("./message.txt", "r")
sequenceNumber = 0
sequenceNumber += 1
line = str(sequenceNumber) + "|"
line += fileToSend.read(BUFFER_SIZE)
allDelays = []
allThroughput = []
timeoutCount = 0

while line:
    while True:
        startOfTransmissionOfPacket = time.time()
        sender_socket.sendto(line.encode(),(IP_ADDRESS, PORT))
        receivedACK = False
        try:
            acknowledgementMessage, serverAddress = sender_socket.recvfrom(2048)
            pointOfReceiptOfAck = time.time()
            delay = pointOfReceiptOfAck-startOfTransmissionOfPacket
            allDelays.append(delay*1000)
            throughput = (BUFFER_SIZE)/(delay/1000)
            allThroughput.append(throughput)
            ACKNumber = int(acknowledgementMessage.decode())
            if type(ACKNumber) == int and ACKNumber >= 0:
                if ACKNumber == sequenceNumber:
                    receivedACK = True
            else:
                receivedACK = False
                # timeoutCount += 0
        except:
            receivedACK = False
            timeoutCount += 1
        
        if receivedACK:
            print()
            print("Current Window: [" + str(sequenceNumber) + "]")
            print("Sequence Number of Packet Sent: " + str(sequenceNumber))
            print("Acknowledgment Number Received: " + acknowledgementMessage.decode())
            print()
            break

    sequenceNumber += 1
    line = fileToSend.read(BUFFER_SIZE)
    if line:
        line = str(sequenceNumber) + "|" + line
    else:
        break

Delay = sum(allDelays) / len(allDelays)
print("Average Delay = <" + str(Delay) + ">")
Throughput = sum(allThroughput) / len(allThroughput)
print("Average Throughput = <" + str(Throughput) + ">")
print("Performance = <" + str(math.log10(Throughput) - math.log10(Delay)) + ">")
sender_socket.close()

print("timeoutCount:" + str(timeoutCount))
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
