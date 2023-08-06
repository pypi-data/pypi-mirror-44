#!/usr/bin/python
# -*- coding: utf-8 -*-
from homevee.VoiceAssistant.Modules import VoiceModule
from homevee.VoiceAssistant.context_keys import CONTEXT_CALCULATOR
from homevee.VoiceAssistant.voice_patterns import PATTERN_CALCULATOR

class VoiceCalculatorModule(VoiceModule):
    def calculator(self, username, text, context, db):
        return {'msg_speech':"Taschenrechner", 'msg_text':"Taschenrechner"}

    def get_pattern(self, db):
        return PATTERN_CALCULATOR

    def get_label(self):
        return "calculator"

    def get_context_key(self):
        return CONTEXT_CALCULATOR

    def run_command(self, username, text, context, db):
        return self.calculator(username, text, context, db)