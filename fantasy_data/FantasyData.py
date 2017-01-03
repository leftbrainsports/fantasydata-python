#coding:utf-8
import requests
from six.moves import urllib


class FantasyDataError(Exception):
    def __init__(self, errorstr):
        self.errorstr = errorstr

    def __str__(self):
        return repr(self.errorstr)


class FantasyDataBase(object):
    """
    Base class for all Fantasy Data APIs
    """
    _api_schema = "http://"
    _api_address = "api.fantasydata.net"  # API hostname
    _api_key = None  # api key for requests
    _get_params = None  # request GET params with API key
    _headers = None  # request additional headers
    _response_format = "json"  # default response format

    def __init__(self, api_key):
        """
        Object contructor. Set key for API requests
        """
        self._api_key = api_key
        # uses six
        self._get_params = urllib.parse.urlencode({'subscription-key': api_key})

        self._headers = {
            # Basic Authorization Sample
            # 'Authorization': 'Basic %s' % base64.encodestring('{username}:{password}'),
        }

    def _method_call(self, method, **kwargs):
        """
        Call API method. Generate request. Parse response. Process errors
        `method` str API method url for request. Contains parameters
        `params` dict parameters for method url
        """
        session = requests.Session()
        try:
            response = session.get("http://" + self._api_address)
        except requests.exceptions.ConnectionError:
            raise FantasyDataError('Error: Cannot connect to the FantasyData API')

        method = method.format(format=self._response_format, **kwargs)
        request_url = "/{game_type}/v2/{format}/{method}?{get_params}".format(
            game_type=self.game_type,
            format=self._response_format,
            method=method,
            get_params=self._get_params)
        response = session.get(self._api_schema + self._api_address + request_url,
                               headers=self._headers)
        result = response.json()

        if isinstance(result, dict) and response.status_code:
            if response.status_code == 401:
                raise FantasyDataError('Error: Invalid API key')
            elif response.status_code == 200:
                # for NBA everything is ok here.
                pass
            else:
                raise FantasyDataError('Error: Failed to get response')

        return result


class FantasyData(FantasyDataBase):
    """
    Class provide Fantasy Data API calls (NFL)
    """
    game_type = 'nfl'

    def get_upcoming_season(self):
        """
        Year of the current NFL season, if we are in the mid-season.
        If we are in the off-season, then year of the next upcoming season.
        This value changes immediately after the Super Bowl.
        The earliest season for Fantasy data is 2001. The earliest season for Team data is 1985.
        """
        result = self._method_call("UpcomingSeason")
        return int(result)

    def get_schedules_for_season(self, season, season_type="REG"):
        """
        Game schedule for a specified season.
        """
        try:
            season = int(season)
            if season_type not in ["REG", "PRE", "POST"]:
                raise ValueError
        except (ValueError, TypeError):
            raise FantasyDataError('Error: Invalid method parameters')

        season_param = "{0}{1}".format(season, season_type)
        result = self._method_call("Schedules/{season}", season=season_param)
        return result

    def get_free_agents(self):
        """
        """
        result = self._method_call("FreeAgents")
        return result

    def get_current_week(self):
        """
        Number of the current week of the NFL season.
        This value usually changes on Tuesday nights or Wednesday mornings at midnight EST.
        Week number is an integer between 1 and 21 or the word current.
        Weeks 1 through 17 are regular season weeks. Weeks 18 through 21 are post-season weeks.
        """
        result = self._method_call("CurrentWeek")
        return int(result)

    def get_team_roster_and_depth_charts(self, team_name):
        """
        `team_name` str Team short name
        """
        result = self._method_call("Players/{team}", team=team_name)
        return result

    def get_players_game_stats_for_season_for_week(self, season, week, season_type="REG"):
        """
        Game stats for a specified season and week.
        `season` int
        `week` int
        `season_type` str Valid value one of ("REG", "PRE", "POST")
        """
        try:
            season = int(season)
            week = int(week)
            if season_type not in ["REG", "PRE", "POST"]:
                raise ValueError
        except (TypeError, ValueError):
            raise FantasyDataError('Error: Invalid method parameters')

        season_param = "{0}{1}".format(season, season_type)
        result = self._method_call("PlayerGameStatsByWeek/{season}/{week}", season=season_param, week=week)
        return result

    def get_teams_active(self):
        """
        Gets all active teams.
        """
        result = self._method_call("Teams")
        return result

    def get_player(self, player_id):
        """
        Player profile information for one specific player.
        `player_id` int
        """
        result = self._method_call("Player/{player_id}", player_id=player_id)
        return result

class FantasyDataNBA(FantasyDataBase):
    """
    Class provide Fantasy Data API calls (NFL)
    """
    game_type = 'nba'

    def get_current_season(self):
        """
        Year of the current NBA season.
        The year is the year of the playoffs.
        I.e. result=2016 is 2015/2016
        """
        result = self._method_call("CurrentSeason")
        return int(result.get('Season'))

    def get_games_by_season(self, season):
        """
        Game schedule for a specified season.
        """
        try:
            season = int(season)
        except ValueError:
            raise FantasyDataError('Error: Invalid method parameters')

        result = self._method_call("Games/{season}", season=season)
        return result

    def get_games_by_date(self, game_date):
        """
        Game schedule for a specified day.
        """
        result = self._method_call("GamesByDate/{game_date}", game_date=game_date)
        return result

    def get_players_game_stats_by_date(self, game_date):
        """
        Game stats for each player at a specified date.
        """
        result = self._method_call("PlayerGameStatsByDate/{game_date}", game_date=game_date)
        return result

    def get_team_game_stats_by_date(self, game_date):
        """
        Game stats for each team at a specified date.
        """
        result = self._method_call("TeamGameStatsByDate/{game_date}", game_date=game_date)
        return result

    def get_standings(self, season):
        """
        Get standings for season
        """
        result = self._method_call("Standings/{season}", season=season)
        return result

    def get_teams_active(self):
        """
        Gets all active teams.
        """
        result = self._method_call("Teams")
        return result
