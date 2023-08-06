import argparse
from pypresence import Presence
import time
import json

argparser = argparse.ArgumentParser(description="Discord RPC command line client")

class Gabriel:
    """Main Class"""

    def __init__(self):
        argparser.add_argument('--config', help="RPC Large image")
        a = argparser.parse_args()
        # self.parser()
        if a.config:
            self.config(a.config)
        else:
            self.parser()


        RPC = Presence(self.shit['client_id'])
        RPC.connect()

        RPC.update(state=self.shit['state'], details=self.shit['details'], large_image=self.shit["lg_img"], large_text=self.shit["lg_text"], small_image=self.shit["sm_img"], small_text=self.shit["sm_text"])
        print('RPC sucessfully running!\nCtrl-C to exit.')

    def parser(self):
        aaaa = argparse.ArgumentParser(description="Discord RPC command line client")

        aaaa.add_argument('client_id', metavar="CLIENT_ID", nargs="?", help="RPC Client ID")
        aaaa.add_argument('details', metavar="DETAILS", nargs="?", help="RPC Details")
        aaaa.add_argument('state', metavar="STATE_MESSAGE", nargs="?", help="RPC State Message")
        aaaa.add_argument('--lg-img', help="RPC Large image")
        aaaa.add_argument('--lg-text', help="RPC Large image tooltip")
        aaaa.add_argument('--sm-img', help="RPC Small image")
        aaaa.add_argument('--sm-text', help="RPC Small image tooptip")


        b = argparser.parse_args()

        self.shit = {
            'client_id': b.client_id,
            'state': b.state,
            'details': b.details,
            'lg_img': b.lg_img,
            'lg_text': blg_text,
            'sm_img': bsm_img,
            'sm_text': b.sm_text
        }

    def config(self, conf):
        conf = json.load(open(conf))

        self.shit = {
            'client_id': conf['client_id'],
            'state': conf['state'],
            'details': conf['details'],
            'lg_img': conf["lg_img"],
            'lg_text': conf["lg_text"],
            'sm_img': conf["sm_img"],
            'sm_text': conf["sm_text"]
        }

