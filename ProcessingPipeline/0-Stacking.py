# This file is used to convert a list of .tif images into a stacked .tif

import glob
import tifffile

inputDir = r"C:\Users\ssbcl\OneDrive\Documents\School\IndependentStudy\Data\ValidationSet\Val_5\Raw"
outputDir = r"C:\Users\ssbcl\OneDrive\Documents\School\IndependentStudy\Data\ValidationSet\Val_5\Val_5.tiff"

with tifffile.TiffWriter(outputDir) as stack:
    for filename in glob.glob(inputDir + "\*.tif"):
        stack.save(
            tifffile.imread(filename), 
            photometric='minisblack', 
            contiguous=True
        )