import socket, threading, pickle, os

def injson(arg,name):
    if str(name) == "None":
        p = {
        'data': {pickle.dumps(arg)},
        'from': {"!SERVER"},
        'mesfrom': {None}
          }
    else:
        p = {
            'data': {pickle.dumps(arg)},
            'from': {"!SERVER"},
            'mesfrom': {name[0]}
          }
    #print(str(p))
    return(pickle.dumps(p))
    

print('Starting...')

port = int(input("What port would you like to use? \n"))
try: print(os.system("ipconfig getifaddr en1"))
except: pass


# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', port))
server.listen(5)

print('Server sucessfully created on port ' + str(port))

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
uids = []
# Sending Messages To All Connected Clients
def broadcast(message):
    #print('got here')
    #try:
    for client in clients:
        #print(pickle.loads(message))
        #print(client)
        ind = clients.index(client)
        print(ind,clients,nicknames)
        client.send(injson(message,nicknames[ind]))
        print('got here')
        #print(nicknames)
    #except: raise ConnectionError
def broadcastspecial(message,clientnot):
    for client in clients:
        if client != clientnot:
            client.send(injson(message,clientnot))
# Handling Messages From Clients
def handle():
    while True:
        for client in clients:
            print('rec')
            #try:
            # Broadcasting Messages

            print('rec2')
            mes, uid = jsonparse(pickle.loads(client.recv(1024)))
            broadcast(mes)
            if not mes == b'':
                print(mes)
            '''
            except:
                # Removing And Closing Clients
                index = clients.index(client)
                clients.remove(client)
                client.close()
                print('dis')
                try:
                    nickname = nicknames[index]
                    broadcast('{} left!'.format(nickname))
                    print('{} left!'.format(nickname))
                    nicknames.remove(nickname)
                    uid = uids[index]
                    uids.remove(uid)
                except: pass
                break
            '''
# Receiving / Listening Function
def jsonparse(arg):
    #print("thing: " + str(arg))
    arg = dict(arg)
    try:
        if arg['from'] == "!EST":
            return(arg['data'])
        else:
            return(arg['data'], arg['from'])
    except: pass
def settostr(strset):
    
    return()
def receive():
    try:
        # Accept Connection
        print('before accept')
        client, address = server.accept()
        print('after accept')
        print("Person connected with {}".format(str(address)))
        clients.append(client)
        #print('next')
        # Request And Store Nickname
        #client.send(injson('!NICK'))
        nickname, uid = jsonparse(pickle.loads(client.recv(1024)))
        #print('got to here: ')
        #nickname = str(nickname[1:-1])
        #print(nickname, "got here")
        #print(str(nickname[1:]))
        nicknames.append(nickname)
        print(nicknames)
        #print('Nicks: %s' % nicknames)
        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        uids.append(uid)
        broadcast("{} joined!".format(nickname))
        client.send(injson('\nConnected to server!',None))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle)
        thread.start()
        print(nicknames, uids)
    except:
        #print('fail')
        pass

thread0 = threading.Thread(target=handle)
thread0.start()
thread1 = threading.Thread(target=receive)
thread1.start()
