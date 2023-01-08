# This file is used to convert a list of .tif images into a stacked .tif

import glob
import tifffile

# Change these directories to match your particular environment
inputDir = r"ValidationSet\Val_1\Raw"
outputDir = r"ValidationSet\Val_1\Raw\Val_1.tiff"

with tifffile.TiffWriter(outputDir) as stack:
    for filename in glob.glob(inputDir + "\*.tif"):
        stack.save(
            tifffile.imread(filename), 
            photometric='minisblack', 
            contiguous=True
        )