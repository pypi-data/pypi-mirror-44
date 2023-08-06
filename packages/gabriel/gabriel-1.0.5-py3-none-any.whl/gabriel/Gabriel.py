import argparse
from pypresence import Presence
import time
import json
import signal
import sys

argparser = argparse.ArgumentParser(description="Discord RPC command line client")

class Gabriel:
    """Main Class"""

    def __init__(self):
        argparser.add_argument('--config', help="Use a config file for RPC")
        argparser.add_argument('--input', action="store_true", help="Get asked for RPC info")
        a = argparser.parse_args()
        if a.config:
            self.config(a.config)
        elif a.input:
            self.input()
        else:
            print('Nothing provided.\nUse gab -h for more info')
            sys.exit()


        RPC = Presence(self.options['client_id'])
        RPC.connect()

        RPC.update(state=self.options['state'], details=self.options['details'], large_image=self.options["lg_img"], large_text=self.options["lg_text"], small_image=self.options["sm_img"], small_text=self.options["sm_text"])
        print('RPC sucessfully running!\nCtrl-C to exit.')

    def input(self):
        print('')
        print('What is the client id? ')
        client_id = input()
        print('State message?')
        state = input()
        print('Details?')
        details = input()
        print('Large image?')
        lg_img = input()
        print('Large image text?')
        lg_text = input()
        print('Small image?')
        sm_img = input()
        print('Small image text?')
        sm_text = input()

        self.options = {
            'client_id':client_id,
            'state': state,
            'details': details,
            'lg_img': lg_img,
            'lg_text': lg_text,
            'sm_img': sm_img,
            'sm_text': sm_text
        }

    def config(self, conf):
        conf = json.load(open(conf))

        self.options = {
            'client_id': conf['client_id'],
            'state': conf['state'],
            'details': conf['details'],
            'lg_img': conf["lg_img"],
            'lg_text': conf["lg_text"],
            'sm_img': conf["sm_img"],
            'sm_text': conf["sm_text"]
        }


signal.signal(signal.SIGINT, lambda number, frame: sys.exit())
Gabriel()

while True:
    time.sleep(15)