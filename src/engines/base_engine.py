import pathlib
from src.data_fetcher import DATA_DIR
from src.orbital_math import degToRad, calculateSemiMajorAxis, get3dPosition
import pandas

def processSatelliteFile(file_path):
    df = pandas.read_csv(file_path)
    df = df.dropna(subset=['MEAN_MOTION', 'INCLINATION', 'RA_OF_ASC_NODE', 'MEAN_ANOMALY']) # 1. Clean missing data
    
    # 2. Degree to Radian Conversions of the numbers from the csv files
    df['INCLINATION_RAD'] = degToRad(df['INCLINATION'])
    df['RAAN_RAD'] = degToRad(df['RA_OF_ASC_NODE'])
    df['MEAN_ANOMALY_RAD'] = degToRad(df['MEAN_ANOMALY'])
    
    # 3. Calculation of the Semi Major Axis using the raw mean motion numbers
    df['SEMI_MAJOR_AXIS'] = calculateSemiMajorAxis(df['MEAN_MOTION'])
    
    # 4. Plugging those nums in so i can get those 3d positions of the orbital elements
    df['X'], df['Y'], df['Z'] = get3dPosition(df['SEMI_MAJOR_AXIS'], df['INCLINATION_RAD'], df['RAAN_RAD'], df['MEAN_ANOMALY_RAD'])
    
    # Quick print so you can see it working in the terminal!
    print(f"Successfully processed {file_path.name}")
    print(df[['X', 'Y', 'Z']].head())

# 5. Master loop to grab all the data files
data_folder = pathlib.Path(DATA_DIR)
csv_files = data_folder.glob("*.csv")

for file_path in csv_files:
    processSatelliteFile(file_path)