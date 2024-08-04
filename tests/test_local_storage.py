import pytest

from lib import local_storage


def test_set_and_get_item():
    """
    The test verifies that an item can be correctly set in the local
    storage and then retrieved. It ensures that the value stored matches
    the value retrieved.
    """

    # Set an item in the storage
    local_storage.set_item("user", "John")

    # Get the item from the storage and assert its value
    assert local_storage.get_item("user") == "John"


def test_get_item_nonexistent_key():
    """
    The test verifies that attempting to retrieve an item with a key that
    does not exist in the local storage returns `None`.
    """

    # Get an item with a nonexistent key
    assert local_storage.get_item("invalid_user_key") is None


def test_clear_storage():
    """
    The test verifies that clearing the local storage removes all items.
    It ensures that after clearing, any previously set items can no longer
    be retrieved.
    """

    # Set an item in the storage
    local_storage.set_item("user", "John")

    # Clear the storage
    local_storage.clear()

    # Try to get the item, should return None since storage was cleared
    assert local_storage.get_item("user") is None


def test_clear_storage_empty():
    """
    The test verifies that calling the clear function on an already empty
    storage does not raise any exceptions and that the storage remains empty.
    """

    # Clear the storage when it's already empty
    local_storage.clear()

    # Ensure no exceptions are raised and storage is empty
    assert local_storage.get_item("user") is None
