import unreal
import random
import sys, os
#from systems_ue_r import QApplication, QWidget, QLabel, QDoubleSpinBox, QCheckBox, QPushButton, QStyle, QSize, QColor,QPalette, QVBoxLayout, EAS, QMainWindow, selected_actors
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout, 
    QLabel,
    QDoubleSpinBox, 
    QCheckBox, 
    QPushButton,
    QStyle,
    QFrame
    
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QPalette, QColor



WINDOW_NAME = "RandomRotationTool"
WINDOW = None

#todo:
#bug, when deselect mesh and selects new mesh - still affects old unselected mesh == fixed -> put eas into def for rotate apply

class RotationTool(QWidget):
    def __init__(self):
        super(RotationTool, self).__init__()

        self.setObjectName(WINDOW_NAME)
        self.setWindowTitle("Random Rotation Tool")
        self.setMinimumSize(QSize(300,512))
        layout = QVBoxLayout(self)
        self.tool_style()




        self.base_pitch = self.make_spin(-360, 360, 0)
        self.base_yaw = self.make_spin(-360, 360, 0)
        self.base_roll = self.make_spin(-360, 360, 0)
        self.min_pitch = self.make_spin(-360, 360, -10)
        self.max_pitch = self.make_spin(-360, 360, 10)
        self.min_yaw = self.make_spin(-360, 360, -10)
        self.max_yaw = self.make_spin(-360, 360, 10)
        self.min_roll = self.make_spin(-360, 360, -10)
        self.max_roll = self.make_spin(-360, 360, 10)

#####            apply change button
        self.use_roll = QCheckBox("Randomize yaw")

        self.use_yaw = QCheckBox("Randomize pitch")
        
        self.use_pitch = QCheckBox("Randomize roll")
        
        

        fields = [
           
            ("Min Roll Offset", self.min_pitch),
            ("Max Roll Offset", self.max_pitch),
            ("Min Pitch Offset", self.min_yaw),
            ("Max Pitch Offset", self.max_yaw),
            ("Min Yaw Offset", self.min_roll),
            ("Max Yaw Offset", self.max_roll),
        ]

        for label, widget in fields:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        layout.addWidget(self.use_pitch)
        layout.addWidget(self.use_yaw)
        layout.addWidget(self.use_roll)

### btn_A = button apply

        btn_A = QPushButton("Apply Rotation Change to Selected")
        btn_A.clicked.connect(self.apply_rotation)
        layout.addWidget(btn_A)



    def make_spin(self, mn, mx, val):
        snxv = QDoubleSpinBox()
        snxv.setRange(mn, mx)
        snxv.setValue(val)
        snxv.setDecimals(2)
        snxv.setSuffix("°")
        return snxv
    #(snxv = "self, min max value")


#### match Slate unreal styles, colour corordination fpr reg green blue xyz axis.
    def tool_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #262626;
                color: #67abeb;
                font-family: Roboto;
                font-size: 14px;
            }
            QLabel {
                color: #67abeb;
                font-family: Roboto;
                font-size: 14px;
            }
            QCheckBox {
                spacing: 8px;
                padding: 3px;
            }
            QDoubleSpinBox {
                background-color: #010103;
                color: #67abeb;
                border: 1px solid #444;
                padding: 4px;
                min-height: 22px;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #67abeb;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #010103;
            }
        """)

    def apply_rotation(self):
        EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        selected_actors = EAS.get_selected_level_actors()        
        base_pitch = self.base_pitch.value()
        base_yaw = self.base_yaw.value()
        base_roll = self.base_roll.value()

        ##use 'sorted' so dont have to list all min max values again and they auto to large and small values

        min_pitch, max_pitch = sorted((self.min_pitch.value(), self.max_pitch.value()))
        min_yaw, max_yaw = sorted((self.min_yaw.value(), self.max_yaw.value()))
        min_roll, max_roll = sorted((self.min_roll.value(), self.max_roll.value()))

        for actor in selected_actors:
            pitch = base_pitch
            yaw = base_yaw
            roll = base_roll

            if self.use_pitch.isChecked():
                pitch = random.uniform(min_pitch, max_pitch)
            elif self.use_yaw.isChecked() or self.use_roll.isChecked():
                pass

            if self.use_yaw.isChecked():
                yaw = random.uniform(min_yaw, max_yaw)

            if self.use_roll.isChecked():
                roll = random.uniform(min_roll, max_roll)


            actor.set_actor_rotation(unreal.Rotator(pitch, yaw, roll), False)



def launch():
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)
    
    for widget in app.allWindows():
        if widget.objectName() == WINDOW_NAME:
            widget.close()

    return app

WINDOW = RotationTool()
WINDOW.show()

#------------------------> sits on UE instead of closing
unreal.parent_external_window_to_slate(
    WINDOW.winId(),
    unreal.SlateParentWindowSearchMethod.MAIN_WINDOW
)

launch()