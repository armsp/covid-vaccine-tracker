'''
Utilities for handling and cleaning of the OWD dataset
'''
import pandas as pd

from path_util import get_owd_dataset_path

DATA_URI = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv"

def save_owd_approval_data(uri):

    raw_data = pd.read_csv(uri)

    vaccine_location_data = raw_data.copy()
    vaccine_location_data['vaccines'] = vaccine_location_data.vaccines.apply(lambda x: list(map(str.lstrip, x.split(','))))
    vaccine_location_data = vaccine_location_data.explode('vaccines').reset_index(drop=True)
    owd_dataset_path = get_owd_dataset_path('vaccine_approval_owd.csv')
    vaccine_location_data.to_csv(owd_dataset_path, index=False)

if __name__=='__main__':
    save_owd_approval_data(uri = DATA_URI)

# TODO
# How to assign iso codes for country constituents like England, Wales, Scotland etc