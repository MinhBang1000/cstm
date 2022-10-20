import pickle


class SpaceSaver():
    
    def local_write(self, storage_spaces, storage_id):
        file = open('./bases/static/storage_spaces_'+str(storage_id)+'.txt', 'wb')
        pickle.dump(storage_spaces, file)
        file.close()
    
    def local_read(self, storage_id):
        with open('./bases/static/storage_spaces_'+str(storage_id)+'.txt', 'rb') as f:
            spaces = pickle.load(f)
        return spaces

