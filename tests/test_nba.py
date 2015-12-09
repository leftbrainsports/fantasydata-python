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

    def test_get_games_by_season(self, api_key, season):
        """
        API call get_schedules_for_season.
        Test response type and items structure
        """
        response = FantasyDataNBA(api_key).get_games_by_season(season)
        assert isinstance(response, list), "response not list"
        assert len(response), "response empty list"

        # item = response[0]
        required_fields = {"AwayTeam", "Status", "DateTime", "HomeTeam", "OverUnder", "PointSpread", "Season", "Day"}
        for item in response:
            item_keys = set(map(str, item.keys()))
            assert item_keys & required_fields == required_fields, "incorrect structure in response item"

            item["DateTime"] and self._check_date(item["DateTime"], "unexpected type of key 'DateTime'")
            assert isinstance(item["AwayTeam"], six.text_type), "unexpected type of key 'AwayTeam'"
            assert isinstance(item["Status"], six.text_type), "unexpected type of key 'Status'"
            assert isinstance(item["HomeTeam"], six.text_type), "unexpected type of key 'HomeTeam'"
            assert item["OverUnder"] is None or isinstance(item["OverUnder"], (float, int)), "unexpected type of key 'OverUnder'"
            assert item["PointSpread"] is None or isinstance(item["PointSpread"], (float, int)), "unexpected type of key 'PointSpread'"
            assert isinstance(item["Season"], int), "unexpected type of key 'Season'"

    def _check_date(self, value, error_msg):
        """
        Check date value. Parse datetime or throw assert exception
        """
        datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
