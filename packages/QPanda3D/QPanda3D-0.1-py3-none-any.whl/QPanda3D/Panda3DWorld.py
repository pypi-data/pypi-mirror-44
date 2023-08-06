# -*- coding: utf-8-*-
"""
Module : Panda3DWorld
Author : Saifeddine ALOUI
Description :
    Inherit this object to create your custom world
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

__all__ = ["Panda3DWorld"]

class Panda3DWorld(DirectObject):  
    def __init__(self):
        base.disableMouse()
        #self.rotateInterval = LerpHprInterval(self.testModel, 3, Point3(360, 360, 0))
        #self.rotateInterval.loop()
        
        self.screenTexture = Texture()
        self.screenTexture.setMinfilter(Texture.FTLinear)
        self.screenTexture.setFormat(Texture.FRgba32)
        print("Format is", self.screenTexture.getFormat())
        base.win.addRenderTexture(self.screenTexture, GraphicsOutput.RTMCopyRam)

