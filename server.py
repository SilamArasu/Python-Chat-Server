import select, socket, sys, pdb
from util import Hall, Room, Player
import util,shelve
from Crypto.Cipher import DES
des = DES.new('password', DES.MODE_ECB)
#cipher_text = des.encrypt(text)

#des.decrypt(cipher_text)
d = None
loginFile = None




READ_BUFFER = 4096

def login(new_socket):
    instructions = "\n<login> to login\n<register> to register\n"

    while True :
      #  dat()
        new_socket.sendall(instructions.encode())
        msg = new_socket.recv(READ_BUFFER).decode()
        if "<login>" in msg :
            new_socket.sendall("Enter username\t".encode())
            name = new_socket.recv(READ_BUFFER).decode()
            new_socket.sendall("Enter password \t".encode())
            pwd = new_socket.recv(READ_BUFFER).decode().strip('\n')
            pwd = des.encrypt(pwd.rjust(8))
            try:
             d = shelve.open('data')
             loginFile = dict(d)
             d.close()
             if loginFile[name]== pwd:
               # loginFile.close()
                break
            except:
                new_socket.sendall("Please check your details".encode())
        if "<register>" in msg:
            new_socket.sendall("Enter username\t".encode())
            name = new_socket.recv(READ_BUFFER).decode()
            new_socket.sendall("Enter password \t".encode())
            pwd = new_socket.recv(READ_BUFFER).decode().strip('\n')
            pwd = des.encrypt(pwd.rjust(8))
            d = shelve.open('data')
            d[name] = pwd
            d.close()
            break
        #loginFile.close()
    print("name "+name)
    return name


host = "127.0.0.1"
#host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = util.create_socket((host, util.PORT))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)
i=1
while True:
    #print("connecttion list")
    #print(connection_list)
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock: # new connection, player is a socket
            new_socket, add = player.accept()
            name = login(new_socket)
            new_player = Player(new_socket)
            connection_list.append(new_player)
            i+=1
            name = "name: "+name
            hall.handle_msg(new_player,name)
           # hall.welcome_new(new_player)

        else: # new message
            msg = player.socket.recv(READ_BUFFER)#client to server
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(player, msg)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
