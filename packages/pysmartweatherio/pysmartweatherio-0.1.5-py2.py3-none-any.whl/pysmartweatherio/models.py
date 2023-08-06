import datetime

import requests

from .utils import Conversion, PropertyUnavailable, UnicodeMixin


class StationData(UnicodeMixin):
    def __init__(self, data, response, headers, units):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.units = units.lower()

        self._alerts = []
        for alertJSON in self.json.get('alerts', []):
            self._alerts.append(Alert(alertJSON))

    def update(self):
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r

    def currentdata(self):
        dtformat = datetime.datetime.fromtimestamp(self.json['obs'][0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        if 'lightning_strike_last_epoch' not in self.json['obs'][0]:
            liformat = "1970-01-01 00:00:00"
        else:
            liformat = datetime.datetime.fromtimestamp(self.json['obs'][0]['lightning_strike_last_epoch']).strftime('%Y-%m-%d %H:%M:%S')
        if 'precip_accum_local_yesterday' not in self.json['obs'][0]:
            precipyesterday = 0
        else:
            precipyesterday = self.json['obs'][0]['precip_accum_local_yesterday']
        if 'lightning_strike_last_distance' not in self.json['obs'][0]:
            lightniglast = 0
        else:
            lightniglast = self.json['obs'][0]['lightning_strike_last_distance']

        return CurrentData(
            self.json['station_name'],
            dtformat,
            self.json['obs'][0]['air_temperature'],
            self.json['obs'][0]['feels_like'],
            Conversion.speed(float(self.json['obs'][0]['wind_avg']), self.units),
            int(self.json['obs'][0]['wind_direction']),
            Conversion.wind_direction(self.json['obs'][0]['wind_direction']),
            Conversion.speed(float(self.json['obs'][0]['wind_gust']), self.units),
            Conversion.speed(float(self.json['obs'][0]['wind_lull']), self.units),
            float(self.json['obs'][0]['uv']),
            Conversion.volume(float(self.json['obs'][0]['precip_accum_local_day']), self.units),
            int(self.json['obs'][0]['relative_humidity']),
            Conversion.rate(float(self.json['obs'][0]['precip']), self.units),
            float(self.json['obs'][0]['precip']),
            Conversion.pressure(float(self.json['obs'][0]['station_pressure']), self.units),
            float(self.json['latitude']),
            float(self.json['longitude']),
            self.json['obs'][0]['heat_index'],
            self.json['obs'][0]['wind_chill'],
            self.json['obs'][0]['dew_point'],
            Conversion.volume(float(self.json['obs'][0]['precip_accum_last_1hr']), self.units),
            Conversion.volume(float(self.json['obs'][0]['precip_accum_last_24hr']), self.units),
            Conversion.volume(float(precipyesterday), self.units),
            int(self.json['obs'][0]['solar_radiation']),
            int(self.json['obs'][0]['brightness']),
            liformat,
            Conversion.distance(lightniglast, self.units),
            int(self.json['obs'][0]['lightning_strike_count']),
            int(self.json['obs'][0]['lightning_strike_count_last_3hr'])
            )

class DeviceData(UnicodeMixin):
    def __init__(self, data, response, headers, units):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.units = units.lower()

        self._alerts = []
        for alertJSON in self.json.get('alerts', []):
            self._alerts.append(Alert(alertJSON))

    def update(self):
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r

    def devicedata(self):
        """ Read Device Data from the Returned JSON. """
        if self.json['type'] == 'obs_sky':
            dtformat = datetime.datetime.fromtimestamp(self.json['obs'][0][0]).strftime('%Y-%m-%d %H:%M:%S')
            return DeviceSkyData(
                dtformat,
                self.json['obs'][0][8]
            )
        elif self.json['type'] == 'obs_air':
            dtformat = datetime.datetime.fromtimestamp(self.json['obs'][0][0]).strftime('%Y-%m-%d %H:%M:%S')
            return DeviceAirData(
                dtformat,
                self.json['obs'][0][8]
            )
        else:
            return None

class Alert(UnicodeMixin):
    def __init__(self, json):
        self.json = json

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            raise PropertyUnavailable(
                "Property '{}' is not valid"
                " or is not available".format(name)
            )

    def __unicode__(self):
        return '<Alert instance: {0} at {1}>'.format(self.title, self.time)

class CurrentData:
    """ Returns an Array with Current Weather Observations. """
    def __init__(self, station_location, timestamp, temperature, feels_like, wind_speed, wind_bearing, wind_direction, wind_gust, wind_lull,
                 uv, precipitation,humidity, precipitation_rate, rain_rate_raw, pressure, latitude, longitude, heat_index, wind_chill, dewpoint,
                 precipitation_last_1hr, precipitation_last_24hr, precipitation_yesterday, solar_radiation, brightness,lightning_time,
                 lightning_distance, lightning_count,lightning_count_3hour
                 ):
        self.station_location = station_location
        self.timestamp = timestamp
        self.temperature = temperature
        self.feels_like_temperature = feels_like
        self.wind_speed = wind_speed
        self.wind_bearing = wind_bearing
        self.wind_direction = wind_direction
        self.wind_gust = wind_gust
        self.wind_lull = wind_lull
        self.uv = uv
        self.precipitation = precipitation
        self.humidity = humidity
        self.precipitation_rate = precipitation_rate * 60
        self.pressure = pressure
        self.latitude = latitude
        self.longitude = longitude
        self.heat_index = heat_index
        self.wind_chill = wind_chill
        self.dewpoint = dewpoint
        self.precipitation_last_1hr = precipitation_last_1hr
        self.precipitation_last_24hr = precipitation_last_24hr
        self.precipitation_yesterday = precipitation_yesterday
        self.solar_radiation = solar_radiation
        self.illuminance = brightness
        self.lightning_time = lightning_time
        self.lightning_distance = lightning_distance
        self.lightning_count = lightning_count
        self.lightning_last_3hr = lightning_count_3hour

        """ Binary Sensor Values """
        self.raining = True if rain_rate_raw > 0 else False
        self.freezing = True if temperature < 0 else False
        self.lightning = True if lightning_count > 0 else False

class DeviceSkyData:
    """ Returns an Array with data from a SKY module. """
    def __init__(self, timestamp, battery):
        self.timestamp = timestamp
        self.battery = battery

class DeviceAirData:
    """ Returns an Array with data from a AIR module. """
    def __init__(self, timestamp, battery):
        self.timestamp = timestamp
        self.battery = battery
