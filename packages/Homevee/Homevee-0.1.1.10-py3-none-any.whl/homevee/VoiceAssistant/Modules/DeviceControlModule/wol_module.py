#!/usr/bin/python
# -*- coding: utf-8 -*-
from homevee.DeviceAPI.wake_on_lan import wake_on_lan
from homevee.Helper import Logger
from homevee.VoiceAssistant import context_keys
from homevee.VoiceAssistant.Modules.DeviceControlModule import VoiceDeviceControlModule
from homevee.VoiceAssistant.helper import generate_string, set_context, get_okay
from homevee.VoiceAssistant.voice_patterns import GET_PATTERN_WOL
from homevee.device_types import *

class VoiceDeviceWakeOnLanModule(VoiceDeviceControlModule):
    def get_context_key(self):
        return "VOICE_WAKE_ON_LAN"

    def get_pattern(self, db):
        return GET_PATTERN_WOL

    def get_label(self):
        return "wakeonlan"

    def voice_wol(self, username, text, context, db):
        room = self.find_room(text, db)

        if room is not None:
            room_key = room['LOCATION']
        else:
            room_key = None

        device_types = [WAKE_ON_LAN, XBOX_ONE_WOL]

        devices = self.find_devices(text, device_types, room_key, db)

        if len(devices) == 0:
            #Keine Geräte gefunden
            answer_data = [
                [['Dieses ', 'Das genannte '], 'Gerät ', ['existiert nicht.', 'gibt es nicht.', 'wurde noch nicht angelegt.']]
            ]

            answer = generate_string(answer_data)

            return {'msg_speech': answer, 'msg_text': answer}

        words = text.split(" ")

        #Geräte schalten
        for device in devices:
            if device['type'] == XBOX_ONE_WOL:
                Logger.log("")
                #xbox_wake_up(username, device['id'], db)
            else:
                wake_on_lan(username, device['id'], db)

        set_context(username, context_keys.CONTEXT_WOL, {'location': room, 'devices': devices}, db)

        DEVICE_STRING = None
        if len(devices) > 1:
            VERB = "wurden"
            DEVICE_WORD = "Die Geräte "

            for i in range(0, len(devices)):
                if DEVICE_STRING is None:
                    DEVICE_STRING = '\'' + devices[i]['name'] + '\''
                elif i == len(devices) - 1:
                    DEVICE_STRING = DEVICE_STRING + ' und ' + '\'' + devices[i]['name'] + '\''
                else:
                    DEVICE_STRING = DEVICE_STRING + ', ' + '\'' + devices[i]['name'] + '\''
        else:
            DEVICE_WORD = "Das Gerät "
            VERB = "wurde"

            DEVICE_STRING = '\'' + devices[0]['name'] + '\''

        answer_data = [
            [get_okay(), [', ' + username, ''], '.',
             ['', [' ', DEVICE_WORD,  [DEVICE_STRING + ' ', ''], VERB + ' ',
                   ['gestartet', 'eingeschalten', 'eingeschaltet', 'an gemacht', 'hochgefahren'], '.']]]
        ]

        answer = generate_string(answer_data)

        return {'msg_speech': answer, 'msg_text': answer}