import socket

KNOWN_PORT = 9999
PORT = 9999
SERVER = socket.gethostbyname(socket.gethostname()) #Gets IP of server
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind(ADDR)

while True:
    clients = []

    while True:
        data, address = sock.recvfrom(128)
        password = sock.recv(1024).decode(FORMAT)
        #print(password.strip())
        if (password.strip() == 'password'):
            print('connection from: {}'.format(address))
            clients.append(address)
            sock.sendto(b'ready', address)
        else:
            sock.sendto(b'access denied', address)

        if len(clients) == 2:
            print('got 2 clients, sending details to each')
            c1 = clients.pop()
            c1_addr, c1_port = c1
            c2 = clients.pop()
            c2_addr, c2_port = c2

            sock.sendto('{} {} {}'.format(c1_addr, c1_port, KNOWN_PORT).encode(FORMAT), c2)
            sock.sendto('{} {} {}'.format(c2_addr, c2_port, KNOWN_PORT).encode(FORMAT), c1)
            break
