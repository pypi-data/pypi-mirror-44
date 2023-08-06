#!/usr/bin/python
# -*- coding: utf-8 -*-

from homevee.Functions.tv_data import get_tv_plan
from homevee.VoiceAssistant import helper
from homevee.VoiceAssistant.Modules import VoiceModule
from homevee.VoiceAssistant.voice_patterns import PATTERN_GET_TV_SCHEDULE

class VoiceGetTvScheduleModule(VoiceModule):
    def get_pattern(self, db):
        return PATTERN_GET_TV_SCHEDULE

    def get_label(self):
        return "gettvschedule"

    def run_command(self, username, text, context, db):
        return self.get_tv(username, text, context, db)

    def get_tv(self, username, text, context, db):
        return {'msg_speech':'TV-Programm', 'msg_text':'TV-Programm'}