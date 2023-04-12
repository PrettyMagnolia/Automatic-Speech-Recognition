import os
import sys
import threading
import win32api
import webbrowser
from functools import partial
import speech_recognition as sr
from asrInterface import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore, uic


def play_music():
    win32api.ShellExecute(0, 'open', 'music.mp3', '', '', 1)


def open_notepad():
    win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)


def open_webpage():
    webbrowser.open("https://www.bing.com")


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("I'm listening")
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


# Visual window
class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.myThread = None

        # add button binding events
        self.ui.button1.clicked.connect(self.button_click)

    def button_click(self):
        # play microphone gif
        self.ui.gif_.start()
        # modify button content
        self.ui.button1.setText("Please say")
        try:
            # Start the voice recognition thread
            MyThread().start()
        except:
            print("thread start failed")

    def recognize_over(self):
        # play microphone gif
        self.ui.gif_.stop()
        # modify button content
        self.ui.button1.setText("Click Here to Start！")


# create multithreading
class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def run(self):
        res = recognize_speech_from_mic(self.recognizer, self.microphone)
        if res["error"]:
            print("ERROR: {}".format(res["error"]))
        else:
            words = res["transcription"]
            print(words)
            if "play" in words or "music" in words:
                play_music()
            elif "open" in words or "notepad" in words:
                open_notepad()
            elif "web" in words or "page" in words:
                open_webpage()

        # operations after recognize
        application.recognize_over()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec())
