from MI import MI
from skimage import io
import matplotlib.pyplot as plt
import os

def test_reconstruction():
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'brain_tumor.jpg')
    image = io.imread(image_path)
    mi = MI(image, maxAngle=180, filterName="ramp")
    
    print("Image size:", image.shape)
    
    sinogram = mi.radonTransform()
    print("Sinogram created")
    
    print("Starting FBP reconstruction...")
    fbp_reconstruction = mi.filteredBackProjection()
    
    print("Starting SART reconstruction...")
    sart_reconstruction = mi.sart()
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 5))
    
    ax1.imshow(mi.image, cmap='gray')
    ax1.set_title('Original Image')
    ax1.axis('off')

    ax2.imshow(sinogram, cmap='gray')
    ax2.set_title('Sinogram')
    ax2.axis('off')
    
    ax3.imshow(fbp_reconstruction, cmap='gray')
    ax3.set_title('FBP Reconstruction')
    ax3.axis('off')
    
    ax4.imshow(sart_reconstruction, cmap='gray')
    ax4.set_title('SART Reconstruction')
    ax4.axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_reconstruction()