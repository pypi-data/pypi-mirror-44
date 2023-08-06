#!/usr/bin/python
# -*- coding: utf-8 -*-
from homevee.DeviceAPI.rgb_control import rgb_control
from homevee.VoiceAssistant.Modules.DeviceControlModule import VoiceDeviceControlModule
from homevee.VoiceAssistant.voice_patterns import PATTERN_RGB_CONTROL
from homevee.colors import COLORS, COLOR_NAMES
from homevee.device_types import *

class VoiceRgbDeviceControlModule(VoiceDeviceControlModule):
    def get_pattern(self, db):
        return PATTERN_RGB_CONTROL

    def get_label(self):
        return "rgb"

    def run_command(self, username, text, context, db):
        return self.voice_rgb_control(username, text, context, db)

    def voice_rgb_control(self, username, text, context, db):
        room = self.find_room(text, db)

        if room is not None:
            room_key = room['LOCATION']
        else:
            room_key = None

        device_types = [PHILIPS_HUE_LIGHT, URL_RGB_LIGHT]

        devices = self.find_devices(text, device_types, room_key, db)

        color = self.find_color(text)
        if color != False:
            color_hex = COLOR_NAMES[color]
        else:
            return "Du musst mir eine Farbe sagen."

        for device in devices:
            rgb_control(username, device['type'], device['id'], True, None, color_hex, db)

            return {'msg_speech': 'Ok.', 'msg_text': 'Ok.'}

    def find_color(self, text):
        for word in text.split():
            for color in COLORS:
                if word == color:
                    return color
        return False