import argparse


def mini_qc_default_parser(parser):
    parser.add_argument(
        "--modality",
        type=str,
        choices=["anat", "fmri"],
        default="fmri",
        help="Specify the modality to be analyzed. Default is 'fmri' (for 4D niftis), use 'anat' for 3D niftis.",
    )
    parser.add_argument(
        "--plot",
        type=str,
        choices=["mean", "std"],
        default="mean",
        help="Specify how to summarize 4D niftis. Defaul is 'mean', i.e. the mean over time. Ignored for 3D.",
    )
    parser.add_argument(
        "--extension",
        type=str,
        default="nii.gz",
        help="The extension of the files of interest.",
    )
    parser.add_argument(
        "--colormap",
        type=str,
        default="Greys_r",
        help="The matplotlib colormap that can be applied for visualization. Default 'Greys_r'.",
    )
    parser.add_argument(
        "--njobs",
        type=int,
        default=5,
        help="How many niftis should be processed in parallel. Defaullt is 5",
    )
    parser.add_argument(
        "--image_index_first",
        type=int,
        default=0,
        help="If a only a subset of the dataset should be loaded, this defines the first index of the image list.",
    )
    parser.add_argument(
        "--image_index_last",
        type=int,
        default=None,
        help="If only a subset of the dataset should be loaded, this defines the final index to the image list.",
    )
    return parser


def create_glob_parser():
    parser = argparse.ArgumentParser(description="Easy parser - using glob.")
    # Required BIDS arguments
    parser.add_argument(
        "globstr",
        type=str,
        help="String with wildcards, to search for specific files following this pattern. Bash will do this automatically, otherwise glob is used.",
        nargs="+",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory where the output file should be stored.",
    )

    parser = mini_qc_default_parser(parser)
    return parser


def create_bids_parser():
    parser = argparse.ArgumentParser(description="BIDS-compatible command line parser.")
    # Required BIDS arguments
    parser.add_argument(
        "bids_dir",
        type=str,
        help="The directory with the input dataset formatted according to the BIDS standard.",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory where the output files should be stored.",
    )
    parser.add_argument(
        "--task_id",
        type=str,
        default=None,
        help="Select a specific task to be loaded. If this parameter is not provided all tasks should be loaded.",
    )
    parser.add_argument(
        "--session_id",
        type=str,
        default=None,
        help="Select a specific session to be loaded. If this parameter is not provided all sessions should be loaded.",
    )
    parser.add_argument(
        "--run_id",
        type=str,
        default=None,
        help="Select a specific run to be loaded. If this parameter is not provided all runs should be loaded.",
    )
    parser.add_argument(
        "--space_id",
        type=str,
        default=None,
        help="Select a specific space to be loaded. If this parameter is not provided all spaces should be loaded.",
    )

    parser = mini_qc_default_parser(parser)
    return parser
