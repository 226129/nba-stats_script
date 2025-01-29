""" 
    Author: Santiago Mendivil Alvarez
"""

import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


def one_dict(list_dict):
    """
    Converts a list of dictionaries into a single dictionary with lists as values.

    Args:
        list_dict (list): A list of dictionaries, where each dictionary has the same keys.

    Returns:
        dict: A dictionary where each key contains a list of values from the input dictionaries.
    """
    keys = list_dict[0].keys()
    out_dict = {key: [] for key in keys}
    for dict_ in list_dict:
        for key, value in dict_.items():
            out_dict[key].append(value)
    return out_dict


nba_teams = teams.get_teams()

dict_nba_team = one_dict(nba_teams)

df_teams = pd.DataFrame(dict_nba_team)  # Displays all the teams in the NBA


# Saves the nicknames for later usage
teams = [i for i in df_teams['nickname']]


print("\tStats for NBA teams")
print("Choose a team from the list below to see their stats: ")
for team in enumerate(teams):
    """Prints the teams in the NBA"""
    print(f"{team[0]} {team[1]} ")

try:
    """Tries to select a team index presented"""
    selection = int(
        input("Enter the number of the team you want to see the stats for: "))
except ValueError:
    """Catches an invalid value"""
    print("Invalid selection. Please try again")
    exit()

# Selects the team based on the index selected
df_team = df_teams[df_teams['nickname'] == teams[selection]]
id_team = df_team[['id']].values[0][0]

# Print the team ID and name
print(f"Team ID: {id_team}")
print(f"Team Name: {teams[selection]}")

# This initializes the leaguegamefinder object with the team ID that we got from the input
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id_team)

games = gamefinder.get_data_frames()[0]

games_home = games[games['MATCHUP'].str.contains('vs.')]
games_away = games[games['MATCHUP'].str.contains('@')]

# Print the number of games played at home and away by using .shape[0]
print(f"Games played at home: {games_home.shape[0]}")
print(f"Games played away: {games_away.shape[0]}")

# Calculates the mean for the graphic
mean_games_home = games_home['PLUS_MINUS'].mean()
mean_games_away = games_away['PLUS_MINUS'].mean()

# initializes and show the plot
fig, ax = plt.subplots()
games_away.plot(x='GAME_DATE', y='PLUS_MINUS', ax=ax)
games_home.plot(x='GAME_DATE', y='PLUS_MINUS', ax=ax)
ax.legend(["away", "home"])
plt.show()
