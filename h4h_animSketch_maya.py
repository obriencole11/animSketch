from .vendor import Qt
from .vendor.Qt import QtWidgets, QtCore
from .vendor.Qt.QtCore import Slot
import maya.OpenMayaUI as omUI
import h4h_animSketch_ui as ui
import h4h_animSketch
import pymel.core as pmc
import logging

window = None
tool = None

@Slot(float, float, bool, bool, float, bool, bool)
def createTool(sensitivity, timeScale, singleAxis, simplify, tolerance, inverted, vertical):

    ready = None

    attributes = pmc.channelBox('mainChannelBox', selectedMainAttributes=True, q=True)

    if attributes is None and singleAxis:
        ready = 'No Channels Selected'

    selection = pmc.selected()

    if len(selection) < 1:
        ready = 'No Target Selected'


    if ready is None:
        selectionName = selection[0].shortName()

        if singleAxis:
            attributeNames = [selectionName + '.' + attribute for attribute in attributes]
        else:
            attributeNames = [selectionName+'.tx',selectionName+'.ty',selectionName+'.tz']

        tool.create(attributeNames, sensitivity=sensitivity, timeScale=timeScale, singleAxis=singleAxis,
                    simplify=simplify, verticalControl=vertical, tolerance=tolerance, inverted=inverted)
    else:
        logging.warning(ready)


def load():

    global window
    global tool

    # If there is no window created, create a new one
    # Otherwise just show the current one
    if window is None:

        app = QtWidgets.QApplication.instance()
        mayaWindow = {o.objectName(): o for o in app.topLevelWidgets()}["MayaWindow"]


        ptr = omUI.MQtUtil.mainWindow()
        mayaWindow = Qt.QtCompat.wrapInstance(long(ptr), QtWidgets.QWidget)

        window = ui.animSketchWindow(mayaWindow, QtCore.Qt.Tool)

        tool = h4h_animSketch.animSketchTool()
        window.onRecord.connect(createTool)

    # Show the window
    window.show()