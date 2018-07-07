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
    _api_schema = "https://"
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

    def _method_call(self, method, category, **kwargs):
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
        request_url = "/v3/{game_type}/{category}/{format}/{method}?{get_params}".format(
            game_type=self.game_type,
            category=category,
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
        result = self._method_call("UpcomingSeason", "stats")
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
        result = self._method_call("Schedules/{season}", "stats", season=season_param)
        return result

    def get_free_agents(self):
        """
        """
        result = self._method_call("FreeAgents", "stats")
        return result

    def get_current_week(self):
        """
        Number of the current week of the NFL season.
        This value usually changes on Tuesday nights or Wednesday mornings at midnight EST.
        Week number is an integer between 1 and 21 or the word current.
        Weeks 1 through 17 are regular season weeks. Weeks 18 through 21 are post-season weeks.
        """
        result = self._method_call("CurrentWeek", "stats")
        return int(result)

    def get_team_roster_and_depth_charts(self, team_name):
        """
        `team_name` str Team short name
        """
        result = self._method_call("Players/{team}", "stats", team=team_name)
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
        result = self._method_call("PlayerGameStatsByWeek/{season}/{week}", "stats", season=season_param, week=week)
        return result

    def get_teams_active(self):
        """
        Gets all active teams.
        """
        result = self._method_call("Teams", "stats")
        return result

    def get_player(self, player_id):
        """
        Player profile information for one specific player.
        `player_id` int
        """
        result = self._method_call("Player/{player_id}", "stats", player_id=player_id)
        return result

    def get_projected_player_game_stats_by_player(self, season, week, player_id):
        """
        Projected Player Game Stats by Player
        """
        result = self._method_call("PlayerGameProjectionStatsByPlayerID/{season}/{week}/{player_id}", "projections", season=season, week=week, player_id=player_id)
        return result

    def get_projected_player_game_stats_by_team(self, season, week, team_id):
        """
        Projected Player Game Stats by Team
        """
        result = self._method_call("PlayerGameProjectionStatsByTeam/{season}/{week}/{team_id}", "projections", season=season, week=week, team_id=team_id)
        return result

    def get_projected_player_game_stats_by_week(self, season, week):
        """
        Projected Player Game Stats by Week
        """
        result = self._method_call("PlayerGameProjectionStatsByWeek/{season}/{week}", "projections", season=season, week=week)
        return result

    def get_projected_fantasy_defense_game_stats_by_week(self, season, week):
        """
        Projected Fantasy Defense Game Stats by Week
        """
        result = self._method_call("FantasyDefenseProjectionsByGame/{season}/{week}", "projections", season=season, week=week)
        return result

    def get_player_season_projected_stats(self, season):
        """
        Projected Stats By Player By Season
        """
        result = self._method_call("PlayerSeasonProjectionStats/{season}", "projections", season=season)
        return result
    
    def get_rotoballer_premium_news(self):
        """
        RotoBaller Premium News
        """
        result = self._method_call("RotoBallerPremiumNews", "news-rotoballer")
        return result

    def get_rotoballer_premium_news_by_date(self, date):
        """
        RotoBaller Premium News By Date
        Date format: 2017-JUL-31
        """
        result = self._method_call("RotoBallerPremiumNewsByDate/{date}", "news-rotoballer", date=date)
        return result

    def get_rotoballer_premium_news_by_player(self, player_id):
        """
        RotoBaller Premium News By Player ID
        """
        result = self._method_call("RotoBallerPremiumNewsByPlayerID/{player_id}", "news-rotoballer", player_id=player_id)
        return result

    def get_rotoballer_premium_news_by_team(self, team_id):
        """
        RotoBaller Premium News By Team ID
        """
        result = self._method_call("RotoBallerPremiumNewsByTeam/{team_id}", "news-rotoballer", team_id=team_id)
        return result

    def get_injuries(self, season, week):
        """
        Injuries by week
        """
        result = self._method_call("Injuries/{season}/{week}", "stats", season=season, week=week)
        return result

    def get_injuries_by_team(self, season, week, team_id):
        """
        Injuries by week and team
        """
        result = self._method_call("Injuries/{season}/{week}/{team_id}", "stats", season=season, week=week, team_id=team_id)
        return result

    def get_box_score_by_team(self, season, week, team_id):
        """
        Box score by week and team
        """
        result = self._method_call("BoxScoreV3/{season}/{week}/{team_id}", "stats", season=season, week=week, team_id=team_id)
        return result

    def get_bye_weeks(self, season):
        """
        Bye weeks
        """
        result = self._method_call("Byes/{season}", "stats", season=season)
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
        result = self._method_call("CurrentSeason", "stats")
        return int(result.get('Season'))

    def get_games_by_season(self, season):
        """
        Game schedule for a specified season.
        """
        try:
            season = int(season)
        except ValueError:
            raise FantasyDataError('Error: Invalid method parameters')

        result = self._method_call("Games/{season}", "stats", season=season)
        return result

    def get_games_by_date(self, game_date):
        """
        Game schedule for a specified day.
        """
        result = self._method_call("GamesByDate/{game_date}", "scores", game_date=game_date)
        return result

    def get_players_game_stats_by_date(self, game_date):
        """
        Game stats for each player at a specified date.
        """
        result = self._method_call("PlayerGameStatsByDate/{game_date}", "stats", game_date=game_date)
        return result

    def get_team_game_stats_by_date(self, game_date):
        """
        Game stats for each team at a specified date.
        """
        result = self._method_call("TeamGameStatsByDate/{game_date}", "stats", game_date=game_date)
        return result

    def get_standings(self, season):
        """
        Get standings for season
        """
        result = self._method_call("Standings/{season}", "stats", season=season)
        return result

    def get_teams_active(self):
        """
        Gets all active teams.
        """
        result = self._method_call("Teams", "stats")
        return result

    def get_stadiums(self):
        """
        Get all stadiums.
        """
        result = self._method_call("Stadiums")
        return result
