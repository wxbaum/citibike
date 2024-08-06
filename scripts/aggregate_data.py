import numpy as np
import os
import pandas as pd 
from pandas import DataFrame


def aggregate_rides(df: DataFrame) -> DataFrame:
    """
    Takes a dataframe of individual rides and aggregates into summary 
    statistics per unique combination of start and end station. 

    Params:
        df DataFrame: Individual timestamped rides with a start and end
          station.

    Returns: DataFrame of aggregated data.  
    """
    # Add date and hour columns
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['month'] = df['started_at'].dt.month.astype('int16')
    df['day'] = df['started_at'].dt.day.astype('int16')
    df['hour'] = df['started_at'].dt.hour.astype('int16')

    # Modify data types
    downscale_cols = ['start_station_id', 'end_station_id', 'membership_id', 'rideable_id', 'month', 'day', 'hour']
    df = df.astype({c: 'int16' for c in downscale_cols})

    # Aggregate data
    group_cols = ['start_station_id', 'end_station_id', 'month', 'day', 'hour', 'membership_id', 'rideable_id']
    # Ridership volume
    ride_counts = df.groupby(group_cols)['ride_id'].count()
    ride_counts = ride_counts.reset_index(name='ride_count')
    
    # Trip duration averages
    median_trip_dur = df.groupby(group_cols)['trip_duration'].median()
    median_trip_dur = median_trip_dur.reset_index(name='median_trip_dur')

    # Merge everything back into a single dataframe
    rides = pd.merge(ride_counts, median_trip_dur, on=group_cols)

    #rides = rides.reset_index().reset_index()
    print(rides.head())
    return rides


def main():
    data_path = os.path.abspath('../data')
    files = os.listdir(data_path)
    
    for file in sorted(files):
        if file.startswith('202406') and file.endswith('.parquet'):
            df = pd.read_parquet(os.path.join(data_path, file))
            print('######')
            print('Ride data')
            print(file)
            print(df.head(3))
            print(f'Data length: {len(df)} rows')
            memory_usage = round(df.memory_usage(deep=True).sum() / (2**20))
            print(f'Data size: {memory_usage} mb')
            print()

            print('Agg data')
            df = aggregate_rides(df).reset_index()
            print(f'Data length: {len(df)} rows')
            memory_usage = round(df.memory_usage(deep=True).sum() / (2**20))
            print(f'Data size: {memory_usage} mb')
            print()

            # Write agg data to CSV
            df.to_csv(
                os.path.join(data_path, 'agg_ride_data.csv'),
                index=False
                )

        else:
            pass


if __name__ == '__main__':
    main()