import socket
import multiprocessing
import time
from threading import Thread

class ServerJoiner(object):
    def __init__(self, invite, hmac_session):
        self.guild_invite = invite
        self.hmac_session = hmac_session
    
    def join(self):
        s = socket.socket()
        s.connect(("www.guilded.gg", 443))

        s.send(f"PUT /api/invites/{self.guild_invite} HTTP/1.1\r\n".encode())
        s.send(f"Host: www.guilded.gg\r\n".encode())
        s.send(f"User-Agent: Python\r\n".encode())
        s.send(f"Accept: */*\r\n".encode())
        s.send(f"Accept-Language: en-US,en;q=0.5\r\n".encode())
        s.send(f"Referer: https://www.guilded.gg/\r\n".encode())
        s.send(f"Cookie: hmac_signed_session={self.hmac_session}\r\n".encode())
        s.send(f"Connection: close\r\n\r\n".encode())

        resp = s.recv(4096)
        if b"code" in resp:
            print(f"Error Joining Server: {self.hmac_session[:30]}")
        elif b"id" in resp:
            print(f"Joined Server: {self.hmac_session[:30]}")
        s.close()

def main():
    invite = input("Enter guild invite code: ")

    with open("cookies.txt", "r") as _cookies:
        cookies =  []
        cookies += [_cookie.strip() for _cookie in _cookies.readlines()]

    for cookie in cookies:
        Thread(target=ServerJoiner(invite=invite, hmac_session=cookie).join).start()
        
if __name__ == "__main__":
    main()
