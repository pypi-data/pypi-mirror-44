# -*- coding: utf-8-*-
"""
Module : QPanda3DWidget
Author : Saifeddine ALOUI
Description :
    This is the QWidget to be inserted in your standard PyQt5 application.
    It takes a Panda3DWorld object at init time.
    You should first create the Panda3DWorkd object before creating this widget.
"""
from panda3d.core import loadPrcFileData
loadPrcFileData("", "window-type offscreen") # Set Panda to draw its main window in an offscreen buffer

from direct.showbase.ShowBase import ShowBase  
#import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# PyQt imports
import sys
# Panda imports
from pandac.PandaModules import GraphicsOutput,  Texture,  StringStream,  PNMImage
from direct.interval.LerpInterval import LerpHprInterval
from pandac.PandaModules import Point3
# Set up Panda environment
import direct.directbase.DirectStart
from struct import *

__all__ = ["QPanda3DWidget"]

class QPanda3DWidget(QWidget):
    """
    An interactive panda3D QWidget
    """
    
    def __init__(self, panda3DWorld,  parent=None, w_geometry = (0, 0, 800, 600)):
        QWidget.__init__(self,  parent)
        #set fixed geometry        
        self.setGeometry(w_geometry[0], w_geometry[1], w_geometry[2], w_geometry[3])
        self.panda3DWorld = panda3DWorld
        # Setup a timer in Qt that runs taskMgr.step() to simulate Panda's own main loop
        pandaTimer = QTimer(self)
        pandaTimer.timeout.connect(taskMgr.step)
        pandaTimer.start(0)
        
        # Setup another timer that redraws this widget in a specific FPS
        redrawTimer = QTimer(self)
        redrawTimer.timeout.connect(self.update)
        redrawTimer.start(1000/60)
        
        self.paintSurface = QPainter()
        self.rotate = QTransform()
        self.rotate.rotate(180)
        
        self.out_image = QImage()

    def resizeEvent(self, evt):
        # TODO implement to allow resizing
        pass

    def minimumSizeHint(self):
        return QSize(400,300)

    def showEvent(self, event):
        self.desktopBg = QApplication.primaryScreen().grabWindow(QApplication.desktop ().winId(), \
                self.geometry().x(),self.geometry().y(), self.rect().width(), self.rect().height())
    
    # Use the paint event to pull the contents of the panda texture to the widget
    def paintEvent(self,  event):
        if self.panda3DWorld.screenTexture.mightHaveRamImage():
            self.panda3DWorld.screenTexture.setFormat(Texture.FRgba32)
            #print "Should draw yes?"
            data = self.panda3DWorld.screenTexture.getRamImage().getData()
            img = QImage(data, self.panda3DWorld.screenTexture.getXSize(), self.panda3DWorld.screenTexture.getYSize(), QImage.Format_ARGB32).mirrored()
            self.paintSurface.begin(self)
            self.paintSurface.drawPixmap(0, 0, self.desktopBg)
            self.paintSurface.drawImage(0, 0, img)
            self.paintSurface.end()
            pixmap = QPixmap.fromImage(img)
            self.setMask(pixmap.mask())
