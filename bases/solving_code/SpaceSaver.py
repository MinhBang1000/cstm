import pickle


class SpaceSaver():
    
    def local_write(self, storage_spaces):
        file = open('./bases/static/storage_spaces.txt', 'wb')
        pickle.dump(storage_spaces, file)
        file.close()
    
    def local_read(self):
        with open('./bases/static/storage_spaces.txt', 'rb') as f:
            spaces = pickle.load(f)
        return spaces

