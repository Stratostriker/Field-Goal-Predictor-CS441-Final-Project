import pandas as pd
import numpy as np

# Load play-by-play data from GitHub (2015–2024)
YEARS = range(2015, 2025)
pbp_list = []

for year in YEARS:
    i_data = pd.read_csv(
        f'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.csv.gz',
        compression='gzip',
        low_memory=False
    )
    i_data['year'] = year
    pbp_list.append(i_data)

data = pd.concat(pbp_list, ignore_index=True)

# Filter to FIELD GOAL ATTEMPTS (per-kick)
fg = data[
    (data['play_type'] == 'field_goal') &
    (data['field_goal_attempt'] == 1)
].copy()

# Target variable: FG made (1) vs missed (0)
fg['fg_made'] = (fg['field_goal_result'] == 'made').astype(int)

# Home / Away
fg['home_away'] = np.where(
    fg['posteam'] == fg['home_team'],
    'Home',
    'Away'
)

# Standardize roof (dome vs outdoors for retractable roof)
fg['roof_standardized'] = np.where(
    fg['roof'].str.contains('closed|dome', case=False, na=False),
    'dome',
    'outdoors'
)

# Weather type
def get_weather_type(weather):
    if pd.isna(weather):
        return 'Unknown'
    w = weather.lower()
    if 'snow' in w:
        return 'Snow'
    elif 'rain' in w or 'shower' in w or 'drizzle' in w:
        return 'Rain'
    elif 'cloud' in w or 'overcast' in w:
        return 'Cloudy'
    elif 'clear' in w or 'sun' in w:
        return 'Clear'
    else:
        return 'Other'

fg['weather_type'] = fg['weather'].apply(get_weather_type)

# Playoff indicator
fg['is_playoff'] = fg['season_type'] == 'POST'

# Roof-aware environmental fixes
fg.loc[
    (fg['roof_standardized'] == 'dome') & (fg['wind'].isna()),
    'wind'
] = 0

fg.loc[
    (fg['roof_standardized'] == 'dome') & (fg['temp'].isna()),
    'temp'
] = 70

fg['wind_missing'] = fg['wind'].isna()
fg['temp_missing'] = fg['temp'].isna()

# Select final columns
final_columns = [
    # Identifiers
    'season',
    'week',
    'game_id',
    'posteam',

    # Stadium info
    'stadium',
    'stadium_id',
    'surface',

    # Context
    'home_away',

    # Weather
    'roof_standardized',
    'weather_type',
    'wind',
    'wind_missing',
    'temp',
    'temp_missing',

    # FG info
    'kick_distance',
    'fg_made',

    # Game context
    'is_playoff'
]

fg = fg[final_columns].dropna(subset=['kick_distance', 'fg_made'])

# Save CSV
fg.to_csv(
    'per_kick_field_goals_2015_2024.csv',
    index=False
)

print("Saved per_kick_field_goals_2015_2024.csv")