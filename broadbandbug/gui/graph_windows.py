#from queue import Queue
from queue import Queue

from PyQt6 import QtCore, QtWidgets
import pyqtgraph as pg

from broadbandbug.library import constants
from broadbandbug.library.classes import Reading
from broadbandbug.library.constants import RecordingMethod


# TODO look into using abc.ABC (abstract class) with this class
class GraphWindow(QtWidgets.QMainWindow):
    REFRESH_INTERVAL_MS = 1000 * 10

    def __init__(self, new_readings: Queue[Reading]):
        super().__init__()

        self.graph = pg.PlotWidget()
        self.setCentralWidget(self.graph)

        self.graph.setBackground("#ffffff")
        styles = {"color": "red", "font-size": "18px"}
        self.graph.setLabel("left", "Megabits/s", **styles)  # Y label
        self.graph.addLegend()
        self.graph.showGrid(x=True, y=True)

        black_pen = pg.mkPen(color=(0, 0, 0), width=3)
        y_axis = self.graph.getAxis('left')
        y_axis.setPen(black_pen)

        self.graph.setAxisItems({'bottom': pg.DateAxisItem()})
        self.graph.setLabel("bottom", "Time", **styles)  # X label
        x_axis = self.graph.getAxis('bottom')
        x_axis.setPen(black_pen)

        # Timer to update new readings
        self.timer = QtCore.QTimer()
        self.timer.setInterval(GraphWindow.REFRESH_INTERVAL_MS)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        # Queue of new readings
        self.new_readings = new_readings

    def update_plot(self):
        print("WARNING: Using abstract base class - use a subclass instead")

    @classmethod
    def run(cls, app, *args):
        window = cls(*args)
        window.show()
        app.exec()

# TODO make graphs not update for values outside of the limits
class MergedGraphWindow(GraphWindow):
    def __init__(self, readings: list[Reading], new_readings: Queue):
        super().__init__(new_readings)
        self.setWindowTitle("Merged Graph")

        # Initialise lists to store all the data
        self.timestamps = []
        self.download_speeds = []
        self.upload_speeds = []

        # Go through each method's results and add the needed data to lists
        for reading in readings:
            # Get data needed for each graph
            self.timestamps.append(reading.timestamp.timestamp())
            self.download_speeds.append(reading.download)
            self.upload_speeds.append(reading.upload)

        # Get a line reference
        self.download_line = self.graph.plot(
            self.timestamps,
            self.download_speeds,
            name="Download",
            pen=pg.mkPen(color=(0, 0, 0), width=3),
            symbol="x",
            symbolSize=15,
            symbolBrush="black",
        )
        self.upload_line = self.graph.plot(
            self.timestamps,
            self.upload_speeds,
            name="Upload",
            pen=pg.mkPen(color=(255, 0, 0), width=2),
            symbol="+",
            symbolSize=15,
            symbolBrush="red",
        )

    def update_plot(self):
        updated = False
        while not self.new_readings.empty():
            reading = self.new_readings.get()
            self.download_speeds.append(reading.download)
            self.upload_speeds.append(reading.upload)
            self.timestamps.append(reading.timestamp.timestamp())
            updated = True

        if updated:
            self.download_line.setData(self.timestamps, self.download_speeds)
            self.upload_line.setData(self.timestamps, self.upload_speeds)

class UnmergedGraphWindow(GraphWindow):
    def __init__(self, readings: dict, new_readings: Queue):
        super().__init__(new_readings)
        self.setWindowTitle("Unmerged Graph")

        # This structure stores
        self.lines = {method: {"down_data": [], "up_data": [], "timestamps": [], "down_line": None, "up_line": None}
                      for method in constants.RecordingMethod}

        for recording_method in readings.keys():
            # Get data needed for each recording method
            timestamps = [reading.timestamp.timestamp() for reading in readings[recording_method]]
            download_speeds = [reading.download for reading in readings[recording_method]]
            upload_speeds = [reading.upload for reading in readings[recording_method]]

            recording_method_data = self.lines[recording_method]
            recording_method_data["down_data"] = download_speeds
            recording_method_data["up_data"] = upload_speeds
            recording_method_data["timestamps"] = timestamps

            # Plot lines

            self.initialise_graphs(recording_method)


    def initialise_graphs(self, recording_method: RecordingMethod):
        recording_method_data = self.lines[recording_method]
        color_scheme = constants.LINE_COLORS[recording_method]

        # Download line
        recording_method_data["down_line"] = self.graph.plot(
            recording_method_data["timestamps"],
            recording_method_data["down_data"],
            name=f"{recording_method.value} download",
            pen=pg.mkPen(color=color_scheme[0], width=3),
            symbol="x",
            symbolSize=15,
            symbolBrush=color_scheme[0],
        )
        recording_method_data["up_line"] = self.graph.plot(
            recording_method_data["timestamps"],
            recording_method_data["up_data"],
            name=f"{recording_method.value} upload",
            pen=pg.mkPen(color=color_scheme[1], width=2),
            symbol="+",
            symbolSize=15,
            symbolBrush=color_scheme[1],
        )

    def update_plot(self):
        updated = []
        while not self.new_readings.empty():
            reading = self.new_readings.get()
            line = self.lines[reading.method]
            line["down_data"].append(reading.download)
            line["up_data"].append(reading.upload)
            line["timestamps"].append(reading.timestamp.timestamp())
            updated.append(reading.method)

        for method in updated:
            line = self.lines[method]
            if line["down_line"] is None:
                self.initialise_graphs(method)
            else:
                line["down_line"].setData(line["timestamps"], line["down_data"])
                line["up_line"].setData(line["timestamps"], line["up_data"])
