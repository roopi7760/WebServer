'''
Author: Roopesh Kumar Krishna Kumar
UTA ID: 1001231753
This python script initialises and creates a multi-threaded TCP/IP Server which serves multiple clients.

*This code is compilable only with python 3.x
Naming convention: camel case
Ref: https://docs.python.org/3/library/socket.html and https://docs.python.org/3/tutorial/index.html'''

import socket
import datetime
import time
import threading
import random


#Method to log to a file
def WriteToFile(FileName,LogToFile):
    with open(FileName,'a+') as LogFile:     
                LogFile.write(LogToFile)
                LogFile.close()
#End of method WriteToFile    

#Method to respond to the client based on its request
def ServeTheClient(ThreadID, Client, ClientAddress,RequestFromClient):
    try:
        
        ServerThread = socket.socket(socket.AF_INET, socket.SOCK_STREAM,socket.IPPROTO_IP)
        ServerThread.bind(('127.0.0.1', ThreadID))
        RequestMethod = RequestFromClient.split(' ')[0]  #Splits the string using the delimiter. 
        FileRequested = RequestFromClient.split(' ')[1]  
        
        if(FileRequested == '/'):  #Check if the request object is null. If it is null, return the index page of the server
            FileRequested = 'webPages/index.html'
        else:                       #else add webPages folder to the request file
            FileRequested = 'webPages' + FileRequested
        '''This is to check the multi-threading
        sec = random.randint(5,15)
        print("Wait time for this thread(", ThreadID ,") is ", sec)
        time.sleep(sec)'''
    #open the request file in the webPages folder
        try:
            print("Request Method from the client is " + RequestMethod)
            if (RequestMethod == 'GET') :  #Check if the client request is a GET request [NOTE: Others are not supported as of now]
                GetRequestedFile = open(FileRequested,'rb') 
                ResponseToClient = GetRequestedFile.read()
                GetRequestedFile.close() 
        except Exception as e:
            print("Warning! File requested by the client was not found. 404 Error sent\n") 
            ResponseToClient = 'HTTP/1.1 404 Not Found\n' 
            ResponseToClient.encode()  #Convert the string to byte format
            ResponseToClient = b'<html><title>404 NOT FOUND</title><body><h1>404 File not found</h1></body></html>'
                    
        Client.send(ResponseToClient) #Send response to the client
        print("Response sent to client:\n", ResponseToClient,"\n\nServer closing the connection with the client ", ClientAddress ,"\n ========END==========\n")
        Client.close()  #Close the client connection

    except Exception as e:
        print("Alas! Following exception occured: \n", e)
#End of method ServeTheClient

#Method to print the socket details
def PrintClientSocketDetails(client):  #Function to display client socket properties
    try:
        print('Client\'s Time out is ' + str(client.gettimeout()))
        print('Client\'s Socket family is ' + str(client.family) )
        print('Client\'s Socket type is ' + str(client.type) )
        print('Client\'s Socket protocol is ' + str(client.proto) )
        print('Client\'s Socket Peer name is ' + str(client.getpeername()) + '\n')
        
    except Exception as e:
        print("Could not display client socket properties.\nFollowing exception occured: ", e)
#End of method PrintClientSocketDetails
        
#Main Program starts here    
#Setup the Server with address and port
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,socket.IPPROTO_IP)
ServerAddress = "127.0.0.1"
ServerPort = 8081
ServerSocket.bind((ServerAddress, ServerPort))
print("PYTHON SERVER is UP and RUNNING with IP:", ServerAddress , " Port:", ServerPort, " \n")
print("Listening port for client request . . . \n")
threads = []
ServerSocket.listen(5)  #Maximum number of connections Server can queue

#Keep listening the port
try:
    while True:
        (client, address) = ServerSocket.accept()    #establish a connection with the client
        FileName = "logs/ServerLog/" + str(address[1]) + "_"+ str(time.strftime("%d%m_%H%M%S")) +".txt"
        #Log the client and its request to the log file
        print ("Server got connection from ", address[0] , " having port " , address[1] , ".\n")
        print("Displaying the client socket details . . . \n")
        PrintClientSocketDetails(client) #calling function to display the client socket properties
        LogToFile = 'WebServer recieved a request from ' + str(address) + ' \n Below is the Request packet from client\n'
        RequestFromClient = client.recv(1024).decode()   #Convert the byte format to string format
        LogToFile += RequestFromClient          
        WriteToFile(FileName,LogToFile)

        ThreadID = random.randint(8000,8050) #Generate a random port number and assign the thread to the client
        print("Client is assigned a new port ", ThreadID)  #print the new port number for the client
        try:
            T = threading.Thread(target=ServeTheClient,args=(ThreadID,client,address,RequestFromClient)) #call the function to serve the client with new port number
            threads.append(T)
            T.start() #Start the thread
            
        except Exception as e:
            print("Could not create thread!\n Check Logs for details\n")
            WriteToFile(FileName,e)
    print("Server is shutting down. . . \n")
   
except  Exception as e:
    print("Error encountered! Server is shutting down!\n")
    WriteToFile(FileName,e)

finally:
    ServerSocket.close(); #Closing the server socket


    '''End of the Program '''

