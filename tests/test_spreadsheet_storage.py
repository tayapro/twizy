import pytest
from unittest import mock
from google.oauth2.service_account import Credentials
import gspread

from lib import spreadsheet_storage


@pytest.fixture
def mock_gspread_client():
    """
    Set up a mock gspread client and credentials for testing.

    This function creates fake versions of the gspread client and credentials
    to simulate interactions with Google Sheets without needing actual
    API calls.
    """
    with mock.patch.object(spreadsheet_storage,
                           'gspread', autospec=True) as mock_gspread, \
         mock.patch.object(spreadsheet_storage, 'Credentials',
                           autospec=True) as mock_creds:

        mock_creds_instance = mock.Mock(spec=Credentials)
        mock_creds.from_service_account_file.return_value = mock_creds_instance
        mock_scope_creds = mock.Mock(spec=Credentials)
        mock_creds_instance.with_scopes.return_value = mock_scope_creds
        mock_client = mock.Mock(spec=gspread.Client)
        mock_gspread.authorize.return_value = mock_client

        yield mock_client


def test_init_storage(mock_gspread_client):
    """
    The test verifies that `init_storage` sets up the gspread client
    and opens the 'twizy' spreadsheet.
    """
    spreadsheet_storage.init_storage()
    mock_gspread_client.open.assert_called_once_with('twizy')


def test_get_column(mock_gspread_client):
    """
    The test verifies that `get_column` retrieves the correct column data
    from the worksheet.
    """
    mock_worksheet = mock_gspread_client.open().worksheet()
    mock_worksheet.col_values.return_value = ["Header", "Value1", "Value2"]

    spreadsheet_storage.init_storage()
    result = spreadsheet_storage.get_column("Sheet1", 1)

    assert result == ["Value1", "Value2"]
    mock_worksheet.col_values.assert_called_once_with(1)


def test_set_column(mock_gspread_client):
    """
    The test verifies that `set_column` updates the worksheet
    with the correct column data.
    """
    mock_worksheet = mock_gspread_client.open().worksheet()
    spreadsheet_storage.init_storage()

    spreadsheet_storage.set_column("Sheet1", 1, ["Value1", "Value2"])

    mock_worksheet.update.assert_called_once_with("A2:A3",
                                                  ["Value1", "Value2"])


def test_get_table(mock_gspread_client):
    """
    The test verifies that `get_table` retrieves the entire table from
    the worksheet correctly.
    """
    mock_worksheet = mock_gspread_client.open().worksheet()
    mock_worksheet.get_all_values.return_value = [["Header1", "Header2"],
                                                  ["Value1", "Value2"]]

    spreadsheet_storage.init_storage()
    result = spreadsheet_storage.get_table("Sheet1")

    assert result == [["Header1", "Header2"], ["Value1", "Value2"]]
    mock_worksheet.get_all_values.assert_called_once()


def test_set_table(mock_gspread_client):
    """
    The test verifies that `set_table` updates the worksheet with the correct
    table data.
    """
    mock_worksheet = mock_gspread_client.open().worksheet()
    spreadsheet_storage.init_storage()

    data = [["Header1", "Header2"], ["Value1", "Value2"]]
    spreadsheet_storage.set_table("Sheet1", data)

    mock_worksheet.update.assert_called_once_with("A2:B3", data)


def test_column_to_range():
    """
    The test verifies that `column_to_range` generates the correct range string
    for a column and data.
    """
    assert spreadsheet_storage.column_to_range(1, ["Value1",
                                                   "Value2"]) == "A2:A3"
    assert spreadsheet_storage.column_to_range(2, ["Value1", "Value2",
                                                   "Value3"]) == "B2:B4"
