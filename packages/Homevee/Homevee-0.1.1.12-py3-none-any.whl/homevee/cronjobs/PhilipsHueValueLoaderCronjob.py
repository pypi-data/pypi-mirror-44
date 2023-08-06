#!/usr/bin/python
# -*- coding: utf-8 -*-

from homevee.DeviceAPI import philips_hue
from homevee.cronjobs import IntervalCronjob
from homevee.database import get_database_con

class PhilipsHueValueLoaderCronjob(IntervalCronjob):
    def __init__(self):
        super(PhilipsHueValueLoaderCronjob, self).__init__(task_name="PhilipsHueValueLoaderCronjob", interval_seconds=5*60)

    def task_to_do(self, *args):
        self.load_hue_values()

    def load_hue_values(self):
        db = get_database_con()

        with db:
            cur = db.cursor()
            cur.execute("SELECT * FROM PHILIPS_HUE_LIGHTS")
            for item in cur.fetchall():
                counter = 3
                for i in range(0, counter):
                    if(philips_hue.get_light_info(item['ID'], db)):
                        break

        db.close()