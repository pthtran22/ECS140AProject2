from socket import *
import time
import math

IP_ADDRESS = ""

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
for i in range(windowSize):
    sequenceNumber += 1
    packet = str(sequenceNumber) + "|"
    packet += fileToSend.read(PACKET_SIZE)
    packetsToSend.append(packet)

responseACKNumber = -1
while True:
    for i in range(windowSize):
        sender_socket.settimeout(timeoutSeconds)
        sender_socket.sendto(packetsToSend[sequenceNumber-windowSize+i].encode(),(IP_ADDRESS, PORT))
    resend = False
    breakOuterLoop = False
    while True:
        receivedACK = False
        try:
            if not resend:
                for i in range(windowSize):
                    response, serverAddress = sender_socket.recvfrom(2048)
                    ackNumbersReceived.append(int(response.decode()))
            else:
                response, serverAddress = sender_socket.recvfrom(2048)
            responseACKNumber = int(response.decode())
            if type(responseACKNumber) is int and responseACKNumber >= 0:
                receivedACK = True
                if responseACKNumber == sequenceNumber:
                    print("successfully sent and received all")
                    print("move window over by 5")
                elif responseACKNumber < sequenceNumber:
                    print("resend responseACKNumber + 1 packet")
                elif responseACKNumber > sequenceNumber:
                    print("TO-DO")
        except:
            # Resend responseACKNumber + 1 packet
            receivedACK = False
            print("Failed to receive packet")
        
        if receivedACK:
            currentWindow = "["
            for i in range(len(packetsToSend)-4, len(packetsToSend)+1):
                currentWindow += str(i) + ", "
            currentWindow += "]"
            if not resend:
                for i in range(windowSize):
                    print("Current Window: " + currentWindow)
                    print("Sequence Number of Packet Sent: " + packetsToSend[sequenceNumber-windowSize+i].split("|")[0])
                    print("Acknowledgment Number Received: " + str(ackNumbersReceived[sequenceNumber-windowSize+i]))
            else:
                print("Current Window: " + currentWindow)
                print("Sequence Number of Packet Sent: " + str(sequenceNumber+1))
                print("Acknowledgment Number Received: " + str(responseACKNumber))
            if responseACKNumber == sequenceNumber:
                sequenceNumber = sequenceNumber
                break
            elif responseACKNumber < sequenceNumber:
                sequenceNumber = responseACKNumber
                resend = True
            elif responseACKNumber > sequenceNumber:
                sequenceNumber = responseACKNumber
                break

        if sequenceNumber == len(packetsToSend):
            break
        elif sequenceNumber < len(packetsToSend):
            sender_socket.settimeout(timeoutSeconds)
            sender_socket.sendto(packetsToSend[sequenceNumber].encode(),(IP_ADDRESS, PORT))
    for i in range(windowSize):
        sequenceNumber += 1
        packet = str(sequenceNumber) + "|"
        contentToAdd = fileToSend.read(PACKET_SIZE)
        if not contentToAdd:
            breakOuterLoop = True
            break
        else:
            packet += contentToAdd
            packetsToSend.append(packet)
    if breakOuterLoop:
        break
            
        
        


