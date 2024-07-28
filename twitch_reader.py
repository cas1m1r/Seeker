# python raw socket irc example
from dotenv import load_dotenv
import logging
import socket
import os


load_dotenv()

app_id = os.environ['AUTH']
oauth_uri = f'https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={app_id}&redirect_uri=https://id.twitch.tv&scope=chat%3Aread+chat%3Aedit'

print(f'VISIT:\n')
print(oauth_uri)


auth = str(input('Now enter the oauth token below: '))
channel = str(input('Enter channel to join: '))

# IRC Server Settings (Example)
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'IAmJacksTestBed'
token = f'oauth:{auth}'
channel = f'#{channel}'

# connect to channel defined above
s = socket.socket()
s.connect((server, port))

# Join channel
s.send(f'PASS {token}\n'.encode('utf-8'))
s.send(f'NICK {nickname}\n'.encode('utf-8'))
s.send(f'JOIN {channel}\n'.encode('utf-8'))

# Setup Logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler(f'{channel.replace("#","")}.chat.log', encoding='utf-8')])
print(f'[+] Connected to Chat')
# listen for events
listening = True
while listening:
    try:
        response = s.recv(2048).decode('utf-8')
        # Check whether it's a heartbeat packet
        if response.startswith('PING'):
            s.send("PONG\n".encode('utf-8'))
        # else log response
        elif len(response) > 0:
            logging.info(response)

    except KeyboardInterrupt:
        listening = False
        print(f'[X] Leaving {channel}')
        pass
