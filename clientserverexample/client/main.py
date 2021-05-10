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
        mes, name, extra = connection.receive()
        #connection.unpack(mes)
        #print('eee')
        BACKSLASH = '\\'
        '''
        formatmes = mes
        formatmes.replace(BACKSLASH * 2, BACKSLASH)
        formatmes.replace(BACKSLASH, BACKSLASH[0])
        formatmes.replace("\t","    ")
        formatmes.replace("\t","    ")
        '''
        mes = mes.replace(BACKSLASH * 2, BACKSLASH)
        mes = mes.replace(BACKSLASH, BACKSLASH[0])
        mes = mes.replace("\t","    ")
        mes = mes.replace("\t","    ")
        if str(extra) == "True":
            print(str(pickle.loads(pickle.dumps(mes))))
        if str(extra) == "False":
            print(name + " said:", mes)
    else: raise connection.ErrorDisconnectedFromServer()
def send():
    connection.send(input("Mes: "))

while 1:
    print('recv')
    receive()
    send()
    
'''   
thread0 = threading.Thread(target=receive)
thread1 = threading.Thread(target=send)

thread1.start()
thread0.start()
'''
