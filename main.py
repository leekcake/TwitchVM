import sys
import typing

import m3u8
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QUrl, QIODevice
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMainWindow, QGridLayout
from streamlink import Streamlink
from streamlink_cli.main import streamlink


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        ## MENU
        exitAction = QAction('Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        mainMenu = menubar.addMenu('TwitchVM')
        mainMenu.addAction(exitAction)

        ## TEST - Player
        self.videoWidget = QVideoWidget()
        self.setCentralWidget(self.videoWidget)
        #self.videoWidget.show()

        self.player = QMediaPlayer(self.videoWidget, QMediaPlayer.LowLatency)
        self.player.error.connect(self.erroralert)

        session = Streamlink()
        session.set_plugin_option('twitch', 'low-latency', True)
        streams = session.streams("http://twitch.tv/{0}".format('lilac_unicorn_'))
        stream = streams['best']

        #self.player.setMedia(None)
        self.player.setMedia(QMediaContent(QUrl(stream.url)))
        self.player.setVideoOutput(self.videoWidget)
        self.player.play()

        self.setWindowTitle('TwitchVM')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1280, 720)
        self.show()

        print(self.player.error())

    def erroralert(self, *args):
        print(args)
        print(self.player.errorString())
        print(self.player.error())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
