# -*- coding: UTF-8 -*-
import json
import os

class QtStyle():

    @staticmethod
    def QButtonStyle(height=28, border_radius=4):
        theme=Functions.readSetting('Global', 'theme')
        if theme == 'black':
            TextColor = "#dbdbdb"
            ButtonBC = "#22252b"
            Button_hoverBC = "#333841"
            Button_pressedBC = "#292c34"
        elif theme == "pink":
            TextColor = "#2f2f2f"
            ButtonBC = "#f3abb6"
            Button_hoverBC = "#f3b7c0"
            Button_pressedBC = "#ffcad4"
        elif theme == 'eyegreen':
            TextColor = "#2f2f2f"
            ButtonBC = "#a6e1ad"
            Button_hoverBC = "#cdedd1"
            Button_pressedBC = "#c7edcc"

        return '''
        QPushButton {{
            height: {_height};
            border: none;
            padding-left: 10px;
            padding-right: 10px;
            font: "Sarasa Gothic SC";
            color: {_TextColor};
            border-radius: {_border_radius};
            background-color: {_ButtonBC};
        }}
        QPushButton:hover {{
            background-color: {_Button_hoverBC};
        }}
        QPushButton:pressed {{
            background-color: {_Button_pressedBC};
        }}
        '''.format(_height = height, _TextColor=TextColor, _border_radius = border_radius, 
                   _ButtonBC = ButtonBC, _Button_hoverBC = Button_hoverBC, _Button_pressedBC = Button_pressedBC
        )

    @staticmethod
    def backgroundMayaColor():
        theme=Functions.readSetting('Global', 'theme')
        if theme == 'black':
            return [.161, .172, .204]
        elif theme == "pink":
            return [1, .792, .831]
        elif theme == 'eyegreen':
            return [.776, .929, .808]
    
    @staticmethod
    def accentMayaColor():
        theme=Functions.readSetting('Global', 'theme')
        if theme == 'black':
            return [.133, .145, .169]
        elif theme == "pink":
            return [.953, .663, .718]
        elif theme == 'eyegreen':
            return [.653, .886, .684]

class Functions():

    @staticmethod
    def check_font(font_name):
        systemfilepath = os.path.join('C:\Windows\Fonts', font_name)
        filepath = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft\Windows\Fonts', font_name)
        if os.path.isfile(filepath) or os.path.isfile(systemfilepath):
            return 0
        else:
            return 1
    
    @staticmethod
    def set_font(font_name):
        folder = '%s/MyToolBoxDir/Data/' %os.getenv('ALLUSERSPROFILE')
        font = os.path.normpath(os.path.join(folder, font_name))
        return font

    @staticmethod
    def editSetting(ui, item, data):
        jsonFile = '%s/MyToolBoxDir/Data/Settings.json' %os.getenv('ALLUSERSPROFILE')
        if os.path.isfile(jsonFile):
            with open(jsonFile, 'r') as jsFile:
                readData = json.load(jsFile)
            with open(jsonFile, 'w') as jsFile:
                readData[ui][item] = data
                json.dump(readData, jsFile, indent=2)

    @staticmethod
    def readSetting(ui, item):
        jsonFile = '%s/MyToolBoxDir/Data/Settings.json' %os.getenv('ALLUSERSPROFILE')
        if not os.path.isfile(jsonFile):
            return None
        else:
            with open(jsonFile, 'r') as jsFile:
                readData = json.load(jsFile)
                jsSetting = readData[ui]
            return jsSetting[item]
            