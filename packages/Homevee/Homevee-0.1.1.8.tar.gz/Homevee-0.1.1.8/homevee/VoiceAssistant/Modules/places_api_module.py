#!/usr/bin/python
# -*- coding: utf-8 -*-
from homevee.VoiceAssistant.Modules import VoiceModule
from homevee.VoiceAssistant.voice_patterns import PATTERN_PLACES

class VoicePlacesApiModule(VoiceModule):
    def get_pattern(self, db):
        return PATTERN_PLACES

    def get_label(self):
        return "placesapi"

    def run_command(self, username, text, context, db):
        return self.get_places(username, text, context, db)

    def get_places(self, username, text, context, db):
        return {'msg_speech': 'Places', 'msg_text': 'Places'}