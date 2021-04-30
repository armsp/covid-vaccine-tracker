import datetime
import requests
import altair as alt
import pandas as pd
import geopandas as gpd
from functools import lru_cache

alt.renderers.set_embed_options(actions=False)

chart_template = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/vega@{vega_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@{vegalite_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@{vegaembed_version}"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-projection-extended@2"></script>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<div id="vis"></div>

<script type="text/javascript">
  vegaEmbed('#vis', {spec}, {kwargs}).catch(console.error);
</script>
<span class="update_time">Updated at {update_time}</span>
</body>
</html>
"""

def get_time():
    current_time = str(datetime.datetime.utcnow())
    return current_time

@lru_cache
def get_shapefiles():
    #uri_50m = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip" # this redirects to the following url
    uri_50m = "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip" # works
    #uri_110m = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip"
    #stream = requests.get(uri_50m, stream=True).raw
    countries_raw = gpd.read_file(uri_50m) #uri_50m also works

    countries_map = countries_raw.drop(columns=list(countries_raw.columns[:17]) + list(countries_raw.columns[18:46]) + list(countries_raw.columns[47:-1]))
    countries_map = countries_map.rename(columns={'ISO_A3': 'iso_code'})
    return countries_map

def make_nyt_chart():
    pass

def make_owd_chart():
    vaccine_location_data = pd.read_csv('./owd_datasets/vaccine_approval_owd.csv')
    vaccine_location_data['vaccines'] = vaccine_location_data.vaccines.apply(lambda x: list(map(str.lstrip, x.split(','))))
    vaccine_location_data = vaccine_location_data.explode('vaccines').reset_index(drop=True)

    countries_map = get_shapefiles()
    countries_map.loc[countries_map.NAME == 'France', 'iso_code'] = "FRA"
    countries_map.loc[countries_map.NAME == 'Norway', 'iso_code'] = "NOR"
    vaccine_location_data.loc[vaccine_location_data.location.isin(['England', 'Wales', 'Scotland', 'Northern Ireland']), 'iso_code'] = "GBR"

    plot_data = countries_map.merge(vaccine_location_data, how='inner', on='iso_code')
    base = alt.Chart(countries_map[countries_map.iso_code!='ATA']).mark_geoshape(fill='#eee', stroke="#fff", strokeWidth=0.5)

    chart = alt.concat(*(
                base + alt.Chart(plot_data[plot_data['vaccines']==vaccine], title=vaccine, height=200, width=350).mark_geoshape(stroke="#fff", strokeWidth=0.5).encode(
                    color=alt.value('#2e7265')
                ).project('equalEarth')
                for vaccine in list(plot_data.vaccines.unique())
                ), columns=3, title="Where each vaccine is being used", spacing=0
            ).configure_view(strokeWidth=0)

    return chart

def modify_owd_chart(chart):
    with open('index.html', 'w+') as f:
        f.write(chart_template.format(
            update_time=get_time(),
            vega_version=alt.VEGA_VERSION,
            vegalite_version=alt.VEGALITE_VERSION,
            vegaembed_version=alt.VEGAEMBED_VERSION,
            spec=chart.to_json(indent=None),
            kwargs = """{"actions": false, "mode": "vega-lite"}"""
        ))
        f.seek(0)
        filedata = f.read()
        filedata = filedata.replace('equalEarth', 'eckert3')


if __name__=='__main__':
    chart = make_owd_chart()
    modify_owd_chart(chart)