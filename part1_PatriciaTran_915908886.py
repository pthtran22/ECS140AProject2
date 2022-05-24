from socket import *
import time

# IP address of the receiver. "" implies localhost
IP_ADDRESS = ""

# Port number on localhost on which receiver runs
PORT = int(input("Enter the Port number you want your sender to run: "))

# Size of the buffer, defining the maximum data that can be buffered for transmission at a time
BUFFER_SIZE = 1000

timeoutSeconds = 5

# Instatiating a UDP Socket
sender_socket = socket(AF_INET, SOCK_DGRAM)

fileToSend = open("./message.txt", "r")
sequenceNumber = 0
sequenceNumber += 1
line = str(sequenceNumber) + "|"
line += fileToSend.read(BUFFER_SIZE)

while line:
    sender_socket.sendto(line.encode(),(IP_ADDRESS, PORT))
    acknowledgementMessage, serverAddress = sender_socket.recvfrom(2048)

    print()
    print("Current Window: [" + str(sequenceNumber) + "]")
    print("Sequence Number of Packet Sent: " + str(sequenceNumber))
    print("Acknowledgment Number Received: " + acknowledgementMessage.decode())
    print()

    sequenceNumber += 1
    line = fileToSend.read(BUFFER_SIZE)
    if line:
        line = str(sequenceNumber) + "|" + line

sender_socket.close()
