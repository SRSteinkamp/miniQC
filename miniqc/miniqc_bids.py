import argparse

import bids
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from tqdm.auto import tqdm

from .application import App
from .fmri_plots import load_prepare_bold


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
        help="Select a specific task to be analyzed. If this parameter is not provided all tasks should be analyzed.",
    )
    parser.add_argument(
        "--session_id",
        type=str,
        default=None,
        help="Select a specific session to be analyzed. If this parameter is not provided all sessions should be analyzed.",
    )
    parser.add_argument(
        "--run_id",
        type=str,
        default=None,
        help="Select a specific run to be analyzed. If this parameter is not provided all runs should be analyzed.",
    )
    parser.add_argument(
        "--space_id",
        type=str,
        default=None,
        help="Select a specific run to be analyzed. If this parameter is not provided all runs should be analyzed.",
    )
    parser.add_argument(
        "--modality",
        type=str,
        choices=["anat", "fmri"],
        default="fmri",
        help="Specify the modality to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--plot",
        type=str,
        choices=["mean", "std"],
        default="mean",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--extension",
        type=str,
        default="nii.gz",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--colormap",
        type=str,
        default="Greys_r",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--njobs",
        type=int,
        default=5,
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--image_index_first",
        type=int,
        default=0,
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--image_index_last",
        type=int,
        default=-1,
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    return parser


def miniqc_gui():
    parser = create_bids_parser()
    args = parser.parse_args()

    dict_args = vars(args)

    cmap = plt.get_cmap(args.colormap)

    if args.modality == "fmri":
        modality = "bold"

    file_filter = {
        i: dict_args[i + "_id"]
        for i in ["task", "run", "session", "space"]
        if dict_args[i + "_id"] is not None
    }

    bids_data = bids.BIDSLayout(args.bids_dir, validate=False)
    if len(file_filter) > 0:
        bids_images = bids_data.get(
            suffix=modality, extension=args.extension, filters=file_filter
        )
    else:
        bids_images = bids_data.get(suffix=modality, extension=args.extension)

    bids_images = [i.path for i in bids_images]
    bids_images = bids_images[args.image_index_first : args.image_index_last]

    if len(bids_images) == 0:
        raise ValueError("Something went wrong")

    results = Parallel(n_jobs=args.njobs)(
        delayed(load_prepare_bold)(i, cmap, args.plot)
        for i in tqdm(bids_images, desc="loading images")
    )

    image_array = {}
    for res in results:
        image_array[res[0]] = [res[1], res[2]]

    app = App(image_array, args.output_dir)
    app.mainloop()


if __name__ == "__main__":
    miniqc_gui()
