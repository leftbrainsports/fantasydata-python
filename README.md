# fantasydata-python
A Python wrapper around the Fantasy Data API.

## Example Usage
```
from fantasy_data.FantasyData import FantasyData
fantasy_data = FantasyData("my_api_key")
player = fantasy_data.get_player(732)
print player
{u'InjuryStartDate': None, u'FirstName': u'Matt', u'PlayerID': 732, u'LastName': u'Ryan',  ....}

```

## Supported Methods
Not all of the FantasyData API is implemented yet. Pull requests welcome!

### NFL
* `get_upcoming_season()`
* `get_schedules_for_season(season, season_type="REG")`
* `get_free_agents()`
* `get_current_week()`
* `get_team_roster_and_depth_charts(team_name)`
* `get_players_game_stats_for_season_for_week(season, week, season_type="REG")`
* `get_teams_active()`
* `get_player(player_id)`


### NBA
* `get_current_season()`
* `get_games_by_season(season)`
* `get_games_by_date(game_date)`
* `get_players_game_stats_by_date(game_date)`
* `get_team_game_stats_by_date(game_date)`
* `get_standings(season)`
* `get_teams_active()`

### Run tests
To run tests, set an environment variable named FANTASYDATA_API_KEY like this:

```export FANTASYDATA_API_KEY=yourapikeyhere```

and for NBA tests:

```export FANTASYDATA_NBA_API_KEY=yourapikeyhere```

Then run the tests with:

```python setup.py test```

or for python 3:

```python3 setup.py test```
