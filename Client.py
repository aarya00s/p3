import socket
import sys
import threading


PORT = 9999
KNOWN_PORT = 50002
SERVER = socket.gethostbyname(socket.gethostname()) #Gets IP of server
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((socket.gethostbyname(socket.gethostname()), 50001))
sock.sendto(b'0', ADDR)

while True:
    password = input('>')
    sock.sendto(password.encode(FORMAT), ADDR)
    data = sock.recv(1024).decode(FORMAT)

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break
    else:
        print(data.strip())
        quit()

data = sock.recv(1024).decode(FORMAT)
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode(FORMAT)), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(FORMAT), (ip, sport))