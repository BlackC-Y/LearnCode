# -*- coding: UTF-8 -*-
import os


class Functions():
    
    @staticmethod
    def set_svg_icon(icon_name):
        modulePath = os.path.join(__file__, '../../')
        folder = "images/svg_icons/"
        path = os.path.join(modulePath, folder)
        icon = os.path.normpath(os.path.join(path, icon_name))
        return icon

    @staticmethod
    def set_svg_image(icon_name):
        modulePath = os.path.join(__file__, '../../')
        folder = "images/svg_images/"
        path = os.path.join(modulePath, folder)
        icon = os.path.normpath(os.path.join(path, icon_name))
        return icon

    @staticmethod
    def set_image(image_name):
        modulePath = os.path.join(__file__, '../../')
        folder = "images/images/"
        path = os.path.join(modulePath, folder)
        image = os.path.normpath(os.path.join(path, image_name))
        return image
    
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
        modulePath = os.path.join(__file__, '../../')
        folder = "font/"
        path = os.path.join(modulePath, folder)
        font = os.path.normpath(os.path.join(path, font_name))
        return font