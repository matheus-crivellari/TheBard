import os
from thebard.thebard import TheBard

tb = TheBard('story.json')

def clear():
    os.system('cls')
    
if __name__ == '__main__':
    clear()
    tb.start()