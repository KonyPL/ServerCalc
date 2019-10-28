import socket

# HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# after connection sever will send sessionId to use
previousId = 0
sessionId = 0b00000000
flags = 0b010
# flags:
# 0-- last message, calculate
# 1-- next messages coming, wait
# -0- sessionId obtained
# -1- sessionId pending
# --0 default flag - client always sends 0
# --1 val1 and val2 are equal
HOST = ''

def reconnect():
    while True:
        recon = input("Do you want to reconnect? (Yes/No) ")
        if recon == "Yes" or recon == "yes" or recon == "Y" or recon == "y":
            print("Reconnecting . . .")
            return True
        elif recon == "No" or recon == "no" or recon == "N" or recon == "n":
            return False


# bin(x)[2:].zfill(y) <- might be helpful ; x - value in decimal to change to binary string; y - total length of the
# value needed

conn = True
session = True

while conn:

    try:
        # user defines the server address
        if HOST == '':
            HOST = input("Type the server address in IPv4 format (ex. 192.168.43.148): ")
            print("Connecting . . .")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print("Connected with server!")
                status = 0b00
                # 00 - all good
                # 01 - overflow error
                # 10 - dividing by zero
                # 11 - error (connection and other not specified before)
                while session:
                    # >? - comparison - uses the 3rd flag to signalise if values are equal and returns the bigger one
                    while True:
                        operation = input("Choose operation type[+, -, *, /, %, ^, >?, root]: ")
                        op = 0b000
                        if operation == '+':
                            op = 0b000
                            break
                        if operation == '-':
                            op = 0b001
                            break
                        if operation == '*':
                            op = 0b010
                            break
                        if operation == '/':
                            op = 0b011
                            break
                        if operation == '%':
                            op = 0b100
                            break
                        if operation == '^':
                            op = 0b101
                            break
                        if operation == '>?':
                            op = 0b110
                            break
                        if operation == 'root':
                            op = 0b111
                            break


                    # Determining how many values user wants to use
                    while True:
                        try:
                            valuesleft = int(input("Choose with how many values you want to work (at least 2): "))
                            if valuesleft < 2:
                                raise OverflowError("Value is less than 2! ")
                            firstTwo = True
                            break
                        except ValueError:
                            print("That is not an integer! Try again:")
                        except OverflowError as error:
                            print(str(error) + "Try again:")

                    # repeat until finishes sending all values
                    while valuesleft > 0:
                        flags += 4
                        if firstTwo:
                            while True:
                                try:
                                    val1 = int(input("Insert first value (max: 4 294 967 295): "))
                                    if val1 > 4294967295:
                                        raise OverflowError("Value is too big. ")
                                    if val1 < 0:
                                        raise OverflowError("Value is negative. This program works only with positive "
                                                            "values. ")
                                    valuesleft -= 1
                                    firstTwo = False
                                    break
                                except ValueError:
                                    print("That is not an integer! Try again:")
                                except OverflowError as error:
                                    print(str(error) + "Try again:")
                        else:
                            val1 = result1

                        while True:
                            try:
                                val2 = int(input("Insert next value (max: 4 294 967 295): "))
                                if val2 > 4294967295:
                                    raise OverflowError("Value is too big. ")
                                if val2 < 0:
                                    raise OverflowError("Value is negative. This program works only with positive "
                                                        "values. ")
                                break
                            except ValueError:
                                print("That is not an integer! Try again:")
                            except OverflowError as error:
                                print(str(error) + "Try again:")
                        valuesleft -= 1
                        if valuesleft == 0:
                            flags -= 4
                        # debugging code
                        # print("Value 1: " + str(val1))
                        # print("Value 2: " + str(val2))
                        # print("Operation type: " + str(op))
                        # print("Status: " + str(status))
                        # print("Session id: " + str(sessionId))
                        # print("Flags: " + str(flags))
                        data = 0
                        data = op*(2**77) + val1*(2**45) + val2*(2**13) + status*(2**11) + sessionId*(2**3) + flags

                        s.sendall(data.to_bytes(10, 'big'))
                        data = s.recv(1024)

                        # start of data processing
                        # getting variables
                        data = int.from_bytes(data, 'big')
                        bitShift = ((2 ** 3), (2 ** 11), (2 ** 13), (2 ** 45), (2 ** 77))

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

                        # getting result2
                        temp = data % bitShift[3]
                        result2 = int(temp / bitShift[2])
                        data -= temp

                        # getting result1
                        temp = data % bitShift[4]
                        result1 = int(temp / bitShift[3])

                        # getting op
                        data -= temp
                        op = int(data / bitShift[4])

                        # end of getting variables

                        # debugging code
                        # print("Result 1: " + str(result1))
                        # print("Operation type: " + str(op))
                        # print("Status: " + str(status))
                        # print("Session id: " + str(sessionId))
                        # print("Flags: " + str(flags))

                        if sessionId != previousId:
                            print("Session id obtained! It's value is " + str(sessionId))
                            previousId = sessionId

                        if status != 0:
                            if status == 1:
                                print("### Error! Result of operation caused overflow!")
                            elif status == 2:
                                print("### Error! Division by zero!")
                            else:
                                print("### Error! Something went wrong!")
                        else:
                            if flags == 1 or flags == 3 or flags == 5 or flags == 7:
                                flags -= 1
                                print("Both values are equal")
                            else:
                                if op == 0:
                                    operation = ' + '
                                if op == 1:
                                    operation = ' - '
                                if op == 2:
                                    operation = ' * '
                                if op == 3:
                                    operation = ' / '
                                if op == 4:
                                    operation = ' % '
                                if op == 5:
                                    operation = ' ^ '
                                if op == 6:
                                    print("The " + str(result1) + " is greater than other")
                                elif op == 7:
                                    if val2 == 1:
                                        order = 'st'
                                    elif val2 == 2:
                                        order = 'nd'
                                    elif val2 == 3:
                                        order = 'rd'
                                    else:
                                        order = 'th'

                                    print(str(val2) + order + " root of " + str(val1) + " = " + str(result1))
                                else:
                                    # showing the result
                                    print(str(val1) + operation + str(val2) + " = " + str(result1))
                    # check if user wants to end connection
                    while True:
                        calc = input("Do you want to make another calculation? If no - program will close. (Yes/No) ")
                        if calc == "Yes" or calc == "yes" or calc == "Y" or calc == "y":
                            break
                        elif calc == "No" or calc == "no" or calc == "N" or calc == "n":
                            session = False
                            conn = False
                            while True:
                                serverpwr = input("Do you want to shut server down? (Yes/No) ")
                                if serverpwr == "Yes" or serverpwr == "yes" or serverpwr == "Y" or serverpwr == "y":
                                    status = 3
                                    data = 0
                                    data = status * (2 ** 11) + sessionId * (2 ** 3) + flags
                                    s.sendall(data.to_bytes(10, 'big'))
                                    data = s.recv(1024)
                                    data = int.from_bytes(data, 'big')
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
                                    data = 0
                                    if status == 0:
                                        print("Server shut down properly.")
                                    break
                                elif serverpwr == "No" or serverpwr == "no" or serverpwr == "N" or serverpwr == "n":
                                    break
                            break
        except ConnectionRefusedError:
            print("### Error! Connection refused by server. It is very probable that the server isn't running or the "
                  "address is wrong.")
            conn = reconnect()
        except ConnectionAbortedError:
            print("### Error! Connection has been aborted by the server!")
            conn = reconnect()
        except ConnectionResetError:
            print("### Error! Connection has been reset by server. ")
            conn = reconnect()

    except socket.gaierror:
        print("### Error! Wrong IP address format!")
        HOST = ''
    except TimeoutError:
        print("""### Timeout Error! Connection attempt failed, because connected device didn't reply properly after 
### set time period or connection failed, because connected host didn't reply.""")
        HOST = ''
