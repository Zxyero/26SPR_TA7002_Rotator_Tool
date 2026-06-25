import unreal
import random
import sys


from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout, 
    QLabel,
    QDoubleSpinBox, 
    QCheckBox, 
    QPushButton,
    QFrame,
    QHBoxLayout
    
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QKeySequence
WINDOW_NAME = "RandomRotationTool"
WINDOW = None

#bug, when deselect mesh and selects new mesh - still affects old unselected mesh == fixed -> put eas into def for rotate apply




class RotationTool(QWidget):
    def __init__(self):
        super().__init__()
        self.original_rotations = {} #stores original rotation of selected actor for later
        self.setObjectName(WINDOW_NAME)
        self.setWindowTitle("Random Rotation Tool")
        self.setMinimumSize(QSize(300,512))

        ## widget UI design
        layout = QVBoxLayout(self)
        self.myframe = QFrame()
        self.myframe.setFrameShape(QFrame.StyledPanel)
        self.myframe.setFrameShadow(QFrame.Plain)
        self.myframe.setLineWidth(3)
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
        self.use_roll = QCheckBox("Randomize Yaw")

        self.use_yaw = QCheckBox("Randomize Pitch")
        
        self.use_pitch = QCheckBox("Randomize Roll")
        
        

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


### btn_E = button enter

        btn_E = QPushButton("Apply Rotation Change to Selected")
        btn_E.setShortcut(QKeySequence("Ctrl+E"))
        btn_E.clicked.connect(self.apply_rotation)
        layout.addWidget(btn_E)

### btn_C = button clear rotation

        btn_C = QPushButton("Clear All Random Rotations")
        btn_C.setShortcut(QKeySequence("Ctrl+C"))
        btn_C.clicked.connect(self.clear_rotation)
        layout.addWidget(btn_C)


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
                background-color: #242424;
                color: #0f0f0f;
                font-family: Roboto;
                font-size: 14px;
            }
            QLabel {
                color: #f5f5f5;
                font-family: Roboto;
                font-size: 14px;
            }
            QCheckBox {
                color: #f5f5f5;
                spacing: 8px;
                padding: 4px;
            }      
            QDoubleSpinBox {
                background-color: #010103;
                color: #f5f5f5;
                border: 1px solid #444;
                padding: 10px;
                min-height: 22px;
            }
            QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                padding: 4px;
            }
            QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                padding: 4px;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #f5f5f5;
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


         ##get actor original rotation , allows for returning the actor to it's original rotational value set in unreal before randomisation
        for actor in selected_actors:
            if actor not in self.original_rotations:
                self.original_rotations[actor] = actor.get_actor_rotation()

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
    
    def clear_rotation(self):

        #rot = rotation. stored from selected actors and listed. clear = return to original value.

        for actor, rot in list(self.original_rotations.items()):
            if actor:
                actor.set_actor_rotation(rot, False)
        self.original_rotations.clear()


def launch():
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    for win in (QApplication.allWindows()):
        if win.objectName() == WINDOW_NAME:
            win.close()
            win.deleteLater()

    global WINDOW
    WINDOW = RotationTool()
    WINDOW.show()
    #------------------------> sits on UE instead of closing
    unreal.parent_external_window_to_slate(
    WINDOW.winId(),
    unreal.SlateParentWindowSearchMethod.MAIN_WINDOW
    )

    return WINDOW



launch()

##chane launch to ->
"""


-> sync spin box with a slider (so it acts like UE5 entry box; type in , spin and slider)
if QApplication.instance():
    # Id any current instances of tool and destroy
    for win in (QApplication.allWindows()):
        if 'RandomRotationTool' in win.objectName(): # update this name to match name below
            win.destroy() ### DIDN'T WORK BECAUSE OREDER IS WRONG AND CRASHED UE5
else:
    app = QApplication(sys.argv)


window = QWidget()
window.setObjectName("Tool Window")
window.setWindowTitle("My Tool")
window.show()
unreal.parent_external_window_to_slate(window.winId())


## also setup slider
 # slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-360)
        self.slider.setMaximum(360)
        self.slider.setSliderPosition(10)
        self.slider.valueChanged.connect(self.sliderChanged)

### and add Qmainwindow parent to unreal 
ADD ERROR MESSAGE ALSO
"""