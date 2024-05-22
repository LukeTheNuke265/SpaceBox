# -*- coding: utf-8 -*-
"""
Created on Wed May 22 13:32:53 2024

@author: lukas
"""


import subprocess

def run_converter():
    subprocess.run(["python", "Converter PyQt.py"])

def run_plotter():
    subprocess.run(["python", "PythonImageRetrieveQt.py"])

def run_Orbits():
    subprocess.run(["python", "Orbits in Qt Final.py"])
    
if __name__ == "__main__":
    run_converter()
    run_plotter()
    run_Orbits()


