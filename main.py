import requests
import threading


class ServerJoiner(threading.Thread):
    def __init__(self, invite, hmac_session):
        threading.Thread.__init__(self)
        self.guild_invite = invite
        self.hmac_session = hmac_session
        
    def run(self):
        session = requests.Session()
        session.headers = {"cookie" : f"hmac_signed_session={self.hmac_session}"}
        resp = session.put(f"https://www.guilded.gg/api/invites/{self.guild_invite}")
        
        if "id" in resp.json(): 
            print(f"Joined Server: {self.hmac_session[:30]}")
        elif "code" in resp.json(): 
            print(f"Error Joining Server: {self.hmac_session[:30]}")


if __name__ == "__main__":
    invite = input("Enter guild invite code: ")

    with open("cookies.txt", "r") as _cookies:
        cookies =  []
        cookies += [_cookie.strip() for _cookie in _cookies.readlines()]

    for cookie in cookies:
        ServerJoiner(invite=invite, hmac_session=cookie).start()
