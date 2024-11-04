import base64
import json
import math
from enum import Enum, auto
from typing import List, Optional, Tuple

import colour
import numpy as np
import scipy.interpolate
from bell.avr.mqtt.payloads import (
    AvrPcmFireLaserPayload,
    AvrPcmSetLaserOffPayload,
    AvrPcmSetLaserOnPayload,
    AvrPcmSetServoAbsPayload,
    AvrPcmSetServoPctPayload,
)
from bell.avr.utils.timing import rate_limit
from PySide6 import QtCore, QtGui, QtWidgets

from ..lib.calc import constrain, map_value
from ..lib.color import wrap_text
from ..lib.config import config
from ..lib.widgets import DoubleLineEdit
from .base import BaseTabWidget


class Direction(Enum):
    Left = auto()
    Right = auto()
    Up = auto()
    Down = auto()


class ThermalView(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        # canvas size
        self.width_ = 300
        self.height_ = self.width_

        # pixels within canvas
        self.pixels_x = 30
        self.pixels_y = self.pixels_x

        self.pixel_width = self.width_ / self.pixels_x
        self.pixel_height = self.height_ / self.pixels_y

        # low range of the sensor (this will be blue on the screen)
        self.MINTEMP = 20.0

        # high range of the sensor (this will be red on the screen)
        self.MAXTEMP = 32.0

        # last lowest temp from camera
        self.last_lowest_temp = 999.0

        # how many color values we can have
        self.COLORDEPTH = 1024

        # how many pixels the camera is
        self.camera_x = 8
        self.camera_y = self.camera_x
        self.camera_total = self.camera_x * self.camera_y

        # create list of x/y points
        self.points = [(math.floor(ix / self.camera_x), (ix % self.camera_y)) for ix in range(self.camera_total)]
        # i'm not fully sure what this does
        self.grid_x, self.grid_y = np.mgrid[
            0 : self.camera_x - 1 : self.camera_total / 2j,
            0 : self.camera_y - 1 : self.camera_total / 2j,
        ]

        # create avaiable colors
        self.colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in list(colour.Color("indigo").range_to(colour.Color("red"), self.COLORDEPTH))]

        # create canvas
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.canvas = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.canvas)
        self.view.setGeometry(0, 0, self.width_, self.height_)

        layout.addWidget(self.view)

        # need a bit of padding for the edges of the canvas
        self.setFixedSize(self.width_ + 50, self.height_ + 50)

    def set_temp_range(self, mintemp: float, maxtemp: float) -> None:
        self.MINTEMP = mintemp
        self.MAXTEMP = maxtemp

    def set_calibrted_temp_range(self) -> None:
        self.MINTEMP = self.last_lowest_temp + 0.0
        self.MAXTEMP = self.last_lowest_temp + 15.0

    def update_canvas(self, pixels: List[int]) -> None:
        float_pixels = [map_value(p, self.MINTEMP, self.MAXTEMP, 0, self.COLORDEPTH - 1) for p in pixels]

        # Rotate 90° to orient for mounting correctly
        float_pixels_matrix = np.reshape(float_pixels, (self.camera_x, self.camera_y))
        float_pixels_matrix = np.rot90(float_pixels_matrix, 1)
        rotated_float_pixels = float_pixels_matrix.flatten()

        bicubic = scipy.interpolate.griddata(
            self.points,
            rotated_float_pixels,
            (self.grid_x, self.grid_y),
            method="cubic",
        )

        pen = QtGui.QPen(QtCore.Qt.PenStyle.NoPen)
        self.canvas.clear()

        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                brush = QtGui.QBrush(QtGui.QColor(*self.colors[int(constrain(pixel, 0, self.COLORDEPTH - 1))]))
                self.canvas.addRect(
                    self.pixel_width * jx,
                    self.pixel_height * ix,
                    self.pixel_width,
                    self.pixel_height,
                    pen,
                    brush,
                )


class ApriltagView(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        # canvas size
        self.width_ = 320
        self.height_ = 180

        # pixels within canvas
        self.pixels_x = 320
        self.pixels_y = 180

        self.pixel_width = self.width_ / self.pixels_x
        self.pixel_height = self.height_ / self.pixels_y

        # low range of the camera (idk anymore)
        self.MINTEMP = 0.0

        # high range of the camera (idk anymore)
        self.MAXTEMP = 256.0
        """
        # last lowest temp from camera
        self.last_lowest_temp = 999.0
        """
        # how many color values we can have
        self.COLORDEPTH = 1024

        # how many pixels the camera is
        self.camera_x = 128
        self.camera_y = 72
        self.camera_total = self.camera_x * self.camera_y

        # create list of x/y points
        self.points = [(math.floor(ix / self.camera_x), (ix % self.camera_y)) for ix in range(self.camera_total)]
        # i'm not fully sure what this does
        self.grid_x, self.grid_y = np.mgrid[
            0 : self.camera_x - 1 : self.camera_total / 2j,
            0 : self.camera_y - 1 : self.camera_total / 2j,
        ]

        # create avaiable colors
        self.colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in list(colour.Color("indigo").range_to(colour.Color("red"), self.COLORDEPTH))]

        # create canvas
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.canvas = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.canvas)
        self.view.setGeometry(0, 0, self.width_, self.height_)

        layout.addWidget(self.view)

        # need a bit of padding for the edges of the canvas
        self.setFixedSize(self.width_ + 50, self.height_ + 50)

    """
    def set_temp_range(self, mintemp: float, maxtemp: float) -> None:
        self.MINTEMP = mintemp
        self.MAXTEMP = maxtemp

    def set_calibrted_temp_range(self) -> None:
        self.MINTEMP = self.last_lowest_temp + 0.0
        self.MAXTEMP = self.last_lowest_temp + 15.0
    """

    def update_canvas(self, pixels: List[int]) -> None:
        float_pixels = [map_value(p, self.MINTEMP, self.MAXTEMP, 0, self.COLORDEPTH - 1) for p in pixels]

        # Rotate 90° to orient for mounting correctly
        float_pixels_matrix = np.reshape(float_pixels, (self.camera_x, self.camera_y))
        float_pixels_matrix = np.rot90(float_pixels_matrix, 1)
        rotated_float_pixels = float_pixels_matrix.flatten()

        bicubic = scipy.interpolate.griddata(
            self.points,
            rotated_float_pixels,
            (self.grid_x, self.grid_y),
            method="cubic",
        )

        pen = QtGui.QPen(QtCore.Qt.PenStyle.NoPen)
        self.canvas.clear()

        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                brush = QtGui.QBrush(QtGui.QColor(*self.colors[int(constrain(pixel, 0, self.COLORDEPTH - 1))]))
                self.canvas.addRect(
                    self.pixel_width * jx,
                    self.pixel_height * ix,
                    self.pixel_width,
                    self.pixel_height,
                    pen,
                    brush,
                )


class JoystickWidget(BaseTabWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.setFixedSize(300, 300)

        self.moving_offset = QtCore.QPointF(0, 0)

        self.grab_center = False
        self.__max_distance = 100

        self.current_y = 0
        self.current_x = 0

        self.servoxmin = 10
        self.servoymin = 10
        self.servoxmax = 99
        self.servoymax = 99

        self.gimbal_num = 1

        self.gimbal_servos = {1: (2, 3), 2: (4, 8), 3: (9, 10)}

        # servo declarations
        self.SERVO_ABS_MAX = 2200
        self.SERVO_ABS_MIN = 700

    def _center(self) -> QtCore.QPointF:
        """
        Return the center of the widget.
        """
        return QtCore.QPointF(self.width() / 2, self.height() / 2)

    def move_gimbal(self, x_servo_percent: int, y_servo_percent: int) -> None:
        # Currently unused, possibly depreciated
        self.send_message(
            "avr/pcm/set_servo_pct",
            AvrPcmSetServoPctPayload(servo=self.gimbal_servos[self.gimbal_num][0], percent=x_servo_percent),
        )
        self.send_message(
            "avr/pcm/set_servo_pct",
            AvrPcmSetServoPctPayload(servo=self.gimbal_servos[self.gimbal_num][1], percent=y_servo_percent),
        )

    def move_gimbal_absolute(self, x_servo_abs: int, y_servo_abs: int) -> None:
        if self.gimbal_num == 0:  # Potential Idea: Add a system where any gimbal number outside of the given gimbal numbers would control all gimbals (i.e gimbal number == 4 would control all)
            for i in range(len(self.gimbal_servos)):
                self.send_message(
                    "avr/pcm/set_servo_abs",
                    AvrPcmSetServoAbsPayload(servo=self.gimbal_servos[i + 1][0], absolute=x_servo_abs),
                )
                self.send_message(
                    "avr/pcm/set_servo_abs",
                    AvrPcmSetServoAbsPayload(servo=self.gimbal_servos[i + 1][1], absolute=y_servo_abs),
                )
        else:
            self.send_message(
                "avr/pcm/set_servo_abs",
                AvrPcmSetServoAbsPayload(servo=self.gimbal_servos[self.gimbal_num][0], absolute=x_servo_abs),
            )
            self.send_message(
                "avr/pcm/set_servo_abs",
                AvrPcmSetServoAbsPayload(servo=self.gimbal_servos[self.gimbal_num][1], absolute=y_servo_abs),
            )

    def center_gimbal(self) -> None:
        self.move_gimbal_absolute(1450, 1450)
        self.moving_offset = self._center()
        self.update()

    def set_gimbal(self, num):
        self.gimbal_num = num
        print(f"Set gimbal {num} as active")

    def update_servos(self) -> None:
        """
        Update the servos on joystick movement.
        """
        # y_reversed = 100 - self.current_y

        # x_servo_percent = round(map_value(self.current_x, 0, 100, 10, 99))
        # y_servo_percent = round(map_value(y_reversed, 0, 100, 10, 99))
        #
        # if x_servo_percent < self.servoxmin:
        #     return
        # if y_servo_percent < self.servoymin:
        #     return
        # if x_servo_percent > self.servoxmax:
        #     return
        # if y_servo_percent > self.servoymax:
        #     return
        #
        # self.move_gimbal(x_servo_percent, y_servo_percent)

        y_reversed = 225 - self.current_y
        # side to side  270 left, 360 right

        x_servo_abs = round(map_value(self.current_x + 25, 25, 225, self.SERVO_ABS_MIN, self.SERVO_ABS_MAX))
        y_servo_abs = round(map_value(y_reversed, 25, 225, self.SERVO_ABS_MIN, self.SERVO_ABS_MAX))

        self.move_gimbal_absolute(x_servo_abs, y_servo_abs)

    def _center_ellipse(self) -> QtCore.QRectF:
        # sourcery skip: assign-if-exp
        if self.grab_center:
            center = self.moving_offset
        else:
            center = self._center()

        return QtCore.QRectF(-20, -20, 40, 40).translated(center)

    def _bound_joystick(self, point: QtCore.QPoint) -> QtCore.QPoint:
        """
        If the joystick is leaving the widget, bound it to the edge of the widget.
        """
        if point.x() > (self._center().x() + self.__max_distance):
            point.setX(int(self._center().x() + self.__max_distance))
        elif point.x() < (self._center().x() - self.__max_distance):
            point.setX(int(self._center().x() - self.__max_distance))

        if point.y() > (self._center().y() + self.__max_distance):
            point.setY(int(self._center().y() + self.__max_distance))
        elif point.y() < (self._center().y() - self.__max_distance):
            point.setY(int(self._center().y() - self.__max_distance))
        return point

    def joystick_direction(self) -> Optional[Tuple[Direction, float]]:
        """
        Retrieve the direction the joystick is moving
        """
        if not self.grab_center:
            return None

        norm_vector = QtCore.QLineF(self._center(), self.moving_offset)
        current_distance = norm_vector.length()
        angle = norm_vector.angle()

        distance = min(current_distance / self.__max_distance, 1.0)

        if 45 <= angle < 135:
            return (Direction.Up, distance)
        elif 135 <= angle < 225:
            return (Direction.Left, distance)
        elif 225 <= angle < 315:
            return (Direction.Down, distance)

        return (Direction.Right, distance)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        bounds = QtCore.QRectF(
            -self.__max_distance,
            -self.__max_distance,
            self.__max_distance * 2,
            self.__max_distance * 2,
        ).translated(self._center())

        # painter.drawEllipse(bounds)
        painter.drawRect(bounds)
        painter.setBrush(QtCore.Qt.GlobalColor.black)

        painter.drawEllipse(self._center_ellipse())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> QtGui.QMouseEvent:
        """
        On a mouse press, check if we've clicked on the center of the joystick.
        """
        self.grab_center = self._center_ellipse().contains(event.pos())
        return event

    def mouseReleaseEvent(self, event: QtCore.QEvent) -> None:
        # self.grab_center = False
        # self.moving_offset = QtCore.QPointF(0, 0)
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.grab_center:
            self.moving_offset = self._bound_joystick(event.pos())
            self.update()

        moving_offset_y = self.moving_offset.y()
        if not config.joystick_inverted:
            moving_offset_y = self.height() - moving_offset_y

        # print(self.joystick_direction())
        self.current_x = self.moving_offset.x() - self._center().x() + self.__max_distance
        self.current_y = moving_offset_y - self._center().y() + self.__max_distance

        rate_limit(self.update_servos, frequency=50)


class ThermalViewControlWidget(BaseTabWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.setWindowTitle("Thermal View/Control")

    def build(self) -> None:
        """
        Build the GUI layout
        """
        layout = QtWidgets.QHBoxLayout(self)
        layout_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.setLayout(layout)

        # viewer
        viewer_groupbox = QtWidgets.QGroupBox("Viewer")
        viewer_layout = QtWidgets.QVBoxLayout()
        viewer_groupbox.setLayout(viewer_layout)

        # Thermal camera feed
        self.thermal_viewer = ThermalView(self)
        viewer_layout.addWidget(self.thermal_viewer)

        # set temp range (?)

        # lay out the host label and line edit
        temp_range_layout = QtWidgets.QFormLayout()

        self.temp_min_line_edit = DoubleLineEdit()
        temp_range_layout.addRow(QtWidgets.QLabel("Min Temp:"), self.temp_min_line_edit)
        self.temp_min_line_edit.setText(str(self.thermal_viewer.MINTEMP))

        self.temp_max_line_edit = DoubleLineEdit()
        temp_range_layout.addRow(QtWidgets.QLabel("Max Temp:"), self.temp_max_line_edit)
        self.temp_max_line_edit.setText(str(self.thermal_viewer.MAXTEMP))

        set_temp_range_button = QtWidgets.QPushButton("Set Temp Range")
        temp_range_layout.addWidget(set_temp_range_button)

        set_temp_range_calibrate_button = QtWidgets.QPushButton("Auto Calibrate Temp Range")
        temp_range_layout.addWidget(set_temp_range_calibrate_button)

        viewer_layout.addLayout(temp_range_layout)

        set_temp_range_button.clicked.connect(  # type: ignore
            lambda: self.thermal_viewer.set_temp_range(
                float(self.temp_min_line_edit.text()),
                float(self.temp_max_line_edit.text()),
            )
        )

        set_temp_range_calibrate_button.clicked.connect(lambda: self.calibrate_temp())  # type: ignore

        # Apriltag camera feed
        self.apriltag_viewer = ApriltagView(self)
        viewer_layout.addWidget(self.apriltag_viewer)

        layout_splitter.addWidget(viewer_groupbox)

        # joystick
        joystick_groupbox = QtWidgets.QGroupBox("Joystick")
        joystick_layout = QtWidgets.QVBoxLayout()
        joystick_groupbox.setLayout(joystick_layout)

        sub_joystick_layout = QtWidgets.QHBoxLayout()
        joystick_layout.addLayout(sub_joystick_layout)

        self.joystick = JoystickWidget(self)
        sub_joystick_layout.addWidget(self.joystick)

        gimbal_picker_layout = QtWidgets.QFormLayout()
        gimbal_picker = DoubleLineEdit()
        gimbal_picker_layout.addRow(QtWidgets.QLabel("Gimbal:"), gimbal_picker)
        gimbal_picker.setText(str(1))

        set_gimbal_button = QtWidgets.QPushButton("Set Gimbal")
        gimbal_picker_layout.addWidget(set_gimbal_button)

        center_gimbal_button = QtWidgets.QPushButton("Center Gimbal")
        gimbal_picker_layout.addWidget(center_gimbal_button)

        joystick_layout.addLayout(gimbal_picker_layout)

        laser_toggle_layout = QtWidgets.QHBoxLayout()

        laser_on_button = QtWidgets.QPushButton("Laser On")
        laser_toggle_layout.addWidget(laser_on_button)

        laser_off_button = QtWidgets.QPushButton("Laser Off")
        laser_toggle_layout.addWidget(laser_off_button)

        fire_laser_button = QtWidgets.QPushButton("Fire Laser (Pulse)")
        joystick_layout.addWidget(fire_laser_button)

        self.laser_toggle_label = QtWidgets.QLabel()
        self.laser_toggle_label.setText(wrap_text("Laser Off", "red"))
        self.laser_toggle_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.laser_toggle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        laser_toggle_layout.addWidget(self.laser_toggle_label)

        joystick_layout.addLayout(laser_toggle_layout)

        # https://i.imgur.com/yvgNiFE.jpg
        self.joystick_inverted_checkbox = QtWidgets.QCheckBox("Invert Joystick")
        joystick_layout.addWidget(self.joystick_inverted_checkbox)
        self.joystick_inverted_checkbox.setChecked(config.joystick_inverted)

        layout_splitter.addWidget(joystick_groupbox)
        layout.addWidget(layout_splitter)

        # connect signals
        self.joystick.emit_message.connect(self.emit_message.emit)

        set_gimbal_button.clicked.connect(lambda: self.joystick.set_gimbal(int(gimbal_picker.text())))

        center_gimbal_button.clicked.connect(lambda: self.joystick.center_gimbal())

        fire_laser_button.clicked.connect(lambda: self.send_message("avr/pcm/fire_laser", AvrPcmFireLaserPayload()))  # type: ignore

        laser_on_button.clicked.connect(lambda: self.set_laser(True))  # type: ignore
        laser_off_button.clicked.connect(lambda: self.set_laser(False))  # type: ignore

        self.joystick_inverted_checkbox.clicked.connect(self.inverted_checkbox_clicked)  # type: ignore

        # don't allow us to shrink below size hint
        self.setMinimumSize(self.sizeHint())

    def inverted_checkbox_clicked(self) -> None:
        """
        Callback when joystick inverted checkbox is clicked
        """
        config.joystick_inverted = self.joystick_inverted_checkbox.isChecked()

    def set_laser(self, state: bool) -> None:
        if state:
            topic = "avr/pcm/set_laser_on"
            payload = AvrPcmSetLaserOnPayload()
            text = "Laser On"
            color = "green"
        else:
            topic = "avr/pcm/set_laser_off"
            payload = AvrPcmSetLaserOffPayload()
            text = "Laser Off"
            color = "red"

        self.send_message(topic, payload)
        self.laser_toggle_label.setText(wrap_text(text, color))

    def calibrate_temp(self) -> None:
        self.thermal_viewer.set_calibrted_temp_range()
        self.temp_min_line_edit.setText(str(self.thermal_viewer.MINTEMP))
        self.temp_max_line_edit.setText(str(self.thermal_viewer.MAXTEMP))

    def process_message(self, topic: str, payload: str) -> None:
        """
        Process an incoming message and update the appropriate component
        """
        # discard topics we don't recognize
        if topic == "avr/thermal/reading":
            # process payload data into a Python object
            data = json.loads(payload)["data"]

            # decode the payload
            base64Decoded = data.encode("utf-8")
            asbytes = base64.b64decode(base64Decoded)
            pixel_ints = list(bytearray(asbytes))

            # find lowest temp
            lowest = min(pixel_ints)
            self.thermal_viewer.last_lowest_temp = lowest

            # update the canvas
            # pixel_ints = data
            self.thermal_viewer.update_canvas(pixel_ints)
        elif topic == "avr/apriltags/camfeed":
            # process payload data into a Python object
            data = json.loads(payload)["img"]

            # decode the payload
            base64Decoded = data.encode("utf-8")
            asbytes = base64.b64decode(base64Decoded)
            pixel_ints = list(bytearray(asbytes))
            """ Don't think I need this since we aren't using temps
            # find lowest temp
            lowest = min(pixel_ints)
            self.apriltag_viewer.last_lowest_temp = lowest
            """
            # update the canvas
            # pixel_ints = data
            self.apriltag_viewer.update_canvas(pixel_ints)

    def clear(self) -> None:
        self.thermal_viewer.canvas.clear()
