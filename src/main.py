import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                              QComboBox, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import time
from MI import MI
from skimage import io
plt.style.use('dark_background') 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Image Reconstruction")
        self.setMinimumSize(1000, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        control_layout = QHBoxLayout()
        
        param_layout = QVBoxLayout()
        self.load_button = QPushButton("Load Image")
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Max Angle (e.g., 180)")
        
        self.method_combo = QComboBox()
        self.method_combo.addItems(["ramp", "shepp-logan", "cosine", "hamming", "hann"])
        self.method_combo.addItems(["SART"])
        
        self.calculate_button = QPushButton("Calculate")
        self.animation_button = QPushButton("Show Animation")
        
        param_layout.addWidget(QLabel("Image Operations:"))
        param_layout.addWidget(self.load_button)
        param_layout.addWidget(QLabel("Maximum Angle:"))
        param_layout.addWidget(self.angle_input)
        param_layout.addWidget(QLabel("Reconstruction Method:"))
        param_layout.addWidget(self.method_combo)
        param_layout.addWidget(self.calculate_button)
        param_layout.addWidget(self.animation_button)
        param_layout.addStretch()
        
        self.display_layout = QHBoxLayout()
        
        self.load_button.clicked.connect(self.load_image)
        self.calculate_button.clicked.connect(self.calculate)
        self.animation_button.clicked.connect(self.show_animation)
        
        control_layout.addLayout(param_layout)
        layout.addLayout(control_layout)
        layout.addLayout(self.display_layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image File",
            "",  
            "Images (*.png *.jpg *.jpeg *.bmp)"  
        )
        
        if file_name:  
            try:
                self.image = io.imread(file_name)
                
                self.fig_original = plt.figure(figsize=(4, 4))
                canvas_original = FigureCanvas(self.fig_original)
                
                while self.display_layout.count():
                    item = self.display_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                
                plt.clf()
                plt.imshow(self.image, cmap='gray')
                plt.axis('off')
                plt.title('Original Image')
                
                self.display_layout.addWidget(canvas_original)
                
                print("Image loaded successfully:", self.image.shape)
                
            except Exception as e:
                print("Error loading image:", str(e))

    def calculate(self):
        if not hasattr(self, 'image'):
            QMessageBox.warning(self, "Warning", "Please load an image first!")
            return
        
        try:
            while self.display_layout.count():
                item = self.display_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            
            theta = int(self.angle_input.text())
            method = self.method_combo.currentText()
            
            mi = MI(self.image, theta, method)
            
            sinogram = mi.radonTransform()
            
            if method == "SART":
                reconstruction = mi.sart()
            else:
                reconstruction = mi.filteredBackProjection()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.tight_layout(pad=3.0)  
            
            ax1.imshow(sinogram, cmap='gray')
            ax1.set_title(f'Sinogram (Angle: {theta}°)')
            ax1.axis('off')
            
            ax2.imshow(reconstruction, cmap='gray')
            ax2.set_title(f'Reconstruction (Angle: {theta}°)')
            ax2.axis('off')
            
            canvas = FigureCanvas(fig)
            self.display_layout.addWidget(canvas)
            
        except ValueError as ve:
            QMessageBox.warning(self, "Error", "Please enter a valid angle!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def show_animation(self):
        if not hasattr(self, 'image'):
            QMessageBox.warning(self, "Warning", "Please load an image first!")
            return

        try:
            while self.display_layout.count():
                item = self.display_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            theta = int(self.angle_input.text())
            method = self.method_combo.currentText()
            
            figure = plt.figure(figsize=(12, 4))
            canvas = FigureCanvas(figure)
            self.display_layout.addWidget(canvas)
            
            ax1 = figure.add_subplot(141)  
            ax2 = figure.add_subplot(142) 
            ax3 = figure.add_subplot(143)  
            
            ax1.imshow(self.image, cmap='gray')
            ax1.set_title('Original Image')
            ax1.axis('off')
            
            for current_angle in range(10, theta + 1, 10):
                mi = MI(self.image, current_angle, "ramp")  
                
                sinogram = mi.radonTransform()
                ax2.clear()
                ax2.imshow(sinogram, cmap='gray')
                ax2.set_title(f'Sinogram (Angle: {current_angle}°)')
                ax2.axis('off')
                
                if method == "SART":
                    reconstruction = mi.sart()
                else:
                    mi.filter = method  
                    reconstruction = mi.filteredBackProjection()
                
                ax3.clear()
                ax3.imshow(reconstruction, cmap='gray')
                ax3.set_title(f'Reconstruction (Angle: {current_angle}°)')
                ax3.axis('off')
                
                figure.tight_layout()
                canvas.draw()
                QApplication.processEvents()
                time.sleep(0.5)  

        except ValueError as ve:
            QMessageBox.warning(self, "Error", str(ve))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())