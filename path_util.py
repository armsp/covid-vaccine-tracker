'''
Dataset saving path utils
'''

import os
from pathlib import Path

def get_owd_dataset_path(filename):
    parent_dir = Path().absolute()
    Path(f"{parent_dir}/owd_datasets").mkdir(parents=True, exist_ok=True)
    return Path(f'./owd_datasets/{filename}').resolve()


def get_nyt_dataset_path(filename, dataset_type=None):
    parent_dir = Path().absolute()
    Path(f"{parent_dir}/nyt_datasets").mkdir(parents=True, exist_ok=True)
    return Path(f'./nyt_datasets/{filename}').resolve()

if __name__=='__main__':
    print(get_owd_dataset_path('dummy.txt'))
    print(get_nyt_dataset_path('dummy.txt'))