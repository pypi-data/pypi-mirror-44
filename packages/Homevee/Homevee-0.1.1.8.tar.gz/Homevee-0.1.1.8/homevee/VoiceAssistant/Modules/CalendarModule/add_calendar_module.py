#!/usr/bin/python
# -*- coding: utf-8 -*-
from homevee.VoiceAssistant.Modules.CalendarModule import VoiceCalendarModule
from homevee.VoiceAssistant.voice_patterns import PATTERN_ADD_CALENDAR


class VoiceAddCalendarModule(VoiceCalendarModule):
    def get_context_key(self):
        return "VOICE_ADD_CALENDAR"

    def get_pattern(self, db):
        return PATTERN_ADD_CALENDAR

    def get_label(self):
        return "addcalendar"

    def run_command(self, username, text, context, db):
        return self.add_calendar(username, text, context, db)

    def add_calendar(self, username, text, context, db):
        return {'msg_speech': 'Add Calendar', 'msg_text': 'Add Calendar'}