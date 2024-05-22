# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:20:22 2024

@author: lukas
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog, QSpinBox
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from skyfield.api import load
from datetime import datetime, timedelta

# Load ephemeris data
eph = load('de440s.bsp')
ts = load.timescale()

#PLANETS ABND THEIR BARYCENTERS
planets = {
    'Mercury': 'mercury',
    'Venus': 'venus',
    'Earth': 'earth',
    'Mars': 'mars barycenter',
    'Jupiter': 'jupiter barycenter',
    'Saturn': 'saturn barycenter',
    'Uranus': 'uranus barycenter',
    'Neptune': 'neptune barycenter'
}

#Qt CLASS STUFF

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Planetary Orbit Plotter')
        self.layout = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
        self.date_widgets = []
        for label_text in ['Start Year', 'Start Month', 'Start Day', 'End Year', 'End Month', 'End Day', 'Delta']:
            hbox = QHBoxLayout()
            label = QLabel(label_text)
            hbox.addWidget(label)
            line_edit = QLineEdit()
            hbox.addWidget(line_edit)
            self.layout.addLayout(hbox)
            self.date_widgets.append(line_edit)

        self.resolution_label = QLabel('Resolution:')
        self.layout.addWidget(self.resolution_label)
        self.resolution_spinbox = QSpinBox()
        self.resolution_spinbox.setValue(100)
        self.resolution_spinbox.setMinimum(50)
        self.layout.addWidget(self.resolution_spinbox)

        self.start_markersize_label = QLabel('Start Markersize:')
        self.layout.addWidget(self.start_markersize_label)
        self.start_markersize_spinbox = QSpinBox()
        self.start_markersize_spinbox.setValue(10)
        self.layout.addWidget(self.start_markersize_spinbox)

        self.end_markersize_label = QLabel('End Markersize:')
        self.layout.addWidget(self.end_markersize_label)
        self.end_markersize_spinbox = QSpinBox()
        self.end_markersize_spinbox.setValue(10)
        self.layout.addWidget(self.end_markersize_spinbox)

        self.data_markersize_label = QLabel('Data Markersize:')
        self.layout.addWidget(self.data_markersize_label)
        self.data_markersize_spinbox = QSpinBox()
        self.data_markersize_spinbox.setValue(2)
        self.layout.addWidget(self.data_markersize_spinbox)

        self.planet_button = QPushButton('Select Planets')
        self.planet_button.clicked.connect(self.select_planets)
        self.layout.addWidget(self.planet_button)

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot_orbits)
        self.layout.addWidget(self.plot_button)

        self.save_button = QPushButton('Save Plot')
        self.save_button.clicked.connect(self.save_plot)
        self.layout.addWidget(self.save_button)

        self.start_coordinates_label = QLabel('Start Coordinates:')
        self.layout.addWidget(self.start_coordinates_label)

        self.end_coordinates_label = QLabel('End Coordinates:')
        self.layout.addWidget(self.end_coordinates_label)

        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def select_planets(self):
        selected_planets = []
        for planet in planets.keys():
            if self.ask_yes_no(f"Select {planet}?"):
                selected_planets.append(planet)
        self.selected_planets = selected_planets

    def ask_yes_no(self, question):
        reply = QMessageBox.question(self, 'Message', question,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def plot_orbits(self):
        syear, smonth, sday, eyear, emonth, eday, delta_value = [int(widget.text()) for widget in self.date_widgets]
        delta = timedelta(days=delta_value)

        start = datetime(syear, smonth, sday)
        end = datetime(eyear, emonth, eday)

        dates = []
        current_date = start
        while current_date <= end:
            dates.append(current_date)
            current_date += delta

        times = ts.utc([date.year for date in dates], [date.month for date in dates], [date.day for date in dates])

        coordinates = {planet: ([], []) for planet in self.selected_planets}

        for time in times:
            for planet in self.selected_planets:
                target = eph[planets[planet]]
                position = target.at(time)
                ecliptic_pos = position.ecliptic_position()
                x, y = ecliptic_pos.au[0], ecliptic_pos.au[1]
                coordinates[planet][0].append(x)
                coordinates[planet][1].append(y)

        fig, ax = plt.subplots(figsize=(10, 15), dpi=self.resolution_spinbox.value())
        fig.patch.set_facecolor('black')  # Set the background color of the figure

        for planet in self.selected_planets:
            x, y = coordinates[planet]
            ax.plot(x, y, label=planet, marker='o', markersize=self.data_markersize_spinbox.value(), linestyle='')
            ax.plot(x[0], y[0], 'o', markersize=self.start_markersize_spinbox.value(), color='red', alpha=0.8)  # First data point with faded circle
            ax.plot(x[-1], y[-1], 'o', markersize=self.end_markersize_spinbox.value(), color='green', alpha=0.8)  # Last data point with faded circle

        #SUN SIZE
        ax.plot(0, 0, 'yo', markersize=10 , label='Sun')

        #BACKGROUND COLOR (set tom black)
        ax.set_facecolor('black')
        ax.spines['top'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        #LABEL AND LEGEND SIZES
        ax.set_xlabel('X (AU)', fontsize=20)
        ax.set_ylabel('Y (AU)', fontsize=20)
        ax.set_title('Orbital Plot of Selected Planets (Ecliptic Plane)', fontsize=25)
        ax.legend(fontsize=15)

       
        ax.tick_params(axis='both', which='major', labelsize = 10)
        ax.grid(True)
        ax.axis('equal')
    
       
        start_coordinates_text = f'Start Coordinates:\n'
        end_coordinates_text = f'End Coordinates:\n'
    
        for planet in self.selected_planets:
            start_coordinates_text += f'{planet}: ({coordinates[planet][0][0]:.2f} AU, {coordinates[planet][1][0]:.2f} AU)\n'
            end_coordinates_text += f'{planet}: ({coordinates[planet][0][-1]:.2f} AU, {coordinates[planet][1][-1]:.2f} AU)\n'
    
        self.start_coordinates_label.setText(start_coordinates_text)
        self.end_coordinates_label.setText(end_coordinates_text)
    
        self.canvas.figure = fig
        self.canvas.draw()
    
    def save_plot(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;All Files (*)")
        if filename:
            self.canvas.figure.savefig(filename)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
