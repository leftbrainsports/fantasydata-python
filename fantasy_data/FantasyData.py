#coding:utf-8
import json
import httplib
import urllib


class FantasyDataError(Exception):
    def __init__(self, errorstr):
        self.errorstr = errorstr
    def __str__(self):
        return repr(self.errorstr)


class FantasyData(object):
    """
    Class provide Fantasy Data API calls 
    """
    _api_address = "api.nfldata.apiphany.com"  # API hostname
    _api_key = None  # api key for requests
    _get_params = None  # request GET params with API key
    _headers = None  # request additional headers
    _response_format = "json"  # default response format

    def __init__(self, api_key):
        """
        Object contructor. Set key for API requests
        """
        self._api_key = api_key
        self._get_params = urllib.urlencode({'subscription-key': api_key})
        self._headers = {
                        # Basic Authorization Sample 
                        # 'Authorization': 'Basic %s' % base64.encodestring('{username}:{password}'),
                        }
    
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

    def _method_call(self, method, **kwargs):
        """
        Call API method. Generate request. Parse response. Process errors
        `method` str API method url for request. Contains parameters
        `params` dict parameters for method url
        """
        try:
            connection = httplib.HTTPConnection(self._api_address)
        except:
            raise FantasyDataError('Error: Cannot connect to the FantasyData API')

        try:
            method = method.format(format=self._response_format, **kwargs)
            request_url = "/standard/{format}/{method}?{get_params}".format(format=self._response_format, method=method,
                                                                            get_params=self._get_params)
            connection.request("GET", request_url, "", self._headers)
            response = connection.getresponse()

            result = json.loads(response.read())

            if isinstance(result, dict) and "statusCode" in result:
                if (result['statusCode']) == 401:
                    raise FantasyDataError('Error: Invalid API key')
                else:
                    raise FantasyDataError('Error: Failed to get response')

            return result
        finally:
            connection.close()

