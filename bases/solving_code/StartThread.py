from threading import Thread
import time
import pickle

# 0 or 1 - 0 is False, 1 is True
def write_file(value):
    file = open('./bases/static/active.txt', 'wb')
    pickle.dump(value, file)
    file.close()

def check_real_time_update():
    with open('./bases/static/active.txt', 'rb') as f:
        activate = pickle.load(f)
    return activate == 1

def start_update():
    write_file(1)

def stop_update():
    write_file(0)

