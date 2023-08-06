# pySmartWeatherIO
Wrapper for the WeatherFlow Smart Weather REST API. Designed to work with Home Assistant.

This module communicates with a Smart Home Weather station from the company [WeatherFlow](http://weatherflow.com/smart-home-weather-stations/) using their REST API. It retrieves current weather data from the attached units. Currently they have two types of Units:
* **AIR** - This unit measures Temperature, Humidity, Pressure and Lightning Strikes
* **SKY** - This unit measures Precipitation, Wind, Illuminance and UV
They are both attached to a central hub, that broadcasts the data via UDP and sends the data to a cloud database managed by WeatherFlow. This module retrieves the data back from the cloud database.

## Functions
The module exposes the following functions:<br>
### load_stationdata(station_id, api_key, units)
this will return a Data Class with all the data collected from a specific Station.<br>

**station_id**<br>
(string)(required) If you have your own Smart Weather Station, then you know your Station ID. If you don't have one, there are a lot of public stations available, and you can find one near you on [this link](https://smartweather.weatherflow.com/map). If you click on one of the stations on the map, you will see that the URL changes, locate the number right after */map/* - this is the Station ID<br>

**api_key**<br>
(string)(Required) The WeatherFlow REST API requires a API Key, but for personal use, you can use a development key, which you can [find here](https://weatherflow.github.io/SmartWeather/api/#getting-started). Please note the restrictions applied.

**units**<br>
(string)(optional) The unit system to use. Metric or Imperial<br>
Default value: Metric<br>

**Data Class Definition**<br>
* **temperature** - Current temperature
* **feels_like_temperature** - How the temperature Feels Like. A combination of Heat Index and Wind Chill
* **heat_index** - A temperature measurement combining Humidity and temperature. How hot does it feel. Only used when temperature is above 26.67°C (80°F)
* **wind_chill** - How cold does it feel. Only used if temperature is below 10°C (50°F)
* **dewpoint** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form
* **wind_speed** - Current Wind Speed
* **wind_gust** - Highest Wind Speed in the last minute
* **wind_lull** - Lowest Wind Speed in the last minute
* **wind_bearing** - Wind bearing in degrees (Example: 287°)
* **wind_direction** - Wind bearing as directional text (Example: NNW)
* **precipitation** - Precipitation since midnight
* **precipitation_rate** - The current precipitation rate - 0 if it is not raining
* **precipitation_last_1hr** - Precipitation in the last hour
* **precipitation_last_24hr** - Precipitation in the last 24 hours.
* **precipitation_yesterday** - Precipitation yesterday
* **humidity** - Current humidity in %
* **pressure** - Current barometric pressure, taking in to account the position of the station
* **uv** - The UV index
* **solar_radiation** - The current Solar Radiation measured in W/m2
* **illuminance** - Shows the brightness in Lux
* **lightning_count** - Shows the numbers of lightning strikes for last minute. Attributes of this sensor has more Lightning i
<hr>
