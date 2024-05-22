# -*- coding: utf-8 -*-
"""
Created on Wed May 22 12:18:10 2024

@author: lukas
"""


import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from astroquery.skyview import SkyView
import astropy.units as u
import matplotlib.pyplot as plt

class Locate:
    def __init__(self):
        self.ra = None
        self.dec = None
        self.fov = 0.1
        self.Astroimages = {}
        self.selected_surveys = []

    def get_location(self):
        self.ra = float(input("Enter the Right Ascension (RA) value in degrees or hours: "))
        self.dec = float(input("Enter the Declination (Dec) value in degrees: "))
        self.fov = float(input("Enter your imagery field of view (fov) in degrees: "))

    def zoom_in(self):
        self.fov /= 2

    def zoom_out(self):
        self.fov *= 2

    def get_images(self):
        if self.ra is None or self.dec is None:
            print("Coordinates not set. Please enter RA and Dec values!")
            return None
        
        aspect_ratio = 1.5
        height = self.fov / aspect_ratio

        try:
            paths = SkyView.get_images(position=f'{self.ra}, {self.dec}', survey=self.selected_surveys, 
                                       width=self.fov * u.deg, height=height * u.deg)
            return paths
        except Exception as e:
            print(f"Failed to retrieve images: {e}")
            return None

    def save_images_lib(self, paths):
        if paths is None:
            return
        
        for i, path in enumerate(paths):
            image_data = path[0].data
            self.Astroimages[f'image_{i}'] = image_data
        
        print(f"Saved {len(paths)} images to the Astroimages dictionary.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.locate = Locate()
        self.predefined_surveys =  [
#ALL bands GOOD/HDF/CDF

            'GOODS: Chandra ACIS HB',
            'GOODS: Chandra ACIS FB',
            'GOODS: Chandra ACIS SB',
            'GOODS: VLT VIMOS U',
            'GOODS: VLT VIMOS R',
            'GOODS: HST ACS B',
            'GOODS: HST ACS V',
            'GOODS: HST ACS I',
            'GOODS: HST ACS Z',
            'Hawaii HDF U',
            'Hawaii HDF B',
            'Hawaii HDF V0201',
            'Hawaii HDF V0401',
            'Hawaii HDF R',
            'Hawaii HDF I',
            'Hawaii HDF z',
            'Hawaii HDF HK',
            'GOODS: HST NICMOS',
            'GOODS: VLT ISAAC J',
            'GOODS: VLT ISAAC H',
            'GOODS: VLT ISAAC Ks',
            'HUDF: VLT ISAAC Ks',
            'GOODS: Spitzer IRAC 3.6',
            'GOODS: Spitzer IRAC 4.5',
            'GOODS: Spitzer IRAC 5.8',
            'GOODS: Spitzer IRAC 8.0',
            'GOODS: Spitzer MIPS 24',
            'GOODS: Herschel 100',
            'GOODS: Herschel 160',
            'GOODS: Herschel 250',
            'GOODS: Herschel 350',
            'GOODS: Herschel 500',
            'CDFS: LESS',
            'GOODS: VLA North'

#Allbands: HiPs
        
            'UltraVista-H',
            'UltraVista-J',
            'UltraVista-Ks',
            'UltraVista-NB118',
            'UltraVista-Y',
            'CFHTLS-W-u',
            'CFHTLS-W-g',
            'CFHTLS-W-r',
            'CFHTLS-W-i',
            'CFHTLS-W-z',
            'CFHTLS-D-u',
            'CFHTLS-D-g',
            'CFHTLS-D-r',
            'CFHTLS-D-i',
            'CFHTLS-D-z'

#GammaRay
            
            'Fermi 5',
            'Fermi 4',
            'Fermi 3',
            'Fermi 2',
            'Fermi 1',
            'EGRET (3D)',
            'EGRET <100 MeV',
            'EGRET >100 MeV',
            'COMPTEL'
    
#HardX-Ray
            
            'INT GAL 17-35 Flux',
            'INT GAL 17-60 Flux',
            'INT GAL 35-80 Flux',
            'INTEGRAL/SPI GC',
            'GRANAT/SIGMA',
            'RXTE Allsky 3-8keV Flux',
            'RXTE Allsky 3-20keV Flux',
            'RXTE Allsky 8-20keV Flux'
            
#IR 2MASS, AKARI, IRAS
            
            '2MASS-J', '2MASS-H', '2MASS-K', 'AKARI N60', 'AKARI WIDE-S', 'AKARI WIDE-L', 'AKARI N160','IRIS  12',
                        'IRIS  25',
                        'IRIS  60',
                        'IRIS 100',
                        'SFD100m',
                        'SFD Dust Map',
                        'IRAS  12 micron',
                        'IRAS  25 micron',
                        'IRAS  60 micron',
                        'IRAS 100 micron'
                        
#IR Planck
            'Planck 857 I',
            'Planck 545 I',
            'Planck 353 I',
            'Planck 353 Q',
            'Planck 353 U',
            'Planck 353 PI',
            'Planck 353 PA',
            'Planck 353 PI/I',
            'Planck 217 I',
            'Planck 217 Q',
            'Planck 217 U',
            'Planck 217 PI',
            'Planck 217 PA',
            'Planck 217 PI/I',
            'Planck 143 I',
            'Planck 143 Q',
            'Planck 143 U',
            'Planck 143 PI',
            'Planck 143 PA',
            'Planck 143 PI/I',
            'Planck 100 I',
            'Planck 100 Q',
            'Planck 100 U',
            'Planck 100 PI',
            'Planck 100 PA',
            'Planck 100 PI/I',
            'Planck 070 I',
            'Planck 070 Q',
            'Planck 070 U',
            'Planck 070 PI',
            'Planck 070 PA',
            'Planck 070 PI/I',
            'Planck 044 I',
            'Planck 044 Q',
            'Planck 044 U',
            'Planck 044 PI',
            'Planck 044 PA',
            'Planck 044 PI/I',
            'Planck 030 I',
            'Planck 030 Q',
            'Planck 030 U',
            'Planck 030 PI',
            'Planck 030 PA',
            'Planck 030 PI/I'
            
#IR UKIDSS
            
            'UKIDSS-Y',
            'UKIDSS-J',
            'UKIDSS-H',
            'UKIDSS-K',
            'UKIDSS-1-0S1'
            
            
#IR WISE

            'WISE 3.4', 'WISE 4.6', 'WISE 12', 'WISE 22'
            
#IR WMAP AND COBE

            'WMAP ILC',
            'WMAP Ka',
            'WMAP K',
            'WMAP Q',
            'WMAP V',
            'WMAP W',
            'COBE DIRBE/AAM',
            'COBE DIRBE/ZSMA'

#Optical DSS 

            'DSS',
            'DSS',
            'DSS1 Blue',
            'DSS1 Red',
            'DSS2 Red',
            'DSS2 Blue',
            'DSS2 IR'

#Optical SDSS

            'SDSSg',
            'SDSSi',
            'SDSSr',
            'SDSSu',
            'SDSSz',
            'SDSSdr7g',
            'SDSSdr7i',
            'SDSSdr7r',
            'SDSSdr7u',
            'SDSSdr7z'

#Other Optical

            'TESS',
            'Mellinger Red',
            'Mellinger Green',
            'Mellinger Blue',
            'H-Alpha Comp',
            'SHASSA H',
            'SHASSA CC',
            'SHASSA C',
            'SHASSA Sm'

#ROSAT diffuse

            'RASS Background 1',
            'RASS Background 2',
            'RASS Background 3',
            'RASS Background 4',
            'RASS Background 5',
            'RASS Background 6',
            'RASS Background 7'
            
#ROSAT w/sources

            'RASS-Cnt Soft',
            'RASS-Cnt Hard',
            'RASS-Cnt Broad',
            'PSPC 2.0 Deg-Int',
            'PSPC 1.0 Deg-Int',
            'PSPC 0.6 Deg-Int',
            'HRI'

#Radio GHz
        
            'CO',
            'GB6 (4850MHz)',
            'VLA FIRST (1.4 GHz)',
            'NVSS',
            'Stripe82VLA',
            '1420MHz (Bonn)',
            'HI4PI',
            'EBHIS',
            'nH'
            
#Radio GLEAM

            'GLEAM 72-103 MHz',
            'GLEAM 103-134 MHz',
            'GLEAM 139-170 MHz',
            'GLEAM 170-231 MHz'

#Radio MHz 
            
            'SUMSS 843 MHz',
            '0408MHz',
            'WENSS',
            'TGSS ADR1',
            'VLSSr',
            '0035MHz',
            '0022MHz'
            
            
#SOFT XRAY 

            'SwiftXRTCnt',
            'SwiftXRTExp',
            'SwiftXRTInt',
            'HEAO 1 A-2'
            
#SWIFTUVOT

            'UVOT WHITE Intensity',
            'UVOT V Intensity',
            'UVOT B Intensity',
            'UVOT U Intensity',
            'UVOT UVW1 Intensity',
            'UVOT UVM2 Intensity',
            'UVOT UVW2 Intensity'

#UV
        
            'GALEX Near UV',
            'GALEX Far UV',
            'ROSAT WFC F1',
            'ROSAT WFC F2',
            'EUVE 83 A',
            'EUVE 171 A',
            'EUVE 405 A',
            'EUVE 555 A'
            
#XRay SwiftBAT

            'BAT SNR 14-195',
            'BAT SNR 14-20',
            'BAT SNR 20-24',
            'BAT SNR 24-35',
            'BAT SNR 35-50',
            'BAT SNR 50-75',
            'BAT SNR 75-100',
            'BAT SNR 100-150',
            'BAT SNR 150-195'

                    ]
        
        
    

        self.setWindowTitle("Astronomy Image Locator")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.ra_label = QLabel("Right Ascension (RA):")
        self.ra_input = QLineEdit()
        layout.addWidget(self.ra_label)
        layout.addWidget(self.ra_input)

        self.dec_label = QLabel("Declination (Dec):")
        self.dec_input = QLineEdit()
        layout.addWidget(self.dec_label)
        layout.addWidget(self.dec_input)

        self.fov_label = QLabel("Field of View (FOV):")
        self.fov_input = QLineEdit()
        layout.addWidget(self.fov_label)
        layout.addWidget(self.fov_input)

        self.surveys_label = QLabel("Available Surveys:")
        self.surveys_combo = QComboBox()
        self.surveys_combo.addItems(self.predefined_surveys)
        layout.addWidget(self.surveys_label)
        layout.addWidget(self.surveys_combo)

        self.get_images_button = QPushButton("Get Images")
        self.get_images_button.clicked.connect(self.get_images)
        layout.addWidget(self.get_images_button)

        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        layout.addWidget(self.zoom_out_button)

        self.image_display = QLabel("Images will be displayed here.")
        layout.addWidget(self.image_display)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_images(self):
        try:
            ra = float(self.ra_input.text())
            dec = float(self.dec_input.text())
            fov = float(self.fov_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for RA, Dec, and FOV.")
            return

        self.locate.ra = ra
        self.locate.dec = dec
        self.locate.fov = fov

        selected_survey = self.surveys_combo.currentText()
        self.locate.selected_surveys = [selected_survey]

        paths = self.locate.get_images()
        if paths:
            self.locate.save_images_lib(paths)
            self.display_images(paths)
        else:
            QMessageBox.warning(self, "Image Error", "No images were returned. Please check your inputs and try again.")

    def display_images(self, paths):
        fig, axes = plt.subplots(1, len(paths), figsize=(15, 5))
        if len(paths) == 1:
            axes = [axes] 
        for ax, path in zip(axes, paths):
            ax.imshow(path[0].data, cmap='gray')  
            ax.set_title(path[0].header['SURVEY'])
            ax.axis('off')

        plt.tight_layout()
        plt.show()


    def zoom_in(self):
        self.locate.zoom_in()
        self.fov_input.setText(str(self.locate.fov))

    def zoom_out(self):
        self.locate.zoom_out()
        self.fov_input.setText(str(self.locate.fov))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
