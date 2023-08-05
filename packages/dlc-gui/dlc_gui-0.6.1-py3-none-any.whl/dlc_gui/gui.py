"""
This module handles all the GUI aspects of dlc_gui.

This module creates a main window containing the main widget containing subset widgets.
"""

# TODO add feature to specify project_path

import sys
from typing import Union
import webbrowser

from PySide2.QtCore import QEvent, QRect, QRectF, Qt
from PySide2.QtGui import QBrush, QColor, QCursor, QKeySequence, QPen, QPixmap
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QDesktopWidget,
    QFileDialog,
    QGraphicsEllipseItem,
    QGraphicsScene,
    QGraphicsView,
    QGridLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QShortcut,
    QSlider,
    QSplitter,
    QToolTip,
    QVBoxLayout,
    QWidget,
)


import dlc_gui.data
import dlc_gui.util


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super(GraphicsScene, self).__init__(parent)

    def load_image(self, image: str) -> None:
        # Load frame png into scene
        self.frame_image = QPixmap()
        self.frame_image.load(image)
        self.addPixmap(self.frame_image)


class GraphicsView(QGraphicsView):
    def __init__(self, parent):
        super(GraphicsView, self).__init__(parent)

        self.scene = GraphicsScene(self)

        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), aspectRadioMode=Qt.KeepAspectRatio)

        self.viewport().setCursor(Qt.CrossCursor)

        # keep track of the current scale value to prevent zooming too far out
        self.current_scale = 1.0

    def zoom(self, pos: tuple, scale: float, anchor: str = "NoAnchor") -> None:
        if anchor == "NoAnchor":
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.setResizeAnchor(QGraphicsView.NoAnchor)

        old_pos = self.mapToScene(*pos)

        # Prevent zooming out beyond 0.3 or in beyond 33
        if (self.current_scale > 0.3 or scale > 1) and (
            self.current_scale < 33 or scale < 1
        ):
            self.scale(scale, scale)
            self.current_scale *= scale

        new_pos = self.mapToScene(*pos)

        translate_delta = (new_pos - old_pos).toTuple()
        self.translate(*translate_delta)

    # Scroll wheel to zoom in and out
    def wheelEvent(self, event):
        scale_factor = 1.25
        if event.delta() > 0:
            self.zoom(event.pos().toTuple(), scale_factor)
        else:
            self.zoom(event.pos().toTuple(), 1 / scale_factor)

    # Toggle on dragging when middle mouse is pressed
    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MiddleButton
            or QApplication.keyboardModifiers() == Qt.ShiftModifier
        ):
            self.__og_pos = event.pos()
            self.viewport().setCursor(Qt.ClosedHandCursor)
        else:
            return super(GraphicsView, self).mousePressEvent(event)

    # TODO find a legit way to engage the ScrollHandDrag mode
    # rather than simply using it to change the cursor look

    # Translate scene using scrollbars while middle button is held
    def mouseMoveEvent(self, event):
        if (
            event.button() == Qt.MiddleButton
            or QApplication.keyboardModifiers() == Qt.ShiftModifier
        ):
            offset = self.__og_pos - event.pos()
            self.__og_pos = event.pos()

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + offset.y()
            )
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + offset.x()
            )
        else:
            super(GraphicsView, self).mouseMoveEvent(event)

    # Toggle off dragging when middle mouse is pressed
    def mouseReleaseEvent(self, event):
        if (
            event.button() == Qt.MiddleButton
            or QApplication.keyboardModifiers() == Qt.ShiftModifier
        ):
            self.viewport().setCursor(Qt.CrossCursor)
        else:
            return super(GraphicsView, self).mouseReleaseEvent(event)


class MainWidget(QWidget):
    """
    Create the main user interface and controls, connected to DataModel
    """

    def __init__(self, parent, config_path):
        super(MainWidget, self).__init__(parent)

        # Create the main widgets
        self.graphics_view = GraphicsView(self)
        self.bodyparts_view = QListWidget()
        self.dot_label_lines_state = QCheckBox("Show dot labels")
        self.dot_size_slider = QSlider(Qt.Horizontal)
        self.dot_size_label = QLabel(parent=self.dot_size_slider)
        self.frames_view = QListWidget()

        # Setup the data_model, get config values, and setup widgets based on data_model
        self.config_path = config_path
        data_model = dlc_gui.data.DataModel(self.config_path)
        self.init_from_data_model(data_model)

        # Setup the checkbox for dot labels visibility
        self.dot_label_lines_state.stateChanged.connect(lambda x: self.update_scene())

        # Set up the dot_size_slider
        dot_size_from_config = self.data_model.config_dict["dotsize"]
        self.dot_size_slider.setMinimum(2)
        self.dot_size_slider.setMaximum(100)
        self.dot_size_slider.setValue(dot_size_from_config)
        self.dot_size_slider.setTickPosition(QSlider.TicksBothSides)
        self.dot_size_slider.setTickInterval(10)
        self.dot_size_label.setText(
            "Label dot size: {} (from config.yaml)".format(dot_size_from_config)
        )
        self.dot_size_slider.valueChanged.connect(
            lambda: self.dot_size_label.setText(
                "Label dot size: {}".format(self.dot_size_slider.value())
            )
        )

        self.dot_size_slider.valueChanged.connect(lambda: self.update_scene())

        # Add a widget to add a layout containing the bodyparts and the slider
        labeling_widget = QWidget()
        labeling_layout = QVBoxLayout()
        labeling_layout.addWidget(self.bodyparts_view)
        labeling_layout.addWidget(self.dot_label_lines_state)
        labeling_layout.addWidget(self.dot_size_label)
        labeling_layout.addWidget(self.dot_size_slider)
        labeling_widget.setLayout(labeling_layout)

        # Set the main layout of Widget
        main_layout = QGridLayout()
        splitter = QSplitter()

        splitter.addWidget(self.frames_view)
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(labeling_widget)

        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Set up events
        self.frames_view.currentItemChanged.connect(lambda x: self.update_scene())

        self.graphics_view.scene.installEventFilter(self)

        shortcut_next_bodypart = QShortcut(QKeySequence("d"), self)
        shortcut_prev_bodypart = QShortcut(QKeySequence("a"), self)
        shortcut_next_frame = QShortcut(QKeySequence("s"), self)
        shortcut_prev_frame = QShortcut(QKeySequence("w"), self)
        # setattr is used as an assignment function, because lambdas cannot assign
        # prior to python 3.8
        shortcut_next_bodypart.activated.connect(lambda: self.switch_bodypart("next"))
        shortcut_prev_bodypart.activated.connect(lambda: self.switch_bodypart("prev"))
        shortcut_next_frame.activated.connect(
            lambda: setattr(self, "current_frame_row", self.current_frame_row + 1)
        )
        shortcut_prev_frame.activated.connect(
            lambda: setattr(self, "current_frame_row", self.current_frame_row - 1)
        )

        shortcut_toggle_dot_label_lines_state = QShortcut(QKeySequence("f"), self)
        shortcut_toggle_dot_label_lines_state.activated.connect(
            lambda: self.dot_label_lines_state.toggle()
        )

        self.save_file_dialog = QFileDialog()
        self.save_file_dialog.setFileMode(QFileDialog.AnyFile)
        self.save_file_dialog.setAcceptMode(QFileDialog.AcceptSave)

    def init_from_data_model_from_file(self, dataframe_file) -> None:
        data_model = dlc_gui.data.DataModel(self.config_path)
        exit_code = data_model.init_from_file(dataframe_file)
        if exit_code == 1:
            self.send_status("Invalid file.", 5)
        elif exit_code == 2 or exit_code == 3:
            self.send_status(
                "Error: {} is not structured correctly.".format(dataframe_file), 5
            )
        elif exit_code == 0:
            self.init_from_data_model(data_model)

    def init_from_data_model_from_dir(self, dir: str) -> None:
        data_model = dlc_gui.data.DataModel(self.config_path)
        exit_code = data_model.init_from_dir(dir)
        if exit_code == 1:
            self.send_status("Error: No frames (*.png) found in {}".format(dir), 5)
        elif exit_code == 2:
            self.send_status(
                'Error: {} is not within the project path "{}"'.format(
                    dir, self.data_model.config_dict["project_path"]
                ),
                5,
            )
        elif exit_code == 0:
            self.init_from_data_model(data_model)

    def init_from_data_model(self, data_model) -> None:

        self.data_model = data_model

        self.bodyparts = self.data_model.bodyparts
        self.project_path = self.data_model.project_path

        # Populate the frames and bodyparts lists
        if self.data_model.frames_dict:
            self.frames_dict = self.data_model.frames_dict

            self.frames_view.clear()
            for frame in self.frames_dict.keys():
                self.frames_view.addItem(frame)

        self.bodyparts_view.clear()
        for bodypart in self.bodyparts:
            self.bodyparts_view.addItem(bodypart)

        # Convert tuples to QColors

        self.data_model.colors = [
            QColor.fromHsvF(*color) for color in self.data_model.colors
        ]
        self.data_model.colors_opposite = [
            QColor.fromHsvF(*color) for color in self.data_model.colors_opposite
        ]
        self.data_model.colors_opaque = [
            QColor.fromHsvF(*color) for color in self.data_model.colors_opaque
        ]

        # Set initial selections for both listwidgets, load the first frame,
        # and add color icons
        frames_view_items = self.frames_view.findItems("*", Qt.MatchWildcard)
        if frames_view_items:
            self.frames_view.setCurrentItem(frames_view_items[0])
            self.graphics_view.scene.load_image(str(list(self.frames_dict.values())[0]))

        self.bodyparts_view_items = self.bodyparts_view.findItems("*", Qt.MatchWildcard)
        if self.bodyparts_view_items:
            self.bodyparts_view.setCurrentItem(self.bodyparts_view_items[0])
            for item, color in zip(
                self.bodyparts_view_items, self.data_model.colors_opaque
            ):
                pixmap = QPixmap(100, 100)
                pixmap.fill(color)
                item.setIcon(pixmap)

        self.update_scene()

    def eventFilter(self, obj, event):
        """
        Implement left and right mouse clicking functionalities
        """
        # Check if the click is within the QGraphicsView
        if (
            obj is self.graphics_view.scene
            and event.type() == QEvent.Type.GraphicsSceneMousePress
        ):

            scene_pos = event.scenePos()
            coords = (scene_pos.x(), scene_pos.y())

            frame = self.current_frame_text
            bodypart = self.current_bodypart_text

            if frame and bodypart:
                if event.buttons() == Qt.LeftButton:
                    self.data_model.add_coords_to_dataframe(frame, bodypart, coords)
                elif event.buttons() == Qt.RightButton:
                    self.data_model.add_coords_to_dataframe(
                        frame, bodypart, (None, None)
                    )

            self.update_scene()

        return super(MainWidget, self).eventFilter(obj, event)

    def switch_bodypart(self, prev_or_next: str) -> None:
        if prev_or_next == "prev":
            setattr(self, "current_bodypart_row", self.current_bodypart_row - 1)
        elif prev_or_next == "next":
            setattr(self, "current_bodypart_row", self.current_bodypart_row + 1)

        tool_tip = QToolTip()
        tool_tip.showText(
            QCursor.pos(), self.current_bodypart_text, self.graphics_view, QRect(), 300
        )

    @property
    def current_bodypart_row(self) -> int:
        return self.bodyparts_view.currentRow()

    @current_bodypart_row.setter
    def current_bodypart_row(self, row) -> None:
        self.bodyparts_view.setCurrentRow(row)

    @property
    def current_frame_row(self) -> int:
        return self.frames_view.currentRow()

    @current_frame_row.setter
    def current_frame_row(self, row) -> None:
        self.frames_view.setCurrentRow(row)

    @property
    def current_bodypart_text(self) -> Union[str, None]:
        try:
            return self.bodyparts_view.currentItem().text()
        except AttributeError:
            return None

    @property
    def current_frame_text(self) -> Union[str, None]:
        try:
            return self.frames_view.currentItem().text()
        except AttributeError:
            return None

    def send_status(self, msg, timeout) -> None:
        self.parent().status_bar.showMessage(msg, timeout * 1000)

    def save_as_pkl(self) -> None:
        self.save_file_dialog.selectFile(str(self.data_model.save_path_pkl))
        self.save_file_dialog.setNameFilter("(*.pkl *.pickle)")
        self.save_file_dialog.setDefaultSuffix(".pkl")
        if self.save_file_dialog.exec():
            save_path = self.save_file_dialog.selectedFiles()[0]
            self.data_model.save_as_pkl(save_path)

    def save_as_hdf(self) -> None:
        self.save_file_dialog.selectFile(str(self.data_model.save_path_hdf))
        self.save_file_dialog.setNameFilter("(*.h5 *.hdf)")
        self.save_file_dialog.setDefaultSuffix(".h5")
        if self.save_file_dialog.exec():
            save_path = self.save_file_dialog.selectedFiles()[0]
            self.data_model.save_as_hdf(save_path)

    # Updating scene is in MainWidget and not GraphicsScene because it needs to know
    # current frame and current bodypart, both properties of MainWidget
    def update_scene(self) -> None:
        def add_dots_to_scene(
            coords: tuple,
            size: float,
            brush_color: QColor,
            pen_color: QColor,
            tooltip: str,
        ) -> None:
            # Adds dots to the scene
            x, y = coords

            dot_rect = QRectF(x - size / 2, y - size / 2, size, size)
            dot_brush = QBrush(Qt.SolidPattern)
            dot_brush.setColor(brush_color)
            dot_pen = QPen(dot_brush, size / 40)
            dot_pen.setColor(pen_color)

            dot_ellipse = QGraphicsEllipseItem(dot_rect)
            dot_ellipse.setPen(dot_pen)
            dot_ellipse.setBrush(dot_brush)

            dot_ellipse.setToolTip(tooltip)

            self.graphics_view.scene.addItem(dot_ellipse)

        def add_dot_labels_to_scene(
            text: str, coords: tuple, size: float, fg_color: QColor, bg_color: QColor
        ) -> None:

            x, y = coords

            x_offset = size * 2
            y_offset = size * 2

            label = self.graphics_view.scene.addText(text)
            label.setPos(
                x + label.boundingRect().width() / 2 + x_offset,
                y - label.boundingRect().height() / 2 - y_offset,
            )
            label.setHtml(
                """<div style='background:rgba({1}, {2}, {3}, {4});'>
                    <span style='color:rgb({5}, {6}, {7});
                    font-size:{8}px;font-weight:bold;'>
                        {0}
                    </span>
                </div>""".format(
                    text,
                    bg_color.red(),
                    bg_color.green(),
                    bg_color.blue(),
                    bg_color.alphaF(),
                    fg_color.red(),
                    fg_color.green(),
                    fg_color.blue(),
                    size,
                )
            )
            label_line_pen = QPen()
            label_line_pen.setWidth(size / 3)
            label_line_pen.setCapStyle(Qt.RoundCap)
            label_line_pen.setStyle(Qt.DotLine)
            label_line_pen.setColor(bg_color)

            self.graphics_view.scene.addLine(
                x,
                y,
                label.pos().x() + label.boundingRect().width() / 2,
                label.pos().y() + label.boundingRect().height() / 2,
                pen=label_line_pen,
            )

            label.setZValue(10)

        self.graphics_view.scene.clear()

        frame = self.current_frame_text

        if frame:
            self.graphics_view.scene.load_image(str(self.frames_dict[frame]))

            dot_size = self.dot_size_slider.value()

            if self.data_model.data_frame is not None:
                for bodypart, brush_color, pen_color in zip(
                    self.bodyparts,
                    self.data_model.colors,
                    self.data_model.colors_opposite,
                ):
                    coords = self.data_model.get_coords_from_dataframe(frame, bodypart)
                    if all(coord is not None for coord in coords):
                        add_dots_to_scene(
                            coords, dot_size, brush_color, pen_color, bodypart
                        )
                        if self.dot_label_lines_state.isChecked():
                            add_dot_labels_to_scene(
                                bodypart, coords, dot_size, pen_color, brush_color
                            )


class MainWindow(QMainWindow):
    """
    Define the main window and its menubar and statusbar
    """

    def __init__(self, config=None, relative_size=0.8):
        super(MainWindow, self).__init__()

        self.setWindowTitle("DeepLabCut Labeling GUI")

        # Statusbar
        # must be defined before children for children to access it
        self.status_bar = self.statusBar()

        self.open_file_dialog = QFileDialog()

        if config is None:
            config = self.open_file("(*.yml *.yaml)", "config.yaml")
            if config == "" or config is None:
                print("No config.yaml file provided, exiting...")
                sys.exit()

        self.main_widget = MainWidget(self, config)

        self.open_file_dialog.setDirectory(
            str(self.main_widget.data_model.labeled_data_path)
        )

        # Menubar
        self.open_frames_dir = QAction("Open directory of frames", self)
        self.open_frames_dir.setShortcut(QKeySequence("Ctrl+O"))
        self.open_frames_dir.triggered.connect(
            lambda x: self.main_widget.init_from_data_model_from_dir(self.open_dir())
        )

        self.open_dataframe_file = QAction("Open *.h5 or *.pkl file", self)
        self.open_dataframe_file.setShortcut(QKeySequence("Ctrl+F"))
        self.open_dataframe_file.triggered.connect(
            lambda x: self.main_widget.init_from_data_model_from_file(
                self.open_file(
                    "(*.h5 *.hdf *.pkl *.pickle)",
                    str(self.main_widget.data_model.save_path_hdf),
                )
            )
        )

        save_as_hdf = QAction("Save as .h5", self)
        save_as_hdf.setShortcut(QKeySequence("Ctrl+S"))
        save_as_hdf.triggered.connect(lambda x: self.main_widget.save_as_hdf())

        save_as_pkl = QAction("Save as .pkl", self)
        save_as_pkl.triggered.connect(lambda x: self.main_widget.save_as_pkl())

        help_url = "https://dlc-gui.readthedocs.io/en/latest/README.html#using-the-gui"
        open_help = QAction("Help", self)
        open_help.setShortcut(QKeySequence("Ctrl+H"))
        open_help.triggered.connect(lambda x: webbrowser.open(help_url))

        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction(self.open_frames_dir)
        self.file_menu.addAction(self.open_dataframe_file)
        self.file_menu.addAction(save_as_hdf)
        self.file_menu.addAction(save_as_pkl)

        self.help_menu = self.menu_bar.addMenu("Help")
        self.help_menu.addAction(open_help)

        # Window dimensions
        self.resize(QDesktopWidget().availableGeometry(self).size() * relative_size)

        self.setCentralWidget(self.main_widget)

    #
    ## TODO fix bug of open_file_dialog object remembering
    ## selectedFiles and starting directory
    #

    def open_file(self, name_filter: str, select_file: str = None) -> Union[str, None]:
        if select_file is not None:
            self.open_file_dialog.selectFile(select_file)
        self.open_file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.open_file_dialog.setNameFilter(name_filter)
        if self.open_file_dialog.exec():
            file = self.open_file_dialog.selectedFiles()[0]
            return file
        return None

    def open_dir(self) -> Union[str, None]:
        self.open_file_dialog.setFileMode(QFileDialog.Directory)
        if self.open_file_dialog.exec():
            dir = self.open_file_dialog.selectedFiles()[0]
            return dir
        return None


def show(config: Union[None, str] = None, relative_size: float = 0.8) -> None:
    """
    Show the GUI.

    Parameters
    ----------
    config : str or None, optional (default None)
        The config.yaml file to use.
        May be None to use the GUI to pick the config.yaml file.
    relative_size : float, optional (default 0.8)
        What portion of the display to set the main window's size to.

    """

    app = QApplication(sys.argv)
    window = MainWindow(config, relative_size)
    window.show()
    sys.exit(app.exec_())
