# Data quilt 

## Temperature quilts

Temperature quilts display daily weather information for a selected location and range of time. These quilts display trends in the climate over a period of time. 

This is a demonstration project that creates a digital mockup of quilt based on real world data. 

## Project Description
This project is a streamlit app that constructs a quilt pattern based on daily temperature data 
from the National Oceanic and Atomospheric Administration (NOAA)[https://www.noa.gov].
In the data quilt package,
the module *weather_station_inv* sorts data from the (gchnd weather station inventory)[https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt] and determines the ten closest weather stations to the given zip code.  
The *data_from_api* requests data from those weather stations and determines which have a complete data set. 
The *image_generator* sorts the maximum temperature data into 15 color coded bins and plots the levels into the quilt
pattern by day. Finally, the *colors_kona* uses data based on commercially available fabric and 
creates a digital mockup and pattern of the quilt. 



## To install the package and run the streamlit app

1. Install the conda environment
2. Add an API token for NOAA
3. Install the dataquilt package using:
```python 
python -m pip install -e .\dataquilt
```

4. Run the streamlit app using: 
``` python
streamlit run \stream\stream_app.py
```

## Resources
This app uses the following packages:

- Numpy
- Pillow
- Pandas
- Requests 
- Streamlit

## Credits

This project was completed in the (Pybites Developer Mindset Program)[https://pybit.es/catalogue/the-pdm-program/] with Robin Beer as mentor. 