from .vendor import Qt
from .vendor.Qt import QtWidgets, QtGui
from .vendor.Qt.QtCore import Signal, Slot

class animSketchWindow(QtWidgets.QMainWindow):
    '''
    The Main Window class for the Tool. This determines UI look and internal events.
    '''


    onRecord = Signal(float, float, bool, bool, float, bool, bool)

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        #### General Window Setup

        self.setWindowTitle('Hero4Hire Animation Sketch')

        self.mainWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)


        #### Settings Group

        settingsGroup = QtWidgets.QGroupBox('Settings', self.mainWidget)
        self.mainLayout.addWidget(settingsGroup)

        settingsLayout = QtWidgets.QFormLayout()
        settingsGroup.setLayout(settingsLayout)

        # Sensitivity Setting
        self.sensitivitySetting = QtWidgets.QDoubleSpinBox(settingsGroup)
        settingsLayout.addRow('Sensitivity', self.sensitivitySetting)
        self.sensitivitySetting.setValue(1.0)
        self.sensitivitySetting.setMinimum(0.01)
        self.sensitivitySetting.setSingleStep(0.1)

        # TimeScale Setting
        self.timeScaleSetting = QtWidgets.QDoubleSpinBox(settingsGroup)
        settingsLayout.addRow('Time Scale', self.timeScaleSetting)
        self.timeScaleSetting.setValue(1.0)
        self.timeScaleSetting.setMinimum(0.01)
        self.timeScaleSetting.setSingleStep(0.1)

        # Simplify Setting
        self.simplifySetting = QtWidgets.QCheckBox(settingsGroup)
        settingsLayout.addRow('Simplify Curves', self.simplifySetting)
        self.simplifySetting.setChecked(True)

        # Tolerance Setting
        self.toleranceSetting = QtWidgets.QDoubleSpinBox(settingsGroup)
        settingsLayout.addRow('Simplify Tolerance', self.toleranceSetting)
        self.toleranceSetting.setValue(0.05)
        self.toleranceSetting.setMinimum(0.01)
        self.toleranceSetting.setSingleStep(0.01)
        self.toleranceSetting.setDecimals(2)

        # Direction Setting
        self.directionSetting = QtWidgets.QComboBox(settingsGroup)
        self.directionSetting.addItems(['Vertical', 'Horizontal'])
        settingsLayout.addRow('Control Direction', self.directionSetting)

        # Invert Setting
        self.invertSetting = QtWidgets.QCheckBox(settingsGroup)
        settingsLayout.addRow('Invert', self.invertSetting)
        self.invertSetting.setChecked(False)

        #### Record Group

        recordGroup = QtWidgets.QGroupBox('Record', self.mainWidget)
        self.mainLayout.addWidget(recordGroup)
        recordLayout = QtWidgets.QHBoxLayout()
        recordGroup.setLayout(recordLayout)

        # Record Position Button
        self.recordPositionButton = QtWidgets.QPushButton('Record Position', self.mainWidget)
        icon = QtGui.QIcon(':/move_M.png')
        self.recordPositionButton.setIcon(icon)
        recordLayout.addWidget(self.recordPositionButton)
        self.recordPositionButton.clicked.connect(self.recordPositionClicked)

        # Record Channels Button
        self.recordChannelButton = QtWidgets.QPushButton('Record Channels', self.mainWidget)
        icon = QtGui.QIcon(':/channelBox.png')
        self.recordChannelButton.setIcon(icon)
        recordLayout.addWidget(self.recordChannelButton)
        self.recordChannelButton.clicked.connect(self.recordChannelClicked)

    def recordChannelClicked(self):

        self.onRecord.emit(self.sensitivitySetting.value(), self.timeScaleSetting.value(), True,
                                  self.simplifySetting.checkState(), self.toleranceSetting.value(),
                                    self.invertSetting.checkState(),
                                  True if self.directionSetting.currentIndex()==0 else False)

    def recordPositionClicked(self):

        self.onRecord.emit(1.0, self.timeScaleSetting.value(), False, self.simplifySetting.checkState(),
                                   self.toleranceSetting.value(),
                                    self.invertSetting.checkState(),
                                   True if self.directionSetting.currentIndex()==0 else False)