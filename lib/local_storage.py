storage = {}


def set_item(key, value):
    global storage
    storage[key] = value


def get_item(key):
    return storage.get(key)
  

def clear():
    global storage
    storage = {}
