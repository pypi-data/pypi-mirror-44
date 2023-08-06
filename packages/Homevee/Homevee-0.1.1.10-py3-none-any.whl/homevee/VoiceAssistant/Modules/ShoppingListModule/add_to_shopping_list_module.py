#!/usr/bin/python
# -*- coding: utf-8 -*-
from homevee.VoiceAssistant.Modules.ShoppingListModule import VoiceShoppingListModule
from homevee.VoiceAssistant.voice_patterns import *


class VoiceAddToShoppingListModule(VoiceShoppingListModule):
    def get_pattern(self, db):
        return PATTERN_ADD_SHOPPING_LIST

    def get_label(self):
        return "getshoppinglist"

    def run_command(self, username, text, context, db):
        return self.add_to_shopping_list(username, text, context, db)

    def add_to_shopping_list(self, username, text, context, db):
        '''words = text.split(" ")

        for i in range(0, len(words)):
            word = words[i]



        if item_count > 1:
            answer_data = [
                ['Ok']
            ]
        else:
            answer_data = [
                ['Ok']
            ]

        output = generate_string(answer_data)'''

        output = "Add Shopping List"

        return {'msg_speech': output, 'msg_text': output}

