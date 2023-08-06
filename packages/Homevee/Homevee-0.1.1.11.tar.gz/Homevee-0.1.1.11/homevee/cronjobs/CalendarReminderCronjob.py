#!/usr/bin/python
# -*- coding: utf-8 -*-

from homevee.cronjobs import IntervalCronjob
from homevee.database import get_database_con

class CalendarReminderCronjob(IntervalCronjob):
    def __init__(self):
        super(CalendarReminderCronjob, self).__init__(task_name="CalendarReminder", interval_seconds=60)

    def task_to_do(self, *args):
        self.remind_users()

    def remind_users(self):
        db = get_database_con()

        with db:
            #query events and remind users of upcoming calendar entries

            return