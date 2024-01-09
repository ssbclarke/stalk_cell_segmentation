from PIL import Image
import numpy as np
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tqdm import tqdm, trange
from tifffile import imsave

from multiprocessing import Process
import multiprocessing as mp

# Change these paths
inputDir = r"..\ValidationSet\Val_1\Val_1_CellProfilerProcessed.tiff"
outputDir = r"..\ValidationSet\Val_1\Val_1_CellProfilerProcessed_Eroded_V2.tiff"



# Program to count islands in boolean 2D matrix
class Graph:
 
    def __init__(self, row, col, g):
        self.ROW = row
        self.COL = col
        self.graph = g
 
    # A function to check if a given cell
    # (row, col) can be included in DFS
    def isSafe(self, i, j, visited):
        # row number is in range, column number
        # is in range and value is 1
        # and not yet visited
        return (i >= 0 and i < self.ROW and
                j >= 0 and j < self.COL and
                not visited[i][j] and self.graph[i][j])
 
    # A utility function to do DFS for a 2D
    # boolean matrix. It only considers
    # the 8 neighbours as adjacent vertices
 
    def DFS(self, i, j, visited):
 
        # These arrays are used to get row and
        # column numbers of 8 neighbours
        # of a given cell
        # rowNbr = [-1, -1, -1,  0, 0,  1, 1, 1]
        # colNbr = [-1,  0,  1, -1, 1, -1, 0, 1]

        # NEW: Making neighbors just up,down,left, and right so that we don't count diagonals as islands
        rowNbr = [-1,  0, 0, 1]
        colNbr = [0, -1, 1, 0]
 
        # Mark this cell as visited
        visited[i][j] = True
 
        # Recur for all connected neighbours
        # for k in range(8):
        for k in range(4):
            if self.isSafe(i + rowNbr[k], j + colNbr[k], visited):
                self.DFS(i + rowNbr[k], j + colNbr[k], visited)
 
    # The main function that returns
    # count of islands in a given boolean
    # 2D matrix
 
    def countIslands(self):
        # Make a bool array to mark visited cells.
        # Initially all cells are unvisited
        visited = [[False for j in range(self.COL)]for i in range(self.ROW)]
 
        # Initialize count as 0 and traverse
        # through the all cells of
        # given matrix
        count = 0
        for i in range(self.ROW):
            for j in range(self.COL):
                # If a cell with value 1 is not visited yet,
                # then new island found
                if visited[i][j] == False and self.graph[i][j] == 255:
                    # Visit all cells in this island
                    # and increment island count
                    self.DFS(i, j, visited)
                    count += 1
 
        return count


# example = np.array([
#     [0,255,255],
#     [255,0,255],
#     [255,255,0]
# ])

# g_e = Graph(len(example), len(example[0]), example)
# g_e.countIslands()

# Loading data
print("The selected stack is a .tif")
dataset = Image.open(inputDir)
h,w = np.shape(dataset)
tiffarray = np.zeros((h,w,dataset.n_frames))
for i in range(dataset.n_frames):
   dataset.seek(i)
   tiffarray[:,:,i] = np.array(dataset)
expim = tiffarray.astype(np.uint8);
print(expim.shape)



# 2D-stacked smart erode
large_window_size=5
small_window_size=1
outCombined = np.zeros(tiffarray.shape, dtype=np.uint8)
for slice in trange(tiffarray.shape[0]):
    test_example = tiffarray[:,:,slice]
    out2D = test_example.copy()
    # x=4
    # y=4
    for x in range(large_window_size, out2D.shape[0] - large_window_size):
        for y in range(large_window_size, out2D.shape[1] - large_window_size):
            rows = list(range(x-large_window_size,x+large_window_size+1))
            columns = list(range(y-large_window_size, y+large_window_size+1))
            window = test_example[np.ix_(rows, columns)]

            newWindow = window.copy()
            for i in range(large_window_size-1, large_window_size+2):
                for j in range(large_window_size-1, large_window_size+2):
                    newWindow[i][j] = np.min(window)

            g1 = Graph(len(window), len(window[0]), window)
            g2 = Graph(len(window), len(window[0]), newWindow)

            if g2.countIslands() > g1.countIslands():
                out2D[x][y] = test_example[x][y]
            else:
                rows = list(range(x-small_window_size,x+small_window_size+1))
                columns = list(range(y-small_window_size, y+small_window_size+1))
                small_window = test_example[np.ix_(rows, columns)]            
                out2D[x][y] = np.min(small_window)
    outCombined[slice] = out2D

imsave(outputDir, outCombined, imagej=True)



