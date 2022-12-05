# Data quilt 

A streamlit app that creates a quilt pattern based on temperature data. The temperature data files are 
in the subdirectory dataquilt. The weather_station_inv determines the ten weather stations nearest to a zip code. 
The data_from_api requests data from those weather stations and determines which have a complete data set. 
The image_generator sorts the maximum temperature data into 15 color coded bins and plots the levels into the quilt
pattern by day. 

## To install the package

1. Install the conda environment
2. Add an API token for NOAA
3. Install the dataquilt package using: python -m pip install -e .\dataquilt
4. Run the streamlit app using: streamlit run \stream\stream_app.py
