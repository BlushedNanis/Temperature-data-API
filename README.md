# Weather Data API

This project has been developed during the "Python Mega Course" by Ardit Sulce.

REST API which returns temperature data from weather stations all across Europe,  is able to return data from a single weather station in multiple data formats through multiple endpoints.

The call will return a list instance with the date and temperature in celsius degrees and fahrenheit degrees, of the given date range, depending on the called enpoint.

The data is read from .txt files with pandas, and the API uses Flask as framework.
