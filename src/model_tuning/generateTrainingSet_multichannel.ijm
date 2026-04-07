
close("*")
run("Close All");

//folderName = "D:/Projects/Mikala/images/downsampled/02092024";
folderName = "D:/Projects/Mikala/images/downsampled/02072024"

channels = newArray(2,4)
nChunks = 5;
nChunksYZ = 3;

ch1Folder = "ch1";
ch2Folder = "ch2";
ch3Folder = "ch3";
ch4Folder = "ch4";
VASA_trainingFolder = "VASA";
TJ_trainingFolder = "TJ";
membrane_trainingFolder = "membrane";


output = "D:/Projects/Mikala/images/training_norm";
File.makeDirectory(output);
File.makeDirectory(output + File.separator + ch1Folder );
File.makeDirectory(output + File.separator + ch2Folder );
File.makeDirectory(output + File.separator + ch3Folder );
File.makeDirectory(output + File.separator + ch4Folder );
File.makeDirectory(output + File.separator + VASA_trainingFolder );
File.makeDirectory(output + File.separator + TJ_trainingFolder );
File.makeDirectory(output + File.separator + membrane_trainingFolder );

/*baseNameFiles = newArray("02092024_ovary2_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02092024_ovary5_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02092024_ovary6_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02092024_ovary7_dapi_488_568_647_63x_0,5um_ch1_downs.tiff");*/
baseNameFiles = newArray("02072024_ovary1_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02072024_ovary2_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02072024_ovary3_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02072024_ovary4_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02072024_ovary5_dapi_488_568_647_63x_0,5um_ch1_downs.tiff",
"02072024_ovary6_dapi_488_568_647_63x_0,5um_ch1_downs.tiff");
ch1Files = baseNameFiles;
ch2Files = newArray(baseNameFiles.length);
ch3Files = newArray(baseNameFiles.length);
ch4Files = newArray(baseNameFiles.length);
for(i=0; i<baseNameFiles.length; i++){
	//ch1Files[i] = replace(baseNamefiles[i], "ch4","ch1");	
	ch2Files[i] = replace(baseNameFiles[i], "ch1","ch2");
	ch3Files[i] = replace(baseNameFiles[i], "ch1","ch3");
	ch4Files[i] = replace(baseNameFiles[i], "ch1","ch4");
	print("Image " + toString(i));
	print("\tCh1: " +baseNameFiles[i] );
	print("\tCh2: " +ch2Files[i]);
	print("\tCh3: " +ch3Files[i]);
	print("\tCh4: " +ch4Files[i]);
}


nFiles = baseNameFiles.length;
print(nFiles);
//nFiles =1;
for (f=0;f<nFiles;f++){
	//ch1
	file = folderName + File.separator + ch1Files[f];
	exportName = File.getNameWithoutExtension(ch1Files[f]);
	exportName = replace(exportName, "_ch1","");
	print("Opening ch1 file: " + file);
	open(file);
	rename("ch1Stack");
	run("Enhance Contrast...", "saturated=0.05 normalize process_all use");
	//ch2
	file = folderName + File.separator + ch2Files[f];
	print("Opening ch2 file: " + file);
	open(file);
	rename("ch2Stack");
	run("Enhance Contrast...", "saturated=0.05 normalize process_all use");
	//ch3
	file = folderName + File.separator + ch3Files[f];
	print("Opening ch3 file: " + file);
	open(file);
	rename("ch3Stack");
	run("Enhance Contrast...", "saturated=0.05 normalize process_all use");
	//ch4
	file = folderName + File.separator + ch4Files[f];
	print("Opening ch4 file: " + file);
	open(file);
	rename("ch4Stack");
	run("Enhance Contrast...", "saturated=0.05 normalize process_all use");
	zSize = nSlices;
	for(r = 0; r < nChunks;r++){		
		z = round(random*zSize);
		print(z);
		if(z==0)
			z=1;
		
		selectImage("ch1Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch1Slice");
		saveAs("Tiff", output +  File.separator + ch1Folder + File.separator + exportName + "_ch1_xy" + "_" + r + ".tif");
		rename("ch1Slice_vasa");
		
		selectImage("ch2Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch2Slice");
		saveAs("Tiff", output +  File.separator  + ch2Folder + File.separator + exportName + "_ch2_xy" + "_" + r + ".tif");
		rename("ch2Slice_vasa");
		run("Duplicate...", " ");
		rename("ch2Slice_tj");
		run("Duplicate...", " ");
		rename("ch2Slice_mem");
		
		selectImage("ch3Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch3Slice");
		saveAs("Tiff", output +  File.separator  + ch3Folder + File.separator + exportName + "_ch3_xy" + "_" + r + ".tif");
		rename("ch3Slice_tj");
		//rename("ch3Slice");
		
		selectImage("ch4Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch4Slice");
		saveAs("Tiff", output +  File.separator  + ch4Folder + File.separator + exportName + "_ch4_xy" + "_" + r + ".tif");
		rename("ch4Slice_vasa");
		run("Duplicate...", " ");
		rename("ch4Slice_tj");
		run("Duplicate...", " ");
		rename("ch4Slice_mem");
		
		//run("Merge Channels...", "c1=[ch1Slice] c2=[ch2Slice] c3=[ch4Slice] create");		
		//saveAs("Tiff", output +  File.separator + VASA_trainingFolder + File.separator + exportName + "_ch1_ch2_ch4_xy" + "_" + r + ".tif");
		//close();
		
		run("Merge Channels...", "c1=[ch1Slice_vasa] c2=[ch2Slice_vasa] c3=[ch4Slice_vasa] create");		
		saveAs("Tiff", output +  File.separator + VASA_trainingFolder + File.separator + exportName + "_VASA_xy" + "_" + r + ".tif");
		close();
		
		run("Merge Channels...", "c1=[ch3Slice_tj] c2=[ch2Slice_tj] c3=[ch4Slice_tj] create");		
		saveAs("Tiff", output +  File.separator + TJ_trainingFolder + File.separator + exportName + "_TJ_xy" + "_" + r + ".tif");
		close();
		
		run("Merge Channels...", "c1=[ch2Slice_mem] c2=[ch4Slice_mem] create");		
		saveAs("Tiff", output +  File.separator + membrane_trainingFolder + File.separator + exportName + "_membrane_xy" + "_" + r + ".tif");
		close();
		
	}
	selectImage("ch1Stack");
	run("Reslice [/]...", "output=1.000 start=Top avoid");
	rename("r_ch1Stack");
	selectImage("ch2Stack");
	run("Reslice [/]...", "output=1.000 start=Top avoid");
	rename("r_ch2Stack");
	selectImage("ch3Stack");
	run("Reslice [/]...", "output=1.000 start=Top avoid");
	rename("r_ch3Stack");
	selectImage("ch4Stack");
	run("Reslice [/]...", "output=1.000 start=Top avoid");
	rename("r_ch4Stack");
	
	zSize = nSlices;
	for(r = 0; r < nChunksYZ;r++){
		z = round(random*zSize);
		if(z==0)
			z=1;
		print(z);
		
		selectImage("r_ch1Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch1Slice");
		saveAs("Tiff", output +  File.separator  + ch1Folder + File.separator + exportName + "_ch1_xz" + "_" + r + ".tif");
		rename("ch1Slice_vasa");
		
		selectImage("r_ch2Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch2Slice");
		saveAs("Tiff", output +  File.separator  + ch2Folder + File.separator + exportName + "_ch2_xz" + "_" + r + ".tif");
		rename("ch2Slice_vasa");
		run("Duplicate...", " ");
		rename("ch2Slice_tj");
		run("Duplicate...", " ");
		rename("ch2Slice_mem");
		
		selectImage("r_ch3Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch3Slice");
		saveAs("Tiff", output +  File.separator  + ch3Folder + File.separator + exportName + "_ch3_xz" + "_" + r + ".tif");
		rename("ch3Slice_tj");
		
		selectImage("r_ch4Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch4Slice");
		saveAs("Tiff", output +  File.separator  + ch4Folder + File.separator + exportName + "_ch4_xz" + "_" + r + ".tif");
		rename("ch4Slice_vasa");
		run("Duplicate...", " ");
		rename("ch4Slice_tj");
		run("Duplicate...", " ");
		rename("ch4Slice_mem");
		
		//run("Merge Channels...", "c1=[ch1Slice] c2=[ch2Slice] c3=[ch4Slice] create");
		
		//saveAs("Tiff", output +  File.separator + VASA_trainingFolder + File.separator + exportName + "_ch1_ch2_ch4_xz" + "_" + r + ".tif");
		
		//close();
		
		run("Merge Channels...", "c1=[ch1Slice_vasa] c2=[ch2Slice_vasa] c3=[ch4Slice_vasa] create");		
		saveAs("Tiff", output +  File.separator + VASA_trainingFolder + File.separator + exportName + "_VASA_xz" + "_" + r + ".tif");
		close();
		
		run("Merge Channels...", "c1=[ch3Slice_tj] c2=[ch2Slice_tj] c3=[ch4Slice_tj] create");		
		saveAs("Tiff", output +  File.separator + TJ_trainingFolder + File.separator + exportName + "_TJ_xz" + "_" + r + ".tif");
		close();
		
		run("Merge Channels...", "c1=[ch2Slice_mem] c2=[ch4Slice_mem] create");		
		saveAs("Tiff", output +  File.separator + membrane_trainingFolder + File.separator + exportName + "_membrane_xz" + "_" + r + ".tif");
		close();
		
		
	}
	close();
	
	close("r_ch1Stack");
	close("r_ch2Stack");
	close("r_ch3Stack");
	close("r_ch4Stack");
	
	selectImage("ch1Stack");
	run("Reslice [/]...", "output=1.000 start=Left avoid");
	rename("r_ch1Stack");
	selectImage("ch2Stack");
	run("Reslice [/]...", "output=1.000 start=Left avoid");
	rename("r_ch2Stack");
	selectImage("ch3Stack");
	run("Reslice [/]...", "output=1.000 start=Left avoid");
	rename("r_ch3Stack");
	selectImage("ch4Stack");
	run("Reslice [/]...", "output=1.000 start=Left avoid");
	rename("r_ch4Stack");	
	
	zSize = nSlices;
	for(r = 0; r < nChunksYZ;r++){
		z = round(random*zSize);
		if(z==0)
			z=1;
		print(z);
		setSlice(z);
				
		selectImage("r_ch1Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch1Slice");
		saveAs("Tiff", output +  File.separator  + ch1Folder + File.separator + exportName + "_ch1_yz" + "_" + r + ".tif");
		rename("ch1Slice_vasa");	
		
		selectImage("r_ch2Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch2Slice");
		saveAs("Tiff", output +  File.separator  + ch2Folder + File.separator + exportName + "_ch2_yz" + "_" + r + ".tif");
		rename("ch2Slice_vasa");
		run("Duplicate...", " ");
		rename("ch2Slice_tj");
		run("Duplicate...", " ");
		rename("ch2Slice_mem");
		
		selectImage("r_ch3Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch3Slice");
		saveAs("Tiff", output +  File.separator  + ch3Folder + File.separator + exportName + "_ch3_yz" + "_" + r + ".tif");
		rename("ch3Slice_tj");
		
		selectImage("r_ch4Stack");
		setSlice(z);
		run("Duplicate...", " ");
		rename("ch4Slice");
		saveAs("Tiff", output +  File.separator  + ch4Folder + File.separator + exportName + "_ch4_yz" + "_" + r + ".tif");
		rename("ch4Slice_vasa");
		run("Duplicate...", " ");
		rename("ch4Slice_tj");
		run("Duplicate...", " ");
		rename("ch4Slice_mem");
		
		run("Merge Channels...", "c1=[ch1Slice_vasa] c2=[ch2Slice_vasa] c3=[ch4Slice_vasa] create");		
		saveAs("Tiff", output +  File.separator + VASA_trainingFolder + File.separator + exportName + "_VASA_yz" + "_" + r + ".tif");
		close();
		
		run("Merge Channels...", "c1=[ch3Slice_tj] c2=[ch2Slice_tj] c3=[ch4Slice_tj] create");		
		saveAs("Tiff", output +  File.separator + TJ_trainingFolder + File.separator + exportName + "_TJ_yz" + "_" + r + ".tif");
		close();
		
		run("Merge Channels...", "c1=[ch2Slice_mem] c2=[ch4Slice_mem] create");		
		saveAs("Tiff", output +  File.separator + membrane_trainingFolder + File.separator + exportName + "_membrane_yz" + "_" + r + ".tif");
		close();
	}
	run("Close All");
}
