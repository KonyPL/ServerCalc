import socket
import random
import math

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # start of data processing
            # getting variables
            data = int.from_bytes(data, 'big')
            bitShift = ((2**3), (2**11), (2**13), (2**45), (2**77))
            # getting flags
            temp = data % bitShift[0]
            flags = temp
            data -= temp
            # getting sessionId
            temp = data % bitShift[1]
            sessionId = int(temp / bitShift[0])
            data -= temp
            # getting status
            temp = data % bitShift[2]
            status = int(temp / bitShift[1])
            data -= temp
            # getting val2
            temp = data % bitShift[3]
            val2 = int(temp / bitShift[2])
            data -= temp
            # getting val1
            temp = data % bitShift[4]
            val1 = int(temp / bitShift[3])
            # getting op
            data -= temp
            op = int(data / bitShift[4])
            # end of getting variables

            # sessionId setting
            if flags == 7 or 6 or 3 or 2:
                sessionId = random.randint(1, 255)
                flags -= 2

            # math operations
            try:
                if op == 0:
                    val1 = val1 + val2
                if op == 1:
                    val1 = val1 - val2
                if op == 2:
                    val1 = val1 * val2
                if op == 3:
                    val1 = val1 / val2
                if op == 4:
                    val1 = val1 % val2
                if op == 5:
                    val1 = val1**val2
                if op == 6:
                    if val1 == val2:
                        flags += 1
                    elif val2 > val1:
                        val1 = val2
                if op == 7:
                    val1 = val1 ** (1. / val2)
                    val1 = int(val1)

                val2 = 0
                status = 0

            except ZeroDivisionError:
                status = 2
            except OverflowError:
                status = 1


            print("Value 1: " + str(val1))
            print("Value 2: " + str(val2))
            print("Operation type: " + str(op))
            print("Status: " + str(status))
            print("Session id: " + str(sessionId))
            print("Flags: " + str(flags))

            data = op * (2**77) + val1 * (2**45) + val2 * (2**13) + status * (2**11) + sessionId * (2**3) + flags
            # end of processing data
            conn.sendall(data.to_bytes(10, 'big'))
