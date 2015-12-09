#coding:utf-8
import datetime
import os
import six

import pytest

from fantasy_data.FantasyData import FantasyDataNBA, FantasyDataError


@pytest.fixture(scope="module")
def api_key():
    """
    use different key for NBA
    """
    return os.environ.get('FANTASYDATA_NBA_API_KEY')


@pytest.fixture(scope="module")
def season():
    """
    """
    return 2016


class TestFantasyData:
    """
    """
    def test_get_current_season_api_is_unavailable(self):
        """
        API is unavailable

        Given
            The FantasyData API is not available over the network
            A valid API key
        When
            I call get_current_season() on a FantasyData object
        Then
            It throws an exception stating "Error: Cannot connect to the FantasyData API"
        """
        invalid_api_key = 'invalid api key'
        with pytest.raises(FantasyDataError):
            FantasyDataNBA(invalid_api_key).get_current_season()

    def test_get_current_season_invalid_api_key(self):
        """
        Invalid API key

        Given
            The FantasyData API is available
            A invalid API key
        When
            I call get_current_season() on a FantasyData object
        Then
            It throws an exception stating "Error: Invalid API key"
        """
        invalid_api_key = 'invalid api key'
        with pytest.raises(FantasyDataError):
            FantasyDataNBA(invalid_api_key).get_current_season()

    def test_get_current_season(self, api_key):
        """
        API call get_current_season
        """
        assert isinstance(FantasyDataNBA(api_key).get_current_season(), int), "Invalid value type"
