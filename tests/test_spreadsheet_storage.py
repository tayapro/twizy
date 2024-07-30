import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest import mock
from google.oauth2.service_account import Credentials
import gspread

from lib import spreadsheet_storage

@pytest.fixture
def mock_gspread_client():
    """ Fixture to mock gspread client and related methods. """
    with mock.patch.object(spreadsheet_storage, 'gspread', autospec=True) as mock_gspread, \
         mock.patch.object(spreadsheet_storage, 'Credentials', autospec=True) as mock_creds:
        
        mock_creds_instance = mock.Mock(spec=Credentials)
        mock_creds.from_service_account_file.return_value = mock_creds_instance
        mock_scope_creds = mock.Mock(spec=Credentials)
        mock_creds_instance.with_scopes.return_value = mock_scope_creds
        mock_client = mock.Mock(spec=gspread.Client)
        mock_gspread.authorize.return_value = mock_client
        
        yield mock_client


def test_init_storage(mock_gspread_client):
    spreadsheet_storage.init_storage()
    mock_gspread_client.open.assert_called_once_with('twizy')


def test_get_column(mock_gspread_client):
    mock_worksheet = mock_gspread_client.open().worksheet()
    mock_worksheet.col_values.return_value = ["Header", "Value1", "Value2"]

    spreadsheet_storage.init_storage()
    result = spreadsheet_storage.get_column("Sheet1", 1)
    
    assert result == ["Value1", "Value2"]
    mock_worksheet.col_values.assert_called_once_with(1)


def test_set_column(mock_gspread_client):
    mock_worksheet = mock_gspread_client.open().worksheet()
    spreadsheet_storage.init_storage()
    
    spreadsheet_storage.set_column("Sheet1", 1, ["Value1", "Value2"])
    
    mock_worksheet.update.assert_called_once_with("A2:A3", ["Value1", "Value2"])


def test_get_table(mock_gspread_client):
    mock_worksheet = mock_gspread_client.open().worksheet()
    mock_worksheet.get_all_values.return_value = [["Header1", "Header2"], ["Value1", "Value2"]]
    
    spreadsheet_storage.init_storage()
    result = spreadsheet_storage.get_table("Sheet1")
    
    assert result == [["Header1", "Header2"], ["Value1", "Value2"]]
    mock_worksheet.get_all_values.assert_called_once()


def test_set_table(mock_gspread_client):
    mock_worksheet = mock_gspread_client.open().worksheet()
    spreadsheet_storage.init_storage()
    
    data = [["Header1", "Header2"], ["Value1", "Value2"]]
    spreadsheet_storage.set_table("Sheet1", data)
    
    mock_worksheet.update.assert_called_once_with("A2:B3", data)


def test_column_to_range():
    assert spreadsheet_storage.column_to_range(1, ["Value1", "Value2"]) == "A2:A3"
    assert spreadsheet_storage.column_to_range(2, ["Value1", "Value2", "Value3"]) == "B2:B4"
