import crypttools as crypt
#import errormessages
import socket, threading, pickle, handle, json
class ErrorDisconnectedFromServer(Exception):
    pass
class ErrorReceivingMessage(Exception):
    pass
class ErrorSendingMessage(Exception):
    pass
class ErrorMessageNotFromServer(Exception):
    pass
class ErrorConnectingToServer(Exception):
    pass

class Connection:
  def __init__(self,name,ip,port):
    self.name = name
    self.ip = ip
    self.port = port
    self.uid = crypt.strHash(self.name)
    self.connected = False
    self.connection = None
  
  def injson(self,args,first):
    if first:
      p = {
        'data': {pickle.dumps(args)},
        'from': {"!EST"},
      }
      return(p)
    else:
      if len(args) == 1:
        x = args[0]
        p = {
          'data': {x},
          'from': {self.uid},
        }
      else:
        p = {
          'data': {pickle.dumps(p)},
          'from': {self.uid},
          }
      return(p)
  def unpack(self,mes):
    #print("thing: " + str(mes))
    try:
      if mes['from'] == "!SERVER":
        args = mes['data']
        print(args)
        handle.handle(args)
      else:
        raise ErrorMessageNotFromServer()
    except:
      pass

  def receive(self):
    try:
      mes = None
      try: mes = pickle.loads(self.connection.recv(1024))
      except EOFError: raise ErrorReceivingMessage()
      if mes != None:
        if mes['from'] == "!SERVER":
          args = mes['data']
            #print(args)
            #handle.handle(args)
          #print(args[0])
          if args[0] == "!NICK":
            #print('got here')
            self.connection.send(self.injson([self.name,self.uid],True))
          else:
            print('got here: ' + str(mes))
            return(mes)
        else:
          return(None)
    except:
        self.connection.close()
        ErrorDisconnectedFromServer()
  def _connect(self):
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.connection.connect((str(self.ip),int(self.port)))
      self.connected = True
    except:
      self.connected = False
      self.connection = None
      raise ErrorConnectingToServer()

  def send(self,mes):
    try:
      self.connection.send(pickle.dumps(self.injson([mes],False)))
    except: raise ErrorSendingMessage()
