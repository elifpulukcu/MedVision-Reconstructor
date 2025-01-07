import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.transform import radon, iradon, iradon_sart, rescale

class MI:
    def __init__(self, image, maxAngle, filterName):
        self.image = image
        if len(self.image.shape) == 3:
            self.image = color.rgb2gray(image)
        self.angle = maxAngle
        self.filter = filterName
    
    def processImage(self):
        imageScaled = rescale(self.image, scale=0.4, mode='reflect')
        theta = np.linspace(0.0, self.angle, max(imageScaled.shape))
        numProjection = len(theta)*max(imageScaled.shape)
        return imageScaled, theta, numProjection
    
    def radonTransform(self):
        image, theta, __ = self.processImage()
        sinogram = radon(image, theta=theta)
        return sinogram
    
    def filteredBackProjection(self):
        __, theta, __ = self.processImage()
        sinogram = self.radonTransform()
        reconstruction = iradon(sinogram, theta=theta, filter_name=self.filter)
        return reconstruction
    
    def sart(self):
        __, theta, __ = self.processImage()
        sinogram = self.radonTransform()
        
        reconstructionSart = iradon_sart(
            sinogram,
            theta=theta,
            relaxation=0.15,  
        )
        return reconstructionSart