import pandas as pd
import numpy as np

# Load play-by-play data from GitHub (2015–2024)
YEARS = range(2015, 2025)
pbp_list = []

for year in YEARS:
    print(f"Loading {year}...")
    df = pd.read_csv(
        f'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.csv.gz',
        compression='gzip',
        low_memory=False
    )
    pbp_list.append(df)

data = pd.concat(pbp_list, ignore_index=True)

# Ensure stadium_id exists
if 'stadium_id' not in data.columns:
    data['stadium_id'] = np.nan

# Select stadium-related columns
stadium_df = data[
    ['stadium', 'stadium_id']
].dropna(subset=['stadium'])

# Reduce to one row per stadium
stadium_metadata = (
    stadium_df
    .drop_duplicates()
    .sort_values(by='stadium')
    .reset_index(drop=True)
)

ALTITUDE_MAP = {
    # US stadiums
    'AT&T Stadium': 575,                       # Dallas
    'Acrisure Stadium': 725,                   # Pittsburgh
    'Allegiant Stadium': 2000,                 # Las Vegas
    'Bank of America Stadium': 707,            # Carolina
    'Caesars Superdome': 2,                    # New Orleans
    'Cleveland Browns Stadium': 582,           # Cleveland
    'Commanders Field': 195,                   # Washington DC
    'Edward Jones Dome': 463,                  # St. Louis Rams
    'Empower Field at Mile High': 5195,        # Denver
    'EverBank Stadium': 3,                     # Jacksonville
    'Ford Field': 604,                         # Detroit
    'GEHA Field at Arrowhead Stadium': 842,    # Kansas City
    'Georgia Dome': 989,                       # Atlanta (2012–2016)
    'Mercedes-Benz Stadium': 1009,             # Atlanta (2017–)
    'Gillette Stadium': 260,                   # New England
    'Hard Rock Stadium': 9,                    # Miami
    'Highmark Stadium': 763,                   # Buffalo
    'Huntington Bank Field': 582,              # Cleveland
    'Lambeau Field': 620,                      # Green Bay
    "Levi's® Stadium": 15,                     # San Francisco (2014–)
    'Lincoln Financial Field': 11,             # Philadelphia
    'Los Angeles Memorial Coliseum': 161,      # LA Rams
    'Lucas Oil Stadium': 708,                  # Indianapolis
    'Lumen Field': 16,                         # Seattle
    'M&T Bank Stadium': 10,                    # Baltimore
    'MetLife Stadium': 6,                      # New York
    'NRG Stadium': 50,                         # Houston
    'Nissan Stadium': 397,                     # Tennessee
    'Oakland-Alameda County Stadium': 0,       # Oakland
    'Paycor Stadium': 480,                     # Cincinnati
    'Qualcomm Stadium': 53,                    # San Diego
    'Raymond James Stadium': 36,               # Tampa Bay
    'SoFi Stadium': 161,                       # Los Angeles Rams/Chargers
    'Soldier Field': 592,                      # Chicago
    'State Farm Stadium': 1068,                # Arizona
    'TCF Bank Stadium': 844,                   # Minnesota
    'U.S. Bank Stadium': 844,                  # Minnesota
    'FedExField': 195,                         # Washington DC
    'Northwest Stadium': 195,                  # Washington DC

    # International
    'Wembley Stadium': 62,                     # London
    'Twickenham Stadium': 85,                  # London
    'Tottenham Hotspur Stadium': 197,          # London
    'Estadio Azteca (Mexico City)': 7503,      # Mexico City
    'Allianz Arena': 1700,                     # Munich
    'Arena Corinthians': 2500,                 # São Paulo
    'Frankfurt Stadium': 370,                  # Frankfurt
}

# Apply altitude mapping
stadium_metadata['altitude_ft'] = stadium_metadata['stadium'].map(ALTITUDE_MAP)

# Save CSV
stadium_metadata.to_csv(
    'stadium_metadata.csv',
    index=False
)

print("\nSaved stadium_metadata.csv")
print(f"Total stadiums: {len(stadium_metadata)}")