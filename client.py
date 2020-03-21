import select, socket, sys
from util import Room, Hall, Player
import util
import shelve

READ_BUFFER = 4096

#namenpass = shelve.open('mydata')
#sign =
#while True:
host = ""
if len(sys.argv) < 2:
    host = "127.0.0.1"
else:
    host = sys.argv[1]



server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_connection.connect((host, util.PORT))

def prompt():
    print('>', end=' ', flush = True)

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection: # incoming message 
            msg = s.recv(READ_BUFFER)
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                if msg == util.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    #sys.stdout.write(msg.decode())
                    print(msg.decode())
                    '''
                    if 'Please tell us your name' in msg.decode():
                        msg_prefix = 'name: ' # identifier for name
                    else:
                        msg_prefix = ''
                    '''
                    prompt()

        else:


            msg = msg_prefix + sys.stdin.readline()
            server_connection.sendall(msg.encode())

