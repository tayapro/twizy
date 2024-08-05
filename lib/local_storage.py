storage = {}


def set_item(key, value):
    """
    The function sets a key-value pair in the in-memory storage.
    """
    global storage
    storage[key] = value


def get_item(key):
    """
    The function retrieves a value from the in-memory storage by key.
    """
    return storage.get(key)
  

def clear():
    """
    The function clear all items from the in-memory storage.
    """
    global storage
    storage = {}
