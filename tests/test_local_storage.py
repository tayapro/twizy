import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from lib import local_storage

def test_set_and_get_item():
    # Set an item in the storage
    local_storage.set_item("user", "John")

    # Get the item from the storage and assert its value
    assert local_storage.get_item("user") == "John"

def test_get_item_nonexistent_key():
    # Get an item with a nonexistent key
    assert local_storage.get_item("invalid_user_key") is None

def test_clear_storage():
    # Set an item in the storage
    local_storage.set_item("user", "John")

    # Clear the storage
    local_storage.clear()

    # Try to get the item, should return None since storage was cleared
    assert local_storage.get_item("user") is None

def test_clear_storage_empty():
    # Clear the storage when it's already empty
    local_storage.clear()

    # Ensure no exceptions are raised and storage is empty
    assert local_storage.get_item("user") is None

# if __name__ == "__main__":
#     pytest.main()
