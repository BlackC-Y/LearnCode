# -*- coding: UTF-8 -*-
import json
import os

# IMPORT SETTINGS
from MyToolBox.gui.core.json_settings import Settings

# APP THEMES
class Themes(object):
    # LOAD SETTINGS
    setup_settings = Settings()
    _settings = setup_settings.items

    json_file = "themes/%s.json" %_settings['theme_name']
    modulePath = os.path.join(__file__, '../../')
    settings_path = os.path.normpath(os.path.join(modulePath, json_file))
    if not os.path.isfile(settings_path):
        print("WARNING: \"%s\" not found! check in the folder %s" %(json_file, settings_path))

    # INIT SETTINGS
    def __init__(self):
        super(Themes, self).__init__()

        # DICTIONARY WITH SETTINGS
        self.items = {}

        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    def serialize(self):
        # WRITE JSON FILE
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    def deserialize(self):
        # READ JSON FILE
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings