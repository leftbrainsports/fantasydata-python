# content of test_sysexit.py
import pytest
from fantasy_data.FantasyData import FantasyData, FantasyDataError

class TestFantasyData:
    
    def read_api_key(self):
        with open("api_key.txt", "r") as api_key_file:
            return api_key_file.read().replace('\n', '')
    
    '''
    Happy path

    Given
        The FantasyData API is available
        A valid API key
    When
        I call get_upcoming_season() on a FantasyData object
    Then
        It returns the integer 2015
    '''
    def test_get_upcoming_season_happy_path(self):
        api_key = self.read_api_key()
        print api_key
        fantasy_data = FantasyData(api_key)
        assert (fantasy_data.get_upcoming_season() == 2015)
    
    '''
    API is unavailable

    Given
        The FantasyData API is not available over the network
        A valid API key
    When
        I call get_upcoming_season() on a FantasyData object
    Then
        It throws an exception stating "Error: Cannot connect to the FantasyData API"
    '''
    def test_get_upcoming_season_api_is_unavailable(self):
        invalid_api_key = '19944f3e54d84a5a93918aa35bbe5ab_'
        fantasy_data = FantasyData(invalid_api_key)
        with pytest.raises(FantasyDataError): 
            fantasy_data.get_upcoming_season()
    
    '''
    Invalid API key

    Given
        The FantasyData API is available
        A invalid API key
    When
        I call get_upcoming_season() on a FantasyData object
    Then
        It throws an exception stating "Error: Invalid API key"
    '''
    def test_get_upcoming_season_invalid_api_key(self):
        invalid_api_key = '19944f3e54d84a5a93918aa35bbe5ab_'
        fantasy_data = FantasyData(invalid_api_key)
        with pytest.raises(FantasyDataError): 
            fantasy_data.get_upcoming_season()
    
    def test_get_schedules_for_season(self):
        api_key = self.read_api_key()
        fantasy_data = FantasyData(api_key)
        fantasy_data.get_schedules_for_season(2014)