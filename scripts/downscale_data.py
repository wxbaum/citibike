import os
import pandas as pd 

def main(downscale_frac=0.1):
    data_path = os.path.abspath('../data')
    files = os.listdir(data_path)
    
    for file in files:
        if file.startswith('2024') and file.endswith('.parquet'):
            df = pd.read_parquet(os.path.join(data_path, file))
            print('\n', '######', '\n')
            print(file)
            print(f'Input data size: {len(df)}')
            print(df.head(3))

            output_filename = f'{file.split(".")[0]}.csv'
            output_sample = df.sample(frac=downscale_frac)
            output_sample.to_csv(os.path.join(data_path, output_filename))
            print(f'Output data size: {len(output_sample)}')
            
        elif file.endswith('parquet'):
            df = pd.read_parquet(os.path.join(data_path, file))
            output_filename = f'{file.split(".")[0]}.csv'
            df.to_csv(os.path.join(data_path, output_filename), index=False)

        else:
            pass


if __name__ == '__main__':
    main(1)