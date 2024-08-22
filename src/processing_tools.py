from aicsimageio import AICSImage
from aicsimageprocessing import resize
from aicsimageio.writers import OmeTiffWriter
from aicsimageio.types import PhysicalPixelSizes
from aicsimageio.dimensions import Dimensions
import os
import shutil
from cellpose import core, utils, models, metrics, train, transforms
from cellpose import io as cp_io
from skimage import img_as_float32  
import pandas as pd  
from skimage import ( feature, io, measure,
                      morphology,  transform)



channels = [{'name': 'DAPI', 'id':4, 'color' : [0,0,255]},
            {'name': 'TJ', 'id': 3, 'color' : [0,255,0]},
            {'name': 'membrane', 'id': 2, 'color' : [255,0,0]},
            {'name': 'VASA', 'id': 1, 'color' : [255,0,255]}]

def initializeCellPose():
    
    use_GPU = core.use_gpu()
    yn = ['NO', 'YES']
    print(f'>>> GPU activated? {yn[use_GPU]}')

    core.assign_device(use_torch=True, gpu=True, device=0)

def  readFolder(input_folder):
    print('Preprocessing files from directory: ' + input_folder)

    fileList = [f for f in os.listdir(input_folder)  if f.endswith('.czi')]

    print(str(len(fileList)) + ' files found:')
    for f in fileList:
        print('\t'+ f)

    return fileList


def buildOutputFolder(outputFolder, outputBasename):
    print('\t[buildOutputFolder] Creating:' + outputFolder)
    outputFolder = os.path.join(outputFolder, outputBasename)

    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)

        for i in range(4):
            if not os.path.isdir(os.path.join(outputFolder,'ch'+str(i+1))):
                os.mkdir(os.path.join(outputFolder,'ch'+str(i+1)))
                print('\t[buildOutputFolder] Creating '+os.path.join(outputFolder,'ch'+str(i+1)))

    return outputFolder


def calculateResizingFactor(currentPxSize, targetPxSize):
    resizeFactor = [currentPxSize.Z / targetPxSize[0]  , currentPxSize.Y / targetPxSize[1]  ,  currentPxSize.X / targetPxSize[2]]

    return resizeFactor


def calculateResizedPxSize(originalDims, resizedDims, originalPxSize):
    newPxSize = PhysicalPixelSizes((originalDims.Z/resizedDims.Z) * originalPxSize.Z, (originalDims.Y/resizedDims.Y) * originalPxSize.Y, (originalDims.X/resizedDims.X) * originalPxSize.X )

    return newPxSize


def processFiles(fileList, outputFolder, targetPxSize, channelMapping):
    targetPxSize = PhysicalPixelSizes(targetPxSize[0], targetPxSize[1], targetPxSize[2])
    for idx, f in enumerate(fileList):
        print('[processFiles] processing file ' + str(idx+1) + ' of ' +str(len(fileList)))
        czifile = f
        basename = os.path.basename(f)

        # Get an AICSImage object
        img = AICSImage(czifile)  # selects the first scene found        

        pxSize = img.physical_pixel_sizes   

        #print(img.shape)  # returns tuple of dimension sizes in TCZYX order
        img.get_image_data("CZYX", T=0)  # returns 4D CZYX numpy array

        nChannels = img.dims.C  # returns size of X dimension

        resizeFactor = calculateResizingFactor(pxSize, targetPxSize)

        pxreSize = PhysicalPixelSizes(pxSize.Z / resizeFactor[0], pxSize.Y / resizeFactor[1], pxSize.X / resizeFactor[2])

        for idx , ch in enumerate(channelMapping):
            print('\tProcessing channel ' + ch + '(' +channels[int(ch)-1]['name']+ ')'+ ' as channel ' + str(idx+1))
            chID =int(ch)-1

            data = img.get_image_data("ZYX", C=chID)  # returns 4D CZYX numpy array
            resizedData= resize(data,resizeFactor)
            #d =  Dimensions("ZYX", resizedData.shape)
            newDimensions = Dimensions("ZYX", resizedData.shape)
            oldDimensions = Dimensions("ZYX", data.shape)
            newPxSize = calculateResizedPxSize(newDimensions, oldDimensions, pxSize)
            print('\t\tResizing image from ['  + str(oldDimensions.X) +', '+ str(oldDimensions.Y) +', '+ str(oldDimensions.Z) +'] to ['+ str(newDimensions.X) +' '+ str(newDimensions.Y) +' '+ str(newDimensions.Z) +']')

            #img.save(os.path.join(INPUT_FOLDER, 'test.tiff'))
            outputname = basename.split('_63x')[0] + '_ch' + str(idx+1) + '_downs'
            print('\t\tSaving resized file as ' + os.path.join(outputFolder,'ch'+str(idx+1), outputname + '.tiff'))
            OmeTiffWriter.save(resizedData, os.path.join(outputFolder,'ch'+str(idx+1), outputname + '.tiff'), image_name = outputname, channel_colors=[channels[chID]['color']], 
                            channel_names =channels[chID]['name'], dim_order="ZYX",physical_pixel_sizes=pxreSize)


def processTJ(dataset_path, output_path,  model_path, model_name, TJdiameter=19.59):

    Batch_size = 512
    Channels = [0, 0] 
    diameter = TJdiameter
    Det_threshold = 0
    Flow_threshold=0.4
    Cellprob_threshold=0 
    Do_3D=False 
    Anisotropy = 0, 
    Stitch_threshold=0.3
    Min_size=15

    images_path = os.path.join(dataset_path,'ch3')
    TJ_output_path = os.path.join(output_path, 'TJ_ch3')

    #model_path = "D:/Projects/Mikala/images/training_norm/models" + "/models/"
    #modelName = 'TJ_xy_pipeline_norm_Mikala'


    normalize_custom = {
        "lowhigh": None ,
        "percentile": [1.0,99.0],
        "normalize": True,
        "norm3D": True,
        "sharpen_radius": 0,
        "smooth_radius": 0,
        "tile_norm_blocksize": 0,
        "tile_norm_smooth3D": 1,
        "invert": False
    }


    print('Processing TJ channel:')

    # model_type='cyto' or model_type='nuclei'
    fullpath_model = os.path.join(model_path,model_name)
    print('Cellpose model path = ' + fullpath_model)

    model = models.CellposeModel(gpu=True, pretrained_model=fullpath_model,  diam_mean=30.0)

    #model = models.CellposeModel(pretrained_model=os.path.join(model_path,modelName), gpu = True, diam_mean=diameter)

    
    target_files = []
    # Iterate directory
    for file in os.listdir(images_path):
        # check only text files
        if file.endswith('downs.tiff'):
            target_files.append(file)

    
    if not os.path.isdir(TJ_output_path):
        # Create a new directory because it does not exist
        os.makedirs(TJ_output_path)

    TJ_output_path = os.path.join(TJ_output_path, target_files[0].split('_')[0])
    if not os.path.isdir(TJ_output_path):
        # Create a new directory because it does not exist
        os.makedirs(TJ_output_path)
    
    for f in target_files:
        shutil.copy(os.path.join(images_path,f), os.path.join(TJ_output_path,f))

   
    # channel to segment and nuclear channel 
    # numbering starts at 1 
    # for your single channel image use [0, 0] 
    # for the multi channel image it's [3, 0]

    Diameter = model.diam_labels

    for idx, image in enumerate(target_files):
        print('Processing file ' + str(idx+1) + ' of ' + str(len(target_files)))
        imPath = os.path.join(TJ_output_path,image)
        print("Performing prediction on: "+ imPath)
    
        stack = io.imread(imPath)
        short_name = os.path.splitext(image)
        n_plane = stack.shape[0]
       
    
        masks, flows, styles = model.eval(stack, batch_size = Batch_size, diameter=Diameter, channels=Channels,normalize = normalize_custom, stitch_threshold=Stitch_threshold, do_3D=Do_3D, anisotropy = Anisotropy, min_size=Min_size, cellprob_threshold=Cellprob_threshold)
                
        prediction_stack_32 = img_as_float32(masks, force_copy=False)

        print('Saving output files to directory:' + TJ_output_path)
        os.chdir(TJ_output_path)
    
        cp_io.masks_flows_to_seg(stack, masks, flows, str(short_name[0]), diams=diameter, channels=Channels)
        cp_io.save_masks(stack, masks, flows, str(short_name[0]), png=False, tif=True, channels=Channels)

    return TJ_output_path
        


def processVASA(dataset_path, output_path, model_path, model_name, VASAdiameter = 39):
    Channels = [0, 0] 
    diameter = VASAdiameter
    Det_threshold = 0
    Flow_threshold=0.4
    Cellprob_threshold=0 
    Batch_size = 1024
    Do_3D=False 
    Anisotropy = 0 
    Stitch_threshold=0.3
    Min_size=15

    images_path = os.path.join(dataset_path,'ch1')
    VASA_output_path = os.path.join(output_path, 'VASA_ch1')


    #model_path = 'D:/Projects/Mikala/images/training_bright/single_channel/ch1/xy_seg_model/models/models'
    #model_name = 'VASA_xy_pipeline_bright_Mikala'

    normalize_custom = {
        "lowhigh": None ,
        "percentile": [1.0,99.0],
        "normalize": True,
        "norm3D": True,
        "sharpen_radius": 0,
        "smooth_radius": 0,
        "tile_norm_blocksize": 0,
        "tile_norm_smooth3D": 1,
        "invert": False
    }


    print('Processing VASA channel:')

    # model_type='cyto' or model_type='nuclei'
    fullpath_model = os.path.join(model_path,model_name)
    print('Cellpose model path = ' + fullpath_model)

    model = models.CellposeModel(gpu=True, pretrained_model=fullpath_model,  diam_mean=30.0)

    #model = models.CellposeModel(pretrained_model=os.path.join(model_path,modelName), gpu = True, diam_mean=diameter)

    #isExist = os.path.exists(VASA_output_path)
    if not os.path.exists(VASA_output_path):
        # Create a new directory because it does not exist
        os.makedirs(VASA_output_path)


    target_files = []
    # Iterate directory
    for file in os.listdir(images_path):
        # check only text files
        if file.endswith('downs.tiff'):
            target_files.append(file)

    if not os.path.isdir(VASA_output_path):
        # Create a new directory because it does not exist
        os.makedirs(VASA_output_path)

    VASA_output_path = os.path.join(VASA_output_path, target_files[0].split('_')[0])
    if not os.path.isdir(VASA_output_path):
        # Create a new directory because it does not exist
        os.makedirs(VASA_output_path)
    




    #shutil.rmtree(output_path)


    for f in target_files:
        shutil.copy(os.path.join(images_path,f), os.path.join(VASA_output_path,f))

    # channel to segment and nuclear channel 
    # numbering starts at 1 
    # for your single channel image use [0, 0] 
    # for the multi channel image it's [3, 0]

    Diameter = model.diam_labels

    for idx, image in enumerate(target_files):
        print('Processing file ' + str(idx+1) + ' of ' + str(len(target_files)))
        imPath = os.path.join(VASA_output_path,image)
        print("Performing prediction on: "+ imPath)   
        
        stack = io.imread(imPath)
        short_name = os.path.splitext(image)
        n_plane = stack.shape[0]     
    
        masks, flows, styles = model.eval(stack, batch_size = Batch_size, diameter=Diameter, channels=Channels,normalize = normalize_custom, stitch_threshold=Stitch_threshold, do_3D=Do_3D, anisotropy = Anisotropy, min_size=Min_size, cellprob_threshold=Cellprob_threshold)
        
        
        prediction_stack_32 = img_as_float32(masks, force_copy=False)

        print('Saving output files to directory:' + VASA_output_path)
        os.chdir(VASA_output_path)
    
        cp_io.masks_flows_to_seg(stack, masks, flows, str(short_name[0]), diams=diameter, channels=Channels)
        cp_io.save_masks(stack, masks, flows, str(short_name[0]), png=False, tif=True, channels=Channels)
        
    return VASA_output_path    

def processSegmentationMasks(masksFolder, label):

    minSize = 100
   

    masks = []
    for file in os.listdir(masksFolder):
        # check only text files
        if file.endswith('masks.tif'):
            masks.append(file)


    segmentedRegions = pd.DataFrame()
    for maskFile in masks:
        mask = io.imread(os.path.join(masksFolder,maskFile))
        props = pd.DataFrame(measure.regionprops_table(mask, properties =['label', 'num_pixels']))
        props['dataset'] = maskFile.split('_ch')[0] 
        props['date'] = maskFile.split('_')[0]   

        segmentedRegions= pd.concat([segmentedRegions, props],ignore_index=True)

    segmentedRegions = segmentedRegions[segmentedRegions['num_pixels'] > minSize ]

    regionStats = segmentedRegions.groupby(['dataset','date'],as_index=False, group_keys=False).size()
    regionStats['marker']= label  

    return regionStats 

def mergeSegmentationResults(TJstats, VASAstats):  
    TJstatsf = TJstats.rename(columns={"size": "TJ_counts"})
    TJstatsf = TJstatsf.drop(columns='marker')
    VASAstatsf = VASAstats.rename(columns={"size": "VASA_counts"})
    VASAstatsf = VASAstatsf.drop(columns='date')
    VASAstatsf = VASAstatsf.drop(columns='marker')

    exportStats = pd.merge(TJstatsf, VASAstatsf, how='inner', on='dataset')   

    return exportStats

def exportSegmentationResults(exportdata, outputpath, basename):
           exportdata.to_csv(os.path.join(outputpath,basename + '_counts.csv'), index=False)   