from nba_api.stats.endpoints import leaguedashplayerstats, commonplayerinfo
import pandas as pd
import time

def get_nba_player_stats(season='2024-25', season_type='Regular Season', league_id_nullable='00'):
    # Fetch player stats and create data frame
    print(f"Fetching player statistics for season: {season}, type: {season_type}, league ID: {league_id_nullable}...")
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star=season_type,
        league_id_nullable=league_id_nullable
    )

    df = player_stats.get_data_frames()[0]

    # Select relevant columns
    df_relevant = df[[
        'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
        'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'PTS', 'PLUS_MINUS',
        'NBA_FANTASY_PTS', 'DD2', 'TD3'
    ]].copy()

    # Get game averages and add them to the DataFrame
    df_relevant['PPG'] = (df_relevant['PTS'] / df_relevant['GP']).round(1)
    df_relevant['APG'] = (df_relevant['AST'] / df_relevant['GP']).round(1)
    df_relevant['ORPG'] = (df_relevant['OREB'] / df_relevant['GP']).round(1)
    df_relevant['DRPG'] = (df_relevant['DREB'] / df_relevant['GP']).round(1)
    df_relevant['RPG'] = (df_relevant['REB'] / df_relevant['GP']).round(1)
    df_relevant['SPG'] = (df_relevant['STL'] / df_relevant['GP']).round(1)
    df_relevant['BPG'] = (df_relevant['BLK'] / df_relevant['GP']).round(1)
    df_relevant['TPG'] = (df_relevant['TOV'] / df_relevant['GP']).round(1)
    df_relevant['PFPG'] = (df_relevant['PF'] / df_relevant['GP']).round(1)
    df_relevant['MPG'] = (df_relevant['MIN'] / df_relevant['GP']).round(1)
    df_relevant['FPPG'] = (df_relevant['NBA_FANTASY_PTS'] / df_relevant['GP']).round(1)
    df_relevant['FG3PG'] = (df_relevant['FG3M'] / df_relevant['GP']).round(1)
    df_relevant['FG3APG'] = (df_relevant['FG3A'] / df_relevant['GP']).round(1)
    df_relevant['FTPG'] = (df_relevant['FTM'] / df_relevant['GP']).round(1)
    df_relevant['FTAPG'] = (df_relevant['FTA'] / df_relevant['GP']).round(1)
    df_relevant['FGPG'] = (df_relevant['FGM'] / df_relevant['GP']).round(1)
    df_relevant['FGAPG'] = (df_relevant['FGA'] / df_relevant['GP']).round(1)


    # Now we can drop the original columns that were used for calculations and keep only the relevant ones
    df_relevant = df_relevant[[
        'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'MPG', 'FGPG', 'FGAPG', 'FG_PCT', 'FG3PG', 'FG3APG', 'FG3_PCT',
        'FTPG', 'FTAPG', 'FT_PCT', 'ORPG', 'DRPG', 'RPG', 'APG', 'TPG', 'SPG', 'BPG', 'PFPG', 'FPPG', 'DD2', 'TD3'
    ]]
    
    # Save to CSV
    output_file = 'nba_player_stats.csv'
    df_relevant.to_csv(output_file, index=False)
    print(f"Player statistics fetched and saved to {output_file}.")
    return player_stats

if __name__ == "__main__":
    get_nba_player_stats()