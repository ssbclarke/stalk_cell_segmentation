outDir = getDirectory("image");
name = File.getName(outDir);

outDir = outDir + name + ".stl";
run("Reslice Z", "new=1.000");
run("3D Viewer");
call("ij3d.ImageJ3DViewer.setCoordinateSystem", "false");
call("ij3d.ImageJ3DViewer.add", "Resliced", "White", "Resliced", "50", "true", "true", "true", "2", "2");
call("ij3d.ImageJ3DViewer.select", "Resliced");
call("ij3d.ImageJ3DViewer.exportContent", "STL Binary", outDir);
print(outDir);