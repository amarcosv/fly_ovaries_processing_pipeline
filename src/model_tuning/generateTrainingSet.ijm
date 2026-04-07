
close("*")

folderName = "D:/Mikala/images/preproc/10042024_test/ch1";

channels = newArray(2,4);
nChunks = 5;
nChunksYZ = 5;

output = "D:/Mikala/images/training/VASA";

files = newArray("10042024_cntrl_ovary3_dapi_488_555_647_ch1_downs.tiff","10042024_cntrl_ovary5_dapi_488_555_647_ch1_downs.tiff",
	"10042024_cora_ovary8_dapi_488_555_647_ch1_downs.tiff","10042024_cora_ovary5_dapi_488_555_647_ch1_downs.tiff");



nFiles = files.length;
print(nFiles);
//nFiles =1;
for (f=0;f<nFiles;f++){
	file = folderName + File.separator + files[f];
	exportName = File.getNameWithoutExtension(files[f]);
	open(file);
	zSize = nSlices;
	for(r = 0; r < nChunks;r++){
		z = round(random*zSize);
		print(z);
		if(z==0)
			z=1;
		setSlice(z);
		run("Duplicate...", " ");
		saveAs("Tiff", output +  File.separator  + exportName + "_xy" + "_" + r + ".tif");
		close();
	}
//	run("Reslice [/]...", "output=1.000 start=Top avoid");
//	zSize = nSlices;
//	for(r = 0; r < nChunksYZ;r++){
//		z = round(random*zSize);
//		if(z==0)
//			z=1;
//		print(z);
//		setSlice(z);
//		run("Duplicate...", " ");
//		saveAs("Tiff", output +  File.separator  + exportName + "_xz" + "_" + r + ".tif");
//		close();
//	}
//	close();
//	run("Reslice [/]...", "output=1.000 start=Left avoid");
//	zSize = nSlices;
//	for(r = 0; r < nChunksYZ;r++){
//		z = round(random*zSize);
//		if(z==0)
//			z=1;
//		print(z);
//		setSlice(z);
//		run("Duplicate...", " ");
//		saveAs("Tiff", output +  File.separator  + exportName + "_yz" + "_" + r + ".tif");
//		close();
//	}
	close();
}
