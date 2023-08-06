#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from homevee.cronjobs import FixedTimeCronjob
from homevee.database import get_database_con
from homevee.device_types import *


class SaveSensorDataCronjob(FixedTimeCronjob):
    def __init__(self):
        super(SaveSensorDataCronjob, self).__init__(task_name="SaveSensorDataCronjob")

    def task_to_do(self, *args):
        self.save_sensor_data()

    def get_seconds_to_wait(self, execution_time=None):
        t = datetime.datetime.today()

        seconds_to_wait = (60*60) - (t.minute*60) - t.second

        return seconds_to_wait

    def save_sensor_data(self):
        db = get_database_con()

        with db:
            cur = db.cursor()

            #Z-Wave Sensoren
            cur.execute("SELECT * FROM ZWAVE_SENSOREN")
            for item in cur.fetchall():
                if item['SAVE_DATA']:
                    self.save_to_db(ZWAVE_SENSOR, item['ID'], item['VALUE'], db)

            #MQTT Sensoren
            cur.execute("SELECT * FROM MQTT_SENSORS")
            for item in cur.fetchall():
                if item['SAVE_DATA']:
                    self.save_to_db(MQTT_SENSOR, item['ID'], item['LAST_VALUE'], db)
        db.close()

    def save_to_db(self,type, id, value, db):
        with db:
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:00')

            cur = db.cursor()

            cur.execute("INSERT INTO SENSOR_DATA (DEVICE_ID, DEVICE_TYPE, DATETIME, VALUE) \
                            VALUES (:id, :type, :time, :value)",
                        {'id': id, 'type': type, 'time': time, 'value':value})