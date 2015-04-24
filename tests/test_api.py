#coding:utf-8
import pytest

from fantasy_data.FantasyData import FantasyData, FantasyDataError


@pytest.fixture(scope="module")
def api_key():
    """
    """
    with open("api_key.txt", "r") as api_key_file:
        return api_key_file.read().replace('\n', '')


@pytest.fixture(scope="module")
def season():
    """
    Season for calls which use season in parameters
    """
    return 2014


@pytest.fixture(scope="module")
def team():
    """
    Team short name for API calls
    """
    return "WAS"


@pytest.fixture(scope="module")
def week():
    """
    Week number for API calls
    """
    return 5


class TestFantasyData:
    """
    """

    # def test_get_upcoming_season_happy_path(self, api_key):
    #     '''
    #     Happy path

    #     Given
    #         The FantasyData API is available
    #         A valid API key
    #     When
    #         I call get_upcoming_season() on a FantasyData object
    #     Then
    #         It returns the integer 2015
    #     '''
    #     assert (FantasyData(api_key).get_upcoming_season() == 2015)

    def test_get_upcoming_season_api_is_unavailable(self):
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
        invalid_api_key = 'invalid api key'
        with pytest.raises(FantasyDataError): 
            FantasyData(invalid_api_key).get_upcoming_season()

    def test_get_upcoming_season_invalid_api_key(self):
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
        invalid_api_key = 'invalid api key'
        with pytest.raises(FantasyDataError): 
            FantasyData(invalid_api_key).get_upcoming_season()

    def test_get_upcoming_season(self, api_key):
        """
        API call get_upcoming_season
        """
        assert isinstance(FantasyData(api_key).get_upcoming_season(), int), "Invalid value type"

    def test_get_current_week(self, api_key):
        """
        API call get_current_week
        """
        assert isinstance(FantasyData(api_key).get_current_week(), int), "Invalid value type"

    def test_get_schedules_for_season(self, api_key, season):
        """
        API call get_schedules_for_season.
        Test response type and items structure
        """
        response = FantasyData(api_key).get_schedules_for_season(season)

        assert isinstance(response, list), "response not list"
        assert len(response), "response empty list"

        item = response[0]
        required_fields = {"AwayTeam", "Channel", "Date", "HomeTeam", "OverUnder", "PointSpread", "Season", "Week"}
        item_keys = set(map(str, item.keys()))
        assert item_keys & required_fields == required_fields, "incorrect structure in response item"

        # TODO: check date format
        # assert isinstance(item["Date"], date), "unexpected type of key 'AwayTeam'", "Date": "/Date(-62135578800000-0500)/",
        assert isinstance(item["AwayTeam"], unicode), "unexpected type of key 'AwayTeam'"
        assert item["Channel"] is None or isinstance(item["Channel"], unicode), "unexpected type of key 'Channel'"
        assert isinstance(item["HomeTeam"], unicode), "unexpected type of key 'HomeTeam'"
        assert isinstance(item["OverUnder"], (float, int)), "unexpected type of key 'OverUnder'"
        assert isinstance(item["PointSpread"], (float, int)), "unexpected type of key 'PointSpread'"
        assert isinstance(item["Season"], int), "unexpected type of key 'Season'"
        assert isinstance(item["Week"], int), "unexpected type of key 'Week'"

    def test_get_team_roster_and_depth_charts(self, api_key, team):
        """
        API call get_team_roster_and_depth_charts
        Test response type and items structure
        """
        response = FantasyData(api_key).get_team_roster_and_depth_charts(team)

        assert isinstance(response, list), "response not list"
        assert len(response), "response empty list"

        item = response[0]
        required_fields = {"Active", "Age", "AverageDraftPosition", "BirthDate", "BirthDateString", "ByeWeek", 
                           "College", "DepthDisplayOrder", "DepthOrder", "DepthPosition", "DepthPositionCategory", 
                           "Experience", "ExperienceString", "FantasyPosition", "FirstName", "Height", "InjuryStatus", 
                           "LastName", "LatestNews", "Name", "Number", "PhotoUrl", "PlayerID", "Position", 
                           "PositionCategory", "ShortName", "Status", "Team", "UpcomingGameOpponent", 
                           "UpcomingGameWeek", "Weight", "PlayerSeason"}
        item_keys = set(map(str, item.keys()))
        assert item_keys & required_fields == required_fields, "incorrect structure in response item"

        # TODO: check date format
        # assert isinstance(item["BirthDate"], date), "unexpected type of key 'BirthDate'"
        assert isinstance(item["Active"], bool), "unexpected type of key 'Active'"
        assert isinstance(item["Age"], int), "unexpected type of key 'Age'"
        assert item["AverageDraftPosition"] is None or isinstance(item["AverageDraftPosition"], unicode), "unexpected type of key 'AverageDraftPosition'"
        assert isinstance(item["BirthDateString"], unicode), "unexpected type of key 'BirthDateString'"
        assert isinstance(item["ByeWeek"], int), "unexpected type of key 'ByeWeek'"
        assert isinstance(item["College"], unicode), "unexpected type of key 'College'"
        assert isinstance(item["DepthDisplayOrder"], int), "unexpected type of key 'DepthDisplayOrder'"
        assert isinstance(item["DepthOrder"], int), "unexpected type of key 'DepthOrder'"
        assert isinstance(item["DepthPosition"], unicode), "unexpected type of key 'DepthPosition'"
        assert isinstance(item["DepthPositionCategory"], unicode), "unexpected type of key 'DepthPositionCategory'"
        assert isinstance(item["Experience"], int), "unexpected type of key 'Experience'"
        assert isinstance(item["ExperienceString"], unicode), "unexpected type of key 'ExperienceString'"
        assert isinstance(item["FantasyPosition"], unicode), "unexpected type of key 'FantasyPosition'"
        assert isinstance(item["FirstName"], unicode), "unexpected type of key 'FirstName'"
        assert isinstance(item["Height"], unicode), "unexpected type of key 'Height'"
        assert item["InjuryStatus"] is None or isinstance(item["InjuryStatus"], int), "unexpected type of key 'InjuryStatus'"
        assert isinstance(item["LastName"], unicode), "unexpected type of key 'LastName'"
        assert isinstance(item["LatestNews"], list), "unexpected type of key 'LatestNews'"
        assert isinstance(item["Name"], unicode), "unexpected type of key 'Name'"
        assert isinstance(item["Number"], int), "unexpected type of key 'Number'"
        assert isinstance(item["PhotoUrl"], unicode), "unexpected type of key 'PhotoUrl'"
        assert isinstance(item["PlayerID"], int), "unexpected type of key 'PlayerID'"
        assert isinstance(item["PlayerSeason"], dict), "unexpected type of key 'PlayerSeason'"
        assert isinstance(item["Position"], unicode), "unexpected type of key 'Position'"
        assert isinstance(item["PositionCategory"], unicode), "unexpected type of key 'PositionCategory'"
        assert isinstance(item["ShortName"], unicode), "unexpected type of key 'ShortName'"
        assert isinstance(item["Status"], unicode), "unexpected type of key 'Status'"
        assert isinstance(item["Team"], unicode), "unexpected type of key 'Team'"
        assert isinstance(item["UpcomingGameOpponent"], unicode), "unexpected type of key 'UpcomingGameOpponent'"
        assert isinstance(item["UpcomingGameWeek"], int), "unexpected type of key 'UpcomingGameWeek'"
        assert isinstance(item["Weight"], unicode), "unexpected type of key 'Weight'"

    def test_players_game_stats_for_season_for_week(self, api_key, season, week):
        """
        API call players_game_stats_for_season_for_week
        Test response type and items structure
        """
        response = FantasyData(api_key).get_players_game_stats_for_season_for_week(season, week)

        assert isinstance(response, list), "response not list"
        assert len(response), "response empty list"

        item = response[0]
        required_fields = {"AwayTeam", "HomeTeam", "Season", "Week", "OverUnder", "IsGameOver", "GameKey", "GameID", 
                           "Date"}
        item_keys = set(map(str, item.keys()))
        assert item_keys & required_fields == required_fields, "incorrect structure in response item"

        # TODO: check date format
        # assert isinstance(item["Date"], date), "unexpected type of key 'AwayTeam'", "Date": "/Date(-62135578800000-0500)/",
        assert isinstance(item["AwayTeam"], unicode), "unexpected type of key 'AwayTeam'"
        assert isinstance(item["HomeTeam"], unicode), "unexpected type of key 'HomeTeam'"
        assert isinstance(item["OverUnder"], (float, int)), "unexpected type of key 'OverUnder'"
        assert isinstance(item["PointSpread"], (float, int)), "unexpected type of key 'PointSpread'"
        assert isinstance(item["Season"], int), "unexpected type of key 'Season'"
        assert isinstance(item["Week"], int), "unexpected type of key 'Week'"
        assert isinstance(item["IsGameOver"], bool), "unexpected type of key 'IsGameOver'"
        assert isinstance(item["GameKey"], unicode), "unexpected type of key 'GameKey'"
        assert isinstance(item["GameID"], int), "unexpected type of key 'GameID'"
