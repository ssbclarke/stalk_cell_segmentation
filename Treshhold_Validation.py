from PIL import Image
import numpy as np
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tqdm import tqdm, trange
from tifffile import imsave
import cv2 as cv
# from image_similarity_measures.quality_metrics import rmse

#%% RMSE code 

# Citation
# Müller, M. U., Ekhtiari, N., Almeida, R. M., and Rieke, C.: SUPER-RESOLUTION OF MULTISPECTRAL SATELLITE IMAGES USING CONVOLUTIONAL NEURAL NETWORKS, ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci., V-1-2020, 33–40, https://doi.org/10.5194/isprs-annals-V-1-2020-33-2020, 2020.

def _assert_image_shapes_equal(org_img: np.ndarray, pred_img: np.ndarray, metric: str):
    # shape of the image should be like this (rows, cols, bands)
    # Please note that: The interpretation of a 3-dimension array read from rasterio is: (bands, rows, columns) while
    # image processing software like scikit-image, pillow and matplotlib are generally ordered: (rows, columns, bands)
    # in order efficiently swap the axis order one can use reshape_as_raster, reshape_as_image from rasterio.plot
    msg = (
        f"Cannot calculate {metric}. Input shapes not identical. y_true shape ="
        f"{str(org_img.shape)}, y_pred shape = {str(pred_img.shape)}"
    )

    assert org_img.shape == pred_img.shape, msg

def rmse(org_img: np.ndarray, pred_img: np.ndarray, max_p: int = 4095) -> float:
    """
    Root Mean Squared Error

    Calculated individually for all bands, then averaged
    """
    _assert_image_shapes_equal(org_img, pred_img, "RMSE")

    org_img = org_img.astype(np.float32)
    
    # if image is a gray image - add empty 3rd dimension for the .shape[2] to exist
    if org_img.ndim == 2:
        org_img = np.expand_dims(org_img, axis=-1)
    
    rmse_bands = []
    diff = org_img - pred_img
    mse_bands = np.mean(np.square(diff / max_p), axis=(0, 1))
    rmse_bands = np.sqrt(mse_bands)
    return np.mean(rmse_bands)

#%%

# Change these paths
my_processed = r"ValidationSet\Val_1\Val_1_CellProfilerProcessed_Eroded.tiff"
original = r"ValidationSet\Val_1\Val_1.tiff"

#%% Basic Thresholding

my_processed_img = cv.imread(my_processed)
original_img = cv.imread(original)
up_points = (128, 128)
original_img_resized = cv.resize(original_img, up_points, interpolation= cv.INTER_LINEAR)

# ret,thresh1 = cv.threshold(original_img_resized,96,255,cv.THRESH_BINARY)
ret,thresh1 = cv.threshold(original_img,94,255,cv.THRESH_BINARY)
thresh1_resized = cv.resize(thresh1, up_points, interpolation= cv.INTER_AREA)

plt.imshow(thresh1,'gray',vmin=0,vmax=255)

#%%

# Calculate RMSE (root mean square error)
# rmse(thresh1, my_processed_img)
rmse(thresh1_resized, my_processed_img)

rmse(original_img_resized, thresh1_resized)
rmse(original_img_resized, my_processed_img)


#%% Calculate closest rmse

rmses = []
for i in range(0, 255):
    # ret,threshn = cv.threshold(original_img_resized,i,255,cv.THRESH_BINARY)
    ret,threshn = cv.threshold(original_img,i,255,cv.THRESH_BINARY)
    threshn_resized = cv.resize(threshn, up_points, interpolation= cv.INTER_AREA)
    # rmses.append(rmse(threshn, my_processed_img))
    rmses.append(rmse(my_processed_img, threshn_resized))

print(np.argmin(rmses)); print(np.min(rmses))

# %%

titles = ["Original", "My Processed", "Basic Thresholding"]
images = [original_img_resized, my_processed_img, thresh1]

for i in range(3):
 plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
 plt.title(titles[i])
 plt.xticks([]),plt.yticks([])
# %%

# np.unique(thresh1_resized)

thresh1[0]

# my_processed_img[0:]
# %%
