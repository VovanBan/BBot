import threading
from bots.memabot import main_memabot
from bots.memabotedit import main_memabotedit

if __name__ == '__main__':
    threading.Thread(target=main_memabot()).start()
    threading.Thread(target=main_memabotedit()).start()
