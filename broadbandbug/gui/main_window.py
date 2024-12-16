import dearpygui.dearpygui as dpg
import numpy as np
from datetime import datetime, timedelta
import random
from broadbandbug.library.constants import TIME_FORMAT


class MainWindow:
    def __init__(self):
        # Initialize recording state
        self.is_recording = False
        self.recorded_data = []
        self.plot_points = []

        # Initialize DearPyGui
        dpg.create_context()

        # Add font
        with dpg.font_registry():
            normal_size_font = dpg.add_font("Kode-Regular.ttf", 28)
            smaller_font = dpg.add_font("Kode-Regular.ttf", 20)
        dpg.bind_font(normal_size_font)

        with dpg.item_handler_registry():
            dpg.add_item_resize_handler(callback=self.resize_graph)

        # Primary window
        with dpg.window(tag="Window", width=600, height=500):
            with dpg.group(horizontal=False):
                # Tab bar
                with dpg.tab_bar():
                    with dpg.tab(label="Recording"):
                        # Recording controls
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Start recording",
                                           callback=None,
                                           tag="start_btn",
                                           width=200)
                            dpg.add_button(label="Stop recording",
                                           callback=None,
                                           tag="stop_btn",
                                           width=200)

                    with dpg.tab(label="Graph"):
                        # Visualization controls
                        with dpg.group(horizontal=True):
                            with dpg.group(horizontal=False):
                                dpg.add_text("Start date:")
                                dpg.add_input_text(tag="start_date",
                                                   default_value=datetime.now().strftime(TIME_FORMAT),
                                                   width=250)

                            with dpg.group(horizontal=False):
                                dpg.add_text("End date:")
                                dpg.add_input_text(tag="end_date",
                                                   default_value=datetime.now().strftime(TIME_FORMAT),
                                                   width=250)

                        with dpg.group(horizontal=False):
                            # Checkbox and buttons
                            with dpg.group(horizontal=True):
                                dpg.add_checkbox(label="Merge methods", tag="merge_checkbox")

                            with dpg.group(horizontal=True):
                                dpg.add_button(label="Update graph",
                                               callback=self.plot_graph,
                                               width=200)

                        with dpg.group(horizontal=False):
                            # Graph plot area
                            with dpg.plot(label="Recording Graph", height=400, width=500, tag="graph"):
                                dpg.add_plot_legend()
                                formatted_time_format = TIME_FORMAT.replace("%d", "dd").replace("%m", "mm").replace("%Y", "yyyy").replace("%H", "HH").replace("%M", "MM").replace("%S", "SS")
                                dpg.add_plot_axis(dpg.mvXAxis, label=f"Time ({formatted_time_format})")
                                dpg.add_plot_axis(dpg.mvYAxis, label="Broadband (mb/s)", tag="y_axis")

                        # Tabs
                # Tab bar
            # Window
            #dpg.bind_font(default_font)

    def resize_graph(self):
        print("Test")
        height, width = dpg.get_item_rect_size("Window")
        dpg.set_item_width("graph", width)
        dpg.set_item_height("graph", height)

    def start_recording(self):
        self.is_recording = True
        self.recorded_data = []
        dpg.configure_item("start_button", enabled=False)
        dpg.configure_item("stop_button", enabled=True)
        print("Recording started...")

    def stop_recording(self):
        self.is_recording = False
        # Simulating data recording
        self.recorded_data = [
            {"timestamp": datetime.now() + timedelta(seconds=i),
             "value": random.uniform(0, 10)}
            for i in range(100)
        ]
        dpg.configure_item("start_button", enabled=True)
        dpg.configure_item("stop_button", enabled=False)
        print(f"Recording stopped. Recorded {len(self.recorded_data)} data points.")

    def add_random_point(self):
        # Add a new random point to the plot
        new_point = random.uniform(0, 10)
        self.plot_points.append(new_point)

        # Clear existing plot
        dpg.delete_item("graph_plot", children_only=True)

        # Replot with all points
        with dpg.plot(parent="graph_plot"):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Index")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Value", tag="y_axis")

            # Plot the points
            dpg.add_line_series(
                x=range(len(self.plot_points)),
                y=self.plot_points,
                label="Dynamic Points",
                parent=y_axis
            )

        print(f"Added point: {new_point}. Total points: {len(self.plot_points)}")

    def plot_graph(self):
        if not self.recorded_data:
            print("No data to plot.")
            return

        # Clear existing plot
        dpg.delete_item("graph_plot", children_only=True)

        # Reestablish plot axes
        with dpg.plot(parent="graph_plot"):
            dpg.add_plot_legend()
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Index")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Value", tag="y_axis")

            # Extract values
            values = [d['value'] for d in self.recorded_data]

            # Plot the data
            dpg.add_line_series(
                x=range(len(values)),
                y=values,
                label="Recording",
                parent=y_axis
            )

    def run(self):
        # Create viewport
        dpg.create_viewport(title='Recording Application', width=600, height=500)

        # Setup primary window
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Window", True)

        # Start DPG main loop
        dpg.start_dearpygui()
        # This can be used instead of dpg.start_dearpygui()
        """while dpg.is_dearpygui_running():
            # insert here any code you would like to run in the render loop

            # you can manually stop by using stop_dearpygui()
            print("this will run every frame")
            dpg.render_dearpygui_frame()"""

        # Cleanup
        dpg.destroy_context()


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
