# -*- coding: UTF-8 -*-
import os

class QtStyle():

    @staticmethod
    def QButtonStyle(height=28, border_radius=4):
        return '''QPushButton {
                height: %s;
                border: none;
                padding-left: 10px;
                padding-right: 10px;
                font: "Sarasa Gothic SC";
                color: "#dbdbdb";
                border-radius: %s;
                background-color: "#22252b";
            }
            QPushButton:hover {background-color: "#333841";}
            QPushButton:pressed {background-color: "#292c34";}
        ''' %(height, border_radius)

    @staticmethod
    def backgroundColor(themes='black'):
        if themes == 'black':
            return [.161, .172, .204]


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
