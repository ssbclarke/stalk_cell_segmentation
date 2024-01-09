## stalk_cell_segmentation
Research repository for stalk plant cell segmentation code. Advised by Dr. Christopher Stubbs

# Step 0: File Preprocessing
This step involves converting the format of our original data from a series of .png images to a stacked .tif file which is required for 3d processing by cell profiler
<ol type="a">
  <li>To do this, a simple script called 0-Stacking.py is used</li>
  <li>Change the directories of the input and output path on lines 7 and 8</li>
  <li>Run the script</li>
</ol>

```
inputDir = r"ValidationSet\Val_1\Raw"
outputDir = r"ValidationSet\Val_1\Raw\Val_1.tiff"
```

# Step 1: CellProfiler Processiing
Now, the bulk of the processing is done. CellProfiler provides a streamlined way to process images using pipelined modules.
<ol type="a">
  <li>After launching CellProfiler, open a project (File > Open Project), and select the provided file at ProcessingPipeline/1-StalkCellProcessing3D.cpproj</li> 
  <li>Navigate to the images tab, remove any previous files opened, and then drag-and-drop your selected stacked .tiff to be processed</li>
  <li>Optional) Select the ‘SaveImages’ module and configure the output image location, by default is in the directory of the input image.</li>
  <li>Click on ‘Analyze Images’</li>
</ol>

# Step 2: Erosion
From analysis, the cell wall thickness appeared to be too thick after CellProfiler processing. Although CellProfiler supports 3D erosion of images, it does not account for newly created holes in the cell walls. Therefore, we have a custom implementation: 2-Erosion.py.
<ol type="a">
  <li>Change the directories of the input and output path on lines 13 and 14</li>
  <li>(Optional) Adjust small and large window sizes (explained on Slide 13) on lines 100 and 101</li>
  <li>Run the script</li>
</ol>

```
inputDir = r"ValidationSet\Val_1\Val_1_CellProfilerProcessed.tiff"
outputDir = r"ValidationSet\Val_1\Val_1_CellProfilerProcessed_Eroded.tiff"
```

# Step 3: 3D Creation
After eroding, we are ready to create a 3D .stl file using imagej
<ol type="a">
  <li>Launch ImageJ</li>
  <li>File>Open>Select the targeted eroded image.</li>
  <li>Plugins>Macro>Run>Select ProcessingPipeline/3-Stalk_3D_Surface_Creation.imj</li>
  <li>The script should run automatically and a .stl file will be saved to the eroded image directory.</li>
</ol>

