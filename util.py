

# chat changes , chatroom archives
import gc,shelve
import socket, pdb
import traceback

a = shelve.open('chat_archive')
archive = dict(a)
a.close()
MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'

details= {}
block = {}

def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return s

#flagcj = 0 #  0-join 1 -chat

class Hall:

    def recheck(self):
         print("recheck\n")
         l = self.chats_map.keys()
         c = self.chats.keys()
         d = self.chats.copy()
         d = { k : v for k,v in d.items() if k in self.chats_map.keys()}
         print(d)
         self.chats.clear()
         self.chats = d.copy()
         print("recheck ends")
         '''
         for x in self.chats.keys():
             if x in self.chats_map.keys():
                 pass
             else:
                 self.chats.pop(x,None)
         '''

    def __init__(self):
        self.chats ={}
        self.chats_map ={}
        self.rooms = {} # {room_name: Room}
        self.room_player_map = {} # {playerName: roomName}
       # self.flagcj = None


    def welcome_new(self, new_player):
        new_player.socket.sendall(b'Welcome to pychat.\nPlease tell us your name:\n')

    def list_chats(self, player):
        if archive[player.name] == {}:
            msg = 'Oops, no active chatrooms currently\n' \
                + 'Use [<chat> friend_name] to create a room.\n'
            player.socket.sendall(msg.encode())
        else:
            y = ""
            for x in archive[player.name].keys():
                y +=x+"\n"
            player.socket.sendall(y.encode())

        """
        if len(self.chats) == 0:
            msg = 'Oops, no active chatrooms currently\n' \
                + 'Use [<chat> friend_name] to create a room.\n'
            player.socket.sendall(msg.encode())
        else:
            msg = 'Listing current chatrooms...\n'
            print("chats \n\n" + str(self.chats))
            for chat in self.chats:
                if str(chat)!= player.name:
                  msg += chat + "\n"
            player.socket.sendall(msg.encode())
        """
    def list_rooms(self, player):
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently.\n' \
                + 'Use [<join> room_name] to create a room.\n'
            player.socket.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(msg.encode())

    def handle_msg(self, player, msg):

        instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch to a room\n' \
            + b'[<chat> friend_name] to start a Personal Chat\n' \
            + b'[<block> friend_name] to block a friend\n' \
            + b'[<unblock> friend_name] to unblock a friend\n' \
            + b'[<manual>] to show instructions\n' \
            + b'[<quit>] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

        print(player.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            player.name = name
            print("New connection from:", player.name)
            details[player.name] = player
            player.socket.sendall(instructions)
            block[player.name]=list()
            print(details)
            self.chats_map[player.name] = ""
            if player.name not in archive.keys():
                archive[player.name] = {}

        elif "<chat>" in msg:
          try:
            player.flagcj =1
            frnd = msg.split()[1]
            same_chat = False
            self.recheck()
            print("chats")
            print(self.chats)
            print("chats map")
            print(self.chats_map)
            if frnd not in archive[player.name].keys():
                archive[player.name][frnd] = ""
            if frnd in player.chat_msg.keys():
                archive[player.name][frnd] = "{0}\n{1}".format(archive[player.name][frnd],player.chat_msg[frnd])
            player.chat_msg[frnd] = ""
            player.socket.sendall(archive[player.name][frnd].encode())
            if player.name not in block[frnd]: # error check

                print("not blocked lmao")
            #    print(self.chats)
                if frnd in self.chats: # switching?
                    if self.chats_map[player.name] == frnd :
             #           print("in if")
                        if player.flagcj == 0:
                            player.socket.sendall(b'You are already chatting with ' + frnd.encode())
                        same_chat = True
                    else: # switch
              #          print("in else")
                       # old_chat = self.chats_map[player.name]

                        if self.chats_map[player.name] != "":
                            self.chats.pop(self.chats_map[player.name],None)

                      #  self.chats.pop(player.name,None)

                        if self.chats_map[player.name]:
                            self.chats.pop(self.chats_map[player.name],None)
                if not same_chat:
               #     print("out if")
                    if not frnd in self.chats: # new room:
                        if self.chats_map[player.name] != "":
                            #self.chats.pop(self.chats_map[player.name],None)
                #            print("previous chat" )
                            n = self.chats.pop(self.chats_map[player.name],None)
                           # del self.chats[self.chats_map[player.name]]
                 #           print("success \n n is")
                  #          print(n)
                            del n
                            gc.collect()
                   #         print(self.chats)
                        self.chats_map[self.chats_map[player.name]] = ""
                        new_chat = ChatRoom(player.name,frnd)
                        self.chats[frnd] = new_chat
                        #self.chats.pop(player.name,None)
                        #print(type(self))
                   # self.chats[frnd].players.append(player)
                    if self.chats_map[player.name] != frnd and self.chats_map[player.name]!="":
                        self.chats.pop(player.name,None)
                        self.chats.pop(self.chats_map[player.name],None)
                    self.chats[frnd].welcome_new(player)
                    #self.chats_map[self.chats_map[player.name]] = ""
                    self.chats_map[player.name] = frnd
            else:
                #pass
                player.socket.sendall("you have been blocked".encode())
            self.recheck()
            print(self.chats)
            print("chats above")
            print(self.chats_map)
            print("chat maps above")
          except Exception as e:
              #pass
             traceback.print_exc()
        elif "<join>" in msg:
            player.flagcj = 0
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                print(self.rooms)
                if player.name in self.room_player_map: # switching?
                    if self.room_player_map[player.name] == room_name and not player.flagcj:
                        player.socket.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                        player.socket.sendall(archive[room_name])
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    if room_name not in archive.keys():
                        archive[room_name] = ""
                   #     self.chats = ""
                    player.socket.sendall(archive[room_name].encode())
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.socket.sendall(instructions)
            self.recheck()

        elif "<list>" in msg:
            self.list_rooms(player)
            self.list_chats(player)

        elif "<block>" in msg:
            block[player.name].append(msg.split()[1])
            print(str(block))
        elif "<unblock>" in msg:
            block[player.name].remove(msg.split()[1])
            print(str(block))
        elif "<manual>" in msg:
            player.socket.sendall(instructions)

        elif "<quit>" in msg:
            for frnd in player.chat_msg.keys():
                archive[player.name][frnd] = "{0}\n{1}".format(archive[player.name][frnd],player.chat_msg[frnd])
            a = shelve.open('chat_archive')
          #  archive = dict(a)
         #   a.close()
            '''
            print("exiting",end=" ")
            print(player.name)
            print("chat msgs")
            print(archive[player.name])
            print("already in archive")
            #print(a[player.name])
            '''
            a[player.name] = archive[player.name]
            a.close()
            '''
            if player.name not in a:
                a[player.name] = archive[player.name]

            for p in player.chat_msg.keys():
                a[player.name][p] = "{0}\n{1}".format(a[player.name][p],archive[player.name][p])
            '''
            player.socket.sendall(QUIT_STRING.encode())
            self.remove_player(player)
           # self.recheck()
            print(archive)


        else:
           try:

            # check if in a room or not first
            if player.flagcj == 0 and player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
            elif player.flagcj ==1 and player.name in self.chats_map:
                if block[self.chats_map[player.name]] and player.flagcj ==1:
                  if player.name in block[self.chats_map[player.name]] :
                    player.socket.sendall("you have been blocked".encode())
                    return
                print("sending")
                self.chats[self.chats_map[player.name]].broadcast(player, msg.encode())
            else:

                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                player.socket.sendall(msg.encode())
           except Exception as e:
               traceback.print_exc()
    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
            gc.collect()
        if player.name in self.chats_map:
           # self.chats[self.chats_map[player.name]].remove_player(player)
            self.chats.pop(self.chats_map[player.name],None)
            self.chats.pop(player.name,None)
            self.chats_map[self.chats_map[player.name]] = ""
            self.chats_map[player.name] = ""



            gc.collect()
        print("Player: " + player.name + " has left\n")

class ChatRoom:
    def __init__(self,str1,str2):
        #self.players = [player1,player2]
        self.players = [details[str1],details[str2]]
        self.name = str1 + " " +str2
        msg = str1 + " has invited you for chat \n"
        self.players[1].socket.sendall(msg.encode())

        #if self.players[0].chat_msg[self.players[1].name]:
        print("setting " +self.players[0].name +" message with "+ self.players[1].name )
        self.players[0].chat_msg[self.players[1].name] = ""
        print("setting " +self.players[1].name +" message with "+ self.players[0].name )
        #if self.players[1].chat_msg[self.players[0].name]:
        self.players[1].chat_msg[self.players[0].name] = ""



       # self.players[1]
    def welcome_new(self,player):
        msg = self.name + "Chatroom \n"
        self.players[0].socket.sendall(msg.encode())

       # self.players[1].socket.sendall(msg.encode())
    def broadcast(self, from_player, msg):
      #  st = msg.decode()
        msg = from_player.name.encode() + b":" + msg
        '''        not working - blocks
        self.players[1].chat_msg[self.players[2].name] += msg.decode()
        self.players[2].chat_msg[self.players[1].name] += msg.decode()
        '''
        self.players[0].chat_msg[self.players[1].name] = "{0}\n{1}".format(self.players[0].chat_msg[self.players[1].name], msg.decode())
        self.players[1].chat_msg[self.players[0].name] = "{0}\n{1}".format(self.players[1].chat_msg[self.players[0].name], msg.decode())

        #print(type(st))
        for player in self.players:
          #  print(player.chat_msg)
            #print(player.chat_msg)
            if player.name != from_player.name and player.flagcj ==1:

             #   player.chat_msg[from_player.name] = "{0}\n{1}".format(player.chat_msg[from_player.name], st)
              #  print(player.chat_msg[from_player.name])
                    #+= msg.docode()
                player.socket.sendall(msg)
             #   print("stored")
            else:
               # from_player.chat_msg[player.name] = "{0}\n{1}".format(player.chat_msg[from_player.name], st)
                #print("{0}\n{1}".format(player.chat_msg[from_player.name], st))
               # print("stored")
                pass

    def remove_player(self, player):
        self.players.remove(player)
        #leave_msg = player.name.encode() + b"has left the room\n"
        #self.broadcast(player, leave_msg)

class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name
        self.leaveflag = 0
        if self.name not in archive.keys():
                archive[self.name] = ""
                self.chats = ""
        else:
            self.chats = archive[self.name]

    def welcome_new(self, from_player):
        msg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
          if player.name!= from_player.name:
            player.socket.sendall(msg.encode())

    def broadcast(self, from_player, msg):
        ms = from_player.name + " : "+ msg.decode()
        if self.leaveflag == 0:
         archive[self.name] = "{0}\n{1}".format(archive[self.name],ms)

        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
          if player.flagcj ==0 or player.name!=from_player.name:
            player.socket.sendall(msg)

    def remove_player(self, player):
        self.leaveflag = 1
        self.players.remove(player)
        leave_msg = b"has left the room\n"
        self.broadcast(player, leave_msg)
        a = shelve.open('chat_archive')
        a[self.name] = archive[self.name]
        a.close()
        self.leaveflag = 0

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
        self.chat_msg = {}
        #sockets_list()
        self.flagcj = 1

    def fileno(self):
        return self.socket.fileno()
