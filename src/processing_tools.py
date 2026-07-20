from bioio import BioImage
from bioio import PhysicalPixelSizes
from bioio import Dimensions
from bioio.writers import OmeTiffWriter
import os
import shutil
from cellpose import core, models
from cellpose import io as cp_io
from skimage import img_as_float32
from skimage.segmentation import find_boundaries  
import pandas as pd  
from skimage import ( io, measure,
                      transform)
import numpy as np
import tifffile


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
        img = BioImage(czifile)  # selects the first scene found

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
            resizedData = transform.rescale(data, resizeFactor, order=1, anti_aliasing=False, channel_axis=None, preserve_range=True).astype(data.dtype)
            #d =  Dimensions("ZYX", resizedData.shape)
            newDimensions = Dimensions("ZYX", resizedData.shape)
            oldDimensions = Dimensions("ZYX", data.shape)
            newPxSize = calculateResizedPxSize(newDimensions, oldDimensions, pxSize)
            print('\t\tResizing image from ['  + str(oldDimensions.X) +', '+ str(oldDimensions.Y) +', '+ str(oldDimensions.Z) +'] to ['+ str(newDimensions.X) +' '+ str(newDimensions.Y) +' '+ str(newDimensions.Z) +']')

            #img.save(os.path.join(INPUT_FOLDER, 'test.tiff'))
            basename_output = basename.split('-Airyscan')[0]
            outputname = basename_output.split('_63x')[0] + '_ch' + str(idx+1) + '_downs'
            print('\t\tSaving resized file as ' + os.path.join(outputFolder,'ch'+str(idx+1), outputname + '.tiff'))
            OmeTiffWriter.save(resizedData, os.path.join(outputFolder,'ch'+str(idx+1), outputname + '.tiff'), image_name = outputname, channel_colors=[channels[chID]['color']], 
                            channel_names =channels[chID]['name'], dim_order="ZYX",physical_pixel_sizes=pxreSize)


def processTJ(dataset_path, output_path,  model_path, model_name, TJdiameter=19.59):

    Batch_size = 32
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
    
        #cp_io.masks_flows_to_seg(stack, masks, flows, str(short_name[0]), diams=diameter, channels=Channels)
        cp_io.save_masks(stack, masks, flows, str(short_name[0]), png=False, tif=True, channels=Channels)

    return TJ_output_path
        


def processVASA(dataset_path, output_path, model_path, model_name, VASAdiameter = 39):
    Channels = [0, 0] 
    diameter = VASAdiameter
    Det_threshold = 0
    Flow_threshold=0.4
    Cellprob_threshold=0 
    Batch_size = 512
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
    
        #cp_io.masks_flows_to_seg(stack, masks, flows, str(short_name[0]), diams=diameter, channels=Channels)
        cp_io.save_masks(stack, masks, flows, str(short_name[0]), png=False, tif=True, channels=Channels)
        
    return VASA_output_path    

def processVASA_cp4(dataset_path, output_path, model_path, model_name):
    Channels = [0, 0] 
    #diameter = VASAdiameter
    Det_threshold = 0
    Flow_threshold=0.4
    Cellprob_threshold=0 
    Batch_size = 32
    Do_3D=True
    Flow3D_smooth= 2
    Z_axis = 0 
    Anisotropy = 1.78 
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

    model = models.CellposeModel(gpu=True, pretrained_model=fullpath_model)

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



    for idx, image in enumerate(target_files):
        print('Processing file ' + str(idx+1) + ' of ' + str(len(target_files)))
        imPath = os.path.join(VASA_output_path,image)
        print("Performing prediction on: "+ imPath)   
        
        stack = io.imread(imPath)
        short_name = os.path.splitext(image)
        n_plane = stack.shape[0]     
    
        masks, flows, styles = model.eval(stack, batch_size = Batch_size, 
                                          normalize = normalize_custom, stitch_threshold=Stitch_threshold, 
                                          do_3D=Do_3D, anisotropy = Anisotropy, min_size=Min_size, flow3D_smooth = Flow3D_smooth, 
                                          cellprob_threshold=Cellprob_threshold ,z_axis = Z_axis)
        
        
        prediction_stack_32 = img_as_float32(masks, force_copy=False)

        print('Saving output files to directory:' + VASA_output_path)
        os.chdir(VASA_output_path)
    
        #cp_io.masks_flows_to_seg(stack, masks, flows, str(short_name[0]), channels=Channels)
        cp_io.save_masks(stack, masks, flows, str(short_name[0]), png=False, tif=True, channels=Channels)

    return VASA_output_path


def processTJSegmentationMasks(masksFolder, label, px_size= [0.25, 0.14, 0.14]):

    minSize = 100

    masks = []
    for file in os.listdir(masksFolder):
        # check only text files
        if file.endswith('masks.tif'):
            masks.append(file)

    segmentedRegions = pd.DataFrame()
    for maskFile in masks:
        labeled_image = io.imread(os.path.join(masksFolder,maskFile))

        intensityFile = maskFile.replace('_cp_masks.tif', '.tiff')
        intensity_image = io.imread(os.path.join(masksFolder,intensityFile))

        metrics = pd.DataFrame(measure.regionprops_table(labeled_image, intensity_image=intensity_image, properties = ['label','num_pixels','area','mean_intensity'], spacing =px_size))

        metrics=metrics.rename(columns={"area": "volume"})
        metrics['dataset'] = maskFile.split('_ch')[0]
        metrics['date'] = maskFile.split('_')[0]

        segmentedRegions= pd.concat([segmentedRegions, metrics],ignore_index=True)

    segmentedRegions = segmentedRegions[segmentedRegions['num_pixels'] > minSize]

    regionStats = segmentedRegions.groupby(['dataset','date'],as_index=False, group_keys=False).size()
    regionStats['marker']= label

    return regionStats, segmentedRegions



def refine_outliers(metrics, masks):
    Q1 = metrics['num_pixels'].quantile(0.25)
    Q3 = metrics['num_pixels'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    refined_metrics = metrics[(metrics['num_pixels'] >= lower_bound)]
    cleared_labels = metrics[(metrics['num_pixels'] <lower_bound)]['label'].values
    print(cleared_labels)
    #refined_masks = masks[cleared_labels]
    refined_masks = masks.copy()
    refined_masks[np.isin(masks, cleared_labels)] = 0
   
    return refined_metrics, refined_masks



def processVASASegmentationMasks(masksFolder, label,  px_size= [0.25, 0.14, 0.14]):

    minSize = 100

    masks = []
    for file in os.listdir(masksFolder):
        # check only text files
        if file.endswith('masks.tif'):
            masks.append(file)

    segmentedRegions = pd.DataFrame()
    for maskFile in masks:
        labels = io.imread(os.path.join(masksFolder,maskFile))

        metrics = pd.DataFrame(measure.regionprops_table(labels, properties = ['label','num_pixels','area'], spacing =px_size))

        metrics['surface_area']= calculate_surface_area(labels, metrics['label'], px_size=px_size)
        metrics=metrics.rename(columns={"area": "volume"})
        metrics['dataset'] = maskFile.split('_ch')[0] 
        metrics['date'] = maskFile.split('_')[0] 

        refined_metrics, refined_masks = refine_outliers(metrics, labels)

        segmentedRegions= pd.concat([segmentedRegions, refined_metrics],ignore_index=True)


        io.imsave(os.path.join(masksFolder, maskFile.split('.tif')[0] + '_refined.tif'), refined_masks.astype('uint16'))

        #props = pd.DataFrame(measure.regionprops_table(mask, properties =['label', 'num_pixels']))
        #props['dataset'] = maskFile.split('_ch')[0] 
        #props['date'] = maskFile.split('_')[0]   

        #= pd.concat([segmentedRegions, props],ignore_index=True)

    #segmentedRegions = segmentedRegions[segmentedRegions['num_pixels'] > minSize ]

    regionStats = segmentedRegions.groupby(['dataset','date'],as_index=False, group_keys=False).size()
    regionStats['marker']= label  

    return regionStats, segmentedRegions 


def find_outliers(metrics, masks):
    metrics['outlier'] = False
    Q1 = metrics['num_pixels'].quantile(0.25)
    Q3 = metrics['num_pixels'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    

    metrics.loc[(metrics['num_pixels'] < lower_bound), 'outlier'] = True
    outlier_labels = metrics[metrics['outlier']==True]['label'].tolist()

    return metrics, outlier_labels

def calculate_surface_area(masks, labels, px_size=(1,1,1)):
    n = len(labels)
    lab = masks.copy()
    lab[find_boundaries(lab, mode='outer')] = 0
    vts, fs, ns, cs = measure.marching_cubes(lab, level=0, spacing=px_size)

    lst = [[] for i in range(n+1)]
    for i in fs: lst[int(cs[i[0]])].append(i)
    areas = [0 if len(i)==0 else measure.mesh_surface_area(vts, i) for i in lst]
    areas = areas[1:]    

    return areas

def refineVASASegmentationMasks(masksFolder, label,  px_size= [0.25, 0.14, 0.14]):

    masks = []
    for file in os.listdir(masksFolder):
        # check only text files
        if file.endswith('masks.tif'):
            masks.append(file)


    segmentedRegions = pd.DataFrame()
    refined_metrics  = pd.DataFrame()
    for maskFile in masks:
        labeled_image = io.imread(os.path.join(masksFolder,maskFile))

        metrics = pd.DataFrame(measure.regionprops_table(labeled_image, properties = ['label','num_pixels','area'], spacing =px_size))

        metrics['surface_area']= calculate_surface_area(labeled_image, metrics['label'], px_size=px_size)
        metrics=metrics.rename(columns={"area": "volume"})
        metrics['dataset'] = maskFile.split('_ch')[0] 
        metrics['date'] = maskFile.split('_')[0] 

        refined_metrics, outlier_labels = find_outliers(metrics, labeled_image)
        print(f'[processVASASegmentationMasks] Found {len(outlier_labels)} outliers in file: ', maskFile)
        segmentedRegions= pd.concat([segmentedRegions, refined_metrics],ignore_index=True)

        
        refined_labeled_image = labeled_image.copy()
        refined_labeled_image[np.isin(labeled_image, outlier_labels)] = 0
        tifffile.imwrite(os.path.join(masksFolder, maskFile.split('.tif')[0] + '_refined.tif'), refined_labeled_image.astype('uint16'), compression='lzw')

        #props = pd.DataFrame(measure.regionprops_table(mask, properties =['label', 'num_pixels']))
        #props['dataset'] = maskFile.split('_ch')[0] 
        #props['date'] = maskFile.split('_')[0]   

        #= pd.concat([segmentedRegions, props],ignore_index=True)
    
    regionStats = segmentedRegions.groupby(['dataset','date'],as_index=False, group_keys=False)['outlier'].count()
    outliers = segmentedRegions.groupby(['dataset','date'],as_index=False, group_keys=False)['outlier'].sum()
    regionStats['refined_counts'] = regionStats['outlier'] - outliers['outlier']
    regionStats = regionStats.rename(columns={"outlier": "size"})

    regionStats['marker']= label    

    return regionStats, segmentedRegions 




def mergeSegmentationResults(TJstats, VASAstats):  
    TJstatsf = TJstats.rename(columns={"size": "TJ_counts"})
    TJstatsf = TJstatsf.drop(columns='marker')
    VASAstatsf = VASAstats.rename(columns={"size": "VASA_counts"})
    VASAstatsf = VASAstatsf.drop(columns='date')
    VASAstatsf = VASAstatsf.drop(columns='marker')

    exportStats = pd.merge(TJstatsf, VASAstatsf, how='inner', on='dataset')   

    return exportStats

def exportSegmentationResults(  exportdata, outputpath, basename):
    exportdata.to_csv(os.path.join(outputpath,basename + '_counts.csv'), index=False) 

def exportTJSegmentationCounts(TJstats, outputpath,basename):
    TJstatsf = TJstats.rename(columns={"size": "TJ_counts"})
    TJstatsf = TJstatsf.drop(columns='marker')

    TJstatsf.to_csv(os.path.join(outputpath,basename + '_TJ_counts.csv'), index=False)

def exportTJSegmentationPercellMetrics(TJsegmentedRegions, outputpath,basename):
    TJsegmentedRegions.to_csv(os.path.join(outputpath,basename + '_TJ_percell_metrics.csv'), index=False)

def exportVASASegmentationCounts(VASAstats, outputpath,basename):
    VASAstatsf = VASAstats.rename(columns={"size": "VASA_counts"})
    if 'refined_counts' in VASAstatsf.columns:
        VASAstatsf = VASAstatsf.rename(columns={"refined_counts": "VASA_refined_counts"})
    if 'marker' in VASAstatsf.columns:
        VASAstatsf = VASAstatsf.drop(columns='marker')

    VASAstatsf.to_csv(os.path.join(outputpath,basename + '_VASA_counts.csv'), index=False)

def exportVASASegmentationPercellMetrics(VASAsegmentedRegions, outputpath,basename):
    VASAsegmentedRegions.to_csv(os.path.join(outputpath,basename + '_VASA_percell_metrics.csv'), index=False)