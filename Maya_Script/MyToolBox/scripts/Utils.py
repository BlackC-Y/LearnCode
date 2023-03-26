# -*- coding: UTF-8 -*-

class QtStyle():

    backgroundColor = [.172, .192, .235]

    @staticmethod
    def QButton(height=28):
        return '''QPushButton {
                height: %s;
                border: none;
                padding-left: 10px;
                padding-right: 10px;
                font: "Sarasa Gothic SC";
                color: "#dbdbdb";
                border-radius: 4;
                background-color: "#21252d";
            }
            QPushButton:hover {background-color: "#626d80";}
            QPushButton:pressed {background-color: "#272c36";}
        ''' %height
