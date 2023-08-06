#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import urllib.error
import urllib.parse
import urllib.request

from homevee.Manager.api_key import get_api_key
from homevee.cronjobs import IntervalCronjob
from homevee.database import get_server_data, get_database_con


class WeatherUpdaterCronjob(IntervalCronjob):
    def __init__(self):
        super(WeatherUpdaterCronjob, self).__init__(task_name="WeatherUpdaterCronjob", interval_seconds=15*60)

    def task_to_do(self, *args):
        self.refresh_weather_cache()

    def get_seconds_to_wait(self, execution_time=None):
        t = datetime.datetime.today()

        seconds_to_wait = (15 * 60) - ((t.minute * 60) - t.second) % 15 * 60

        return seconds_to_wait

    def refresh_weather_cache(self):
        db = get_database_con()

        api_key = get_api_key("Open Weather Map", db)
        location_id = get_server_data("WEATHER_LOCATION_ID", db)

        try:
            url = "http://api.openweathermap.org/data/2.5/forecast/daily?id=" + location_id + "&cnt=16&units=metric&lang=de&type=accurate&APPID=" + api_key
            response = urllib.request.urlopen(url).read()

            with db:
                cur = db.cursor()

                # Wetter-Daten in Datenbank schreiben
                cur.execute("INSERT OR REPLACE INTO SERVER_DATA (KEY, VALUE) values('WEATHER_CACHE', :response);",
                            {"response": response})
                db.commit()

            db.close()

            return True
        except:
            return False