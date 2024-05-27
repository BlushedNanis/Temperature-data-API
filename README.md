# Temperature Data API (Flask)

REST API created using Flask. The project will load the temperature data (in this case, temperature data from http://www.ecad.eu) from text files into a Pandas data frame; each text file corresponds to a weather station. The home page shows the list of stations and examples of the use of the API. The API can handle different requests from a single station (meaning that each request must point to a specific weather station), which are:

* Specific date: Station - Year - Month - Day (returns the weather data for the specific day)
* Specific month: Station - Year - Month (returns the weather data for the whole month)
* Specific year: Station - Year (returns the weather data for the whole year)
* Specific station: Station (returns the whole weather data of the station)

The API returns a list type object, which contains dictionaries with the following keys:

* DATE
* TC: Temperature in Celsius degrees
* TF: Temperature in Fahrenheit degrees

### Example:

URL: [127.0.0.1:5000/api/v1/10/1997/08/24](http://127.0.0.1:5000/api/v1/10/1997/08/24)

Response: 

[
    {
        "    DATE": "Sun, 24 Aug 1997 00:00:00 GMT",
        "TC": 20.6,
        "TF": 69.08
    }
]
