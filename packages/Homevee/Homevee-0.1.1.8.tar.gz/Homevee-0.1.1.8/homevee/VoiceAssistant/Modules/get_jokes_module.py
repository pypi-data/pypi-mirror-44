#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import traceback
import urllib.request, urllib.parse, urllib.error
import random
from homevee.Helper import Logger
from homevee.VoiceAssistant import helper
from homevee.VoiceAssistant.Modules import VoiceModule
from homevee.VoiceAssistant.voice_patterns import PATTERN_JOKE

class VoiceGetJokesModule(VoiceModule):
    def get_pattern(self, db):
        return PATTERN_JOKE

    def get_label(self):
        return "joke"

    def run_command(self, username, text, context, db):
        return self.get_joke(username, text, context, db)

    def get_joke(self, username, text, context, db):
        try:
            url = helper.SMART_API_PATH + "/?action=joke&text=" + urllib.parse.quote(text.encode('utf8'))
            Logger.log(url)
            data = urllib.request.urlopen(url).read()

            data = data.decode('utf-8')

        except Exception as e:
            traceback.print_exc()
            data = None

        if data is not None:
            return {'msg_speech': data, 'msg_text': data}
        else:
            result = self.get_error()
            return {'msg_speech': result, 'msg_text': result}

    def get_error(self):
        return random.choice([
            'Mir fällt gerade kein Witz ein.'
        ])