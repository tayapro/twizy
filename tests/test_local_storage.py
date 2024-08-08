import pytest

from lib import local_storage


def test_set_and_get_item():
    """
    The test verifies that an item can be correctly set in the local
    storage and then retrieved. It ensures that the value stored matches
    the value retrieved.
    """
    local_storage.set_item("user", "John")
    assert local_storage.get_item("user") == "John"


def test_get_item_nonexistent_key():
    """
    The test verifies that attempting to retrieve an item with a key that
    does not exist in the local storage returns `None`.
    """
    assert local_storage.get_item("invalid_user_key") is None


# def test_clear_storage(mock_localstorage_get_item, mock_localstorage_set_item):
def test_clear_storage():
    """
    The test verifies that clearing the local storage removes all items.
    It ensures that after clearing, any previously set items can no longer
    be retrieved.
    """
    # mock_localstorage_set_item.assert_called_with("user", "TestUser")
    local_storage.set_item("user", "John")

    local_storage.clear()

    assert local_storage.get_item("user") is None


def test_clear_storage_empty():
    """
    The test verifies that calling the clear function on an already empty
    storage does not raise any exceptions and that the storage remains empty.
    """
    local_storage.clear()

    assert local_storage.get_item("user") is None
