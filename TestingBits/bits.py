# after connection sever will send sessionId to use
sessionId = bin(0)[2:].zfill(8)
flags = bin(2)[2:].zfill(3)
# flags:
# 0-- last message, calculate
# 1-- next messages coming, wait
# -0- sessionId obtained
# -1- sessionId pending
# --0 for future use
# --1 ^

status = bin(0)[2:].zfill(2)
# 00 - all good
# 01 - result out of bounds
# 10 - dividing by zero
# 11 - error (connection and other not specified before)

operation = input("Choose operation type[+, -, *, /, %, ^, ==, sqrt]: ")

#Change these if you can:

if operation == '+':
    op = bin(0)[2:].zfill(3)
if operation == '-':
    op = bin(1)[2:].zfill(3)
if operation == '*':
    op = bin(2)[2:].zfill(3)
if operation == '/':
    op = bin(3)[2:].zfill(3)
if operation == '%':
    op = bin(4)[2:].zfill(3)
if operation == '^':
    op = bin(5)[2:].zfill(3)
if operation == '==':
    op = bin(6)[2:].zfill(3)
if operation == 'sqrt':
    op = bin(7)[2:].zfill(3)

val1 = input("Insert first value (max: 4 294 967 296): ")
val2 = input("Insert second value (max: 4 294 967 296): ")
val1b = bin(int(val1))[2:].zfill(32)
val2b = bin(int(val2))[2:].zfill(32)
print("Value 1: " + val1b)
print("Value 2: " + val2b)
print("Operation type: " + op)
print("Status: " + status)
print("Session id: " + sessionId)
print("Flags: " + flags)

#All of these are strings so we can append them:

binaryPacket = op + val1b + val2b + status + sessionId + flags

print(binaryPacket)