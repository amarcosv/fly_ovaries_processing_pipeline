import sys
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='VASA segmentation pipeline (CellPose 4)')
    parser.add_argument('--input', required=True, help='Folder with raw .czi files')
    parser.add_argument('--preproc', required=True, help='Base folder for preprocessed output')
    parser.add_argument('--output', required=True, help='Base folder for segmentation output')
    parser.add_argument('--model-path', required=True, help='Path to VASA model directory')
    parser.add_argument('--model-name', required=True, help='VASA model filename')
    parser.add_argument('--preprocess', action='store_true', help='Run preprocessing before segmentation')
    parser.add_argument('--px-size', default='0.25,0.14,0.14', help='Target pixel size ZYX comma-separated (default: 0.25,0.14,0.14)')
    parser.add_argument('--channel-mapping', default='4321', help='Channel order mapping (default: 4321)')
    return parser.parse_args()


def main():
    args = parse_args()

    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    sys.path.insert(0, src_dir)
    import processing_tools as pt

    target_px_size = [float(x) for x in args.px_size.split(',')]

    # pt.readFolder, pt.buildOutputFolder
    file_list = pt.readFolder(args.input)
    basename = file_list[0].split('_')[0]

    print('Preparing output directory:')
    preproc_dataset_folder = pt.buildOutputFolder(args.preproc, basename + '_test')

    # pt.processFiles (optional)
    if args.preprocess:
        full_path_file_list = [os.path.join(args.input, f) for f in file_list]
        print('Preprocessing started')
        pt.processFiles(full_path_file_list, preproc_dataset_folder, target_px_size, args.channel_mapping)

    # pt.initializeCellPose
    print('Initializing CellPose:')
    pt.initializeCellPose()

    # pt.processVASA_cp4
    print('Running VASA segmentation (CellPose 4):')
    vasa_output_folder = pt.processVASA_cp4(
        preproc_dataset_folder, args.output, args.model_path, args.model_name
    )

    print('Segmentation finished')

    # pt.refineVASASegmentationMasks, pt.exportVASASegmentationDetailedStats, pt.exportVASASegmentationResults
    vasa_stats, vasa_regions = pt.refineVASASegmentationMasks(vasa_output_folder, 'VASA')
    pt.exportVASASegmentationDetailedStats(vasa_stats, args.output, basename)
    pt.exportVASASegmentationResults(vasa_regions, args.output, basename)

    print('VASA pipeline complete')


if __name__ == '__main__':
    main()
