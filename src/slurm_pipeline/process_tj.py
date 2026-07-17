import sys
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='TJ segmentation pipeline (CellPose 3)')
    parser.add_argument('--input', required=True, help='Folder with raw .czi files')
    parser.add_argument('--preproc', required=True, help='Base folder for preprocessed data')
    parser.add_argument('--output', required=True, help='Base folder for segmentation output')
    parser.add_argument('--model-path', required=True, help='Path to TJ model directory')
    parser.add_argument('--model-name', required=True, help='TJ model filename')
    return parser.parse_args()


def main():
    args = parse_args()

    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    sys.path.insert(0, src_dir)
    import processing_tools as pt

    # pt.readFolder — used to infer basename and preprocessed folder path
    file_list = pt.readFolder(args.input)
    basename = file_list[0].split('_')[0]

    # pt.buildOutputFolder — infers the same preproc folder created by process_vasa.py
    print('Inferring preprocessed data folder:')
    preproc_dataset_folder = pt.buildOutputFolder(args.preproc, basename + '_test')

    # pt.initializeCellPose
    print('Initializing CellPose:')
    pt.initializeCellPose()

    # pt.processTJ
    print('Running TJ segmentation (CellPose 3):')
    tj_output_folder = pt.processTJ(
        preproc_dataset_folder, args.output, args.model_path, args.model_name
    )

    print('Segmentation finished')

    # pt.processTJSegmentationMasks, pt.exportTJSegmentationCounts, pt.exportTJSegmentationPercellMetrics
    tj_stats, tj_regions = pt.processTJSegmentationMasks(tj_output_folder, 'TJ')
    pt.exportTJSegmentationCounts(tj_stats, args.output, basename)
    pt.exportTJSegmentationPercellMetrics(tj_regions, args.output, basename)

    print('TJ pipeline complete')


if __name__ == '__main__':
    main()
