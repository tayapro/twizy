storage = {}


def set_item(key, value):
    """
    Set a key-value pair in the in-memory storage.
    """
    global storage
    storage[key] = value


def get_item(key):
    """
    Retrieve a value from the in-memory storage by key.
    """
    return storage.get(key)
  

def clear():
    """
    Clear all items from the in-memory storage.
    """
    global storage
    storage = {}
