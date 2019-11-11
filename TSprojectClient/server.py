import socket
import random

HOST = '127.0.0.1'  # Set here this server IP Address
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

print("Server is running!")
pwr = True
while pwr:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # from now on connected socket is referenced as 's'
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    # recieve data from client
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
                    data = 0
                    # end of getting variables
                    
                    #print all variables got from client
                    print("Value 1: " + str(val1))
                    print("Value 2: " + str(val2))
                    print("Operation type: " + str(op))
                    print("Status: " + str(status))
                    print("Session id: " + str(sessionId))
                    print("Flags: " + str(flags))

                    if status == 3: # if status sent from client equals 11 (binary) shut down the server
                        pwr = False
                        status = 0
                    # sessionId setting
                    if flags == 7 or flags == 6 or flags == 3 or flags == 2:
                        sessionId = random.randint(1, 255)
                        flags -= 2

                    # math operations
                    try:
                        if op == 0: # addition
                            if val1 + val2 > 4294967295:
                                val1 = val2 = 0
                                raise OverflowError
                            val1 = val1 + val2
                        if op == 1: # subtraction
                            if val2 > val1:
                                val1 = val2 = 0
                                raise OverflowError
                            val1 = val1 - val2
                        if op == 2: # multiplication
                            if val1 * val2 > 4294967295:
                                val1 = val2 = 0
                                raise OverflowError
                            val1 = val1 * val2
                        if op == 3: # division
                            val1 = int(val1 / val2)
                        if op == 4: # modulo
                            val1 = val1 % val2
                        if op == 5: # exponentation
                            if val1 ** val2 > 4294967295:
                                val1 = val2 = 0
                                raise OverflowError
                            val1 = val1**val2
                        if op == 6: # comparation
                            if val1 == val2:
                                flags += 1
                            elif val2 > val1:
                                val1 = val2
                        if op == 7: # root
                            val1 = val1 ** (1. / val2)
                            val1 = int(val1)

                        val2 = 0
                        status = 0
                    # handling errors
                    except ZeroDivisionError:
                        status = 2
                    except OverflowError:
                        status = 1
                    
                    # checking if "next message coming" flag is set, if so - change it to 0
                    if (int(flags / 4)) > 0:
                        flags -= 4
                    # print all values that are going to be send back to client
                    print("### After calculations ###")
                    print("Result: " + str(val1))
                    print("Status: " + str(status))
                    print("Session id: " + str(sessionId))
                    print("Flags: " + str(flags))
                    print("### ------------------ ###")

                    # packing up data into one value
                    data = op * (2**77) + val1 * (2**45) + val2 * (2**13) + status * (2**11) + sessionId * (2**3) + flags
                    # end of processing data
                    # sending data in bytes back to client
                    conn.sendall(data.to_bytes(10, 'big'))
                    if not pwr:
                        print("Server shut down due to client request")
    except ConnectionError:
        print("Connection with " + str(addr[0]) + " lost!")



