import pickle

def local_write(storage_spaces):
    file = open('./bases/static/storage_spaces.txt', 'wb')
    pickle.dump(storage_spaces, file)
    file.close()

def local_read():
    with open('./bases/static/storage_spaces.txt', 'rb') as f:
        spaces = pickle.load(f)
    return spaces

