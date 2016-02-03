'''
Author: Roopesh Kumar Krishna Kumar
UTA ID: 1001231753

This is the Client program which sends the request to the server and displays the response

*This code is compilable only with python 3.x
Naming convention: camel case

Ref: https://docs.python.org/3/library/socket.html and https://docs.python.org/3/tutorial/index.html  '''


import sys
import socket
import time
import datetime

#Method to print socket details
def PrintServerDetails(ServerAddress, ServerPort):
    ServerDetails = socket.getaddrinfo(ServerAddress, ServerPort, proto=0) #This function returns a list of 5-tuples(family, type, proto, canonname, sockaddr)
    print("Server socket family:", ServerDetails[0][0])
    print("Server socket type:", ServerDetails[0][1])
    print("Server name: " , socket.gethostbyaddr(ServerAddress)[0])
#End of method PrintServerDetails

#Main program starts here
try:
    print("Client Started. . .\n")
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket to connect to server

    
    if(len(sys.argv) < 3):   #Check whether the command line argument is less than 3. [argv[0]:File Name]
        print("No or insufficient parameters recieved! \n") 
        ServerAddress = input("Enter the Server address: ") #Take the input from the user if the arguments are not sufficient.
        ServerPort = int(input("Enter the port: "))
        FileName = input("Enter the file you want request: ")
    else: #if the command line argument is sufficient, then assign them to respective variables.
        ServerAddress = (sys.argv[1])
        ServerPort = int(sys.argv[2])
        FileName = (sys.argv[3])

    SendMsg = 'GET /'+FileName+ ' HTTP/1.1' #Prepare the header for the request
    
    StartTime = datetime.datetime.now() #Mark the start time of the connection to calculate RTT
    
    ClientSocket.connect((ServerAddress, ServerPort)) #Connect to the server
    ClientSocket.sendall(SendMsg.encode())  #send the request to the server
    ReplyFromServer = ClientSocket.recv(1024) #Recieve the request from the server
    
    EndTime=datetime.datetime.now() #Mark the end time of the connection to calculate RTT

    PrintServerDetails(ServerAddress,ServerPort)
    print("Peer name: " , ClientSocket.getpeername() , "\n")
    
    print("\nReply from the server: \n============\n")
    print(ReplyFromServer.decode())
    RTT = (EndTime - StartTime) #calculate the RTT 
    print("\nThe RTT is ", (RTT.total_seconds()) , " seconds or %.2f" %((RTT.total_seconds())*1000) , " milliseconds.") #print the RTT in seconds and milliseconds format
    ClientSocket.close()  #close the client socket
    k = input("\nPress any key to exit") #close the program

except Exception as e:
    print("Client encountered an error! Client is closing!\n",e)


    '''End of the program'''

