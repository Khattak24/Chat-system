import socket, threading
import logging
import datetime
import urllib.request as urllib2
import random
from chat_database import connect_db

# get logger for the XFlowResearch Chat System
logger = logging.getLogger(__name__)

# socket
ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind
HOST = '127.0.0.1'
PORT = 12345
ser_sock.bind((HOST, PORT))

# listen
ser_sock.listen(1)
print('XFlowResearch Chat started on port : ' + str(PORT))

def store_data(chat, chat_time):
    try:
        conn = connect_db()
        # Insert recors into the database
        conn.execute("INSERT INTO chat VALUES (?,?)", (chat, chat_time))
        logging.exception("Database : Data inserted successfully and timestamp is : " + str(datetime.datetime.now()))
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        logging.exception(
            "Error : Error while adding data into database and timestamp is : " + str(datetime.datetime.now))
        return False


def server_status(server_time):
    print("************  ALL Clients ***************")
    print("Total Number of Clients : " + str(len(CONNECTION_LIST)))
    for client in CONNECTION_LIST:
        print(client[0].decode() + " is active")

    print("**************** Server Up Time ******************")
    now = datetime.datetime.now()
    server_total_up_time = now - server_time
    print("Server Up time is : " + str(server_total_up_time / 60) + " Minutes")
    return True


def get_random_words():
    fetch_words = "https://www.mit.edu/~ecprice/wordlist.10000"
    web_response = urllib2.urlopen(fetch_words)
    response_in_txt_format = web_response.read()
    words_list = response_in_txt_format.splitlines()
    first_word = random.choice(words_list)
    second_word = random.choice(words_list)
    return first_word + second_word


def accept_client(server_time):
    while True:
        # accept
        client_socket, cli_add = ser_sock.accept()
        ## first text assumed as a user name
        username = client_socket.recv(1024)

        CONNECTION_LIST.append((username, client_socket))
        print('%s is now connected' % username)

        ## welcome message to client with timestamp
        now = datetime.datetime.now()
        logger.info(
            "New Connection : New client is connected with the username : " + username.decode() + " and connection timestamp is :" + str(
                now))
        welcome_message = " Welcome to the XFlowResearch Chatting System, Your connection time is : " + str(now)
        client_socket.send(welcome_message.encode())

        ## Print the server up time and available clients
        server_status(server_time)

        ## making a thread for each client message
        thread_client = threading.Thread(target=broadcast_usr, args=[username, client_socket])
        thread_client.start()


def broadcast_usr(username, client_socket):
    while True:
        try:
            ## recieve data from client
            data = client_socket.recv(1024)
            if data:
                ## chaeck if user wants to quit then send a good bye message
                ## replace \r is use because i'm using packet tracer so it format the data
                if data.decode().replace("\r", "") == "quit":
                    goodbye_message_list = ['Catch ya later, future dudes! Good Bye',
                                            'Shine on, you crazy diamonds. Good Bye',
                                            'Dont forget to be awesome. Good Bye']
                    goodbye_message = random.choice(goodbye_message_list)
                    msg = ("Hi " + username.decode() + ", " + goodbye_message).encode()

                    ## connection close timestamp
                    now = datetime.datetime.now
                    logger.info(
                        "Connection Close : Client wants to close connection, username is : " + username.decode() + " and closeing connection timestamp is :" + str(
                            now))

                    ## sending good bye message
                    client_socket.send(msg)
                    ## connection close for this specific user
                    client_socket.close()
                    return

                ## Print message on server about the status which user is speaking
                # print ("{0} spoke".format(username))
                print(username.decode() + " Spoke")

                ## broad user message to all connected clients
                broadcast_usr_message(client_socket, username, data)
        except BlockingIOError:
            logger.error("Error while communication : socket is open and reading from it would block")
            return False
        except ConnectionResetError:
            logger.error("Error while communication : socket was closed for some other reason")
            return True
        except Exception as e:
            logging.exception("unexpected exception when checking if a socket is closed")
            return False


def broadcast_usr_message(client_socket, sender_name, msg):
    for client in CONNECTION_LIST:

        ## here check message is not sending to my self means tu current user
        if client[1] != client_socket:
            ## the sender name means the client name
            user_name = sender_name.decode() + " ->"

            ## fetch some random words
            fetch_words = get_random_words()

            ## send data to database by calling bellow function
            store_data(msg.decode(), datetime.datetime.now())

            ## extract only 256 characters it will start from 0 to 255
            msg = msg.decode()[:256]

            """
                finally encode the message again and send it to user 
                format of message is USERNAME, MESSAGE and then the RANDOM WORD
                e.g
                Ishfaq -> Hi this message is from ishfaq : abcdzxcv
            """
            ## set message format
            formatted_message = user_name + msg + " : " + fetch_words.decode()

            client[1].send(formatted_message.encode())


if __name__ == "__main__":
    try:
        CONNECTION_LIST = []
        
        server_time = datetime.datetime.now()
        logger.info("Server setup : Server is start and timestamp is : " + str(server_time))
        thread_ac = threading.Thread(target=accept_client, args=[server_time])
        thread_ac.start()
    except Exception as ex:
        print(ex)
        logging.exception("Error : Error while creating server")

