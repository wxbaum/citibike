from datetime import datetime, timedelta
import json
import requests
import time


class Handler:
    def __init__(self):
        self.ncdc_base_url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/'
        self.ncdc_token = 'DxGMjEIAJipTXlGZfLaWrfvLKEImtCTA'
        self.request_headers = {'token': self.ncdc_token}

    def get_stations_for_zip(self, zipcode):
        data_request = f'stations?locationcategoryid=ZIP&locationid=ZIP:{zipcode}'
        response = json.loads(requests.get(
            f'{self.ncdc_base_url}{data_request}', 
            headers=self.request_headers).text
        )
        stations = [station['id'] for station in response['results']]
        print(f'Found stations: {stations}')
        time.sleep(0.2)
        return stations
    
    def get_available_datasets(self, station_id):
        data_request = f'datatypes?stationid={station_id}'
        response = json.loads(requests.get(
            f'{self.ncdc_base_url}{data_request}', 
            headers=self.request_headers).text
        )
        datasets = [{'name':d['name'], 'id':d['id']} for d in response['results']]
        print(f'Found datasets: {datasets}')
        time.sleep(0.2)
        return datasets


    def get_data(self, station, dataset='PRECIP_15', start_date=None, end_date=None):
        print(f'Requesting {dataset} for {station}')
        if end_date is None:
            end_date = datetime.now().date()

        if start_date == None:
            start_date = end_date - timedelta(days=7)

        data_request = f'data?datasetid={dataset}&stationid={station}&units=metric&startdate={start_date}&enddate={end_date}'
        response = requests.get(
            f'{self.ncdc_base_url}{data_request}', 
            headers=self.request_headers
        )
        time.sleep(0.2)
        return response
    
def main():
    ncdc = Handler()
    station = ncdc.get_stations_for_zip(53205)[0]
    station_dataset = ncdc.get_available_datasets(station)[0]
    
    data = ncdc.get_data(
        station=station,
        dataset=station_dataset
    )
    print(data.text)


if __name__ == '__main__':
    main()




