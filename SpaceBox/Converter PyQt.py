# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:03:01 2024

@author: lukas
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
import re
import json

def convert_coordinates(ra_str, dec_str):
    try:
        ra_hours = float(re.findall(r'\d+', ra_str)[0])
        ra_minutes = float(re.findall(r'\d+', ra_str)[1])
        ra_seconds = float(re.findall(r'\d+', ra_str)[2])
        
        dec_degrees = float(re.findall(r'-?\d+', dec_str)[0])
        dec_minutes = float(re.findall(r'\d+', dec_str)[1])
        dec_seconds = float(re.findall(r'\d+', dec_str)[2])
        
        ra_decimal = (ra_hours + ra_minutes / 60 + ra_seconds / 3600) * 15
        dec_decimal = abs(dec_degrees) + dec_minutes / 60 + dec_seconds / 3600
        
        if dec_str.strip().startswith('-'):
            dec_decimal *= -1
        
        return ra_decimal, dec_decimal
    except Exception as e:
        print(f"Error converting coordinates: {e}")
        return None, None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Coordinates Converter")
        self.setGeometry(100, 100, 400, 400)

        self.coordinates_list = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Enter the name for the coordinates:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.ra_label = QLabel("Enter the Right Ascension (RA) in the format 'hhhrmmms':\nExample: 10h25m30s")
        self.ra_input = QLineEdit()
        layout.addWidget(self.ra_label)
        layout.addWidget(self.ra_input)

        self.dec_label = QLabel("Enter the Declination (Dec) in the format '±dd°mmms':\nExample: +45d30m15s")
        self.dec_input = QLineEdit()
        layout.addWidget(self.dec_label)
        layout.addWidget(self.dec_input)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_coordinates)
        layout.addWidget(self.convert_button)

        self.result_label = QLabel("Converted Coordinates:")
        layout.addWidget(self.result_label)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.save_button = QPushButton("Save Coordinates")
        self.save_button.clicked.connect(self.save_coordinates)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def convert_coordinates(self):
        name = self.name_input.text().strip()
        ra_input = self.ra_input.text().strip()
        dec_input = self.dec_input.text().strip()

        ra_decimal, dec_decimal = convert_coordinates(ra_input, dec_input)

        if ra_decimal is not None and dec_decimal is not None:
            self.result_display.setPlainText(f"RA: {ra_decimal:.6f} degrees\nDec: {dec_decimal:.6f} degrees")
            self.coordinates_list.append({
                'name': name,
                'RA': ra_decimal,
                'Dec': dec_decimal
            })
        else:
            QMessageBox.warning(self, "Conversion Error", "Invalid input format. Please follow the provided examples.")

    def save_coordinates(self):
        if not self.coordinates_list:
            QMessageBox.warning(self, "No Coordinates", "There are no coordinates to save.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Coordinates", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.coordinates_list, file, indent=4)
                QMessageBox.information(self, "Success", "Coordinates saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"An error occurred while saving: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
