'''
Utilities for handling and cleaning of the NYT dataset scraped from their Vaccine tracker website https://www.nytimes.com/interactive/2020/science/coronavirus-vaccine-tracker.html
'''
import pandas as pd
import unicodedata
from requests_html import HTMLSession

from path_util import get_nyt_dataset_path

NYT_URI = "https://www.nytimes.com/interactive/2020/science/coronavirus-vaccine-tracker.html"

SELECTOR_APPROVED = "p.g-filter-approved > span.g-vacinfo"# > span.g-info"
SELECTOR_P3 = ""
SELECTOR_P2 = ""
SELECTOR_P1 = ""
SELECTOR_PRECLINICAL = ""
SELECTOR_ABANDONED = ""
SELECTOR_ALL = ""

def get_NYT_webpage(uri):
    session = HTMLSession()
    r = session.get(uri)
    return r

def process_vaccine_info(all_info_dict):
    return {unicodedata.normalize("NFKD", key.strip()): value.strip() for key, value in (info.split(':') if all_info_dict['vaccine_info'] != '' else ['None','None'] for info in all_info_dict['vaccine_info'].split('\n'))}

def process_location_info(all_info_dict):
    return {key.strip(): value.strip() for key, value in (info.split(':') for info in all_info_dict['location_info'].split('\n'))}

def get_vaccine_location_df_from_selector(extracted_selector_list):
    info_dict = {}
    for i, (vaccine_info, location_info) in enumerate(zip(extracted_selector_list[::2],extracted_selector_list[1::2])):
        info_dict[i] = dict()
        info_dict[i]['vaccine_info'] = vaccine_info.text
        info_dict[i]['location_info'] = location_info.text

    vaccines_locations_df = pd.DataFrame.from_dict({index: {**(process_vaccine_info(vaccine_and_location)), **(process_location_info(vaccine_and_location))} for index, vaccine_and_location in info_dict.items()}, orient='index')

    return vaccines_locations_df

def cleaned_vaccines_location_df(df):
    df['Early use in'] = df['Early use in'].str.rstrip(' .') #remove dots in the end
    df['Limited use in'] = df['Limited use in'].str.rstrip(' .').str.replace('NEW', '') #remove dots in the end and NEW
    df['Emergency use in'] = df['Emergency use in'].str.replace('NEW', '').str.replace("Emergency use validation from the World Health Organization",'').str.rstrip(' .').str.replace("Endorsed by the Africa Regulatory Taskforce. Recommended for emergency use by the Caribbean Regulatory System", '').str.rstrip(' .') #remove dots in the end and NEW, "Emergency use validation from the World Health Organization."
    df['Approved for use in'] = df['Approved for use in'].str.rstrip(' .').str.replace('NEW', '') #remove NEW and .
    df['Stopped use in'] = df['Stopped use in'].str.rstrip(' .')#.str.replace('NEW', '') #remove NEW and .
    df = df .drop(columns=['None'])
    return df

def processed_vaccines_location_df(cleaned_df):
    cleaned_df['Approved for use in'] = cleaned_df['Approved for use in'].apply(lambda x: list(map(str.strip, x.split(','))) if pd.notna(x) else x)
    cleaned_df['Emergency use in'] = cleaned_df['Emergency use in'].apply(lambda x: list(map(str.strip, x.split(','))) if pd.notna(x) else x)
    cleaned_df['Limited use in'] = cleaned_df['Limited use in'].apply(lambda x: list(map(str.strip, x.split(','))) if pd.notna(x) else x)
    cleaned_df['Early use in'] = cleaned_df['Early use in'].apply(lambda x: list(map(str.strip, x.split(','))) if pd.notna(x) else x)
    cleaned_df['Stopped use in'] = cleaned_df['Stopped use in'].apply(lambda x: list(map(str.strip, x.split(','))) if pd.notna(x) else x)
    return cleaned_df

def get_approved_vaccines():
    r = get_NYT_webpage(NYT_URI)
    extracted_info_list = r.html.find(SELECTOR_APPROVED)
    vaccines_locations_df = get_vaccine_location_df_from_selector(extracted_info_list)
    vaccines_locations_df = cleaned_vaccines_location_df(vaccines_locations_df)
    vaccines_locations_df = processed_vaccines_location_df(vaccines_locations_df)
    return vaccines_locations_df

def save_approved_vaccines_nyt(df):
    nyt_dataset_path = get_nyt_dataset_path('nyt_approved_vaccines.csv')
    df.to_csv(nyt_dataset_path, index=False)

def get_phase3_vaccines():
    pass

def get_phase2_vaccines():
    pass

def get_phase1_vaccines():
    pass

def get_preclinical_vaccines():
    pass

def get_abandoned_vaccines():
    pass

def get_all_vaccines():
    pass

if __name__=='__main__':
    approved_vaccines_df = get_approved_vaccines()
    save_approved_vaccines_nyt(approved_vaccines_df)