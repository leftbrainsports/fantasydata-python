import httplib, urllib, base64
import json

class FantasyDataError(Exception):
    def __init__(self, errorstr):
        self.errorstr = errorstr
    def __str__(self):
        return repr(self.errorstr)

class FantasyData :
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.params = urllib.urlencode({'subscription-key': api_key,})
        self.headers = {
                        # Basic Authorization Sample 
                        # 'Authorization': 'Basic %s' % base64.encodestring('{username}:{password}'),
                        }
        self.api_address = 'api.nfldata.apiphany.com'
    
    def raise_api_is_unavailable_exception(self):
        raise FantasyDataError('Error: Cannot connect to the FantasyData API')
    
    def raise_exception_if_error(self, result):
        if (type(result) is dict):
            if result.has_key('statusCode'):
                if (result['statusCode']) == 401:
                    raise FantasyDataError('Error: Invalid API key')
                else:
                    raise FantasyDataError('Error: Failed to get upcoming season')
    
    def get_upcoming_season(self):
        connection = None
        try:
            connection = httplib.HTTPConnection(self.api_address)
        except:
            self.raise_api_is_unavailable_exception()
        try:
            connection.request("GET", "/standard/{json}/UpcomingSeason?%s" % self.params, "", self.headers)
            response = connection.getresponse() 
            result = json.loads(response.read())
            self.raise_exception_if_error(result)
            return int(result)
        finally:
            connection.close()
    
    def get_schedules_for_season(self, season):
        connection = None
        try:
            connection = httplib.HTTPConnection(self.api_address)
        except:
            self.raise_api_is_unavailable_exception()
        try:
            connection.request("GET", "/standard/{json}/Schedules/{" + str(season) + "}?%s" % self.params, "", self.headers)
            response = connection.getresponse()
            result = json.loads(response.read())
            self.raise_exception_if_error(result)
            return result
        finally:
            connection.close()
  
api_key = '19944f3e54d84a5a93918aa35bbe5abf'
fantasy_data = FantasyData(api_key)
print fantasy_data.get_upcoming_season()
print fantasy_data.get_schedules_for_season(1999)