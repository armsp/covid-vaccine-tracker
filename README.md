# Covid Vaccine Tracker

This repository contains dataset on the various vaccines that are in development and(or) being administered around the world. This is not a repository for counts of people inoculated.

This is a fully automated pipeline that runs daily. It collects and parses data from the sources listed below and commits them to the repo - all done using GitHub actions workflow. There are two branches - **main** and **gh-pages**. **main** holds the datasets and scripts for collecting parsing and saving datasets. **gh-pages** has the files for the visualization website.

Visualization Website [Under Construction]: https://armsp.github.io/covid-vaccine-tracker

### Sources

- NYT Source: https://www.nytimes.com/interactive/2020/science/coronavirus-vaccine-tracker.html
- Our World in Data Source: https://ourworldindata.org/covid-vaccinations

Datasets are updated once a day if there is a change.

### Datasets

#### NYT Datasets

The `nt_util.py` script scrapes the NYT Tracker website and forms the dataset for vaccines in various phases and stages of approval.

- **nyt_approved_vaccine.csv** - Contains the dataset for all the approved vaccines around the world.
- Others are coming...

#### Our World in Data Dataset

The `owd_util.py` file gets the `location.csv` data from the [OWID Covid-19 Data repository](https://github.com/owid/covid-19-data) and saves it in the _owd_datasets_ folder.

#### Coming Soon

Notebooks to show processing, merging and making of geospatial charts using the datasets.

---

If these files helped you in anyway then please consider donating so that I can **build a PC for my technical and techno-creative works** or buying me something from my public [Amazon Wishlist](https://www.amazon.in/hz/wishlist/genericItemsPage/3KCSFW4DRG1RY).

**Donate via PayPal or Ko-Fi** 

| Ko-Fi (5 $) | PayPal |
| :---: | :---: |
| <a href='https://ko-fi.com/D1D41SHIS' target='_blank'><img height='40' src='https://cdn.ko-fi.com/cdn/kofi4.png?v=2' alt='Buy Me a Coffee at ko-fi.com' /></a> | <a href="https://paypal.me/shantamraj" target="_blank"><img height='40' src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_150x38.png" alt="PayPal" /></a>|