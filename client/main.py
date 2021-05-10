from connection import Connection as c
import os, threading, pickle, time
name,ip,port = input("Name? "),input("IP? "),input("Port? ")
connection = c(name,ip,port)
connection._connect()
connection.send(name)
def receive():
    #print('e')
    if connection.connected:
        #print('eee')
        mes = connection.receive()
        connection.unpack(mes)
        #print('eee')
        print('thing: ' + str(mes))
    else: raise connection.ErrorDisconnectedFromServer()
def send():
    connection.send(input("Mes: "))

while 1:
    send()
    receive()
'''   
thread0 = threading.Thread(target=receive)
thread1 = threading.Thread(target=send)

thread1.start()
thread0.start()
'''
