import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# after connection sever will send sessionId to use
sessionId = 0b00000000
flags = 0b010
# flags:
# 0-- last message, calculate
# 1-- next messages coming, wait
# -0- sessionId obtained
# -1- sessionId pending
# --0 default flag - client always sends 0
# --1 val1 and val2 are equal

# bin(x)[2:].zfill(y) <- might be helpful ; x - value in decimal to change to binary string; y - total length of the
# value needed

status = 0b00
# 00 - all good
# 01 - overflow error
# 10 - dividing by zero
# 11 - error (connection and other not specified before)

operation = input("Choose operation type[+, -, *, /, %, ^, >?, root]: ")

# >? - comparison - uses the 3rd flag to signalise if values are equal and returns the bigger one

# Change these if you can:
op = 0b000
if operation == '+':
    op = 0b000
if operation == '-':
    op = 0b001
if operation == '*':
    op = 0b010
if operation == '/':
    op = 0b011
if operation == '%':
    op = 0b100
if operation == '^':
    op = 0b101
if operation == '>?':
    op = 0b110
if operation == 'root':
    op = 0b111

val1 = int(input("Insert first value (max: 4 294 967 296): "))
# make this adequate for each operation!
val2 = int(input("Insert second value (max: 4 294 967 296): "))

print("Value 1: " + str(val1))
print("Value 2: " + str(val2))
print("Operation type: " + str(op))
print("Status: " + str(status))
print("Session id: " + str(sessionId))
print("Flags: " + str(flags))

binaryPacket = op*(2**77) + val1*(2**45) + val2*(2**13) + status*(2**11) + sessionId*(2**3) + flags

print(binaryPacket)
print(bin(binaryPacket))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(binaryPacket.to_bytes(10, 'big'))
    data = s.recv(1024)

# before repeating querry change last flag (--*) to zero!

print('Received', repr(data))
