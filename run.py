import os
import argparse
from thebard.thebard import TheBard

tb = TheBard('story.json')

import os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--debug', required=False, help="Runs the bard in debug mode (skips introduction).")
    argv = vars(ap.parse_args())

    clear()
    tb.start(debug=argv['debug'])